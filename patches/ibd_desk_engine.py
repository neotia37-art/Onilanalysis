# 엔진 ⑥-d 기관보증(I) · IBD 데스크 (수동 일지 + 자동 근사)
IBD_DESK_FILE = "ibd_desk.json"
IBD_I_ADJ = (
    "기관보증 패널은 IBD 원전 I가 아니다. 거래량비율·지수 거래량은 자동, "
    "36개월 펀드·블록 목록·종목 분석문은 구독 화면을 보고 수동으로 옮긴다. "
    "자동 점수만으로 매수 허가를 주지 않는다."
)

def empty_ibd_desk():
    return {"front": [], "funds": [], "block": [], "notes": {}}

def load_ibd_desk():
    if "ibd_desk" not in st.session_state:
        st.session_state["ibd_desk"] = load_json_file(IBD_DESK_FILE, empty_ibd_desk())
    d = st.session_state["ibd_desk"]
    d.setdefault("front", []); d.setdefault("funds", [])
    d.setdefault("block", []); d.setdefault("notes", {})
    return d

def save_ibd_desk(d):
    st.session_state["ibd_desk"] = d
    save_json_file(IBD_DESK_FILE, d)

def vol_ratio_corner(df):
    if df is None or len(df) < 55 or "Volume" not in df.columns:
        return None
    v = df["Volume"].astype(float)
    c = df["Close"].astype(float)
    vma = float(v.rolling(50).mean().iloc[-1])
    if not vma or vma <= 0:
        return None
    last = float(v.iloc[-1])
    ratio = last / vma
    chg = float(c.iloc[-1] / c.iloc[-2] - 1) * 100 if len(c) >= 2 else None
    v5 = float(v.tail(5).mean()) / vma
    up = dn = 0.0
    for i in range(-20, 0):
        if abs(i) >= len(df):
            continue
        pc = float(c.iloc[i] / c.iloc[i - 1] - 1) * 100
        vv = float(v.iloc[i])
        if pc > 0:
            up += vv
        elif pc < 0:
            dn += vv
    ad = (up / dn) if dn else None
    if chg is not None and chg >= 0.4 and ratio >= 1.4:
        flag = ("매집형 거래량", "pass", "상승 + 50일평균 1.4배 이상")
    elif chg is not None and chg <= -0.4 and ratio >= 1.4:
        flag = ("분산형 거래량", "fail", "하락 + 거래량 증가")
    elif ratio < 0.7:
        flag = ("거래 건조", "idle", "평균의 70% 미만")
    else:
        flag = ("보통", "idle", "비율만으로는 매집 미확인")
    return {"ratio": ratio, "vma": vma, "last": last, "chg": chg, "v5": v5, "ad20": ad, "flag": flag}

def index_tape(states):
    rows = []
    if not states:
        return rows
    for nm, s in states.items():
        df = s.get("df")
        vol_r = None
        if df is not None and "Volume" in df.columns and len(df) >= 3:
            v0, v1 = float(df["Volume"].iloc[-1]), float(df["Volume"].iloc[-2])
            if v1 > 0:
                vol_r = (v0 / v1 - 1) * 100
        rows.append({"name": nm, "px": s.get("px"), "chg": s.get("chg"), "vol_chg": vol_r, "label": s.get("label"), "kind": s.get("kind")})
    return rows

def ibd_front_seed_20260902():
    return {
        "date": "2026-09-02", "source": "IBD 첫화면 수동",
        "nasdaq": 26099.77, "nasdaq_chg": -1.03, "nasdaq_pts": -271.11,
        "dji": 52766.88, "dji_chg": -0.79, "dji_pts": -419.02,
        "spx": 7631.47, "spx_chg": -0.71, "spx_pts": -54.67,
        "nasdaq_vol": 6751.0, "nasdaq_vol_chg": -12.08,
        "nyse_vol": 4858.0, "nyse_vol_chg": -9.91,
        "qqq_ah": 707.64, "qqq_ah_chg": -1.27,
        "spy_ah": 761.78, "spy_ah_chg": -0.69,
        "dia_ah": 527.75, "dia_ah_chg": -0.72,
        "headline": "Dell, MongoDB Are Big Movers Late After Oil Prices Pressure Stocks",
        "note": "장후 QQQ −1.27% · 나스닥 거래량 −12% · 유가 압력.",
    }

def tickers_from_csv(s):
    if not s:
        return []
    return [x.strip().upper() for x in str(s).replace("，", ",").split(",") if x.strip()]

def fund_hits_for(tk, desk):
    tk = str(tk or "").upper()
    hits = []
    for f in desk.get("funds") or []:
        top = [x.upper() for x in (f.get("top10") or [])]
        new = [x.upper() for x in (f.get("new") or [])]
        cut = [x.upper() for x in (f.get("cut") or [])]
        if tk in new:
            hits.append((f.get("name"), "신규취득", "pass", f.get("grade36")))
        elif tk in cut:
            hits.append((f.get("name"), "축소", "fail", f.get("grade36")))
        elif tk in top:
            hits.append((f.get("name"), "상위10 보유", "pass", f.get("grade36")))
    return hits

def block_hits_for(tk, desk):
    tk = str(tk or "").upper()
    return [b for b in (desk.get("block") or []) if str(b.get("ticker", "")).upper() == tk]

def sponsorship_score(fnd, volc, hits, blocks, notes):
    auto, why = 0, []
    inst = (fnd or {}).get("inst") if fnd else None
    if inst is None:
        why.append("기관보유율 미수집")
    elif 15 <= inst <= 90:
        auto += 16; why.append(f"기관보유 {inst:.0f}% 적정")
    elif inst > 90:
        auto += 6; why.append(f"기관보유 {inst:.0f}% 과밀")
    else:
        why.append(f"기관보유 {inst:.0f}% 미발견")
    if volc and volc.get("flag"):
        lab, k, _ = volc["flag"]
        auto += 16 if k == "pass" else (6 if k != "fail" else 0)
        why.append(lab)
    if volc and volc.get("ad20") and volc["ad20"] >= 1.0:
        auto += 8; why.append(f"20일 상승/하락 거래 {volc['ad20']:.2f}")
    man = 0
    if hits:
        if any(h[1] == "신규취득" for h in hits):
            man += 24; why.append("36개월 상위펀드 신규취득")
        elif any(h[1] == "상위10 보유" for h in hits):
            man += 16; why.append("36개월 상위펀드 상위10")
        if any(h[1] == "축소" for h in hits):
            man -= 12; why.append("36개월 상위펀드 축소")
    if blocks:
        side = str(blocks[-1].get("side") or "")
        if "매수" in side:
            man += 16; why.append("개장 블록 매수")
        elif "매도" in side:
            man -= 10; why.append("개장 블록 매도")
    if notes:
        man += min(20, 6 * min(3, len(notes)))
        why.append(f"IBD 종목분석 일지 {len(notes)}건")
    man = max(0, min(60, man)); auto = max(0, min(40, auto))
    total = auto + man
    if total >= 80 and man >= 16:
        grade, kind = "기관보증 근사 통과", "pass"
    elif total >= 55:
        grade, kind = "관찰 — 수동 확인 필요", "warn"
    else:
        grade, kind = "기관보증 미확인", "idle"
    return {"auto": auto, "man": man, "score": total, "grade": grade, "kind": kind, "why": why, "inst": inst}
