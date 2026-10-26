# v14.28: earnings date warning + volume confirmation breakout flag
# Fixed: pull due from full checkup record; compute volume ratio from df

_orig_sticky_bar3 = sticky_bar

def sticky_bar(ctx, D, extra=""):
    """Add earnings warning and volume confirmation flag with real data."""
    if not ctx.get("ok"):
        return
    _orig_sticky_bar3(ctx, D, extra)

    binfo = ctx.get("binfo")
    price = ctx.get("price")
    df = ctx.get("df")
    if not binfo or price is None:
        return

    # --- Earnings date warning ---
    try:
        due_str = None
        tk = (ctx.get("ticker") or ctx.get("name", "").split()[0] or "").upper()
        if tk and "checkup_for" in globals() and "load_ibd_desk" in globals():
            try:
                desk = load_ibd_desk()
                chk = checkup_for(tk, desk)
                if chk:
                    due_str = chk.get("due") or chk.get("eps_due")
            except Exception:
                pass
        # fallbacks
        if not due_str and ctx.get("earnings_due"):
            due_str = ctx.get("earnings_due")
        if not due_str and isinstance(binfo, dict):
            chk = binfo.get("ibd_chk") or {}
            due_str = chk.get("due") or chk.get("eps_due")
        if due_str:
            from datetime import datetime
            try:
                due_dt = datetime.strptime(str(due_str)[:10], "%Y-%m-%d")
                days = (due_dt.date() - datetime.now().date()).days
                if days < 0:
                    pass  # already reported
                elif days <= 3:
                    st.error(f"실적일 임박: {due_str} ({days}일 전) — 신규매수 금지")
                elif days <= 14:
                    st.warning(f"실적일 주의: {due_str} ({days}일 전) — 신규매수 자제")
            except Exception:
                pass
    except Exception:
        pass

    # --- Volume confirmation breakout flag ---
    try:
        pivot = float(binfo.get("pivot") or 0)
        price = float(price)
        if pivot and price >= pivot and df is not None and len(df) >= 50:
            # Compute volume ratio: latest vs 50-day average
            vol_col = None
            for c in ("Volume", "volume", "vol"):
                if c in df.columns:
                    vol_col = c
                    break
            if vol_col:
                vols = df[vol_col].dropna()
                if len(vols) >= 50:
                    avg50 = float(vols.iloc[-50:].mean())
                    latest = float(vols.iloc[-1])
                    if avg50 > 0:
                        ratio = latest / avg50
                        if ratio >= 1.4:
                            st.success(f"거래량 확인 돌파 ({ratio:.2f}× 50일 평균)")
                        else:
                            st.info(f"피봇 돌파 중 — 거래량 {ratio:.2f}× (1.4× 이상 필요)")
            else:
                st.info("피봇 돌파 중 — 거래량 데이터 확인 필요")
    except Exception:
        pass

print("v14.28 earnings warning + volume flag (data-fixed) loaded")
