# v14.31 priority fixes: next earnings, RS restore, date stamp, pivot filter, DD alignment
# Closer to IBD rules without inventing data.

from datetime import datetime, timedelta
import pandas as pd

def next_earnings_date(due_str, ibd_due=None):
    """Roll past date to next quarter; prefer IBD EPS Due if available."""
    today = datetime.now().date()
    candidates = []
    for s in (due_str, ibd_due):
        if not s:
            continue
        try:
            dt = datetime.strptime(str(s)[:10], "%Y-%m-%d").date()
            candidates.append(dt)
        except Exception:
            pass
    if not candidates:
        return None, None
    # Prefer future; if past, add ~90 days
    future = [d for d in candidates if d >= today]
    if future:
        nxt = min(future)
    else:
        past = max(candidates)
        nxt = past + timedelta(days=90)
    days = (nxt - today).days
    return nxt.strftime("%Y-%m-%d"), days

def compute_rs_score(df, market="US"):
    """Simple relative strength vs index proxy. Returns 1-99 or None."""
    if df is None or len(df) < 252 or "Close" not in df.columns:
        return None
    try:
        close = df["Close"].dropna()
        if len(close) < 252:
            return None
        # 1-year performance as crude RS proxy
        ret = (close.iloc[-1] / close.iloc[-252] - 1) * 100
        # Map to 1-99 (very rough; real RS needs universe)
        score = max(1, min(99, int(50 + ret / 2)))
        return score
    except Exception:
        return None

def filter_pivot(pivot, price, df):
    """Exclude bases older than 1y; flag if pivot >15% above price."""
    if pivot is None or price is None:
        return None, "데이터 부족"
    try:
        pivot = float(pivot)
        price = float(price)
        if price <= 0:
            return pivot, "—"
        gap_pct = (pivot / price - 1) * 100
        # Check recency if df available
        recent = True
        if df is not None and len(df) > 252 and "High" in df.columns:
            year_high = float(df["High"].iloc[-252:].max())
            if pivot > year_high * 1.02:
                recent = False
        if not recent:
            return None, "베이스 없음 (1년 이상 고점)"
        if gap_pct > 15:
            return pivot, "베이스 없음 (피봇 >15% 위)"
        return pivot, None
    except Exception:
        return pivot, None

def count_distribution_days(df_index, threshold=-0.2, lookback=25):
    """IBD-style: decline >=0.2% + volume up, expire after 25 sessions."""
    if df_index is None or len(df_index) < lookback + 1:
        return 0
    try:
        df = df_index.tail(lookback + 5).copy()
        if "Close" not in df.columns or "Volume" not in df.columns:
            return 0
        chg = df["Close"].pct_change() * 100
        vol_up = df["Volume"] > df["Volume"].shift(1)
        dd = ((chg <= threshold) & vol_up).sum()
        return int(dd)
    except Exception:
        return 0

# Hook into sticky_bar for display improvements
_orig_sticky_bar_p31 = sticky_bar if "sticky_bar" in globals() else None

def sticky_bar(ctx, D, extra=""):
    if not ctx.get("ok"):
        return
    if _orig_sticky_bar_p31:
        _orig_sticky_bar_p31(ctx, D, extra)

    # Data date stamp
    df = ctx.get("df")
    if df is not None and len(df):
        try:
            last_dt = df.index[-1].strftime("%Y-%m-%d") if hasattr(df.index[-1], "strftime") else str(df.index[-1])[:10]
            st.caption(f"기준일: {last_dt} (직전 미국 종가 기준)")
        except Exception:
            pass

    # Next earnings
    try:
        tk = (ctx.get("ticker") or "").upper()
        due = None
        ibd_due = None
        if tk and "checkup_for" in globals() and "load_ibd_desk" in globals():
            desk = load_ibd_desk()
            chk = checkup_for(tk, desk)
            if chk:
                due = chk.get("due") or chk.get("eps_due")
                ibd_due = chk.get("eps_due") or due
        nxt, days = next_earnings_date(due, ibd_due)
        if nxt:
            if days is not None and days <= 3:
                st.error(f"다음 예정 실적: {nxt} ({days}일 전) — 신규매수 금지")
            elif days is not None and days <= 14:
                st.warning(f"다음 예정 실적: {nxt} ({days}일 전) — 주의")
            else:
                st.caption(f"다음 예정 실적: {nxt}")
    except Exception:
        pass

    # RS restore note
    rs = compute_rs_score(df, ctx.get("market"))
    if rs is not None:
        st.caption(f"앱 RS 근사: {rs} (1년 수익 기반 대리; IBD RS와 다름)")

    # Pivot filter note
    binfo = ctx.get("binfo")
    if binfo and binfo.get("pivot") and ctx.get("price"):
        _, note = filter_pivot(binfo["pivot"], ctx["price"], df)
        if note:
            st.info(note)

print("v14.31 priority fixes loaded")
