# v14.46 — RARS (Recent Acceleration RS) 3-version + detailed explanation
# 1. RARS basic
# 2. RARS + volatility penalty
# 3. Excess vs SPY
# Weights finalized after sensitivity: 22% 1m / 48% 3m / 22% 6m / 8% 12m + accel bonus, penalty 0.45

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
    """Return dict with three RS versions + notes."""
    if df is None or "Close" not in getattr(df, "columns", []):
        return None
    close = df["Close"].dropna()
    if len(close) < 60:
        return None

    r1 = _ret(close, 21) or 0.0
    r3 = _ret(close, 63) or 0.0
    r6 = _ret(close, 126) or 0.0
    r12 = _ret(close, 252) or 0.0

    # Acceleration: recent 3m stronger than the 6-12m window
    mid = (r6 - r12) if r12 else 0.0
    accel = max(r3 - mid, 0.0)

    # Finalized weights
    rars = (0.22 * r1 + 0.48 * r3 + 0.22 * r6 + 0.08 * r12 + 0.10 * accel)

    # Volatility penalty (strength 0.45)
    mdd = _mdd(close, 126)
    rars_vol = rars * (1.0 + min(mdd, 0.0) * 0.45)

    # Excess vs SPY
    excess = None
    if spy_df is not None and "Close" in spy_df.columns:
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

    # Map raw score to 1-99 (conservative)
    def _map(raw):
        if raw is None:
            return None
        score = 50 + raw * 100 * 0.65
        return max(1, min(99, int(round(score))))

    return {
        "rars": rars,
        "rars_vol": rars_vol,
        "excess": excess,
        "rs1": _map(rars),
        "rs2": _map(rars_vol),
        "rs3": _map(excess) if excess is not None else None,
        "r1": r1, "r3": r3, "r6": r6, "r12": r12,
        "mdd": mdd,
        "accel": accel,
    }


# Chain sticky_bar
_orig_sticky_bar_46 = sticky_bar if "sticky_bar" in globals() else None

def sticky_bar(ctx, D, extra=""):
    if _orig_sticky_bar_46:
        try:
            _orig_sticky_bar_46(ctx, D, extra)
        except Exception as e:
            st.warning(f"이전 sticky_bar 오류: {type(e).__name__}")

    if not isinstance(ctx, dict) or not ctx.get("ok"):
        return

    df = ctx.get("df")
    spy_df = None
    try:
        if "yf" in globals():
            spy_df = yf.download("SPY", period="18mo", interval="1d", auto_adjust=True, progress=False)
    except Exception:
        spy_df = None

    res = compute_rars(df, spy_df)
    if not res:
        st.caption("앱 RS : 이력 부족 또는 계산 불가")
        return

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("1. RARS 기본", res["rs1"] if res["rs1"] else "—",
                  help="최근 가중 + 가속도. 전체 시장 퍼센타일 근사")
    with c2:
        st.metric("2. RARS+변동성", res["rs2"] if res["rs2"] else "—",
                  help="6개월 최대낙폭이 클수록 감점")
    with c3:
        st.metric("3. SPY 대비 초과", res["rs3"] if res["rs3"] else "—",
                  help="동일 가중치로 SPY 대비 초과 성과")

    with st.expander("RARS 상세 설명 (앱 자체 RS 방법)"):
        st.markdown("""
**RARS (Recent Acceleration Relative Strength)** — 우리만의 독창적 RS

| 버전 | 의미 | 특징 |
|------|------|------|
| **1. RARS 기본** | 최근 모멘텀 중심 상대강도 | 지금 강해지는 종목을 빠르게 포착 |
| **2. RARS + 변동성 패널티** | 기본 + 급락 감점 | 과거 좋았지만 최근 크게 빠진 종목을 더 보수적으로 |
| **3. SPY 대비 초과** | 시장 대비 초과 성과 | 절대 수익률이 아니라 시장을 이겼는가 |

**가중치 (최종 조정)**  
- 1개월 22% · 3개월 48% · 6개월 22% · 12개월 8%  
- 가속도 보너스: 최근 3개월이 이전 구간보다 강할 때 소폭 가산  
- 변동성 패널티 강도: 0.45

**계산 원점수**  
- RARS = `{rars:.1%}`  
- RARS+Vol = `{rars_vol:.1%}` (6m MDD `{mdd:.1%}`)  
- 초과(SPY) = `{excess}`  

**기간 수익률**  
1m `{r1:+.1%}` · 3m `{r3:+.1%}` · 6m `{r6:+.1%}` · 12m `{r12:+.1%}`

> 이 점수는 IBD 공식 RS와 다릅니다. 앱 자체 계산이며, 전체 시장 대비 정확한 퍼센타일이 아닌 수익률 기반 근사 매핑입니다.  
> 리더 포착과 최근 모멘텀 확인용으로 사용하세요.
        """.format(
            rars=res["rars"],
            rars_vol=res["rars_vol"],
            mdd=res["mdd"],
            excess=f"{res['excess']:+.1%}" if res["excess"] is not None else "계산 불가",
            r1=res["r1"], r3=res["r3"], r6=res["r6"], r12=res["r12"],
        ))

print("v14.46 RARS 3-version loaded")
