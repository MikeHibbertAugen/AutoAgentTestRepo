# yfinance-cache MCP server

An [MCP](https://modelcontextprotocol.io) server that connects
[`yfinance`](https://github.com/ranaroussi/yfinance) market data to Claude. It
**caches** everything it retrieves per ticker — OHLCV bars, fundamentals, news,
and business/company information — and derives technical signals from daily
prices: the common SMAs, breakouts, and volume-trend changes.

Package: `src/yfinance_mcp/`

## Why a cache?

Yahoo's endpoints are rate-limited and occasionally flaky. Every accessor is
**read-through**: it checks a local SQLite cache first, only hits the network on
a miss or when the entry is older than its per-category TTL, and falls back to a
stale copy if a live fetch fails. Once you've queried a ticker, repeated
analysis is free and works offline.

| Category       | Default TTL |
| -------------- | ----------- |
| `ohlcv`        | 6 hours     |
| `fundamentals` | 24 hours    |
| `info`         | 24 hours    |
| `news`         | 1 hour      |

Cache location defaults to `~/.cache/yfinance_mcp/cache.sqlite`; override with
the `YFINANCE_MCP_CACHE` environment variable.

## Install & run

```bash
pip install -r src/yfinance_mcp/requirements.txt
python -m yfinance_mcp          # starts the MCP server over stdio
```

> **Network note:** the server needs outbound HTTPS to
> `query1.finance.yahoo.com` / `query2.finance.yahoo.com`. On a locked-down
> environment (e.g. Claude Code on the web with a restricted network policy)
> those hosts must be allowlisted, otherwise fetches fail and the tools return
> only cached data.

### Register with Claude Desktop / Claude Code

Add to your MCP client config (e.g. `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "yfinance-cache": {
      "command": "python",
      "args": ["-m", "yfinance_mcp"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/AutoAgentTestRepo/src",
        "YFINANCE_MCP_CACHE": "/absolute/path/to/cache.sqlite"
      }
    }
  }
}
```

## Tools

| Tool                | Purpose |
| ------------------- | ------- |
| `analyze_ticker`    | Full technical analysis for one ticker: SMAs, price-vs-SMA, breakouts, volume. |
| `analyze_tickers`   | Same, across a watchlist; returns per-ticker results + errors. |
| `screen_signals`    | Scan a watchlist and return **only** tickers with a breakout or volume change. |
| `get_ohlcv`         | Raw cached daily OHLCV bars (oldest first). |
| `get_fundamentals`  | Valuation / financial-health metrics (P/E, margins, growth, debt…). |
| `get_business_info` | Company profile: name, sector, industry, summary, exchange. |
| `get_news`          | Recent headlines (title, publisher, url, summary). |
| `refresh_ticker`    | Force a re-fetch of every category, bypassing the cache. |
| `cache_stats`       | What is cached, per category, with counts and ages. |

## The analysis

Given a daily OHLCV series, `analyze_ticker` derives:

* **SMAs** — 20, 50, 100, 200-day simple moving averages, plus whether the last
  close sits **above** or **below** each.
* **Breakouts** —
  * *Range breakout*: latest close makes a new N-day high/low (Donchian style,
    default 20-day look-back).
  * *Price/SMA cross*: close crossed above/below an SMA on the last bar.
  * *SMA/SMA cross*: a faster SMA crossed a slower one — the classic
    **golden cross** (50 over 200) / **death cross** (50 under 200).
* **Volume-trend change** —
  * *Spike*: latest volume ≥ 2× the look-back average.
  * *Trend*: a 5-day volume SMA compared to the 20-day SMA → `rising`,
    `falling`, or `flat`.

### Example: analyse a watchlist

Ask Claude, with the server connected:

> Using yfinance-cache, analyse AAPL, MSFT, NVDA and TSLA on daily bars. Give me
> the SMAs, flag any breakouts, and tell me which have volume building.

Claude will call `analyze_tickers` (or `screen_signals` to get just the movers).

## Design notes

* `analysis.py` is **pure and dependency-free** (plain lists of floats), so the
  signal logic is fully unit-tested without network, pandas, or yfinance.
* `cache.py` is provider-agnostic JSON-blob storage over SQLite.
* `provider.py` is the only module that touches the network; `yfinance`/`pandas`
  are imported lazily so the rest of the package imports without them.

## Tests

```bash
pytest tests/test_yfinance_analysis.py \
       tests/test_yfinance_cache.py \
       tests/test_yfinance_provider.py -o addopts="--import-mode=importlib"
```

All three suites are network-free (the provider tests inject a fake `yfinance`).
