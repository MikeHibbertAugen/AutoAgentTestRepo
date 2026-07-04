"""Network-free tests for the yfinance MCP SQLite cache."""

from __future__ import annotations

from yfinance_mcp.cache import Cache


def make_cache():
    # In-memory DB, short TTLs for deterministic expiry tests.
    return Cache(path=":memory:", ttls={"ohlcv": 100, "news": 10})


def test_set_and_get_roundtrip():
    c = make_cache()
    c.set("ohlcv", "aapl", {"close": [1, 2, 3]}, now=1000.0)
    entry = c.get("ohlcv", "AAPL", now=1050.0)
    assert entry is not None
    assert entry.payload == {"close": [1, 2, 3]}
    assert entry.ticker == "AAPL"  # normalised to upper-case


def test_ticker_case_insensitive():
    c = make_cache()
    c.set("info", "MsFt", {"x": 1}, now=0.0)
    assert c.get("info", "msft", now=1.0) is not None


def test_get_miss_returns_none():
    c = make_cache()
    assert c.get("ohlcv", "NOPE") is None


def test_ttl_expiry():
    c = make_cache()
    c.set("news", "TSLA", [{"title": "hi"}], now=1000.0)
    # within TTL (10s)
    assert c.get("news", "TSLA", now=1005.0) is not None
    # past TTL
    assert c.get("news", "TSLA", now=1020.0) is None


def test_max_age_override():
    c = make_cache()
    c.set("ohlcv", "TSLA", {}, now=1000.0)
    # category TTL is 100s but we override to 5s -> stale
    assert c.get("ohlcv", "TSLA", now=1010.0, max_age=5) is None


def test_peek_ignores_ttl():
    c = make_cache()
    c.set("news", "TSLA", [{"title": "old"}], now=0.0)
    assert c.get("news", "TSLA", now=10_000.0) is None  # expired
    stale = c.peek("news", "TSLA")
    assert stale is not None and stale.payload == [{"title": "old"}]


def test_replace_updates_payload():
    c = make_cache()
    c.set("info", "AAPL", {"v": 1}, now=0.0)
    c.set("info", "AAPL", {"v": 2}, now=1.0)
    entry = c.get("info", "AAPL", now=2.0)
    assert entry is not None and entry.payload == {"v": 2}


def test_invalidate():
    c = make_cache()
    c.set("info", "AAPL", {}, now=0.0)
    c.set("info", "MSFT", {}, now=0.0)
    removed = c.invalidate(category="info", ticker="AAPL")
    assert removed == 1
    assert c.get("info", "AAPL", now=1.0) is None
    assert c.get("info", "MSFT", now=1.0) is not None


def test_stats():
    c = make_cache()
    c.set("info", "AAPL", {}, now=0.0)
    c.set("info", "MSFT", {}, now=0.0)
    c.set("news", "AAPL", [], now=0.0)
    stats = {row["category"]: row["n"] for row in c.stats()}
    assert stats == {"info": 2, "news": 1}
