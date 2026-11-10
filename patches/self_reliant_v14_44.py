# v14.44 — Self-reliant numerical guards + reduced IBD dependency
# Adds defensive helpers, safer RS/score paths, and clearer "app-only" labels.
# Hooks sticky_bar after v14.43.

import math
import pandas as pd

def safe_div(a, b, default=None):
    try:
        if b is None or b == 0 or (isinstance(b, float) and math.isnan(b)):
            return default
        return a / b
    except Exception:
        return default

def safe_ret(close_series, n):
    """Safe n-session return. Returns None on insufficient data or zero base."""
    if close_series is None or len(close_series) <= n:
        return None
    try:
        prev = float(close_series.iloc[-1 - n])
        curr = float(close_series.iloc[-1])
        if prev <= 0 or math.isnan(prev) or math.isnan(curr):
            return None
        return (curr / prev - 1) * 100
    except Exception:
        return None

def robust_rs_proxy(df):
    """More defensive 1y RS proxy. Caps extremes."""
    if df is None or "Close" not in df.columns:
        return None
    close = df["Close"].dropna()
    r = safe_ret(close, 252)
    if r is None:
        r = safe_ret(close, 126)
        if r is None:
            return None
    # Map roughly  -50%→20, 0%→50, +100%→90, +200%→99
    score = 50 + r * 0.4
    return max(1, min(99, int(round(score))))

# Chain after previous sticky_bar
_orig_sticky_bar_s44 = sticky_bar if "sticky_bar" in globals() else None

def sticky_bar(ctx, D, extra=""):
    if _orig_sticky_bar_s44:
        try:
            _orig_sticky_bar_s44(ctx, D, extra)
        except Exception as e:
            st.warning(f"이전 sticky_bar 오류 (무시): {type(e).__name__}")
    if not isinstance(ctx, dict) or not ctx.get("ok"):
        return
    df = ctx.get("df")
    # Robust RS
    rs = robust_rs_proxy(df)
    if rs is not None:
        st.caption(f"앱 RS 대리 (방어적): {rs}  ·  1년/6개월 수익 기반, 극단값 캡")
    # Self-contained note
    st.caption("수치·점수·RS·A/D는 모두 앱 자체 계산 (yfinance 시세 기반). IBD Checkup/Pulse는 참고용이며 없어도 동작합니다.")
    # Basic sanity
    try:
        px = ctx.get("price")
        if px is not None and float(px) <= 0:
            st.error("가격 값이 0 이하입니다. 시세 데이터를 확인하세요.")
    except Exception:
        pass

print("v14.44 self-reliant guards loaded")
