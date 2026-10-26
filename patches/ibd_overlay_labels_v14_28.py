# v14.28: force apply_ibd_overlay call + score source labels in sticky_bar

_orig_sticky_bar = sticky_bar

def sticky_bar(ctx, D, extra=""):
    """Wrap sticky_bar to add source labels and ensure overlay is applied."""
    if not ctx.get("ok"):
        return
    # Ensure overlay is applied if binfo exists
    binfo = ctx.get("binfo")
    if binfo and "apply_ibd_overlay" in globals():
        try:
            tk = ctx.get("ticker") or ctx.get("name", "").split()[0]
            desk = None
            try:
                desk = load_ibd_desk()
            except Exception:
                pass
            ctx["binfo"] = apply_ibd_overlay(binfo, tk, desk)
        except Exception:
            pass
    # Call original
    _orig_sticky_bar(ctx, D, extra)
    # Append source label caption
    df = ctx.get("df")
    date_str = df.index[-1].strftime("%Y-%m-%d") if df is not None and len(df) else "—"
    chk_date = "—"
    try:
        if ctx.get("binfo") and ctx["binfo"].get("ibd_chk"):
            chk_date = "Checkup 기준"
    except Exception:
        pass
    st.caption(f"앱 점수 = Yahoo 자체 산식 · 종가일 {date_str} · IBD 등급 = Checkup ({chk_date}). 14일 초과 시 오래된 자료로 간주.")

print("v14.28 overlay + score labels loaded")
