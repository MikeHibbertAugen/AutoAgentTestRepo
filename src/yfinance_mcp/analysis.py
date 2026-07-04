"""Technical analysis over daily OHLCV series.

All functions here are pure and dependency-free: they operate on plain Python
lists of floats so they can be unit-tested without network access, pandas, or
yfinance. The provider layer is responsible for turning yfinance frames into
the simple :class:`OHLCVSeries` used here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

# Simple moving-average windows that traders most commonly watch.
DEFAULT_SMA_PERIODS = (20, 50, 100, 200)

# Default look-back for Donchian-style breakout detection.
DEFAULT_BREAKOUT_LOOKBACK = 20

# A volume "spike" is the latest volume exceeding this multiple of the
# average volume over the look-back window.
DEFAULT_VOLUME_SPIKE_MULTIPLE = 2.0


@dataclass
class OHLCVSeries:
    """A daily OHLCV series in chronological (oldest-first) order."""

    ticker: str
    dates: list[str]
    open: list[float]
    high: list[float]
    low: list[float]
    close: list[float]
    volume: list[float]

    def __len__(self) -> int:
        return len(self.close)

    def validate(self) -> None:
        n = len(self.close)
        for name, col in (
            ("dates", self.dates),
            ("open", self.open),
            ("high", self.high),
            ("low", self.low),
            ("volume", self.volume),
        ):
            if len(col) != n:
                raise ValueError(
                    f"{self.ticker}: column '{name}' has length {len(col)}, "
                    f"expected {n} to match close"
                )


def sma(values: list[float], period: int) -> list[Optional[float]]:
    """Simple moving average.

    Returns a list the same length as ``values``; entries before enough data
    has accumulated are ``None``.
    """
    if period <= 0:
        raise ValueError("period must be positive")
    out: list[Optional[float]] = []
    running = 0.0
    for i, v in enumerate(values):
        running += v
        if i >= period:
            running -= values[i - period]
        if i >= period - 1:
            out.append(running / period)
        else:
            out.append(None)
    return out


def latest_smas(
    closes: list[float], periods: tuple[int, ...] = DEFAULT_SMA_PERIODS
) -> dict[int, Optional[float]]:
    """Most recent SMA value for each requested period."""
    result: dict[int, Optional[float]] = {}
    for p in periods:
        series = sma(closes, p)
        result[p] = series[-1] if series else None
    return result


def _crossed(prev_a: float, prev_b: float, cur_a: float, cur_b: float) -> Optional[str]:
    """Detect a crossover of series A relative to series B on the last step."""
    if prev_a <= prev_b and cur_a > cur_b:
        return "up"
    if prev_a >= prev_b and cur_a < cur_b:
        return "down"
    return None


@dataclass
class BreakoutSignal:
    kind: str  # e.g. "price_high", "sma_cross", "golden_cross"
    direction: str  # "up" or "down"
    detail: str


def detect_breakouts(
    series: OHLCVSeries,
    lookback: int = DEFAULT_BREAKOUT_LOOKBACK,
    sma_periods: tuple[int, ...] = DEFAULT_SMA_PERIODS,
) -> list[BreakoutSignal]:
    """Detect breakouts on the most recent bar.

    Three families of signal are reported:

    * **Donchian range breakout** — the latest close makes a new high (or low)
      relative to the prior ``lookback`` closes.
    * **Price / SMA cross** — the close crossed above or below an SMA on the
      last bar.
    * **SMA / SMA cross** — a shorter SMA crossed a longer SMA (the classic
      golden cross / death cross when 50 crosses 200).
    """
    signals: list[BreakoutSignal] = []
    closes = series.close
    n = len(closes)
    if n < 2:
        return signals

    # Donchian range breakout: compare latest close to the window *before* it.
    if n > lookback:
        window = closes[-(lookback + 1) : -1]
        prior_high = max(window)
        prior_low = min(window)
        last = closes[-1]
        if last > prior_high:
            signals.append(
                BreakoutSignal(
                    "price_high",
                    "up",
                    f"close {last:.2f} broke above {lookback}-day high {prior_high:.2f}",
                )
            )
        elif last < prior_low:
            signals.append(
                BreakoutSignal(
                    "price_low",
                    "down",
                    f"close {last:.2f} broke below {lookback}-day low {prior_low:.2f}",
                )
            )

    # Price / SMA crossovers.
    for p in sma_periods:
        s = sma(closes, p)
        if s[-1] is None or s[-2] is None:
            continue
        direction = _crossed(closes[-2], s[-2], closes[-1], s[-1])  # type: ignore[arg-type]
        if direction:
            signals.append(
                BreakoutSignal(
                    "sma_cross",
                    direction,
                    f"close crossed {direction} through SMA{p} ({s[-1]:.2f})",
                )
            )

    # SMA / SMA crossovers (golden / death cross for 50 vs 200).
    ordered = sorted(set(sma_periods))
    for i in range(len(ordered)):
        for j in range(i + 1, len(ordered)):
            fast_p, slow_p = ordered[i], ordered[j]
            fast, slow = sma(closes, fast_p), sma(closes, slow_p)
            if None in (fast[-1], fast[-2], slow[-1], slow[-2]):
                continue
            direction = _crossed(fast[-2], slow[-2], fast[-1], slow[-1])  # type: ignore[arg-type]
            if direction:
                kind = (
                    "golden_cross"
                    if (fast_p, slow_p) == (50, 200) and direction == "up"
                    else "death_cross"
                    if (fast_p, slow_p) == (50, 200) and direction == "down"
                    else "sma_sma_cross"
                )
                signals.append(
                    BreakoutSignal(
                        kind,
                        direction,
                        f"SMA{fast_p} crossed {direction} through SMA{slow_p}",
                    )
                )
    return signals


@dataclass
class VolumeAnalysis:
    latest_volume: float
    avg_volume: Optional[float]
    volume_ratio: Optional[float]  # latest / avg
    spike: bool
    short_avg: Optional[float]  # e.g. 5-day
    long_avg: Optional[float]  # e.g. 20-day
    trend: str  # "rising", "falling", "flat", "unknown"
    notes: list[str] = field(default_factory=list)


def analyze_volume(
    series: OHLCVSeries,
    lookback: int = DEFAULT_BREAKOUT_LOOKBACK,
    short_window: int = 5,
    spike_multiple: float = DEFAULT_VOLUME_SPIKE_MULTIPLE,
) -> VolumeAnalysis:
    """Detect volume-trend changes and spikes.

    Compares the latest volume to its average, flags spikes, and classifies the
    trend by comparing a short volume SMA to a longer one (a rising short SMA
    above the long SMA indicates accumulating volume).
    """
    vols = series.volume
    if not vols:
        return VolumeAnalysis(0.0, None, None, False, None, None, "unknown")

    latest = vols[-1]
    window = vols[-(lookback + 1) : -1] if len(vols) > lookback else vols[:-1]
    avg = sum(window) / len(window) if window else None
    ratio = (latest / avg) if avg else None
    spike = bool(ratio is not None and ratio >= spike_multiple)

    short_sma = sma(vols, min(short_window, len(vols)))
    long_sma = sma(vols, min(lookback, len(vols)))
    short_avg = short_sma[-1]
    long_avg = long_sma[-1]

    trend = "unknown"
    notes: list[str] = []
    if short_avg is not None and long_avg is not None:
        if short_avg > long_avg * 1.05:
            trend = "rising"
            notes.append(
                f"{short_window}-day avg volume {short_avg:,.0f} is above "
                f"{lookback}-day avg {long_avg:,.0f} (volume building)"
            )
        elif short_avg < long_avg * 0.95:
            trend = "falling"
            notes.append(
                f"{short_window}-day avg volume {short_avg:,.0f} is below "
                f"{lookback}-day avg {long_avg:,.0f} (volume fading)"
            )
        else:
            trend = "flat"
    if spike:
        notes.append(
            f"volume spike: latest {latest:,.0f} is {ratio:.1f}x the "
            f"{lookback}-day average"
        )

    return VolumeAnalysis(
        latest_volume=latest,
        avg_volume=avg,
        volume_ratio=ratio,
        spike=spike,
        short_avg=short_avg,
        long_avg=long_avg,
        trend=trend,
        notes=notes,
    )


@dataclass
class TickerAnalysis:
    ticker: str
    as_of: Optional[str]
    last_close: Optional[float]
    smas: dict[int, Optional[float]]
    price_vs_smas: dict[int, Optional[str]]  # "above"/"below" per period
    breakouts: list[BreakoutSignal]
    volume: VolumeAnalysis
    bars: int


def analyze(
    series: OHLCVSeries,
    sma_periods: tuple[int, ...] = DEFAULT_SMA_PERIODS,
    lookback: int = DEFAULT_BREAKOUT_LOOKBACK,
) -> TickerAnalysis:
    """Full technical analysis for one ticker's daily series."""
    series.validate()
    closes = series.close
    smas = latest_smas(closes, sma_periods)
    last_close = closes[-1] if closes else None

    price_vs: dict[int, Optional[str]] = {}
    for p, val in smas.items():
        if val is None or last_close is None:
            price_vs[p] = None
        else:
            price_vs[p] = "above" if last_close >= val else "below"

    return TickerAnalysis(
        ticker=series.ticker,
        as_of=series.dates[-1] if series.dates else None,
        last_close=last_close,
        smas=smas,
        price_vs_smas=price_vs,
        breakouts=detect_breakouts(series, lookback, sma_periods),
        volume=analyze_volume(series, lookback),
        bars=len(series),
    )
