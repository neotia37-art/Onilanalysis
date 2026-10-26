# v14.28: pivot/buy zone unification table + sell rule alerts

_orig_sticky_bar2 = sticky_bar

def sticky_bar(ctx, D, extra=""):
    """Extend sticky_bar with pivot table and sell alerts."""
    if not ctx.get("ok"):
        return
    _orig_sticky_bar2(ctx, D, extra)

    binfo = ctx.get("binfo")
    if not binfo:
        return
    m = ctx.get("market", "US")
    price = ctx.get("price")
    pivot = binfo.get("pivot")
    if pivot is None or price is None:
        return

    # Pivot / buy zone table
    try:
        pivot = float(pivot)
        price = float(price)
        upper = pivot * 1.05
        gap = (price / pivot - 1) * 100 if pivot else 0
        status = "대기"
        if price > upper:
            status = "추격금지"
        elif price >= pivot:
            status = "매수가능"
        st.markdown("**피봇·매수구간 산식 통일**")
        st.markdown(
            f"| 항목 | 값 |\n|---|---|\n"
            f"| 피봇 (기준) | {fmt(pivot, m)} |\n"
            f"| 현재가 | {fmt(price, m)} |\n"
            f"| 갭 | {gap:+.1f}% |\n"
            f"| +5% 상단 | {fmt(upper, m)} |\n"
            f"| 상태 | {status} |"
        )
    except Exception:
        pass

    # Sell rule alerts (basic: distance from pivot as proxy for entry)
    try:
        dist = (price / pivot - 1) * 100
        alerts = []
        if dist <= -7:
            alerts.append(f"손절 주의: 피봇 대비 {dist:.1f}% (–7~8% 구간)")
        if dist <= -8:
            alerts.append("강제 손절 권고 구간")
        if binfo.get("fake_bo"):
            alerts.append("가짜 돌파 위험 — 피봇 하회 시 즉시 매도 검토")
        if alerts:
            st.warning(" · ".join(alerts))
    except Exception:
        pass

print("v14.28 pivot table + sell alerts loaded")
