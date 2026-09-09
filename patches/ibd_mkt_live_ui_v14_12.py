# LIVE market UI continuation v14.12 + inline IBD 5 psycho
MKT_LIVE_UI_V14_12 = True
MKT_PSYCHO_V14_13 = True
MKT_PSYCHO_UI_V14_13 = True


def _mkt_live_now():
    try:
        return pd.Timestamp.now(tz="Asia/Seoul").strftime("%Y-%m-%d %H:%M KST")
    except Exception:
        return pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")


def render_market_live(ctx=None):
    ctx = ctx or (globals().get("CTX") or {})
    states = (ctx.get("states") if ctx else None) or {}
    bw = (ctx.get("bw") if ctx else None) or {}
    uni = ctx.get("uni") if ctx else None
    market = ctx.get("market") or "US"

    st.markdown(
        '<div class="masthead"><h1>LIVE 시장 계산</h1>'
        '<div class="sub">앱이 방금 받은 지수로 다시 센다. 아래 수동 IBD 스캔(날짜 고정)과 별개.</div></div>',
        unsafe_allow_html=True)

    b1, b2, b3 = st.columns([2, 2, 2])
    if b1.button("지금 다시 계산", key="mkt_live_refresh_v12"):
        for fn in ("fetch_cnn_fng", "fetch_cnn_fng_full", "_fng_market_data"):
            f = globals().get(fn)
            if f is not None and hasattr(f, "clear"):
                try:
                    f.clear()
                except Exception:
                    pass
        st.cache_data.clear()
        st.rerun()
    b2.caption(f"계산시각 {_mkt_live_now()}")
    b3.caption("캐시 3~30분 · 버튼이 강제 갱신")

    if states:
        cols = st.columns(max(1, len(states)))
        for (nm, s), col in zip(states.items(), cols):
            chg = s.get("chg")
            px = s.get("px")
            try:
                px_s = f"{float(px):,.2f}"
            except Exception:
                px_s = "—"
            try:
                chg_s = f"{float(chg):+.2f}%"
            except Exception:
                chg_s = "—"
            tone = "up" if (chg or 0) >= 0 else "down"
            col.markdown(
                card(nm, px_s, f'{chg_s} · {s.get("label") or "—"} · 분산 {s.get("dd_n", "—")}', tone),
                unsafe_allow_html=True)

    desk = {}
    try:
        desk = load_ibd_desk()
        if callable(globals().get("ensure_book_seed")):
            desk = ensure_book_seed(desk)
    except Exception:
        pass
    lists = (desk.get("lists") if desk else None) or {}
    pulse = (lists.get("market_pulse_latest")
             or lists.get("market_pulse_20260903")
             or {"dist_nasdaq": 4, "dist_spx": 3, "ftd": "2026-06-02",
                 "exposure": "60%-80%", "market_score": 65, "date": "2026-09-03",
                 "headline": "Software rally, lower yields fuel broad-based gains"})

    cnn = fetch_cnn_fng_full()
    app_fg = None
    try:
        fx = None
        if market == "KR" and callable(globals().get("load_fx")):
            try:
                fx = load_fx()[0]
            except Exception:
                fx = None
        app_fg = fear_greed(market, states, uni, fx)
    except Exception:
        app_fg = None
    ibd = _mkt_ibd_stance(pulse, bw=bw, states=states)

    cnn_kr, _ = _mkt_live_cnn_label(cnn.get("score"), cnn.get("rating"))
    app_score = None if not app_fg else app_fg.get("score")
    app_label = "산출 실패" if not app_fg else app_fg.get("label")
    cnn_ts = str(cnn.get("timestamp") or "")[:10]
    cnn_src = cnn.get("source") or "CNN"

    step_header("세 소스 비교", "CNN 공식 · 앱 자체 산출 · IBD Pulse",
                "세 숫자는 같은 물건이 아니다. 나란히 놓고 어긋남을 읽는다.")

    c1, c2, c3 = st.columns(3)
    try:
        cnn_s = f"{float(cnn['score']):.0f}"
    except Exception:
        cnn_s = "—"
    c1.markdown(
        card("CNN 공식 Fear & Greed", f"{cnn_s}<span style='font-size:1rem'>/100</span>",
             f"<b>{cnn_kr}</b> · {cnn_ts or '—'} · {cnn_src}<br>"
             f"전일 {cnn.get('previous_close') and round(float(cnn['previous_close']))} · "
             f"1주 {cnn.get('previous_1_week') and round(float(cnn['previous_1_week']))} · "
             f"1개월 {cnn.get('previous_1_month') and round(float(cnn['previous_1_month']))}",
             _mkt_live_kind(cnn_kr)),
        unsafe_allow_html=True)
    app_s = "—" if app_score is None else str(int(app_score))
    c2.markdown(
        card("앱 자체 산출", f"{app_s}<span style='font-size:1rem'>/100</span>",
             f"<b>{app_label}</b> · 방금 계산 · "
             f"모멘텀·VIX·폭·강도·국채·정크 근사<br>풋콜·NYSE 신고가는 CNN만 있다",
             _mkt_live_kind(app_label)),
        unsafe_allow_html=True)
    c3.markdown(
        card("IBD Pulse · 앱 국면", f"{ibd['score']}<span style='font-size:1rem'>/100</span>",
             f"<b>{ibd['label']}</b> · Pulse {ibd.get('date') or '—'}<br>"
             f"{ibd['why']}<br>적합도 {ibd.get('bw') if ibd.get('bw') is not None else '—'} · "
             f"{ibd.get('live_label') or ''}",
             "warn" if int(pulse.get("dist_nasdaq") or 0) >= 3 else "up"),
        unsafe_allow_html=True)

    try:
        read_box(
            "CNN 공식은 <b>군중 감정</b>이다. 앱 자체 산출은 같은 뼈대를 yfinance로 근사한 숙제다. "
            "IBD Pulse는 <b>노출·분산일·FTD</b>이지 공포탐욕이 아니다. "
            "세 칸을 섞어 한 점수로 사지 않는다. 분산 3~4일이면 신규 추격은 없다.",
            "CNN Fear & Greed · 앱 fear_greed() · MARKET PULSE", "oneil")
    except Exception:
        st.caption("CNN=감정 / 앱=근사 / IBD=노출·분산·FTD. 섞어 사지 않는다.")

    render_market_psycho(ctx)


def render_market_psycho(ctx=None):
    """IBD 5대 심리. 인쇄본 9/8. 공포탐욕 67점과 다른 물건."""
    ctx = ctx or {}
    latest = {
        "date": "2026-09-08",
        "vix": 14.6, "put_call": 0.71, "high_low": 0.71,
        "bulls": 54.9, "bears": 17.6, "margin_yoy": 38.6, "pc_web": 0.72,
    }
    hist = [
        {"date": "2026-09-01", "vix": 15.5, "put_call": 0.79, "high_low": None,
         "bulls": 51.9, "bears": 30.9, "margin_yoy": 38.6},
        {"date": "2026-09-03", "vix": 15.2, "put_call": 0.73, "high_low": None,
         "bulls": 45.0, "bears": None, "margin_yoy": 38.6},
        dict(latest),
    ]
    try:
        desk = load_ibd_desk()
        lists = (desk.get("lists") if desk else None) or {}
        if lists.get("psycho_latest"):
            latest = lists["psycho_latest"]
        if lists.get("psycho_history"):
            hist = lists["psycho_history"]
    except Exception:
        pass

    step_header(
        "IBD 5대 심리지표",
        "VIX · 풋콜 · High-Low · Bulls/Bears · Margin",
        "아래 67점 공포탐욕과 다른 물건. DailyPsycho_090826 인쇄본.",
    )
    specs = [
        ("VIX", latest.get("vix"), "14.6 · 45 미만=안일. 바닥 신호 아님"),
        ("풋콜", latest.get("put_call"), "0.71 · 웹 0.72. 콜 편중=낙관"),
        ("High-Low", latest.get("high_low"), "0.71 · 0.5 아래여야 조정바닥 감시"),
        ("Bulls / Bears", latest.get("bulls"),
         f"Bulls {latest.get('bulls')}% / Bears {latest.get('bears')}% · 자문 낙관"),
        ("Margin YoY", latest.get("margin_yoy"), "38.6% · 55%가 대형 천정 경고"),
    ]
    cols = st.columns(5)
    for col, (title, val, sub) in zip(cols, specs):
        shown = "—" if val is None else (f"{float(val):.2f}" if title in ("풋콜", "High-Low")
                                         else (f"{float(val):.1f}%" if title != "VIX" else f"{float(val):.1f}"))
        try:
            col.markdown(card(title, shown, sub, "warn"), unsafe_allow_html=True)
        except Exception:
            col.metric(title, shown, sub)

    with st.expander("지표 설명 · 오닐이 이 숫자를 어떻게 읽나", expanded=False):
        st.markdown(
            "- **VIX** — IBD는 45 초과를 강세(공포=바닥 후보)로 본다. 14.6은 안일.\n"
            "- **풋콜** — 1.0+ 헤지/공포. 0.50~0.70은 콜 편중=낙관.\n"
            "- **High-Low** — 0.5 아래 첫 상승일이 조정 바닥 힌트. 0.71은 트리거 아님.\n"
            "- **Bulls vs Bears** — 강세 높고 약세 극소=군중 낙관=경계.\n"
            "- **Margin Debt** — 55% 초과가 대형 천정 경고. 지금은 38.6%(2026-07).\n"
            "- 다섯을 평균 내서 사지 않는다. 분산일·FTD·리더 피벗이 먼저다."
        )

    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        xs = [str(r.get("date"))[:10] for r in hist]
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.08,
                            subplot_titles=("VIX · High-Low · Put/Call", "Bulls vs Bears %", "Margin YoY %"))
        fig.add_trace(go.Scatter(x=xs, y=[r.get("vix") for r in hist], name="VIX", mode="lines+markers"), row=1, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("high_low") for r in hist], name="High-Low", mode="lines+markers"), row=1, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("put_call") for r in hist], name="Put/Call", mode="lines+markers"), row=1, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("bulls") for r in hist], name="Bulls %", mode="lines+markers"), row=2, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("bears") for r in hist], name="Bears %", mode="lines+markers"), row=2, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("margin_yoy") for r in hist], name="Margin YoY", mode="lines+markers"), row=3, col=1)
        fig.add_hline(y=55, line_dash="dot", line_color="#c44", annotation_text="55%", row=3, col=1)
        fig.update_layout(height=560, margin=dict(t=48, b=24, l=40, r=20),
                          legend=dict(orientation="h", y=1.08),
                          title="심리지표 누적 (9/1 · 9/3 · 9/8 인쇄)")
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.caption("그래프 생략. 표로 본다.")
        st.dataframe(hist, hide_index=True, use_container_width=True)

    st.markdown(
        '<div class="ev"><b>시장 종합의견</b> · 분산 작업 5 후보 · 신규 추격 0<br>'
        '<span class="m">공식 Pulse(9/3) 노출 60-80% · 분산 NAS 4 / SPX 3. FTD 2026-06-02. '
        "화요 9/8 하락+거래량증가 = 분산일 후보. 작업카운트 NAS 5 / SPX 4. "
        "VIX 14.6 안일 · P/C 0.71 · H/L 0.71 · Bulls 54.9 / Bears 17.6 · Margin 38.6%. "
        "아래 67점 탐욕은 앱 공포탐욕이다. 5대 심리와 섞지 말 것.</span></div>",
        unsafe_allow_html=True)
