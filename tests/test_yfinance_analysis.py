"""Network-free tests for the yfinance MCP analysis module."""

from __future__ import annotations

import pytest

from yfinance_mcp.analysis import (
    OHLCVSeries,
    analyze,
    analyze_volume,
    detect_breakouts,
    latest_smas,
    sma,
)


def make_series(closes, volumes=None, ticker="TEST"):
    n = len(closes)
    volumes = volumes if volumes is not None else [1_000_000.0] * n
    dates = [f"2024-01-{i + 1:02d}" for i in range(n)]
    # highs/lows track close for simplicity.
    return OHLCVSeries(
        ticker=ticker,
        dates=dates,
        open=list(closes),
        high=[c + 0.5 for c in closes],
        low=[c - 0.5 for c in closes],
        close=list(closes),
        volume=list(volumes),
    )


def test_sma_basic():
    assert sma([1, 2, 3, 4, 5], 3) == [None, None, 2.0, 3.0, 4.0]


def test_sma_period_one_is_identity():
    assert sma([5, 6, 7], 1) == [5.0, 6.0, 7.0]


def test_sma_invalid_period():
    with pytest.raises(ValueError):
        sma([1, 2, 3], 0)


def test_latest_smas_insufficient_data_is_none():
    closes = [10.0] * 10  # fewer than 20 bars
    smas = latest_smas(closes, (20, 50))
    assert smas == {20: None, 50: None}


def test_price_high_breakout():
    # 30 flat bars then a jump above the range -> new-high breakout.
    closes = [100.0] * 30 + [110.0]
    series = make_series(closes)
    signals = detect_breakouts(series, lookback=20)
    kinds = {s.kind for s in signals}
    assert "price_high" in kinds
    up = [s for s in signals if s.kind == "price_high"][0]
    assert up.direction == "up"


def test_price_low_breakout():
    closes = [100.0] * 30 + [90.0]
    series = make_series(closes)
    signals = detect_breakouts(series, lookback=20)
    assert any(s.kind == "price_low" and s.direction == "down" for s in signals)


def test_no_breakout_when_flat():
    closes = [100.0] * 40
    series = make_series(closes)
    assert detect_breakouts(series, lookback=20) == []


def test_price_crosses_sma_up():
    # Long downtrend keeps price below its SMA, then a jump crosses above it.
    closes = [float(100 - i) for i in range(25)]  # 100 -> 76
    closes.append(200.0)  # big jump above the SMA20
    series = make_series(closes)
    signals = detect_breakouts(series, lookback=20)
    assert any(
        s.kind == "sma_cross" and s.direction == "up" for s in signals
    )


def test_volume_spike_detected():
    vols = [1_000_000.0] * 30 + [5_000_000.0]
    closes = [100.0] * 31
    series = make_series(closes, vols)
    va = analyze_volume(series, lookback=20)
    assert va.spike is True
    assert va.volume_ratio is not None and va.volume_ratio >= 2.0


def test_volume_trend_rising():
    # Recent volume much higher than the longer-window average.
    vols = [1_000_000.0] * 25 + [4_000_000.0] * 5
    closes = [100.0] * 30
    series = make_series(closes, vols)
    va = analyze_volume(series, lookback=20, short_window=5)
    assert va.trend == "rising"


def test_volume_trend_falling():
    vols = [4_000_000.0] * 25 + [1_000_000.0] * 5
    closes = [100.0] * 30
    series = make_series(closes, vols)
    va = analyze_volume(series, lookback=20, short_window=5)
    assert va.trend == "falling"


def test_full_analyze_shape():
    closes = [float(100 + (i % 5)) for i in range(60)]
    series = make_series(closes)
    a = analyze(series)
    assert a.ticker == "TEST"
    assert a.last_close == closes[-1]
    assert set(a.smas.keys()) == {20, 50, 100, 200}
    assert a.smas[20] is not None  # 60 bars > 20
    assert a.smas[100] is None  # not enough bars
    assert a.price_vs_smas[20] in ("above", "below")
    assert a.bars == 60


def test_analyze_validates_ragged_columns():
    series = make_series([1.0, 2.0, 3.0])
    series.volume = [1.0]  # break the invariant
    with pytest.raises(ValueError):
        analyze(series)
