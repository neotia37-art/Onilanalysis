# v14.29: refined pivot/buy zone unification table + sell rule alerts
# Shows app pivot (from analyze_base) vs note for IBD pivot; clear +5% zone.
# Sell: -7/-8% from pivot, fake BO, MA break hint.

_orig_sticky_bar_ps = sticky_bar

def sticky_bar(ctx, D, extra=""):
    if not ctx.get("ok"):
        return
    _orig_sticky_bar_ps(ctx, D, extra)

    binfo = ctx.get("binfo")
    if not binfo:
        return
    m = ctx.get("market", "US")
    price = ctx.get("price")
    pivot = binfo.get("pivot")
    if pivot is None or price is None:
        return

    try:
        pivot = float(pivot)
        price = float(price)
        upper = round(pivot * 1.05, 2)
        gap = (price / pivot - 1) * 100 if pivot else 0
        if price > upper:
            status = "추격금지"
            tone = "fail"
        elif price >= pivot:
            status = "매수가능"
            tone = "pass"
        else:
            status = "대기"
            tone = "idle"

        st.markdown("**피봇·매수구간 산식 통일**")
        st.caption("앱 피봇 = analyze_base (핸들 고점 또는 베이스 좌측 고점 +$0.10). IBD 피봇은 Checkup/북 기준.")
        rows = [
            ["피봇 (앱)", fmt(pivot, m)],
            ["현재가", fmt(price, m)],
            ["갭", f"{gap:+.1f}%"],
            ["+5% 상단", fmt(upper, m)],
            ["상태", status],
        ]
        st.markdown(table(["항목", "값"], rows), unsafe_allow_html=True)
    except Exception:
        pass

    # Sell alerts
    try:
        dist = (price / pivot - 1) * 100
        alerts = []
        if dist <= -8:
            alerts.append(f"강제 손절 권고: 피봇 대비 {dist:.1f}% (–8% 이하)")
        elif dist <= -7:
            alerts.append(f"손절 주의: 피봇 대비 {dist:.1f}% (–7~8% 구간)")
        if binfo.get("fake_bo"):
            alerts.append("가짜 돌파 위험 — 피봇 하회 시 매도 검토")
        # Simple MA break hint from df if available
        df = ctx.get("df")
        if df is not None and len(df) >= 50 and "Close" in df.columns:
            try:
                ma50 = float(df["Close"].iloc[-50:].mean())
                if price < ma50:
                    alerts.append(f"50일선 종가 이탈 ({fmt(ma50, m)})")
            except Exception:
                pass
        if alerts:
            st.warning(" · ".join(alerts))
    except Exception:
        pass

print("v14.29 pivot table + sell alerts refined")
