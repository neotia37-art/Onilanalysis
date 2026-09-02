            _ed = eps_rating_detail(fnd, q_g, y_g)
            step_header("STEP 3b", "주당순이익등급 근사 · 매출·이익·ROE 분해",
                        "IBD EPS Rating의 앱 보수 근사 — 원점이 아니다")
            ec = st.columns(4)
            ec[0].markdown(card("EPS Rating (근사)", str(_ed["rating"] if _ed["rating"] is not None else "—"),
                                f'곡선 원점수 {_ed["raw"]} · {_ed["cap_why"]}',
                                "up" if (_ed["rating"] or 0) >= 80 else "mut"), unsafe_allow_html=True)
            ec[1].markdown(card("연간 이익 증가", pct(_ed["y_profit"]), "특별 표시선 +30%",
                                "up" if (_ed["y_profit"] or 0) >= 30 else "mut"), unsafe_allow_html=True)
            ec[2].markdown(card("ROE", f'{pct(_ed["roe"],1,False)}' + (f' ({_ed["roe_d"]:+.1f}p)' if _ed["roe_d"] is not None else ""),
                                f'직전 {pct(_ed["roe_prev"],1,False)} · 기준 17%',
                                "up" if (_ed["roe"] or 0) >= 17 else "mut"), unsafe_allow_html=True)
            ec[3].markdown(card("연매출 증가", pct(_ed["y_sales"]), f'분기 매출 {pct(_ed["q_sales"])}',
                                "up" if (_ed["y_sales"] or 0) >= 25 else "mut"), unsafe_allow_html=True)
            if _ed["elite"]:
                st.markdown(tag("A 엘리트", "pass") +
                            ' <span class="hint">연간 이익증가율 <b>30% 이상</b> + ROE <b>17% 이상</b>.</span>',
                            unsafe_allow_html=True)
            _erows = []
            for lab, val, bar_, ok in _ed["rows"]:
                vs = ("—" if val is None else (f'{val:+.1f}p' if lab.endswith("(p)") else pct(val)))
                _erows.append([lab, f'<span class="mono">{vs}</span>', bar_, verdict(ok)])
            st.markdown(table(["항목", "측정", "기준", "판정"], _erows), unsafe_allow_html=True)
            with st.expander("IBD 대비 이 앱의 조정 근거 ( 다음 수정 시 여기)"):
                st.markdown("- EPS는 유니버스 백분위가 아니라 성장률 곡선. C·A 미달 시 상한 80.\n- 특별 배지는 연이익 +30% AND ROE 17%.\n- " + IBD_ADJ)
