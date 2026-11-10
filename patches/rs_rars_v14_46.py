# v14.46 — RARS (Recent Acceleration RS) 3-version + detailed explanation
# Weights: 22% 1m / 48% 3m / 22% 6m / 8% 12m + accel, penalty 0.45

import math
import pandas as pd

def _ret(close, sessions):
    if close is None or len(close) <= sessions + 1:
        return None
    try:
        prev = float(close.iloc[-1 - sessions])
        curr = float(close.iloc[-1])
        if prev <= 0 or math.isnan(prev) or math.isnan(curr):
            return None
        return (curr / prev - 1)
    except Exception:
        return None

def _mdd(close, sessions=126):
    if close is None or len(close) < 30:
        return 0.0
    s = close.dropna().iloc[-sessions:]
    if len(s) < 20:
        return 0.0
    peak = s.cummax()
    dd = (s - peak) / peak
    return float(dd.min())

def compute_rars(df, spy_df=None):
    if df is None or "Close" not in getattr(df, "columns", []):
        return None
    close = df["Close"].dropna()
    if len(close) < 60:
        return None
    r1 = _ret(close, 21) or 0.0
    r3 = _ret(close, 63) or 0.0
    r6 = _ret(close, 126) or 0.0
    r12 = _ret(close, 252) or 0.0
    mid = (r6 - r12) if r12 else 0.0
    accel = max(r3 - mid, 0.0)
    rars = (0.22 * r1 + 0.48 * r3 + 0.22 * r6 + 0.08 * r12 + 0.10 * accel)
    mdd = _mdd(close, 126)
    rars_vol = rars * (1.0 + min(mdd, 0.0) * 0.45)
    excess = None
    if spy_df is not None and "Close" in getattr(spy_df, "columns", []):
        spy_c = spy_df["Close"].dropna()
        if len(spy_c) > 126:
            s1 = _ret(spy_c, 21) or 0.0
            s3 = _ret(spy_c, 63) or 0.0
            s6 = _ret(spy_c, 126) or 0.0
            s12 = _ret(spy_c, 252) or 0.0
            smid = (s6 - s12) if s12 else 0.0
            saccel = max(s3 - smid, 0.0)
            spy_rars = 0.22*s1 + 0.48*s3 + 0.22*s6 + 0.08*s12 + 0.10*saccel
            excess = rars - spy_rars
    def _map(raw):
        if raw is None: return None
        score = 50 + raw * 100 * 0.65
        return max(1, min(99, int(round(score))))
    return {"rars": rars, "rars_vol": rars_vol, "excess": excess, "rs1": _map(rars), "rs2": _map(rars_vol), "rs3": _map(excess) if excess is not None else None, "r1": r1, "r3": r3, "r6": r6, "r12": r12, "mdd": mdd, "accel": accel}

_orig_sticky_bar_46 = sticky_bar if "sticky_bar" in globals() else None
def sticky_bar(ctx, D, extra=""):
    if _orig_sticky_bar_46:
        try: _orig_sticky_bar_46(ctx, D, extra)
        except Exception as e: st.warning(f"이전 sticky_bar 오류: {type(e).__name__}")
    if not isinstance(ctx, dict) or not ctx.get("ok"): return
    df = ctx.get("df")
    spy_df = None
    try:
        if "yf" in globals(): spy_df = yf.download("SPY", period="18mo", interval="1d", auto_adjust=True, progress=False)
    except Exception: spy_df = None
    res = compute_rars(df, spy_df)
    if not res:
        st.caption("앱 RS : 이력 부족 또는 계산 불가")
        return
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("1. RARS 기본", res["rs1"] or "—", help="최근 가중 + 가속도")
    with c2: st.metric("2. RARS+변동성", res["rs2"] or "—", help="6개월 최대낙폭 감점")
    with c3: st.metric("3. SPY 대비 초과", res["rs3"] or "—", help="SPY 대비 초과 성과")
    with st.expander("RARS 상세 설명 (앱 자체 RS 방법)"):
        st.markdown(f"""**RARS** — 우리만의 독창적 RS\n\n- **1. RARS 기본**: 최근 모멘텀 중심 (1m22% / 3m48% / 6m22% / 12m8% + 가속도)\n- **2. RARS+변동성**: 기본 + 6개월 최대낙폭 패널티 (강도 0.45)\n- **3. SPY 대비 초과**: 동일 가중치로 시장 대비 상대강도\n\n**원점수**: RARS {res['rars']:.1%} | Vol조정 {res['rars_vol']:.1%} | 초과 {res['excess']:+.1%} if res['excess'] is not None else 'N/A'\n**기간**: 1m {res['r1']:+.1%} | 3m {res['r3']:+.1%} | 6m {res['r6']:+.1%} | 12m {res['r12']:+.1%} | 6m MDD {res['mdd']:.1%}\n\nIBD 공식 RS와 다릅니다. 앱 자체 계산 근사입니다.""")
print("v14.46 RARS 3-version loaded")
