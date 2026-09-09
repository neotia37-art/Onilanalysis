# psycho functions v14.13 (seed/explain live in ibd_mkt_psycho_v14_13.py)
MKT_PSYCHO_FN_V14_13 = True


def _psycho_norm_date(d):
    try:
        return pd.Timestamp(d).strftime("%Y-%m-%d")
    except Exception:
        return str(d or "")[:10]


def ensure_psycho_history(desk=None):
    if desk is None:
        try:
            desk = load_ibd_desk()
        except Exception:
            desk = {}
    lists = desk.setdefault("lists", {}) if isinstance(desk, dict) else {}
    hist = list(lists.get("psycho_history") or [])
    by_d = {_psycho_norm_date(x.get("date")): dict(x) for x in hist if x}
    for rec in PSYCHO_SEED_HISTORY:
        by_d[_psycho_norm_date(rec["date"])] = dict(rec)
    out = sorted(by_d.values(), key=lambda x: _psycho_norm_date(x.get("date")))
    if isinstance(desk, dict):
        lists["psycho_history"] = out
        lists["psycho_latest"] = out[-1] if out else {}
        pulse = dict(lists.get("market_pulse_latest") or {})
        if not pulse:
            pulse = {"date": "2026-09-03", "exposure": "60%-80%", "dist_nasdaq": 4, "dist_spx": 3, "ftd": "2026-06-02", "market_score": 65, "headline": "Software rally, lower yields fuel broad-based gains"}
        pulse.setdefault("official_date", pulse.get("date") or "2026-09-03")
        pulse.setdefault("dist_nasdaq_official", 4)
        pulse.setdefault("dist_spx_official", 3)
        pulse["candidate_dd_20260908"] = {"nasdaq": True, "spx": True, "why": "Tue down + NYSE vol 4966 vs Fri 4103 / NAS 7714 vs 6529", "nasdaq_close": 26423.6, "nasdaq_chg_pts": -81.7, "dji_close": 52786.0, "dji_chg_pts": -628.1, "spx_chg_pts": -45.0, "nyse_vol": 4966, "nyse_vol_prev": 4103, "nasdaq_vol": 7714, "nasdaq_vol_prev": 6529, "adv": 1593, "dec": 2835}
        pulse["working_dist_nasdaq"] = int(pulse.get("dist_nasdaq_official") or 4) + 1
        pulse["working_dist_spx"] = int(pulse.get("dist_spx_official") or 3) + 1
        pulse["ftd"] = pulse.get("ftd") or "2026-06-02"
        lists["market_pulse_latest"] = pulse
        try:
            save_ibd_desk(desk)
        except Exception:
            pass
    return out


def upsert_psycho_row(desk, rec):
    rec = dict(rec)
    rec["date"] = _psycho_norm_date(rec.get("date"))
    lists = desk.setdefault("lists", {})
    hist = [x for x in (lists.get("psycho_history") or []) if _psycho_norm_date(x.get("date")) != rec["date"]]
    hist.append(rec)
    hist.sort(key=lambda x: _psycho_norm_date(x.get("date")))
    lists["psycho_history"] = hist
    lists["psycho_latest"] = rec
    try:
        save_ibd_desk(desk)
    except Exception:
        pass
    return hist


def _psycho_live_vix(states=None):
    states = states or {}
    for key in ("VIX", "^VIX", "vix"):
        s = states.get(key) or {}
        if s.get("px") is not None:
            try:
                return float(s["px"]), s.get("chg")
            except Exception:
                pass
    try:
        import yfinance as yf
        h = yf.Ticker("^VIX").history(period="5d")
        if h is not None and len(h):
            px = float(h["Close"].iloc[-1])
            chg = None
            if len(h) >= 2:
                prev = float(h["Close"].iloc[-2])
                chg = (px / prev - 1.0) * 100.0 if prev else None
            return px, chg
    except Exception:
        pass
    return None, None


def _psycho_read_one(name, val):
    if val is None or val == "":
        return "수치 없음", "idle"
    try:
        v = float(val)
    except Exception:
        return "수치 없음", "idle"
    if name == "vix":
        if v >= 45:
            return "고VIX · 공포(역발상 바닥 후보)", "up"
        if v >= 20:
            return "변동 확대 · 단기 스윙", "warn"
        return "저VIX · 안일. 바닥 신호가 아니다", "warn"
    if name == "put_call":
        if v >= 1.0:
            return "풋 우세 · 헤지/공포", "up"
        if v >= 0.80:
            return "중립 상단", "idle"
        return "콜 편중 · 낙관", "warn"
    if name == "high_low":
        if v < 0.10:
            return "극단 신저 · 약세장 바닥 문턱", "warn"
        if v < 0.50:
            return "0.5 아래 · 중간조정 바닥 감시", "up"
        return "0.5 위 · 반등 트리거 아님", "idle"
    if name == "bulls":
        if v >= 55:
            return "자문 낙관 과열 쪽", "warn"
        if v <= 35:
            return "자문 비관 · 역발상 관심", "up"
        return "자문 낙관 보통", "idle"
    if name == "bears":
        if v <= 20:
            return "약세 자문 극소 · 군중 안일", "warn"
        if v >= 40:
            return "약세 자문 많음 · 공포", "up"
        return "약세 자문 보통", "idle"
    if name == "margin":
        if v >= 55:
            return "신용 55%+ · 대형 천정 경고", "down"
        if v >= 40:
            return "신용 확장 중 · 경계", "warn"
        return "신용 경고선(55%) 아래", "idle"
    return "—", "idle"
