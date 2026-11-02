RELVAL_TAB_V14_30 = True

# 2026-11-02 Yahoo 실측. 탭이 비어 있지 않도록 먼저 보이고, 버튼으로 실시간 갱신.
_REL_ASOF = "2026-11-02"
_REL_PX = {
    "LITE": (840.7, 23.5, 0.63, 1.093, 0.442),
    "COHR": (210.3, 15.1, 0.92, 0.337, None),
    "NVDA": (204.6, 12.9, 0.25, 1.278, 0.662),
    "AMD": (504.8, 31.7, None, None, None),
    "AVGO": (326.1, 16.8, None, None, None),
    "MRVL": (196.4, 26.8, None, None, None),
    "PLTR": (184.1, 78.3, 1.67, 2.154, 0.848),
    "NOW": (105.1, 21.9, None, None, None),
    "SNOW": (306.1, 101.1, None, None, None),
    "GOOGL": (279.8, 18.4, 0.98, -0.253, 0.609),
    "META": (615.0, 17.3, 0.80, None, None),
    "MSFT": (521.9, 21.6, 1.69, 0.323, 0.677),
    "AMZN": (240.3, 22.1, 1.39, -0.031, 0.514),
    "TSLA": (399.8, 185.2, 4.66, -0.436, 0.193),
    "MU": (884.7, 4.3, 0.16, 10.595, 0.807),
    "SNDK": (1150.9, 4.0, None, None, None),
    "TSM": (406.1, 17.4, 0.73, 0.687, 0.658),
    "DELL": (424.3, 14.0, 0.43, 2.729, 0.199),
    "VRT": (232.5, 23.9, None, None, None),
}
_REL_PAIRS = [
    ("LITE", "COHR"), ("NVDA", "AMD"), ("NVDA", "AVGO"), ("NVDA", "MRVL"),
    ("PLTR", "NOW"), ("PLTR", "SNOW"), ("GOOGL", "META"), ("MSFT", "GOOGL"),
    ("AMZN", "GOOGL"), ("TSLA", "NVDA"), ("MU", "SNDK"), ("TSM", "NVDA"),
    ("DELL", "VRT"),
]


def _rel_num(v):
    try:
        if v is None or v == "":
            return None
        x = float(v)
        if x != x:
            return None
        return x
    except Exception:
        return None


def _rel_fetch_live():
    import yfinance as yf
    book = {}
    for t in _REL_PX:
        info = {}
        try:
            info = yf.Ticker(t).info or {}
        except Exception:
            info = {}
        px = _rel_num(info.get("currentPrice") or info.get("regularMarketPrice"))
        pe = _rel_num(info.get("forwardPE"))
        peg = _rel_num(info.get("pegRatio"))
        g = _rel_num(info.get("earningsGrowth"))
        if g is None:
            g = _rel_num(info.get("revenueGrowth"))
        m = _rel_num(info.get("operatingMargins"))
        if m is None:
            m = _rel_num(info.get("grossMargins"))
        if px is None and pe is None:
            continue
        book[t] = (px, pe, peg, g, m)
    if len(book) < 4:
        raise RuntimeError("Yahoo에서 종목 수치가 너무 적게 들어왔습니다.")
    return book


def _rel_rows(book):
    rows = []
    for a, b in _REL_PAIRS:
        if a not in book or b not in book:
            continue
        pa, pea, pega, ga, ma = book[a]
        pb, peb, pegb, gb, mb = book[b]
        spread = None if pea is None or peb is None else round(pea - peb, 1)
        rows.append({
            "비교": f"{a} vs {b}",
            "주가A": None if pa is None else round(pa, 1),
            "주가B": None if pb is None else round(pb, 1),
            "Fwd PE A": None if pea is None else round(pea, 1),
            "Fwd PE B": None if peb is None else round(peb, 1),
            "PE 스프레드": spread,
            "PEG A": None if pega is None else round(pega, 2),
            "성장A": None if ga is None else round(ga * 100, 1),
            "판독": _rel_read(a, b, spread, pega),
        })
    return rows


def _rel_read(a, b, spread, peg):
    if spread is None:
        return "Forward PE 없음"
    if abs(spread) < 5:
        band = "멀티플이 거의 같은 밴드"
    elif spread >= 20:
        band = f"{a}가 {b}보다 Forward PE {spread:.0f}포인트 비싸"
    elif spread > 0:
        band = f"{a}가 {b}보다 {spread:.1f}포인트 비싸"
    else:
        band = f"{a}가 {b}보다 {abs(spread):.1f}포인트 싼"
    if peg is None:
        extra = ""
    elif peg < 1:
        extra = f" PEG {peg:.2f}는 성장 대비 부담이 작음."
    elif peg < 2:
        extra = f" PEG {peg:.2f}는 성장이 멀티플을 어느 정도 설명."
    else:
        extra = f" PEG {peg:.2f}는 성장 대비 멀티플 부담이 큼."
    return band + "." + extra + " 매수 신호가 아님."


def render_relval_tab():
    st.markdown(
        '<div class="masthead"><h1>상대밸류</h1><div class="sub">'
        "같은 날 Yahoo Forward PE · PEG로 비교한 스프레드. 추천이 아니다.</div></div>",
        unsafe_allow_html=True,
    )
    st.caption(
        "성장A는 Yahoo earningsGrowth(없으면 매출 성장)입니다. "
        "최근 분기 전년비인 종목이 있어, 장기 성장률과 다를 수 있습니다. "
        "스프레드 판단은 Forward PE와 PEG를 먼저 보세요."
    )
    c1, c2 = st.columns([1, 3])
    with c1:
        if st.button("실시간 갱신", key="relval_refresh_v30"):
            with st.spinner("Yahoo에서 Forward PE · PEG 받는 중…"):
                try:
                    st.session_state["relval_book"] = _rel_fetch_live()
                    st.session_state["relval_asof"] = "방금 갱신"
                except Exception as exc:
                    st.session_state["relval_err"] = str(exc)
    book = st.session_state.get("relval_book") or _REL_PX
    asof = st.session_state.get("relval_asof") or _REL_ASOF
    if st.session_state.get("relval_err") and "relval_book" not in st.session_state:
        st.warning("실시간 갱신 실패 · 실측 스냅샷을 표시합니다. " + st.session_state["relval_err"])
    st.caption("기준일 " + str(asof) + " · 종목 " + str(len(book)))

    rows = _rel_rows(book)
    if not rows:
        st.error("비교 행이 없습니다.")
        return
    import pandas as pd
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.subheader("읽기")
    for r in rows:
        st.markdown("- **" + r["비교"] + "** — " + r["판독"])

    st.subheader("멀티플 압축 시나리오")
    st.caption("이익이 그대일 때 Forward PE만 줄이면 주가가 같은 비율로 줄어듭니다. 이익이 늘면 하락폭은 더 작습니다.")
    names = [n for n in ("PLTR", "LITE", "NVDA", "TSLA", "GOOGL", "META", "MSFT", "AMZN", "MU") if n in book and book[n][0] and book[n][1]]
    pick = st.selectbox("종목", names, index=0, key="relval_scenario_tk")
    px, pe = book[pick][0], book[pick][1]
    peg = book[pick][2]
    a, b, c, d = st.columns(4)
    a.metric("주가", f"{px:,.1f}")
    b.metric("Fwd PE", f"{pe:.1f}")
    c.metric("PEG", "—" if peg is None else f"{peg:.2f}")
    d.metric("유지 시", f"{px:,.1f}")
    scen = []
    for label, cut in (("유지", 0.0), ("PE −20%", 0.20), ("PE −40%", 0.40), ("PE −60%", 0.60)):
        new_pe = pe * (1 - cut)
        tgt = px * (1 - cut)
        scen.append({
            "시나리오": label,
            "적용 Fwd PE": round(new_pe, 1),
            "목표 주가": round(tgt, 1),
            "현재 대비": f"{-cut:.0%}",
        })
    st.dataframe(pd.DataFrame(scen), use_container_width=True, hide_index=True)

    if pick == "PLTR":
        st.warning(
            "PLTR 반증 예시 — 매수 조건이 아님. "
            "미국 상업 성장이 2분기 연속 42% 미만이면 고성장 프리미엄 재검토. "
            "전체 성장이 2분기 연속 25% 미만이면 위 표의 −40%~−60% 밴드를 먼저 봅니다."
        )
    elif pick == "TSLA":
        st.warning("TSLA는 Forward PE가 높아 같은 압축률에서도 주가 하락폭이 큽니다. 추격 판단이 아닙니다.")
    elif pick == "MU":
        st.info("MU Forward PE가 낮은 것은 메모리 실적 급증이 반영된 숫자일 수 있습니다. 다음 분기에 정상화될 수 있습니다.")

    st.caption("v14.30 · 상대밸류 · 실적 후 「실시간 갱신」 · 종목 추천이 아님")


try:
    _rel_tab = TABS[13]
except Exception:
    _rel_tab = TABS[-1] if len(TABS) else None
if _rel_tab is not None:
    to_top()
    with _rel_tab, guard("상대밸류"):
        try:
            render_relval_tab()
        except Exception as _re:
            st.error("상대밸류 패널: " + str(_re))
