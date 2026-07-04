"""Network-free tests for the provider's read-through cache and fallbacks.

A fake ``yfinance`` module is injected so no network call is ever made; we can
then assert the provider fetches once, serves subsequent calls from cache, and
falls back to a stale copy when a later fetch raises.
"""

from __future__ import annotations

import sys
import types

import pytest

from yfinance_mcp.cache import Cache
from yfinance_mcp.provider import YFinanceProvider


class _FakeHistory:
    """Minimal stand-in for a pandas DataFrame returned by Ticker.history()."""

    def __init__(self, rows):
        self._rows = rows
        self.empty = len(rows) == 0
        self.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]

    def reset_index(self):
        return self

    def __getitem__(self, key):
        idx = {"Date": 0, "Open": 1, "High": 2, "Low": 3, "Close": 4, "Volume": 5}[key]
        col = [r[idx] for r in self._rows]
        return types.SimpleNamespace(tolist=lambda: col)


class _FakeTicker:
    calls = {"history": 0, "info": 0, "news": 0}
    fail = False

    def __init__(self, symbol):
        self.symbol = symbol

    def history(self, period="1y", interval="1d", auto_adjust=False):
        _FakeTicker.calls["history"] += 1
        if _FakeTicker.fail:
            raise RuntimeError("network down")
        rows = [
            ("2024-01-01", 10.0, 11.0, 9.0, 10.5, 1000),
            ("2024-01-02", 10.5, 12.0, 10.0, 11.5, 2000),
        ]
        return _FakeHistory(rows)

    @property
    def info(self):
        _FakeTicker.calls["info"] += 1
        return {"shortName": "Fake Co", "sector": "Tech", "trailingPE": 15.0}

    @property
    def news(self):
        _FakeTicker.calls["news"] += 1
        return [{"content": {"title": "Big news", "provider": {"displayName": "Wire"}}}]


@pytest.fixture
def provider(monkeypatch):
    fake_yf = types.ModuleType("yfinance")
    fake_yf.Ticker = _FakeTicker
    monkeypatch.setitem(sys.modules, "yfinance", fake_yf)
    _FakeTicker.calls = {"history": 0, "info": 0, "news": 0}
    _FakeTicker.fail = False
    return YFinanceProvider(Cache(path=":memory:"))


def test_ohlcv_fetch_then_cache(provider):
    s1 = provider.get_ohlcv("AAPL")
    assert s1.close == [10.5, 11.5]
    assert _FakeTicker.calls["history"] == 1
    # second call served from cache -> no new fetch
    s2 = provider.get_ohlcv("AAPL")
    assert s2.close == [10.5, 11.5]
    assert _FakeTicker.calls["history"] == 1


def test_ohlcv_force_refetch(provider):
    provider.get_ohlcv("AAPL")
    provider.get_ohlcv("AAPL", force=True)
    assert _FakeTicker.calls["history"] == 2


def test_stale_fallback_on_fetch_failure(provider):
    provider.get_ohlcv("AAPL")  # populate cache
    provider.cache.invalidate()  # drop fresh entry... then re-seed as stale
    # Re-seed and then expire by using force with a failing fetch.
    provider.get_ohlcv("AAPL")  # repopulate
    _FakeTicker.fail = True
    # force=True triggers a fetch which fails -> should fall back to stale cache
    s = provider.get_ohlcv("AAPL", force=True)
    assert s.close == [10.5, 11.5]


def test_fundamentals_and_business_info(provider):
    fund = provider.get_fundamentals("AAPL")
    assert fund["trailingPE"] == 15.0
    info = provider.get_business_info("AAPL")
    assert info["shortName"] == "Fake Co"
    assert info["sector"] == "Tech"
    # both come from the same cached .info -> single network hit
    assert _FakeTicker.calls["info"] == 1


def test_news_normalisation(provider):
    news = provider.get_news("AAPL")
    assert news[0]["title"] == "Big news"
    assert news[0]["publisher"] == "Wire"
