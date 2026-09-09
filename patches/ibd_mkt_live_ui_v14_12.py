# LIVE market UI continuation v14.12
MKT_LIVE_UI_V14_12 = True

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

    rows = []
    rows.append(["점수 0-100", cnn_s, app_s, str(ibd["score"])])
    rows.append(["라벨", cnn_kr, str(app_label), ibd["label"]])
    rows.append(["기준 시각", cnn_ts or "—", "앱 새로고침", str(ibd.get("date") or "—")])
    rows.append(["원전", "CNN dataviz", "yfinance + 유니버스", "Market Pulse + 지수 FTD/DD"])
    if cnn.get("indicators"):
        for name, sc, rat in cnn["indicators"]:
            rows.append([f"CNN {name}", f"{sc:.0f} {rat}", "—", "—"])
    if app_fg and app_fg.get("comps"):
        for name, sc, ev, note in app_fg["comps"]:
            rows.append([f"앱 {name}", "—", f"{'' if sc is None else int(sc)} · {ev}", note])
    rows.append(["IBD 노출", "—", "—", str(ibd.get("exposure") or "—")])
    rows.append(["IBD 분산 NAS/SPX", "—", "—",
                 f"{ibd.get('dist_nasdaq')} / {ibd.get('dist_spx')}"])
    rows.append(["IBD 시장 FTD", "—", "—", str(ibd.get("ftd") or "—")])
    if ibd.get("headline"):
        rows.append(["Pulse 헤드라인", "—", "—", ibd["headline"]])
    try:
        st.markdown(table(["칸", "CNN 공식", "앱 계산", "IBD"], rows), unsafe_allow_html=True)
    except Exception:
        st.dataframe([{"칸": a, "CNN": b, "앱": c, "IBD": d} for a, b, c, d in rows],
                     hide_index=True, use_container_width=True)

    try:
        cs, aps, ibs = float(cnn.get("score") or 0), float(app_score or 0), float(ibd["score"])
        gap_ca = aps - cs
        gap_ci = ibs - cs
        bits = []
        if abs(gap_ca) <= 8:
            bits.append(f"앱과 CNN은 {gap_ca:+.0f}pt로 가깝다.")
        else:
            bits.append(f"앱과 CNN은 {gap_ca:+.0f}pt 벌어졌다. 풋콜·신고가 칸이 비어 있어서다.")
        if cs <= 44 and ibs >= 55:
            bits.append("CNN은 공포인데 IBD는 아직 상승세 쪽이다. 오닐은 CNN을 보지 않고 FTD·분산·리더를 본다.")
        elif cs >= 60 and (pulse.get("dist_nasdaq") or 0) >= 3:
            bits.append("CNN은 탐욕 쪽인데 Pulse 분산이 3~4일이다. 군중 낙관 + 기관 매도 흔적 = 추격 금지.")
        elif (pulse.get("dist_nasdaq") or 0) >= 5:
            bits.append("Pulse 분산 5+ 이면 지수가 어느 감정이든 추가는 없다.")
        else:
            bits.append("세 숫자가 같아도 매수 허가가 아니다. 허가 창은 적합도와 FTD훈련 탭에서 손으로 센다.")
        st.markdown(
            f'<div class="ev"><b>어긋남 읽기</b><br><span class="m">{" ".join(bits)} '
            f"앱-CNN {gap_ca:+.0f} · IBD-CNN {gap_ci:+.0f}.</span></div>",
            unsafe_allow_html=True)
    except Exception:
        pass

    try:
        read_box(
            "CNN 공식은 <b>군중 감정</b>이다. 앱 자체 산출은 같은 뼈대를 yfinance로 근사한 숙제다. "
            "IBD Pulse는 <b>노출·분산일·FTD</b>이지 공포탐욕이 아니다. "
            "세 칸을 섞어 한 점수로 사지 않는다. 분산 3~4일이면 신규 추격은 없다.",
            "CNN Fear & Greed · 앱 fear_greed() · MARKET PULSE", "oneil")
    except Exception:
        st.caption("CNN=감정 / 앱=근사 / IBD=노출·분산·FTD. 섞어 사지 않는다.")

    # v14.13 psycho panel (files already on main/patches)
    try:
        if not callable(globals().get("render_market_psycho")):
            import urllib.request
            _base = "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/main/patches/"
            _blob = ""
            for _n in ("ibd_mkt_psycho_v14_13.py", "ibd_mkt_psycho_fn_v14_13.py", "ibd_mkt_psycho_fn2_v14_13.py", "ibd_mkt_psycho_ui_v14_13.py"):
                _blob += urllib.request.urlopen(_base + _n, timeout=30).read().decode("utf-8") + "\n"
            exec(_blob, globals(), globals())
        render_market_psycho(ctx)
    except Exception:
        pass
