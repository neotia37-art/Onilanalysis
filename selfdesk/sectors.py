"""US sector ranks from SPDR ETF daily bars. Rank is the 6-month return."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from selfdesk.yahoo import fetch_daily

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


def trailing_return(bars: list, sessions: int) -> float | None:
    if not bars or len(bars) <= sessions:
        return None
    last = bars[-1].get("close")
    prev = bars[-1 - sessions].get("close")
    if not last or not prev:
        return None
    return (last / prev - 1.0) * 100.0


def rank_sectors(bars_by_symbol: dict) -> dict:
    """bars_by_symbol maps ETF ticker to daily bars, oldest first."""
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
    asof = max(dates) if dates else None
    return {"rows": rows, "asof": asof, "basis": "6개월 수익률"}


def load_sector_ranks() -> dict:
    symbols = [etf for _, etf in SECTORS]
    found = {}
    errors = []

    def one(symbol):
        return symbol, fetch_daily(symbol, "1y")

    with ThreadPoolExecutor(max_workers=6) as pool:
        for symbol, result in pool.map(lambda s: _safe(one, s), symbols):
            if isinstance(result, Exception):
                errors.append(f"{symbol}: {result}")
            else:
                found[symbol] = result
    if len(found) < 8:
        detail = " · ".join(errors[:3]) or "시세 없음"
        raise RuntimeError("섹터 시세를 충분히 받지 못했습니다. " + detail)
    ranked = rank_sectors(found)
    ranked["errors"] = errors
    return ranked


def _safe(fn, symbol):
    try:
        return fn(symbol)
    except Exception as exc:
        return symbol, exc
