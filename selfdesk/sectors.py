"""US sector ranks from one SPDR request. Rank is the 6-month price return."""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from urllib.request import Request, urlopen

SECTORS = (
    ("기술", "XLK"),
    ("커뮤니케이션", "XLC"),
    ("경기소비재", "XLY"),
    ("필수소비재", "XLP"),
    ("에너지", "XLE"),
    ("금융", "XLF"),
    ("헬스케어", "XLV"),
    ("산업재", "XLI"),
    ("소재", "XLB"),
    ("부동산", "XLRE"),
    ("유틸리티", "XLU"),
)

# Yahoo's English sector name -> SPDR
ENGLISH = {
    "Technology": "XLK",
    "Communication Services": "XLC",
    "Consumer Cyclical": "XLY",
    "Consumer Defensive": "XLP",
    "Energy": "XLE",
    "Financial Services": "XLF",
    "Financial": "XLF",
    "Healthcare": "XLV",
    "Industrials": "XLI",
    "Basic Materials": "XLB",
    "Real Estate": "XLRE",
    "Utilities": "XLU",
}

_CACHE = {"at": 0.0, "data": None}
_TTL = 1800


def clear_sector_cache() -> None:
    _CACHE["at"] = 0.0
    _CACHE["data"] = None


def trailing_return(bars: list, sessions: int) -> float | None:
    if not bars or len(bars) <= sessions:
        return None
    last = bars[-1].get("close")
    prev = bars[-1 - sessions].get("close")
    if not last or not prev:
        return None
    return (last / prev - 1.0) * 100.0


def rank_sectors(bars_by_symbol: dict) -> dict:
    name_of = {etf: name for name, etf in SECTORS}
    rows = []
    dates = []
    for etf, bars in bars_by_symbol.items():
        if not bars:
            continue
        dates.append(bars[-1]["date"])
        rows.append(
            {
                "name": name_of.get(etf, etf),
                "etf": etf,
                "date": bars[-1]["date"],
                "r1": trailing_return(bars, 21),
                "r3": trailing_return(bars, 63),
                "r6": trailing_return(bars, 126),
            }
        )

    def sort_key(row):
        def key(value):
            return value if value is not None else -10_000.0

        return (key(row["r6"]), key(row["r3"]), key(row["r1"]))

    rows.sort(key=sort_key, reverse=True)
    for i, row in enumerate(rows, start=1):
        row["rank"] = i
    return {"rows": rows, "asof": max(dates) if dates else None, "basis": "6개월 가격 수익률"}


def fetch_sector_bars() -> dict:
    symbols = ",".join(etf for _, etf in SECTORS)
    url = (
        "https://query1.finance.yahoo.com/v7/finance/spark"
        f"?symbols={symbols}&range=1y&interval=1d"
    )
    req = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    with urlopen(req, timeout=12) as res:
        body = json.loads(res.read().decode("utf-8"))
    result = ((body.get("spark") or {}).get("result")) or []
    found = {}
    for item in result:
        resp = (item.get("response") or [None])[0] or {}
        ts = resp.get("timestamp") or []
        quote = ((resp.get("indicators") or {}).get("quote") or [{}])[0]
        closes = quote.get("close") or []
        bars = []
        for i, unix in enumerate(ts):
            close = closes[i] if i < len(closes) else None
            if not close or close <= 0:
                continue
            bars.append(
                {
                    "date": datetime.fromtimestamp(unix, tz=timezone.utc).strftime("%Y-%m-%d"),
                    "close": float(close),
                }
            )
        if len(bars) >= 130:
            found[item.get("symbol")] = bars
    if len(found) < 8:
        raise RuntimeError(f"섹터 시세가 {len(found)}개뿐입니다.")
    return found


def load_sector_ranks() -> dict:
    now = time.time()
    if _CACHE["data"] and now - _CACHE["at"] < _TTL:
        return _CACHE["data"]
    ranked = rank_sectors(fetch_sector_bars())
    ranked["errors"] = []
    _CACHE["at"] = now
    _CACHE["data"] = ranked
    return ranked


def sector_for_stock(sector: str | None) -> dict | None:
    """Same shape the individual-stock card already reads."""
    board = load_sector_ranks()
    rows = board.get("rows") or []
    if not rows:
        return None
    etf = ENGLISH.get(sector or "") or dict(SECTORS).get(sector or "")
    hit = next((row for row in rows if row["etf"] == etf), None)
    if not hit or hit.get("r6") is None:
        return None
    return {
        "rank": hit["rank"],
        "total": len(rows),
        "ret": hit["r6"],
        "label": f'{sector} ({hit["etf"]}) · 6개월 {hit["r6"]:+.1f}% · 기준 {hit["date"]}',
        "top": [row["name"] for row in rows[:3]],
    }
