"""yfinance data provider with a read-through cache.

This module is the only place that touches the network. Every accessor first
consults the :class:`~yfinance_mcp.cache.Cache`; on a miss (or stale entry) it
fetches from yfinance, stores the result, and returns it. If a live fetch fails
but a stale cached copy exists, the stale copy is returned so the tools degrade
gracefully when Yahoo is unreachable.

``yfinance`` and ``pandas`` are imported lazily so that the pure-Python parts of
the package (analysis, cache) can be imported and tested without them.
"""

from __future__ import annotations

import math
from typing import Any, Optional

from .analysis import OHLCVSeries
from .cache import Cache


def _clean(value: Any) -> Any:
    """Make a value JSON-serialisable and NaN-free."""
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


class YFinanceProvider:
    def __init__(self, cache: Optional[Cache] = None) -> None:
        self.cache = cache or Cache()

    # -- OHLCV ----------------------------------------------------------------

    def get_ohlcv(
        self,
        ticker: str,
        period: str = "1y",
        interval: str = "1d",
        force: bool = False,
    ) -> OHLCVSeries:
        """Daily OHLCV as an :class:`OHLCVSeries`, cached by ticker+period."""
        ticker = ticker.upper()
        category = "ohlcv"
        cache_key = f"{ticker}:{period}:{interval}"
        if not force:
            entry = self.cache.get(category, cache_key)
            if entry is not None:
                return self._series_from_payload(ticker, entry.payload)

        try:
            payload = self._fetch_ohlcv(ticker, period, interval)
            self.cache.set(category, cache_key, payload)
        except Exception:
            stale = self.cache.peek(category, cache_key)
            if stale is None:
                raise
            payload = stale.payload
        return self._series_from_payload(ticker, payload)

    def _fetch_ohlcv(self, ticker: str, period: str, interval: str) -> dict[str, Any]:
        import yfinance as yf

        df = yf.Ticker(ticker).history(
            period=period, interval=interval, auto_adjust=False
        )
        if df is None or df.empty:
            raise ValueError(f"no price data returned for {ticker}")
        df = df.reset_index()
        date_col = "Date" if "Date" in df.columns else df.columns[0]
        return {
            "dates": [str(d)[:10] for d in df[date_col].tolist()],
            "open": [_clean(float(x)) for x in df["Open"].tolist()],
            "high": [_clean(float(x)) for x in df["High"].tolist()],
            "low": [_clean(float(x)) for x in df["Low"].tolist()],
            "close": [_clean(float(x)) for x in df["Close"].tolist()],
            "volume": [_clean(float(x)) for x in df["Volume"].tolist()],
        }

    @staticmethod
    def _series_from_payload(ticker: str, payload: dict[str, Any]) -> OHLCVSeries:
        # Drop any rows with a missing close so analysis stays clean.
        rows = zip(
            payload["dates"],
            payload["open"],
            payload["high"],
            payload["low"],
            payload["close"],
            payload["volume"],
        )
        dates, o, h, low, c, v = [], [], [], [], [], []
        for d, oo, hh, ll, cc, vv in rows:
            if cc is None:
                continue
            dates.append(d)
            o.append(oo if oo is not None else cc)
            h.append(hh if hh is not None else cc)
            low.append(ll if ll is not None else cc)
            c.append(cc)
            v.append(vv if vv is not None else 0.0)
        return OHLCVSeries(ticker, dates, o, h, low, c, v)

    # -- Fundamentals / info / news ------------------------------------------

    def get_fundamentals(self, ticker: str, force: bool = False) -> dict[str, Any]:
        """Key valuation / financial-health metrics distilled from ``.info``."""
        info = self._get_info_raw(ticker, force=force)
        keys = (
            "marketCap", "trailingPE", "forwardPE", "priceToBook",
            "pegRatio", "trailingEps", "forwardEps", "dividendYield",
            "payoutRatio", "beta", "profitMargins", "grossMargins",
            "operatingMargins", "returnOnEquity", "returnOnAssets",
            "revenueGrowth", "earningsGrowth", "debtToEquity",
            "currentRatio", "quickRatio", "totalRevenue", "totalDebt",
            "totalCash", "freeCashflow", "fiftyTwoWeekHigh",
            "fiftyTwoWeekLow", "sharesOutstanding", "floatShares",
        )
        return {k: _clean(info.get(k)) for k in keys}

    def get_business_info(self, ticker: str, force: bool = False) -> dict[str, Any]:
        """Company/business descriptors from ``.info``."""
        info = self._get_info_raw(ticker, force=force)
        keys = (
            "shortName", "longName", "symbol", "sector", "industry",
            "country", "city", "website", "fullTimeEmployees",
            "longBusinessSummary", "exchange", "quoteType", "currency",
        )
        return {k: _clean(info.get(k)) for k in keys}

    def _get_info_raw(self, ticker: str, force: bool = False) -> dict[str, Any]:
        ticker = ticker.upper()
        category = "info"
        if not force:
            entry = self.cache.get(category, ticker)
            if entry is not None:
                return entry.payload
        try:
            import yfinance as yf

            info = dict(yf.Ticker(ticker).info or {})
            info = {k: _clean(v) for k, v in info.items()}
            self.cache.set(category, ticker, info)
            return info
        except Exception:
            stale = self.cache.peek(category, ticker)
            if stale is None:
                raise
            return stale.payload

    def get_news(self, ticker: str, limit: int = 10, force: bool = False) -> list[dict[str, Any]]:
        ticker = ticker.upper()
        category = "news"
        if not force:
            entry = self.cache.get(category, ticker)
            if entry is not None:
                return entry.payload[:limit]
        try:
            import yfinance as yf

            raw = yf.Ticker(ticker).news or []
            items = [self._normalise_news(n) for n in raw]
            self.cache.set(category, ticker, items)
            return items[:limit]
        except Exception:
            stale = self.cache.peek(category, ticker)
            if stale is None:
                raise
            return stale.payload[:limit]

    @staticmethod
    def _normalise_news(item: dict[str, Any]) -> dict[str, Any]:
        # yfinance has used two shapes over time: flat, and nested under
        # "content". Handle both.
        content = item.get("content", item)
        title = content.get("title") or item.get("title")
        provider = content.get("provider") or {}
        publisher = (
            provider.get("displayName")
            if isinstance(provider, dict)
            else item.get("publisher")
        )
        url = None
        if isinstance(content.get("canonicalUrl"), dict):
            url = content["canonicalUrl"].get("url")
        url = url or item.get("link") or content.get("clickThroughUrl", {}).get("url")
        return {
            "title": title,
            "publisher": publisher or item.get("publisher"),
            "url": url,
            "published": content.get("pubDate") or item.get("providerPublishTime"),
            "summary": content.get("summary"),
        }

    def cache_report(self) -> list[dict[str, Any]]:
        return self.cache.stats()
