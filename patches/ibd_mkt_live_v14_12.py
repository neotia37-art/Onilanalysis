# 시장 탭 LIVE 패널 v14.12 — 앱 계산 + CNN 공식 + IBD Pulse 비교
MKT_LIVE_V14_12 = True

_CNN_FNG_FALLBACK = {
    "score": 41.9, "rating": "fear",
    "timestamp": "2026-09-04T23:59:43+00:00",
    "previous_close": 35.2, "previous_1_week": 52.3,
    "previous_1_month": 60.0, "previous_1_year": 61.2,
    "source": "CNN snapshot 2026-09-04 (fallback)",
    "indicators": [
        ("모멘텀 SPX", 36.6, "fear"),
        ("주가 강도", 12.6, "extreme fear"),
        ("시장 폭", 46.4, "neutral"),
        ("풋콜", 45.2, "neutral"),
        ("VIX", 50.0, "neutral"),
        ("정크본드", 76.2, "extreme greed"),
        ("안전자산", 26.0, "fear"),
    ],
}


def fetch_cnn_fng_full():
    """CNN 공식 Fear & Greed + 7요인. Referer 없으면 418이 난다."""
    try:
        import requests
        r = requests.get(
            "https://production.dataviz.cnn.io/index/fearandgreed/graphdata",
            timeout=12,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Referer": "https://edition.cnn.com/markets/fear-and-greed",
                "Origin": "https://edition.cnn.com",
            },
        )
        r.raise_for_status()
        j = r.json()
        fg = j.get("fear_and_greed") or {}
        keys = [
            ("market_momentum_sp500", "모멘텀 SPX"),
            ("stock_price_strength", "주가 강도"),
            ("stock_price_breadth", "시장 폭"),
            ("put_call_options", "풋콜"),
            ("market_volatility_vix", "VIX"),
            ("junk_bond_demand", "정크본드"),
            ("safe_haven_demand", "안전자산"),
        ]
        inds = []
        for k, name in keys:
            blk = j.get(k) or {}
            if blk.get("score") is not None:
                inds.append((name, float(blk["score"]), str(blk.get("rating") or "")))
        return {
            "score": float(fg.get("score")),
            "rating": fg.get("rating") or "",
            "timestamp": fg.get("timestamp") or "",
            "previous_close": fg.get("previous_close"),
            "previous_1_week": fg.get("previous_1_week"),
            "previous_1_month": fg.get("previous_1_month"),
            "previous_1_year": fg.get("previous_1_year"),
            "source": "CNN production.dataviz",
            "indicators": inds,
        }
    except Exception:
        return dict(_CNN_FNG_FALLBACK)


def _mkt_live_cnn_label(score, rating=""):
    rating = (rating or "").replace("_", " ").strip().lower()
    if rating:
        kr = {"extreme fear": "극단적 공포", "fear": "공포", "neutral": "중립",
              "greed": "탐욕", "extreme greed": "극단적 탐욕"}.get(rating, rating)
        return kr, rating
    try:
        s = float(score)
    except Exception:
        return "—", ""
    if s <= 24:
        return "극단적 공포", "extreme fear"
    if s <= 44:
        return "공포", "fear"
    if s <= 55:
        return "중립", "neutral"
    if s <= 75:
        return "탐욕", "greed"
    return "극단적 탐욕", "extreme greed"


def _mkt_live_kind(label):
    if "극단" in str(label):
        return "down"
    if "공포" in str(label) or "탐욕" in str(label):
        return "warn"
    return "idle"


def _mkt_ibd_stance(pulse, bw=None, states=None):
    """IBD는 공포탐욕이 아니다. 노출·분산·FTD를 0-100으로만 나란히 놓는다."""
    pulse = pulse or {}
    exp = str(pulse.get("exposure") or "")
    exp_map = {"0%-20%": 18, "20%-40%": 32, "40%-60%": 48, "60%-80%": 62, "80%-100%": 78}
    score = exp_map.get(exp)
    if score is None:
        try:
            score = int(pulse.get("market_score") or 50)
        except Exception:
            score = 50
    dd = pulse.get("dist_nasdaq")
    try:
        dd = int(dd)
    except Exception:
        dd = None
    adj = 0
    if dd is not None:
        if dd >= 5:
            adj -= 18
        elif dd >= 3:
            adj -= 8
        elif dd <= 2:
            adj += 6
    if not pulse.get("ftd"):
        adj -= 8
    score = int(max(0, min(100, score + adj)))
    if bw and bw.get("score") is not None:
        try:
            score = int(round(0.55 * score + 0.45 * float(bw["score"])))
        except Exception:
            pass
    if score <= 24:
        label = "현금·관망 (IBD 노출 최저)"
    elif score <= 44:
        label = "압박 · 추격 금지"
    elif score <= 55:
        label = "중립 · 허가는 좁다"
    elif score <= 75:
        label = "확정 상승 · 압박 가능"
    else:
        label = "노출 최대 · 리더만"
    why = (f"노출 {exp or '—'} · 나스닥분산 {pulse.get('dist_nasdaq','—')} "
           f"S&P분산 {pulse.get('dist_spx','—')} · FTD {pulse.get('ftd') or '—'}")
    live_label = None
    if states:
        labs = [s.get("label") for s in states.values() if s.get("label")]
        if labs:
            live_label = " / ".join(dict.fromkeys(labs))
    return {
        "score": score,
        "label": label,
        "why": why,
        "exposure": exp,
        "dist_nasdaq": pulse.get("dist_nasdaq"),
        "dist_spx": pulse.get("dist_spx"),
        "ftd": pulse.get("ftd"),
        "headline": pulse.get("headline") or "",
        "date": pulse.get("date") or "",
        "live_label": live_label,
        "bw": None if not bw else bw.get("score"),
        "bw_grade": None if not bw else bw.get("grade"),
    }
