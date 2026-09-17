def render_eps_streak(fnd, market=None):
    """개별종목 STEP 3 아래 — 3년·6분기 EPS + 최우선 뱃지."""
    st.markdown('<div data-eps-streak="v14.23"></div>', unsafe_allow_html=True)
    S = eps_streak_from_fnd(fnd)
    step_header("C·A 연속", "최근 3년 · 6분기 EPS 증가율",
                "전년동기(분기) · 전년(연간). 손익계산서 열이 짧으면 실적발표 EPS로 6분기를 채운다")
    if S["priority"]:
        st.markdown(
            tag("최우선", "pass")
            + ' <span class="hint"><b>강력한 증가추세</b> — '
            + (S["note"] or "3년·분기 연속 +25%")
            + ". 오닐 A(3년) + C(최근 분기 연속)가 동시에 열린 자리. "
            "시장(M)이 닫혀 있으면 뱃지만 보고 사지 않는다.</span>",
            unsafe_allow_html=True)
    elif S["y_streak"] or S["q_streak"]:
        which = "3년 연속 +25%" if S["y_streak"] else f"{S['q_n']}분기 연속 +25%"
        st.markdown(
            tag("한쪽만 충족", "warn")
            + f' <span class="hint">{which}. 최우선은 <b>3년과 분기(4개 이상)가 동시에 +25%</b>일 때만 단다.</span>',
            unsafe_allow_html=True)
    else:
        st.markdown(
            tag("최우선 아님", "idle")
            + ' <span class="hint">3년 연속 +25% 그리고 최근 분기 4개 이상 모두 +25%가 아니면 뱃지를 달지 않는다.</span>',
            unsafe_allow_html=True)

    c = st.columns(4)
    c[0].markdown(card("3년 +25% 충족",
                       f"{S['y_ge25']}/{S['y_n']}년" if S["y_n"] else "—",
                       "기준 3년 모두",
                       "up" if S["y_streak"] else "mut"),
                  unsafe_allow_html=True)
    c[1].markdown(card("6분기 +25% 충족",
                       f"{S['q_ge25']}/{S['q_n']}분기" if S["q_n"] else "—",
                       "확보분 기준 · 목표 6분기",
                       "up" if S["q_streak"] else "mut"),
                  unsafe_allow_html=True)
    c[2].markdown(card("최근 분기 YoY",
                       _es_fmt_g(S["last_q"]),
                       "C 기준 +25%",
                       "up" if _es_ok(S["last_q"], 25) else "down"),
                  unsafe_allow_html=True)
    acc_lab = "가속" if S["accel"] else ("둔화" if S["accel"] is False else "—")
    c[3].markdown(card("분기 추세",
                       acc_lab,
                       "창 첫 분기 대비 최근",
                       "up" if S["accel"] else ("mut" if S["accel"] is None else "down")),
                  unsafe_allow_html=True)

    def _rows(items, year=False):
        out = []
        for r in items:
            g = r.get("growth")
            if g is None:
                ghtml = "—"
            elif g == 999:
                ghtml = '<span class="mono up">흑자전환</span>'
            else:
                cl = "up" if g >= 25 else ("ink2" if g >= 0 else "down")
                ghtml = f'<span class="mono {cl}">{_es_fmt_g(g)}</span>'
            out.append([
                r.get("label") or "—",
                f'<span class="mono">{_es_fmt_eps(r.get("eps"))}</span>',
                f'<span class="mono">{_es_fmt_eps(r.get("prev"))}</span>',
                ghtml,
                r.get("kind") or "—",
                r.get("src") or "—",
            ])
        return out

    cc = st.columns(2)
    with cc[0]:
        st.markdown('<div class="hint" style="margin:.3rem 0"><b>분기별 EPS 증가율</b> · '
                    "최근 최대 6분기 · 전년 같은 분기 대비</div>",
                    unsafe_allow_html=True)
        qr = _rows(S["q_rows"])
        if qr:
            st.markdown(table(["분기", "EPS", "전년동기", "증가율", "비교", "출처"], qr),
                        unsafe_allow_html=True)
            seq = " → ".join(_es_fmt_g(r.get("growth")) for r in S["q_rows"])
            extra = tag("가속", "pass") if S["accel"] else (
                tag("둔화", "warn") if S["accel"] is False else "")
            st.markdown(f'<div class="ev">6분기 EPS 증가율 추이 <b>{seq}</b> {extra}</div>',
                        unsafe_allow_html=True)
            if S["q_n"] < 6:
                st.markdown(
                    f'<div class="hint">지금은 <b>{S["q_n"]}분기</b>만 확보. '
                    "Yahoo 손익계산서는 보통 4~5분기라 실적발표 EPS로 채운다. "
                    "4분기 미만이면 최우선을 달지 않는다.</div>",
                    unsafe_allow_html=True)
        else:
            st.markdown('<div class="hint">분기 EPS 이력을 못 만들었습니다. '
                        "STEP 3 입력란 또는 다음 실적 수록을 기다리세요.</div>",
                        unsafe_allow_html=True)
    with cc[1]:
        st.markdown('<div class="hint" style="margin:.3rem 0"><b>년도별 EPS 증가율</b> · '
                    "최근 3년 · 전년 대비</div>",
                    unsafe_allow_html=True)
        yr = _rows(S["y_rows"], year=True)
        if yr:
            st.markdown(table(["연도", "EPS", "전년", "증가율", "비교", "출처"], yr),
                        unsafe_allow_html=True)
            seq = " → ".join(_es_fmt_g(r.get("growth")) for r in S["y_rows"])
            st.markdown(f'<div class="ev">3년 EPS 증가율 추이 <b>{seq}</b></div>',
                        unsafe_allow_html=True)
        else:
            st.markdown('<div class="hint">연간 EPS 이력을 불러오지 못했습니다.</div>',
                        unsafe_allow_html=True)

    ev = [
        ("3년 연속 EPS +25%",
         f"{S['y_ge25']}/{S['y_n']}년" if S["y_n"] else "—",
         "3/3", S["y_streak"]),
        ("6분기 연속 EPS +25%",
         f"{S['q_ge25']}/{S['q_n']}분기" if S["q_n"] else "—",
         "확보분 전부 + 최소 4분기", S["q_streak"]),
        ("최근 분기 EPS YoY", _es_fmt_g(S["last_q"]), "+25%", _es_ok(S["last_q"], 25)),
        ("최우선 뱃지", "ON" if S["priority"] else "OFF",
         "3년+분기 동시 충족", S["priority"]),
    ]
    if callable(globals().get("evidence")):
        st.markdown(evidence(ev), unsafe_allow_html=True)
    return S
