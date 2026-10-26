# v14.28: earnings date warning + volume confirmation breakout flag

_orig_sticky_bar3 = sticky_bar

def sticky_bar(ctx, D, extra=""):
    """Add earnings warning and volume confirmation flag."""
    if not ctx.get("ok"):
        return
    _orig_sticky_bar3(ctx, D, extra)

    binfo = ctx.get("binfo")
    price = ctx.get("price")
    if not binfo or price is None:
        return

    # Earnings date warning
    try:
        due_str = None
        if ctx.get("earnings_due"):
            due_str = ctx.get("earnings_due")
        # fallback from checkup if present
        if not due_str and isinstance(binfo, dict):
            chk = binfo.get("ibd_chk") or {}
            due_str = chk.get("due") or chk.get("eps_due")
        if due_str:
            from datetime import datetime
            try:
                due_dt = datetime.strptime(str(due_str)[:10], "%Y-%m-%d")
                days = (due_dt - datetime.now()).days
                if 0 <= days <= 3:
                    st.error(f"실적일 임박: {due_str} ({days}일 전) — 신규매수 금지")
                elif 0 <= days <= 14:
                    st.warning(f"실적일 주의: {due_str} ({days}일 전) — 신규매수 자제")
            except Exception:
                pass
    except Exception:
        pass

    # Volume confirmation breakout flag
    try:
        pivot = float(binfo.get("pivot") or 0)
        price = float(price)
        if pivot and price >= pivot:
            vol_ok = False
            if ctx.get("volume_ratio") and float(ctx.get("volume_ratio") or 0) >= 1.4:
                vol_ok = True
            elif binfo.get("vol_confirm"):
                vol_ok = True
            if vol_ok:
                st.success("거래량 확인 돌파 (≥1.4× 50일 평균)")
            else:
                st.info("피봇 돌파 중 — 거래량 확인 필요 (≥1.4× 50일)")
    except Exception:
        pass

print("v14.28 earnings warning + volume flag loaded")
