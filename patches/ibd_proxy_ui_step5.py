        _sl = rs_line_slopes(CTX.get("rsl"))
        _rf = rs_proxy_flags(CTX.get("rating"), r, _sl)
        _lead = ftd_leader_tag(CTX, CTX.get("rating"), D.get("gap52"))
        _contra = contra_thrust_days(df, CTX.get("bench"))
        rc2 = st.columns(4)
        rc2[0].markdown(card("RS 87+ 주도 후보", "해당" if _rf["elite"] else "아님",
                             "IBD 90 선호 → 앱 87", "up" if _rf["elite"] else "mut"), unsafe_allow_html=True)
        rc2[1].markdown(card("RS선 6·12개월", f'{pct(_rf["s6"])} / {pct(_rf["s12"])}',
                             "둘 다 하락이면 절대 매수 금지", "down" if _rf["trend_down"] else "up"), unsafe_allow_html=True)
        rc2[2].markdown(card("70대 진입 추정", "추가매수 금지" if _rf["drop70"] else "해당 없음",
                             "80~90에서 70 첫 하락 대용", "down" if _rf["drop70"] else "mut"), unsafe_allow_html=True)
        if sect and sect.get("rank"):
            _top5 = sect["rank"] <= 5
            rc2[3].markdown(card("산업군 상대강도", f'{sect["rank"]}위 / {sect["total"]}',
                                 "선도 산업군 상위 5" if _top5 else "상위 5 밖",
                                 "up" if _top5 else "mut"), unsafe_allow_html=True)
        else:
            rc2[3].markdown(card("산업군 상대강도", "미수집", "한국은 섹터 ETF 맵 없음"), unsafe_allow_html=True)
        for lab, k, why in _rf["flags"]:
            st.markdown(tag(lab, k) + f' <span class="hint">{why}</span>', unsafe_allow_html=True)
        if _lead:
            st.markdown(tag(_lead["label"], _lead["kind"]) + f' <span class="hint">{_lead["why"]}</span>', unsafe_allow_html=True)
        if _contra:
            _crow = [[f'{x["date"]:%Y-%m-%d}', f'<span class="up">{x["stock"]:+.2f}%</span>',
                      f'<span class="down">{x["idx"]:+.2f}%</span>', "거래량↑" if x["vol_up"] else "거래량 보통"] for x in _contra[::-1]]
            with st.expander(f'시장 급락일 홀로 오른 세션 {len(_contra)}건'):
                st.markdown(table(["날짜", "종목", "벤치", "거래량"], _crow), unsafe_allow_html=True)
        with st.expander("RS 산정 근거 · IBD 괴리"):
            st.markdown("- 산식 0.4×3M + 0.2×(6+9+12M) 백분위.\n- 87 배지는 IBD 90을 앱에서 한 칸 내린 값.\n- 6~12M 하락 금지는 주가÷벤치 기울기 대용.\n- " + IBD_ADJ)
