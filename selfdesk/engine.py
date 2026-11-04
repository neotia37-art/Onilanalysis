"""Index distribution days and market-score caps. No outside ratings."""
from __future__ import annotations

RULE_VERSION = 1
WINDOW = 25
EXPIRE_UP = 0.05
INDEX_DROP = 0.2
DD_PENALTY = [0, 4, 6, 8, 12, 16, 20]


def _round2(n: float) -> float:
    return round(float(n) + 0.0, 2)


def day_key(day: dict) -> str:
    return f"{day['date']}|{day['chg_pct']:.2f}|{1 if day['expired'] else 0}"


def list_distribution(bars: list[dict], min_drop: float = INDEX_DROP) -> list[dict]:
    if len(bars) < 2:
        return []
    last = bars[-1]["close"]
    end = len(bars) - 1
    start = max(1, end - (WINDOW - 1))
    out = []
    for i in range(start, end + 1):
        prev, bar = bars[i - 1], bars[i]
        if not (prev["volume"] > 0 and bar["volume"] > 0 and prev["close"] > 0):
            continue
        chg = _round2((bar["close"] / prev["close"] - 1) * 100)
        if chg > -min_drop or not (bar["volume"] > prev["volume"]):
            continue
        out.append(
            {
                "date": bar["date"],
                "chg_pct": chg,
                "close": bar["close"],
                "vol_vs_prev": _round2(bar["volume"] / prev["volume"]),
                "expired": last >= bar["close"] * (1 + EXPIRE_UP),
            }
        )
    return out


def active_distribution(bars: list[dict], min_drop: float = INDEX_DROP) -> list[dict]:
    return [d for d in list_distribution(bars, min_drop) if not d["expired"]]


def _sma(bars: list[dict], n: int):
    if len(bars) < n:
        return None
    return sum(b["close"] for b in bars[-n:]) / n


def _ret(bars: list[dict], sessions: int):
    if len(bars) <= sessions:
        return None
    prev = bars[-1 - sessions]["close"]
    if not prev:
        return None
    return bars[-1]["close"] / prev - 1


def score_index(symbol: str, bars: list[dict]) -> dict:
    last, prev = bars[-1], bars[-2]
    chg = _round2((last["close"] / prev["close"] - 1) * 100) if prev["close"] else 0.0
    s50, s200 = _sma(bars, 50), _sma(bars, 200)
    above50 = s50 is not None and last["close"] > s50
    above200 = s200 is not None and last["close"] > s200
    active = active_distribution(bars)
    n = len(active)
    cluster = 0
    for d in active:
        i = next((k for k, b in enumerate(bars) if b["date"] == d["date"]), None)
        if i is None:
            continue
        if len(bars) - 1 - i <= 9:
            cluster += 1
    today = any(d["date"] == last["date"] for d in active)
    raw = 46
    if s50 is None:
        pass
    elif above50:
        raw += 16
    else:
        raw -= 12
    if s200 is None:
        pass
    elif above200:
        raw += 12
    else:
        raw -= 16
    if s50 is not None and s200 is not None and s50 > s200 and above50:
        raw += 6
    raw -= DD_PENALTY[min(n, 6)]
    if cluster >= 3:
        raw -= 10
    if today:
        raw -= 8
    r21 = _ret(bars, 21)
    if r21 is not None and r21 >= 0.08:
        raw -= 4
    elif r21 is not None and r21 > 0:
        raw += 4
    raw = max(0, min(100, round(raw)))
    published = raw
    caps = []
    ceiling = 100

    def apply(cap: int, cid: str, reason: str):
        nonlocal published, ceiling
        if cap < ceiling:
            ceiling = cap
        if published > cap:
            caps.append({"id": cid, "cap": cap, "reason": reason})
            published = cap

    if n >= 6:
        apply(18, "dd6", "유효 분산일 6개 이상 — 상한 18")
    elif n == 5:
        apply(28, "dd5", "유효 분산일 5개 — 상한 28")
    elif n == 4:
        apply(40, "dd4", "유효 분산일 4개 — 상한 40")
    elif n == 3:
        apply(52, "dd3", "유효 분산일 3개 — 상한 52")
    elif n == 2:
        apply(68, "dd2", "유효 분산일 2개 — 상한 68")
    if cluster >= 3:
        apply(30 if n >= 4 else 54, "clusterCap", "10거래일 안에 분산 3개 이상")
    if s200 is not None and not above200:
        apply(32, "under200", "200일선 아래")
    elif s50 is not None and not above50:
        apply(54, "under50", "50일선 아래")
    if today:
        apply(56, "todayCap", "오늘 분산일")
    r10 = _ret(bars, 10)
    if r10 is not None and r10 > 0.06 and n >= 3:
        apply(44, "chase", "단기 급등 위에 분산")
    return {
        "symbol": symbol,
        "session_date": last["date"],
        "close": _round2(last["close"]),
        "chg_pct": chg,
        "active": active,
        "active_count": n,
        "cluster10": cluster,
        "today_dd": today,
        "above50": above50,
        "above200": above200,
        "raw": raw,
        "published": published,
        "ceiling": ceiling,
        "caps": caps,
        "sma50": None if s50 is None else _round2(s50),
        "sma200": None if s200 is None else _round2(s200),
    }


def compose_market(nas: dict, spx: dict) -> dict:
    published = min(nas["published"], spx["published"])
    raw = min(nas["raw"], spx["raw"])
    caps = []
    ceiling = min(nas["ceiling"], spx["ceiling"])

    def apply(cap: int, cid: str, reason: str):
        nonlocal published, ceiling
        if cap < ceiling:
            ceiling = cap
        if published > cap:
            caps.append({"id": cid, "cap": cap, "reason": reason})
            published = cap

    if nas["active_count"] >= 4 and spx["active_count"] >= 4:
        apply(32, "both4", "두 지수 모두 분산일 4개 이상 — 시장 상한 32")
    if nas["active_count"] >= 5 and spx["active_count"] >= 5:
        apply(22, "both5", "두 지수 모두 분산 캠페인 — 시장 상한 22")
    if nas["active_count"] >= 6 or spx["active_count"] >= 6:
        apply(18, "either6", "한쪽이라도 분산일 6개 — 시장 상한 18")
    if (nas["today_dd"] or spx["today_dd"]) and (nas["active_count"] >= 3 or spx["active_count"] >= 3):
        apply(48, "todayPressure", "오늘 분산 + 누적 3개")
    both_trend = nas["above50"] and nas["above200"] and spx["above50"] and spx["above200"]
    both_quiet = (
        nas["active_count"] <= 1
        and spx["active_count"] <= 1
        and not nas["today_dd"]
        and not spx["today_dd"]
    )
    stance, exposure, blocked = "현금 우선", "0–20%", True
    if published >= 76 and both_quiet and both_trend:
        stance, exposure, blocked = "제한적 적극", "80–100%", False
    elif published >= 62:
        stance, exposure = "확인된 돌파만", "60–80%"
    elif published >= 48:
        stance, exposure = "소수 선별", "40–60%"
    elif published >= 30:
        stance, exposure = "신규 억제", "20–40%"
    if blocked and published >= 76:
        apply(74, "noAggressive", "분산·추세 조건이 아니면 적극 구간을 열지 않음")
        stance, exposure = "확인된 돌파만", "60–80%"
    return {
        "raw": raw,
        "published": published,
        "ceiling": ceiling,
        "caps": caps,
        "stance": stance,
        "exposure": exposure,
        "aggressive_blocked": blocked,
    }


def make_entry(symbol: str, bars: list[dict], saved_at: str) -> dict:
    active = active_distribution(bars)
    return {
        "ruleVersion": RULE_VERSION,
        "symbol": symbol,
        "sessionDate": bars[-1]["date"],
        "close": _round2(bars[-1]["close"]),
        "activeCount": len(active),
        "keys": [day_key(d) for d in active],
        "savedAt": saved_at,
    }


def verify_entry(entry: dict, bars: list[dict]) -> dict:
    issues = []
    if entry.get("ruleVersion") != RULE_VERSION:
        issues.append("규칙 버전이 다릅니다")
    sliced = [b for b in bars if b["date"] <= entry["sessionDate"]]
    if not sliced or sliced[-1]["date"] != entry["sessionDate"]:
        return {"ok": False, "issues": ["이 세션의 봉이 없습니다"], "liveCount": 0}
    live = active_distribution(sliced)
    live_keys = [day_key(d) for d in live]
    if _round2(sliced[-1]["close"]) != _round2(entry["close"]):
        issues.append(f"종가 불일치 · 저장 {entry['close']} · 재계산 {_round2(sliced[-1]['close'])}")
    if len(live) != entry["activeCount"]:
        issues.append(f"개수 불일치 · 저장 {entry['activeCount']} · 재계산 {len(live)}")
    missing = [k for k in entry["keys"] if k not in live_keys]
    extra = [k for k in live_keys if k not in entry["keys"]]
    if missing:
        issues.append("저장에만 있는 날: " + ", ".join(k.split("|")[0] for k in missing))
    if extra:
        issues.append("재계산에만 있는 날: " + ", ".join(k.split("|")[0] for k in extra))
    return {"ok": not issues, "issues": issues, "liveCount": len(live)}
