
            # ── 4. 이 종목의 과거에서 배우기
            step_header("LESSON 4", "이 종목의 과거 베이스에서 배우기",
                        "같은 차트라도 종목마다 성향이 다릅니다")
            if len(binfo["bases"]) > 1:
                rows = []
                for bb in binfo["bases"][-8:]:
                    after = df.loc[bb["end"]:].head(120)
                    fwd = ((float(after["Close"].max()) / bb["left_high"] - 1) * 100
                           if bb["completed"] and len(after) > 2 else None)
                    mdd_ = ((float(after["Close"].min()) / bb["left_high"] - 1) * 100
                            if bb["completed"] and len(after) > 2 else None)
                    ok_ = fwd is not None and fwd >= 20
                    rows.append([f'<b>{bb["count"]}차</b>',
                                 f'{bb["start"]:%y.%m.%d} ~ {bb["end"]:%y.%m.%d}',
                                 f'<span class="mono">{bb["weeks"]:.0f}주</span>',
                                 f'<span class="mono">{bb["depth"]:.0f}%</span>',
                                 "돌파" if bb["completed"] else "진행중",
                                 (f'<span class="mono {"up" if ok_ else "mut"}">{fwd:+.0f}%</span>'
                                  if fwd is not None else "—"),
                                 (f'<span class="mono down">{mdd_:+.0f}%</span>'
                                  if mdd_ is not None else "—"),
                                 (tag("성공", "pass") if ok_ else tag("미달", "fail"))
                                 if fwd is not None else ""])
                st.markdown(table(["차수", "기간", "주", "깊이", "상태",
                                   "돌파후 최대", "돌파후 최저", "판정"], rows),
                            unsafe_allow_html=True)
                w_, t_ = binfo["win"]
                read_box(
                    f'이 종목은 과거 베이스 돌파 {t_}회 중 <b>{w_}회</b>가 성공했습니다 '
                    f'(120일 내 +20% 도달 기준). '
                    + ("성공률이 높은 편이라 이번 돌파도 신뢰도가 있습니다."
                       if t_ and w_ / t_ >= 0.5 else
                       "성공률이 낮은 편입니다. 이 종목은 돌파 후 되밀림이 자으니 "
                       "거래량 확인을 더 엄격하게 하세요.")
                    + '<br><br>깊이가 얖고(20% 이내) 기간이 긴 베이스일수록 돌파 성공률이 높습니다. '
                      '위 표에서 성공한 베이스들의 공통점을 찾아보세요 — 그게 이 종목의 패턴입니다.',
                    "과거가 알려주는 것")
            else:
                st.markdown('<div class="hint">비교할 과거 베이스가 아직 없습니다. '
                            '데이터가 짧거나 첫 베이스입니다.</div>', unsafe_allow_html=True)

        # ── 5. 오늘의 차트 문제
        step_header("QUIZ", "오늘의 차트 문제", "이 종목의 실제 수치로 출제됩니다")
        D2 = dict(D)
        D2["rating_val"] = CTX.get("rating")
        qs = base_quiz(df, binfo, D2, market)
        for i, q in enumerate(qs):
            with st.container():
                st.markdown(f'<div class="card" style="margin-bottom:.5rem">'
                            f'<div class="k">문제 {i+1}</div>'
                            f'<div style="font-size:.9rem;font-weight:600;margin:.3rem 0">'
                            f'{q["q"]}</div></div>', unsafe_allow_html=True)
                pick = st.radio("답을 고르세요", q["opts"], index=None,
                                key=f"quiz_{TK}_{i}", horizontal=True,
                                label_visibility="collapsed")
                if pick is not None:
                    ok = q["opts"].index(pick) == q["ans"]
                    st.markdown((tag("정답", "pass") if ok else
                                 tag(f'오답 — 정답은 "{q["opts"][q["ans"]]}"', "fail"))
                                + f'<div class="read" style="margin-top:.4rem">'
                                  f'<span class="h">해설</span>{q["why"]}</div>',
                                unsafe_allow_html=True)

        # ── 6. 패턴 도감
        step_header("ATLAS", "베이스 패턴 도감", "모든 유형을 한자리")
        for nm, L in BASE_LESSON.items():
            cur_mark = " ← 현재 이 종목" if (binfo and binfo["type"] == nm) else ""
            with st.expander(f'{nm}{cur_mark}', expanded=bool(cur_mark)):
                st.markdown(f'<div class="hint"><b>왜 생기나</b> · {L["why"]}</div>'
                            f'<div class="hint" style="margin-top:.4rem"><b>생김새</b> · '
                            f'{L["shape"]}</div>', unsafe_allow_html=True)
                ac = st.columns(2)
                ac[0].markdown("<br>" + table(["합격 기준"], [[x] for x in L["spec"]]),
                               unsafe_allow_html=True)
                ac[1].markdown("<br>" + table(["함정"], [[x] for x in L["trap"]]),
                               unsafe_allow_html=True)
                st.markdown(f'<div class="read oneil" style="margin-top:.5rem">'
                            f'<span class="h">한 줄 기억</span>{L["story"]}</div>',
                            unsafe_allow_html=True)

        # ── 7. 오늘의 오닐 한 마디
        step_header("TIP", "오늘의 오닐 한 마디", "매일 하나씩 · 날짜 기준 순환")
        idx_tip = (datetime.today().timetuple().tm_yday) % len(ONEIL_TIPS)
        t_title, t_body = ONEIL_TIPS[idx_tip]
        st.markdown(f'<div class="big"><div class="k">오늘의 원칙</div>'
                    f'<div class="v" style="font-size:1.15rem">{t_title}</div>'
                    f'<div class="d">{t_body}</div></div>', unsafe_allow_html=True)
        with st.expander("전체 원칙 10가지 보기"):
            st.markdown(table(["원칙", "내용"], [[a, b_] for a, b_ in ONEIL_TIPS]),
                        unsafe_allow_html=True)

        st.markdown('<div class="quote">차트 공부는 하루아침에 되지 않습니다. 매일 이 탭에서 '
                    '한 종목씩 패턴을 확인하고 문제를 풀다 보면, 나중엔 차트를 열자마자 '
                    '모양이 보이게 됩니다. 오닐도 "수천 개의 차트를 직접 그려봤다"고 했습니다.</div>',
                    unsafe_allow_html=True)
    to_top()
