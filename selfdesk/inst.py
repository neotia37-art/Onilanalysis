"""Institutional sponsorship from non-IBD sources.

US: Nasdaq's 13F summary (every filer: new, sold-out, increased, decreased)
plus Yahoo's top mutual funds. One quarter. Not a multi-quarter fund-count streak.
KR: exchange investor net flow (기관/외국인), which is not a 13F sponsorship list.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timedelta
from urllib.parse import quote as urlquote
from urllib.request import Request, urlopen

_INDEXER = (
    "vanguard",
    "blackrock",
    "black rock",
    "state street",
    "geode",
    "northern trust",
    "charles schwab",
)
_US = re.compile(r"[A-Z][A-Z0-9.\-]{0,9}")


def resolve_kind(symbol: str, market: str = "") -> tuple[str, str]:
    """Sidebar market wins. Korean codes stay 6 digits; US tickers stay as typed."""
    raw = (symbol or "").strip().upper().replace(" ", "")
    if not raw:
        raise ValueError("사이드바에서 종목을 조회하면 기관동향이 열립니다.")
    if (market or "").upper() == "KR" or raw.endswith(".KS") or raw.endswith(".KQ") or (raw.isdigit() and len(raw) == 6):
        code = raw[:-3] if raw.endswith(".KS") or raw.endswith(".KQ") else raw
        if not (code.isdigit() and len(code) == 6):
            raise ValueError("한국 종목코드 6자리가 아닙니다.")
        return "KR", code
    if not _US.fullmatch(raw):
        raise ValueError("티커 형식이 아닙니다.")
    return "US", raw


def parse_int(value) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value).strip().replace(",", "").replace("$", "").replace(" ", "")
    if text in ("", "-", "—", "N/A", "NA"):
        return None
    neg = text.startswith("(") and text.endswith(")")
    text = text.strip("()")
    if text[:1] in "+":
        text = text[1:]
    try:
        number = int(float(text))
    except ValueError:
        return None
    return -number if neg else number


def parse_pct(value) -> float | None:
    """'79.70%' or '-0.726%' → percent points. Bare numbers stay as given."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "").replace(" ", "")
    if text in ("", "-", "—", "N/A", "NA"):
        return None
    neg = text.startswith("(") and text.endswith(")")
    text = text.strip("()").rstrip("%")
    if text[:1] in "+":
        text = text[1:]
    try:
        number = float(text)
    except ValueError:
        return None
    return -number if neg else number


def _norm_date(value) -> str:
    text = str(value or "").strip()
    parts = text.split("/")
    if len(parts) == 3 and all(p.isdigit() for p in parts):
        month, day, year = (int(p) for p in parts)
        return f"{year:04d}-{month:02d}-{day:02d}"
    return text


def is_indexer(name: str) -> bool:
    low = (name or "").lower()
    return any(key in low for key in _INDEXER)


def _bias(up: int | None, down: int | None, band: float = 0.08) -> str:
    if up is None or down is None:
        return "없음"
    total = up + down
    if total <= 0:
        return "없음"
    if abs(up - down) / total < band:
        return "비슷"
    return "확대" if up > down else "축소"


def _row_count(rows: list, *needles: str) -> tuple[int | None, int | None]:
    for row in rows:
        label = str(row.get("positions") or "").lower()
        if any(n in label for n in needles):
            return parse_int(row.get("holders")), parse_int(row.get("shares"))
    return None, None


def parse_nasdaq(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("기관 보유 응답이 비었습니다.")
    summary = data.get("ownershipSummary") or {}
    active = ((data.get("activePositions") or {}).get("rows")) or []
    fresh = ((data.get("newSoldOutPositions") or {}).get("rows")) or []
    table = ((data.get("holdingsTransactions") or {}).get("table") or {}).get("rows") or []
    if not active and not fresh and not table:
        raise ValueError("이 티커의 13F 보유 집계가 없습니다.")
    increased, _ = _row_count(active, "increased")
    decreased, _ = _row_count(active, "decreased")
    unchanged, _ = _row_count(active, "held position")
    holders, _ = _row_count(active, "total institutional")
    new, new_shares = _row_count(fresh, "new position")
    sold, sold_shares = _row_count(fresh, "sold")
    if holders is None:
        holders = parse_int((data.get("holdingsTransactions") or {}).get("totalRecords"))
    own = parse_pct(((summary.get("SharesOutstandingPCT") or {}).get("value")))
    rows = []
    for raw in table:
        name = str(raw.get("ownerName") or "").strip()
        if not name:
            continue
        change = parse_int(raw.get("sharesChange"))
        rows.append(
            {
                "name": name,
                "date": _norm_date(raw.get("date")),
                "shares": parse_int(raw.get("sharesHeld")),
                "change": change,
                "change_pct": parse_pct(raw.get("sharesChangePCT")),
                "indexer": is_indexer(name),
                "action": _action(change),
            }
        )
    return {
        "own_pct": own,
        "holders": holders,
        "increased": increased,
        "decreased": decreased,
        "unchanged": unchanged,
        "new": new,
        "sold": sold,
        "new_shares": new_shares,
        "sold_shares": sold_shares,
        "rows": rows,
    }


def _action(change: int | None) -> str:
    if change is None:
        return "—"
    if change > 0:
        return "확대"
    if change < 0:
        return "축소"
    return "유지"


def judge_us(snap: dict) -> dict:
    """One-quarter read. Does not invent a multi-quarter streak or a fund grade."""
    holder_bias = _bias(snap.get("increased"), snap.get("decreased"))
    count_bias = _bias(snap.get("new"), snap.get("sold"))
    if holder_bias == "확대" and count_bias == "확대":
        stance = "이번 분기 보증 확대"
    elif holder_bias == "축소" and count_bias == "축소":
        stance = "이번 분기 보증 축소"
    elif holder_bias == "없음" and count_bias == "없음":
        stance = "자료 부족"
    else:
        stance = "혼조"
    notes = []
    new, sold = snap.get("new"), snap.get("sold")
    if new is not None and sold is not None:
        notes.append(
            f"이번 분기 기관 수는 신규 {new:,}곳, 청산 {sold:,}곳, 차이 {new - sold:+,}곳이다. "
            "몇 분기 연속으로 늘었는지는 이 자료에 없다."
        )
    inc, dec = snap.get("increased"), snap.get("decreased")
    if inc is not None and dec is not None:
        notes.append(f"지분을 늘린 기관 {inc:,}곳, 줄인 기관 {dec:,}곳이다.")
    active_up = active_down = indexer_up = indexer_down = 0
    for row in snap.get("rows") or []:
        if row["action"] == "확대":
            if row["indexer"]:
                indexer_up += 1
            else:
                active_up += 1
        elif row["action"] == "축소":
            if row["indexer"]:
                indexer_down += 1
            else:
                active_down += 1
    if snap.get("rows"):
        notes.append(
            f"보유 상위 이름에서 지수 운용사를 빼면 확대 {active_up}곳, 축소 {active_down}곳이다. "
            "상위 목록이지 전체 기관이 아니다."
        )
        if active_up == 0 and indexer_up > 0:
            notes.append(
                "상위 목록에서 지분을 늘린 이름은 지수 운용사뿐이다. "
                "우량 펀드가 새로 샀다고 말하지 않는다."
            )
    own = snap.get("own_pct")
    if own is not None and own > 100:
        notes.append("보유율이 100%를 넘는다. 공매도나 이중 계상일 수 있어, 비율보다 신규·청산·확대 수를 본다.")
    elif own is not None and own >= 90 and stance != "이번 분기 보증 확대":
        notes.append("기관 보유 비율이 이미 높다. 새로 들어오는 수요로 보기 어렵다.")
    elif own is not None and own < 15:
        notes.append("기관 보유 비율이 낮다. 보증이 얇다.")
    return {
        "stance": stance,
        "holder_bias": holder_bias,
        "count_bias": count_bias,
        "active_up": active_up,
        "active_down": active_down,
        "indexer_up": indexer_up,
        "indexer_down": indexer_down,
        "notes": notes,
    }


def judge_funds(funds: list[dict]) -> dict:
    up = sum(1 for f in funds if f.get("action") == "확대")
    down = sum(1 for f in funds if f.get("action") == "축소")
    if not funds:
        text = "상위 뮤추얼펀드 목록을 받지 못했다."
    else:
        text = (
            f"Yahoo 상위 뮤추얼펀드 {len(funds)}곳 중 확대 {up}곳, 축소 {down}곳이다. "
            "전체 펀드 수가 아니고, 그 펀드 안에서의 보유 순위도 아니다."
        )
    return {"up": up, "down": down, "text": text}


def _num(value):
    try:
        if value is None or value != value:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def fund_action(pct_change: float | None) -> str:
    """Yahoo pctChange is a fraction of the share count (0.016 = +1.6%)."""
    if pct_change is None:
        return "—"
    if abs(pct_change) < 0.002:
        return "유지"
    return "확대" if pct_change > 0 else "축소"


def judge_kr(recent_inst: int | None, prior_inst: int | None, recent_foreign: int | None) -> dict:
    if recent_inst is None:
        return {"stance": "자료 부족", "notes": ["기관 순매수를 만들지 못했습니다."]}
    if prior_inst is None:
        stance = "기관 순매수" if recent_inst > 0 else ("기관 순매도" if recent_inst < 0 else "기관 보합")
    elif recent_inst > 0 and recent_inst > prior_inst:
        stance = "최근 기관 매수 우위"
    elif recent_inst < 0 and recent_inst < prior_inst:
        stance = "최근 기관 매도 우위"
    else:
        stance = "기관 수급 혼조"
    notes = [
        "한국 거래소 투자자 순매수다. 미국 13F나 IBD 펀드 목록이 아니다.",
        "오닐이 말한 '어느 펀드가 신규 상위인지'는 여기서 알 수 없다.",
    ]
    if recent_foreign is not None and recent_inst is not None:
        if recent_inst > 0 and recent_foreign < 0:
            notes.append("최근 20거래일은 기관이 사고 외국인이 판 자리다.")
        elif recent_inst < 0 and recent_foreign > 0:
            notes.append("최근 20거래일은 기관이 팔고 외국인이 산 자리다.")
    return {"stance": stance, "notes": notes}


def fetch_nasdaq(symbol: str) -> dict:
    url = (
        "https://api.nasdaq.com/api/company/"
        f"{urlquote(symbol, safe='')}/institutional-holdings?limit=15"
    )
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://www.nasdaq.com",
            "Referer": "https://www.nasdaq.com/",
        },
    )
    with urlopen(req, timeout=25) as res:
        body = json.loads(res.read().decode("utf-8"))
    data = body.get("data") if isinstance(body, dict) else None
    if not data:
        raise ValueError(f"{symbol}: 13F 보유 자료가 없습니다.")
    return data


def fetch_yahoo_funds(symbol: str) -> dict:
    """Top mutual funds. Failure returns an empty list rather than raising."""
    yahoo_symbol = symbol.replace(".", "-")
    try:
        import yfinance as yf

        ticker = yf.Ticker(yahoo_symbol)
        frame = ticker.mutualfund_holders
        major = ticker.major_holders
    except Exception as exc:
        return {"funds": [], "own_pct": None, "holders": None, "error": str(exc)}
    own_pct = holders = None
    try:
        lookup = {}
        if major is not None and len(getattr(major, "index", [])) > 0:
            columns = list(getattr(major, "columns", []))
            if "Breakdown" in columns and "Value" in columns:
                lookup = dict(zip(major["Breakdown"], major["Value"]))
            else:
                column = columns[0]
                lookup = {str(i): major.loc[i, column] for i in major.index}
        raw_own = _num(lookup.get("institutionsPercentHeld"))
        if raw_own is not None:
            own_pct = raw_own * 100
        holders = parse_int(lookup.get("institutionsCount"))
    except Exception:
        pass
    funds = []
    if frame is not None and len(getattr(frame, "index", [])) > 0:
        for _, row in frame.iterrows():
            change = _num(row.get("pctChange"))
            reported = row.get("Date Reported")
            held = _num(row.get("pctHeld"))
            funds.append(
                {
                    "name": str(row.get("Holder") or ""),
                    "date": str(reported)[:10] if reported is not None else "",
                    "pct_held": None if held is None else held * 100,
                    "shares": parse_int(row.get("Shares")),
                    "change_pct": None if change is None else change * 100,
                    "action": fund_action(change),
                }
            )
    return {"funds": funds, "own_pct": own_pct, "holders": holders, "error": None}


def _col(columns, needle: str):
    for name in columns:
        if needle in str(name):
            return name
    return None


def summarize_kr_frame(frame) -> dict:
    if frame is None or len(getattr(frame, "index", [])) == 0:
        raise ValueError("거래원 순매수가 비었습니다.")
    inst_col = _col(frame.columns, "기관")
    foreign_col = _col(frame.columns, "외국")
    if inst_col is None:
        raise ValueError("기관 열을 찾지 못했습니다.")
    inst = [int(v) for v in frame[inst_col].tolist()]
    foreign = [int(v) for v in frame[foreign_col].tolist()] if foreign_col is not None else []
    recent_i = inst[-20:]
    prior_i = inst[-40:-20]
    recent_f = foreign[-20:] if foreign else []
    recent_inst = sum(recent_i) if recent_i else None
    prior_inst = sum(prior_i) if len(prior_i) >= 10 else None
    recent_foreign = sum(recent_f) if recent_f else None
    dates = [str(i)[:10] for i in frame.index[-8:]]
    tail = []
    start = max(0, len(inst) - 8)
    for offset, value in enumerate(inst[start:]):
        tail.append(
            {
                "date": dates[offset] if offset < len(dates) else "",
                "inst": value,
                "foreign": foreign[start + offset] if foreign else None,
            }
        )
    judged = judge_kr(recent_inst, prior_inst, recent_foreign)
    return {
        "recent_inst": recent_inst,
        "prior_inst": prior_inst,
        "recent_foreign": recent_foreign,
        "days": len(recent_i),
        "tail": tail,
        "judge": judged,
    }


def fetch_kr(code: str) -> dict:
    try:
        from pykrx import stock
    except Exception as exc:
        raise RuntimeError("한국 거래원 자료(pykrx)를 열지 못했습니다: " + str(exc)) from exc
    end = datetime.now()
    start = end - timedelta(days=160)
    frame = stock.get_market_trading_value_by_date(
        start.strftime("%Y%m%d"), end.strftime("%Y%m%d"), code
    )
    out = summarize_kr_frame(frame)
    out["unit"] = "원"
    return out


def load_us(symbol: str) -> dict:
    snap = parse_nasdaq(fetch_nasdaq(symbol))
    yahoo = fetch_yahoo_funds(symbol)
    snap["yahoo"] = yahoo
    snap["judge"] = judge_us(snap)
    snap["funds_judge"] = judge_funds(yahoo.get("funds") or [])
    snap["symbol"] = symbol
    return snap
