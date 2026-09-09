# LIVE psycho UI v14.13
MKT_PSYCHO_UI_V14_13 = True


def render_market_psycho(ctx=None):
    ctx = ctx or (globals().get("CTX") or {})
    states = (ctx.get("states") if ctx else None) or {}
    bw = (ctx.get("bw") if ctx else None) or {}
    desk = {}
    try:
        desk = load_ibd_desk()
        if callable(globals().get("ensure_book_seed")):
            desk = ensure_book_seed(desk)
    except Exception:
        desk = {}
    hist = ensure_psycho_history(desk)
    lists = (desk.get("lists") if desk else None) or {}
    latest = (lists.get("psycho_latest") or (hist[-1] if hist else {}) or {})
    pulse = lists.get("market_pulse_latest") or {}
    step_header("IBD 5대 심리지표", "VIX · 풋콜 · 신고/신저 · 불베어 · 신용잔고",
                "인쇄본을 옮겨 쌓는다. 라이브 VIX만 앱이 받고, 나머지 넷은 IBD 화면이다.")
    live_vix, live_chg = _psycho_live_vix(states)
    c = st.columns(5)
    specs = [
        ("VIX", latest.get("vix"), "vix", f"인쇄 {latest.get('date') or '—'}" + (f" · 라이브 {live_vix:.1f}" if live_vix is not None else "")),
        ("풋콜", latest.get("put_call"), "put_call", f"웹 {latest.get('pc_web')}" if latest.get("pc_web") else "DailyPsycho"),
        ("High-Low", latest.get("high_low"), "high_low", "0.5 아래=조정 바닥 감시"),
        ("Bulls / Bears", latest.get("bulls"), "bulls", f"Bears {latest.get('bears') if latest.get('bears') is not None else '—'}%"),
        ("Margin YoY", latest.get("margin_yoy"), "margin", "월간 · 55% 경고"),
    ]
    for col, (title, val, key, sub) in zip(c, specs):
        lab, tone = _psycho_read_one("margin" if key == "margin" else key, val)
        try:
            if val is None:
                shown = "—"
            elif key in ("put_call", "high_low"):
                shown = f"{float(val):.2f}"
            else:
                shown = f"{float(val):.1f}" + ("%" if key in ("bulls", "margin") else "")
        except Exception:
            shown = "—"
        try:
            col.markdown(card(title, shown, f"{lab}<br>{sub}", tone), unsafe_allow_html=True)
        except Exception:
            col.metric(title, shown, lab)
    with st.expander("지표 설명 · 오닐이 이 숫자를 어떻게 읽나", expanded=False):
        st.markdown(
            f"- **VIX** — {PSYCHO_EXPLAIN['vix']}\n"
            f"- **풋콜** — {PSYCHO_EXPLAIN['put_call']}\n"
            f"- **High-Low** — {PSYCHO_EXPLAIN['high_low']}\n"
            f"- **Bulls vs Bears** — {PSYCHO_EXPLAIN['bulls_bears']}\n"
            f"- **Margin Debt** — {PSYCHO_EXPLAIN['margin']}\n"
            "- 다섯을 평균 내서 사지 않는다. 분산일·FTD·리더 피벗이 먼저다."
        )
    if hist:
        try:
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            xs = [_psycho_norm_date(r.get("date")) for r in hist]
            fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.08,
                                subplot_titles=("VIX · High-Low · Put/Call", "Bulls vs Bears %", "Margin Debt YoY %"))
            fig.add_trace(go.Scatter(x=xs, y=[r.get("vix") for r in hist], name="VIX", mode="lines+markers"), row=1, col=1)
            fig.add_trace(go.Scatter(x=xs, y=[r.get("high_low") for r in hist], name="High-Low", mode="lines+markers"), row=1, col=1)
            fig.add_trace(go.Scatter(x=xs, y=[r.get("put_call") for r in hist], name="Put/Call", mode="lines+markers"), row=1, col=1)
            fig.add_hline(y=45, line_dash="dot", annotation_text="VIX 45", row=1, col=1)
            fig.add_hline(y=0.5, line_dash="dot", annotation_text="H/L 0.5", row=1, col=1)
            fig.add_trace(go.Scatter(x=xs, y=[r.get("bulls") for r in hist], name="Bulls %", mode="lines+markers"), row=2, col=1)
            fig.add_trace(go.Scatter(x=xs, y=[r.get("bears") for r in hist], name="Bears %", mode="lines+markers"), row=2, col=1)
            fig.add_trace(go.Scatter(x=xs, y=[r.get("margin_yoy") for r in hist], name="Margin YoY", mode="lines+markers"), row=3, col=1)
            fig.add_hline(y=55, line_dash="dot", annotation_text="55% 경고", row=3, col=1)
            fig.update_layout(height=620, margin=dict(t=48, b=24, l=40, r=20), legend=dict(orientation="h", y=1.08), title="심리지표 누적 (인쇄일을 쌓는다)")
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.caption(f"그래프 생략: {e}")
    with st.expander("오늘 인쇄본 추가 (누적)", expanded=False):
        st.caption("IBD Psychological Market Indicators 숫자를 옮긴다. 같은 날짜는 덮어쓴다.")
        f1, f2, f3 = st.columns(3)
        dt = f1.text_input("날짜", value=str(latest.get("date") or "2026-09-08"), key="psy_dt")
        vix_i = f2.number_input("VIX", value=float(latest.get("vix") or 14.6), step=0.1, key="psy_vix")
        pc_i = f3.number_input("Put/Call", value=float(latest.get("put_call") or 0.71), step=0.01, key="psy_pc")
        f4, f5, f6 = st.columns(3)
        hl_i = f4.number_input("High-Low", value=float(latest.get("high_low") or 0.71), step=0.01, key="psy_hl")
        bu_i = f5.number_input("Bulls %", value=float(latest.get("bulls") or 54.9), step=0.1, key="psy_bu")
        be_i = f6.number_input("Bears %", value=float(latest.get("bears") or 17.6), step=0.1, key="psy_be")
        f7, f8 = st.columns(2)
        mg_i = f7.number_input("Margin YoY %", value=float(latest.get("margin_yoy") or 38.6), step=0.1, key="psy_mg")
        src_i = f8.text_input("원전", value="DailyPsycho 수동", key="psy_src")
        if st.button("이 날짜를 심리 히스토리에 저장", key="psy_save"):
            upsert_psycho_row(desk, {"date": dt, "vix": vix_i, "put_call": pc_i, "high_low": hl_i, "bulls": bu_i, "bears": be_i, "margin_yoy": mg_i, "source": src_i, "note": "수동 입력"})
            st.rerun()
    html, stance = market_comment_today(pulse=pulse, latest=latest, states=states, bw=bw)
    try:
        st.markdown(f'<div class="ev"><b>시장 종합의견</b> · {stance}<br><span class="m">{html}</span></div>', unsafe_allow_html=True)
    except Exception:
        st.info(stance)
        st.markdown(html, unsafe_allow_html=True)
    try:
        read_box("5대 심리는 <b>군중 온도계</b>다. FTD는 새로운 상승 허가, 분산일은 그 허가를 깎는 칼이다. 화요(9/8)는 하락+거래량증가라 분산 후보다. 공식 Pulse 분산 3~4일에 후보 1을 더하면 작업 5. 작업 5면 신규는 없다.", "DailyPsycho_090826 · Pulse 9/3", "oneil")
    except Exception:
        st.caption("심리 ≠ 매수. 분산 후보 + 안일 = 추격 금지.")
