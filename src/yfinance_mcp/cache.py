"""SQLite-backed cache for data retrieved from yfinance.

Each category of data (``ohlcv``, ``fundamentals``, ``news``, ``info``) is
stored as a JSON blob keyed by ``(category, ticker)`` alongside the time it was
fetched. A per-category TTL controls when an entry is considered stale, so
repeated queries for the same ticker do not re-hit Yahoo within the TTL window.

The cache is deliberately provider-agnostic: it stores whatever JSON the
provider hands it and knows nothing about OHLCV or analysis.
"""

from __future__ import annotations

import json
import os
import sqlite3
import time
from dataclasses import dataclass
from typing import Any, Optional

# Default freshness windows, in seconds, per data category.
DEFAULT_TTLS: dict[str, int] = {
    "ohlcv": 6 * 60 * 60,  # intraday-ish; daily bars settle after close
    "fundamentals": 24 * 60 * 60,
    "info": 24 * 60 * 60,
    "news": 60 * 60,
}

DEFAULT_CACHE_PATH = os.environ.get(
    "YFINANCE_MCP_CACHE", os.path.expanduser("~/.cache/yfinance_mcp/cache.sqlite")
)


@dataclass
class CacheEntry:
    category: str
    ticker: str
    fetched_at: float
    payload: Any

    def age_seconds(self, now: Optional[float] = None) -> float:
        return (now if now is not None else time.time()) - self.fetched_at


class Cache:
    """A tiny JSON blob cache on top of SQLite."""

    def __init__(
        self,
        path: str = DEFAULT_CACHE_PATH,
        ttls: Optional[dict[str, int]] = None,
    ) -> None:
        self.path = path
        self.ttls = {**DEFAULT_TTLS, **(ttls or {})}
        if path != ":memory:":
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self._conn = sqlite3.connect(path)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                category   TEXT NOT NULL,
                ticker     TEXT NOT NULL,
                fetched_at REAL NOT NULL,
                payload    TEXT NOT NULL,
                PRIMARY KEY (category, ticker)
            )
            """
        )
        self._conn.commit()

    def ttl_for(self, category: str) -> int:
        return self.ttls.get(category, 24 * 60 * 60)

    def get(
        self,
        category: str,
        ticker: str,
        *,
        max_age: Optional[float] = None,
        now: Optional[float] = None,
    ) -> Optional[CacheEntry]:
        """Return a fresh cache entry, or ``None`` if missing/stale.

        ``max_age`` overrides the category TTL when provided.
        """
        ticker = ticker.upper()
        row = self._conn.execute(
            "SELECT category, ticker, fetched_at, payload FROM cache "
            "WHERE category = ? AND ticker = ?",
            (category, ticker),
        ).fetchone()
        if row is None:
            return None
        now = time.time() if now is None else now
        ttl = self.ttl_for(category) if max_age is None else max_age
        age = now - row["fetched_at"]
        if age > ttl:
            return None
        return CacheEntry(
            category=row["category"],
            ticker=row["ticker"],
            fetched_at=row["fetched_at"],
            payload=json.loads(row["payload"]),
        )

    def set(
        self,
        category: str,
        ticker: str,
        payload: Any,
        *,
        now: Optional[float] = None,
    ) -> CacheEntry:
        ticker = ticker.upper()
        now = time.time() if now is None else now
        self._conn.execute(
            "INSERT OR REPLACE INTO cache (category, ticker, fetched_at, payload) "
            "VALUES (?, ?, ?, ?)",
            (category, ticker, now, json.dumps(payload, default=str)),
        )
        self._conn.commit()
        return CacheEntry(category, ticker, now, payload)

    def peek(self, category: str, ticker: str) -> Optional[CacheEntry]:
        """Return the entry ignoring TTL (used as a fallback when a fetch fails)."""
        ticker = ticker.upper()
        row = self._conn.execute(
            "SELECT category, ticker, fetched_at, payload FROM cache "
            "WHERE category = ? AND ticker = ?",
            (category, ticker),
        ).fetchone()
        if row is None:
            return None
        return CacheEntry(
            row["category"],
            row["ticker"],
            row["fetched_at"],
            json.loads(row["payload"]),
        )

    def invalidate(self, category: Optional[str] = None, ticker: Optional[str] = None) -> int:
        """Delete entries. Returns the number of rows removed."""
        clauses, params = [], []
        if category is not None:
            clauses.append("category = ?")
            params.append(category)
        if ticker is not None:
            clauses.append("ticker = ?")
            params.append(ticker.upper())
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        cur = self._conn.execute(f"DELETE FROM cache {where}", params)
        self._conn.commit()
        return cur.rowcount

    def stats(self) -> list[dict[str, Any]]:
        rows = self._conn.execute(
            "SELECT category, COUNT(*) AS n, MIN(fetched_at) AS oldest, "
            "MAX(fetched_at) AS newest FROM cache GROUP BY category"
        ).fetchall()
        return [dict(r) for r in rows]

    def close(self) -> None:
        self._conn.close()
