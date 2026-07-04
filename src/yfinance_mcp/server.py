"""MCP server exposing cached yfinance data and technical analysis to Claude.

Run with::

    python -m yfinance_mcp            # stdio transport (for Claude Desktop / CLI)

Every tool reads through the SQLite cache, so once a ticker has been queried its
OHLCV, fundamentals, news and business info are served from disk until the
per-category TTL expires. The analysis tools derive the common SMAs, look for
breakouts, and flag volume-trend changes.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Optional

from mcp.server.fastmcp import FastMCP

from .analysis import (
    DEFAULT_BREAKOUT_LOOKBACK,
    DEFAULT_SMA_PERIODS,
    TickerAnalysis,
    analyze,
)
from .cache import Cache
from .provider import YFinanceProvider

mcp = FastMCP("yfinance-cache")

_provider: Optional[YFinanceProvider] = None


def get_provider() -> YFinanceProvider:
    """Lazily construct the provider so importing this module is side-effect free."""
    global _provider
    if _provider is None:
        _provider = YFinanceProvider(Cache())
    return _provider


def _analysis_to_dict(a: TickerAnalysis) -> dict[str, Any]:
    return {
        "ticker": a.ticker,
        "as_of": a.as_of,
        "bars": a.bars,
        "last_close": a.last_close,
        "smas": {str(p): v for p, v in a.smas.items()},
        "price_vs_smas": {str(p): v for p, v in a.price_vs_smas.items()},
        "breakouts": [asdict(b) for b in a.breakouts],
        "volume": asdict(a.volume),
    }


@mcp.tool()
def analyze_ticker(
    ticker: str,
    period: str = "1y",
    lookback: int = DEFAULT_BREAKOUT_LOOKBACK,
) -> dict[str, Any]:
    """Fetch daily OHLCV for a ticker and run full technical analysis.

    Returns the latest close, the 20/50/100/200-day SMAs, whether price is above
    or below each, any breakout signals (new range highs/lows, price-vs-SMA
    crosses, golden/death crosses), and a volume-trend assessment (spikes and
    rising/falling volume). Data is cached; repeated calls are cheap.
    """
    provider = get_provider()
    series = provider.get_ohlcv(ticker, period=period)
    result = analyze(series, sma_periods=DEFAULT_SMA_PERIODS, lookback=lookback)
    return _analysis_to_dict(result)


@mcp.tool()
def analyze_tickers(
    tickers: list[str],
    period: str = "1y",
    lookback: int = DEFAULT_BREAKOUT_LOOKBACK,
) -> dict[str, Any]:
    """Run :func:`analyze_ticker` across a list of tickers.

    Returns a per-ticker analysis plus an ``errors`` map for any that failed.
    Use this for the workflow "here is my watchlist — derive SMAs, find
    breakouts and volume changes".
    """
    provider = get_provider()
    results: dict[str, Any] = {}
    errors: dict[str, str] = {}
    for t in tickers:
        try:
            series = provider.get_ohlcv(t, period=period)
            results[t.upper()] = _analysis_to_dict(
                analyze(series, sma_periods=DEFAULT_SMA_PERIODS, lookback=lookback)
            )
        except Exception as exc:  # noqa: BLE001 - surface per-ticker failure
            errors[t.upper()] = str(exc)
    return {"analyses": results, "errors": errors}


@mcp.tool()
def screen_signals(
    tickers: list[str],
    period: str = "1y",
    lookback: int = DEFAULT_BREAKOUT_LOOKBACK,
) -> dict[str, Any]:
    """Screen a watchlist and return only tickers with actionable signals.

    A ticker is surfaced if it has any breakout signal or a non-flat volume
    trend / volume spike. Ideal for scanning many tickers and getting back just
    the ones worth a look.
    """
    provider = get_provider()
    hits: list[dict[str, Any]] = []
    errors: dict[str, str] = {}
    for t in tickers:
        try:
            series = provider.get_ohlcv(t, period=period)
            a = analyze(series, sma_periods=DEFAULT_SMA_PERIODS, lookback=lookback)
            interesting = bool(a.breakouts) or a.volume.spike or a.volume.trend in (
                "rising",
                "falling",
            )
            if interesting:
                hits.append(
                    {
                        "ticker": a.ticker,
                        "last_close": a.last_close,
                        "breakouts": [asdict(b) for b in a.breakouts],
                        "volume_trend": a.volume.trend,
                        "volume_spike": a.volume.spike,
                        "volume_notes": a.volume.notes,
                    }
                )
        except Exception as exc:  # noqa: BLE001
            errors[t.upper()] = str(exc)
    return {"signals": hits, "screened": len(tickers), "errors": errors}


@mcp.tool()
def get_ohlcv(ticker: str, period: str = "1y") -> dict[str, Any]:
    """Return cached daily OHLCV bars for a ticker (oldest first)."""
    series = get_provider().get_ohlcv(ticker, period=period)
    return {
        "ticker": series.ticker,
        "bars": len(series),
        "dates": series.dates,
        "open": series.open,
        "high": series.high,
        "low": series.low,
        "close": series.close,
        "volume": series.volume,
    }


@mcp.tool()
def get_fundamentals(ticker: str) -> dict[str, Any]:
    """Valuation and financial-health fundamentals (P/E, margins, growth, etc.)."""
    return get_provider().get_fundamentals(ticker)


@mcp.tool()
def get_business_info(ticker: str) -> dict[str, Any]:
    """Company/business profile: name, sector, industry, summary, exchange."""
    return get_provider().get_business_info(ticker)


@mcp.tool()
def get_news(ticker: str, limit: int = 10) -> list[dict[str, Any]]:
    """Recent news headlines for a ticker (title, publisher, url, summary)."""
    return get_provider().get_news(ticker, limit=limit)


@mcp.tool()
def refresh_ticker(ticker: str, period: str = "1y") -> dict[str, Any]:
    """Force a re-fetch of all categories for a ticker, bypassing the cache."""
    provider = get_provider()
    out: dict[str, Any] = {"ticker": ticker.upper(), "refreshed": []}
    try:
        provider.get_ohlcv(ticker, period=period, force=True)
        out["refreshed"].append("ohlcv")
    except Exception as exc:  # noqa: BLE001
        out.setdefault("errors", {})["ohlcv"] = str(exc)
    for name, fn in (
        ("fundamentals", provider.get_fundamentals),
        ("business_info", provider.get_business_info),
    ):
        try:
            fn(ticker, force=True)
            out["refreshed"].append(name)
        except Exception as exc:  # noqa: BLE001
            out.setdefault("errors", {})[name] = str(exc)
    try:
        provider.get_news(ticker, force=True)
        out["refreshed"].append("news")
    except Exception as exc:  # noqa: BLE001
        out.setdefault("errors", {})["news"] = str(exc)
    return out


@mcp.tool()
def cache_stats() -> list[dict[str, Any]]:
    """Report what is currently cached, per category, with counts and ages."""
    return get_provider().cache_report()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
