"""yfinance-cache MCP server.

Connects yfinance market data to Claude over the Model Context Protocol, caching
OHLCV, fundamentals, news and business information per ticker, and deriving the
common SMAs, breakout signals and volume-trend changes.
"""

from .analysis import (
    OHLCVSeries,
    TickerAnalysis,
    analyze,
    analyze_volume,
    detect_breakouts,
    latest_smas,
    sma,
)
from .cache import Cache
from .provider import YFinanceProvider

__version__ = "0.1.0"

__all__ = [
    "OHLCVSeries",
    "TickerAnalysis",
    "analyze",
    "analyze_volume",
    "detect_breakouts",
    "latest_smas",
    "sma",
    "Cache",
    "YFinanceProvider",
]
