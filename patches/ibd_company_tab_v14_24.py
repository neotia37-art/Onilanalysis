COMPANY_TAB_V14_24 = True

def _co_fmt(v, suffix=""):
    if v is None or v == "":
        return "—"
    return f"{v}{suffix}"


def render_company_overview(tk=None, desk=None):
    keys = sorted(COMPANY_PROFILES.keys())
    default = str(tk or "CRWD").upper()
    if default not in COMPANY_PROFILES:
        default = "CRWD"
    pick = st.selectbox("회사개요 티커", keys, index=keys.index(default), key="co_tab_tk")
    p = COMPANY_PROFILES[pick]
    ck = p.get("checkup") or {}
    a, b, c, d, e = st.columns(5)
    a.metric("Comp", _co_fmt(ck.get("comp")))
    b.metric("EPS / RS", f'{_co_fmt(ck.get("eps"))} / {_co_fmt(ck.get("rs"))}')
    c.metric("SMR / A/D", f'{_co_fmt(ck.get("smr"))} / {_co_fmt(ck.get("ad"))}')
    d.metric("vs50 / off52", f'{_co_fmt(ck.get("vs50"), "%")} / {_co_fmt(ck.get("off52"), "%")}')
    e.metric("Checkup일", _co_fmt(ck.get("date")))
    st.caption(
        f'{p.get("exchange")} · {p.get("group")} · CEO {p.get("ceo")} · HQ {p.get("hq")} · '
        f'FY {p.get("fy_end")} · IPO {p.get("ipo")} · 펌드 {ck.get("funds")} · 그룹 {ck.get("group")}'
    )
    st.info(p.get("one_liner") or "")
    if ck.get("verdict"):
        st.warning("판정 · " + str(ck.get("verdict")) + " · 종목 추천이 아니다.")
    step_header("사업", "무엇을 팔고 누가 적인가", p.get("name") or pick)
    st.write(p.get("business") or "")
    if p.get("products"):
        st.markdown(table(["모듈 / 제품", "메모"], p["products"]), unsafe_allow_html=True)
    if p.get("snapshot"):
        step_header("숫자", "수록 스냅샷", "원전은 Checkup·IR·키움")
        st.markdown(table(["칸", "값"], p["snapshot"]), unsafe_allow_html=True)
    if p.get("risks"):
        step_header("리스크", "S칸의 흉터와 이격", "")
        for r in p["risks"]:
            st.markdown("- " + str(r))
    live = None
    if desk:
        try:
            hist = checkup_history(pick, desk) if callable(globals().get("checkup_history")) else ((desk.get("checkups") or {}).get(pick) or [])
            if hist:
                live = sorted(hist, key=lambda x: str(x.get("date") or ""))[-1]
        except Exception:
            live = None
    if live:
        step_header("장부 Checkup", "앱에 실린 최신 행", str(live.get("date") or ""))
        st.caption(live.get("body") or live.get("inst_note") or live.get("source") or "")
    step_header("링크", "IR · IBD · SEC", "클릭은 공부. 매수 허가 아님")
    for title, url in (p.get("links") or []):
        st.markdown(f"- [{title}]({url})")
    if p.get("local"):
        st.caption("로컬 원전 파일명: " + " · ".join(p["local"]))
    if p.get("study"):
        st.caption("공부장: " + p["study"])
    return pick


to_top()
with TABS[12], guard("회사개요"):
    st.markdown(
        '<div class="masthead"><h1>회사개요</h1><div class="sub">'
        "수록 자료로 사업·숫자·리스크·링크만 정리한다. 추천이 아니다.</div></div>",
        unsafe_allow_html=True,
    )
    try:
        read_box(
            "회사개요는 개별종목 탭의 성적표를 설명하는 칸이다. "
            "<b>점수가 좋으면 사는 칸이 아니다.</b> "
            "CRWD는 Comp 99 / RS 99 / A/D A+여도 50일 +22%면 추격 금지.",
            "오닐 공부장 · v14.24",
            "oneil",
        )
    except Exception:
        st.caption("회사개요 · 추천 아님 · 추격 금지")
    desk = None
    try:
        desk = load_ibd_desk()
        ensure_book_seed(desk)
    except Exception:
        pass
    side_tk = None
    try:
        side_tk = st.session_state.get("tk") or st.session_state.get("ticker")
    except Exception:
        side_tk = None
    try:
        render_company_overview(side_tk, desk)
    except Exception as _ce:
        st.error("회사개요 패널: " + str(_ce))
    st.caption("v14.24 · Pulse 9/28 80-100 NAS3/SPX6 · CRWD Checkup 9/29 · 공통6 교차는 공부 명단")
