# v14.45 — Always show RS + PEG fallbacks; more reasonable RS for short histories
# Fixes missing RS/PEG for names like ALAB.

import math
import pandas as pd

def better_rs_proxy(df):
    """Reasonable RS proxy that works with shorter histories.
    Prefers 1y, falls back to 6m/3m. Maps returns more conservatively.
    """
    if df is None or "Close" not in getattr(df, "columns", []):
        return None, "데이터 없음"
    close = df["Close"].dropna()
    n = len(close)
    if n < 40:
        return None, f"이력 {n}일 (너무 짧음)"

    def _ret(sessions):
        if n <= sessions:
            return None
        try:
            prev = float(close.iloc[-1 - sessions])
            curr = float(close.iloc[-1])
            if prev <= 0 or math.isnan(prev) or math.isnan(curr):
                return None
            return (curr / prev - 1) * 100
        except Exception:
            return None

    r1y = _ret(252)
    r6m = _ret(126)
    r3m = _ret(63)

    used = None
    ret = None
    if r1y is not None:
        used, ret = "1년", r1y
    elif r6m is not None:
        used, ret = "6개월", r6m
    elif r3m is not None:
        used, ret = "3개월", r3m
    else:
        return None, "수익 계산 불가"

    # Conservative mapping: 0%→45, +50%→70, +100%→85, +200%→97, -30%→25
    score = 45 + ret * 0.35
    score = max(1, min(99, int(round(score))))
    note = f"{used} {ret:+.0f}% → {score}"
    return score, note


def peg_fallback(ctx):
    """Try to surface a PEG number or a clear '없음' reason."""
    # Prefer existing context values if present
    for key in ("peg", "pegRatio", "trailingPegRatio", "forwardPeg"):
        v = ctx.get(key) if isinstance(ctx, dict) else None
        if v not in (None, "", "—", "N/A"):
            try:
                return float(v), "컨텍스트"
            except Exception:
                pass

    # Try yfinance info if ticker available
    tk = (ctx.get("ticker") or "").upper() if isinstance(ctx, dict) else ""
    if not tk or "yf" not in globals():
        return None, "yfinance 없음"
    try:
        info = yf.Ticker(tk).info or {}
        for k in ("pegRatio", "trailingPegRatio"):
            v = info.get(k)
            if v is not None:
                try:
                    return float(v), f"yfinance.{k}"
                except Exception:
                    continue
        # Approximate from PE and growth if both exist
        pe = info.get("trailingPE") or info.get("forwardPE")
        growth = info.get("earningsGrowth") or info.get("revenueGrowth")
        if pe and growth and growth > 0:
            approx = float(pe) / (float(growth) * 100)
            return approx, "PE/성장 근사"
    except Exception:
        pass
    return None, "yfinance 미제공"


# Chain sticky_bar
_orig_sticky_bar_45 = sticky_bar if "sticky_bar" in globals() else None

def sticky_bar(ctx, D, extra=""):
    if _orig_sticky_bar_45:
        try:
            _orig_sticky_bar_45(ctx, D, extra)
        except Exception as e:
            st.warning(f"이전 sticky_bar 오류: {type(e).__name__}")
    if not isinstance(ctx, dict) or not ctx.get("ok"):
        return

    df = ctx.get("df")
    rs, rs_note = better_rs_proxy(df)
    if rs is not None:
        st.markdown(f"**앱 RS 대리** : **{rs}**  ·  {rs_note}")
        st.caption("1년 우선, 없으면 6개월/3개월. 수익률을 보수적으로 1–99에 매핑. IBD RS와 다름.")
    else:
        st.caption(f"앱 RS : {rs_note}")

    peg, peg_src = peg_fallback(ctx)
    if peg is not None:
        st.caption(f"PEG : {peg:.2f}  ({peg_src})")
    else:
        st.caption(f"PEG : —  ({peg_src})")

print("v14.45 RS+PEG always-on loaded")
