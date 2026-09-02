        _sl = rs_line_slopes(CTX.get("rsl"))
        _rf = rs_proxy_flags(CTX.get("rating"), r, _sl)
        _lead = ftd_leader_tag(CTX, CTX.get("rating"), D.get("gap52"))
        _contra = contra_thrust_days(df, CTX.get("bench"))
        rc2 = st.columns(4)
        rc2[0].markdown(card("RS 87+ 주도 후보",
                             "해당" if _rf["elite"] else "아님",
                             "IBD 90 선호 → 앱 87 (유니버스 작음)",
                             "up" if _rf["elite"] else "mut"), unsafe_allow_html=True)
        rc2[1].markdown(card("RS선 6·12개월",
                             f'{pct(_rf["s6"])} / {pct(_rf["s12"])}',
                             "둘 다 하락이면 절대 매수 금지",
                             "down" if _rf["trend_down"] else "up"), unsafe_allow_html=True)
        rc2[2].markdown(card("70대 진입 추정",
                             "추가매수 금지" if _rf["drop70"] else "해당 없음",
                             "80~90에서 70으로 첫 하락의 대용",
                             "down" if _rf["drop70"] else "mut"), unsafe_allow_html=True)
        if sect and sect.get("rank"):
            _top5 = sect["rank"] <= 5
            rc2[3].markdown(card("산업군 상대강도",
                                 f'{sect["rank"]}위 / {sect["total"]}',
                                 ("선도 산업군 상위 5 · 이 안에서만 매수 유도"
                                  if _top5 else "상위 5 밖 · 업종 이유로 사지 않는다"),
                                 "up" if _top5 else "mut"), unsafe_allow_html=True)
        else:
            rc2[3].markdown(card("산업군 상대강도", "미수집",
                                 "한국은 섹터 ETF 맵이 없어 업종 매수 유도 안 함"),
                            unsafe_allow_html=True)
        for lab, k, why in _rf["flags"]:
            st.markdown(tag(lab, k) + f' <span class="hint">{why}</span>',
                        unsafe_allow_html=True)
        if _rf["trend_down"]:
            st.markdown(tag("절대 매수 금지", "fail") +
                        ' <span class="hint">최근 6~12개월 RS 추세선이 하락한다. '
                        '오닐은 상대강도가 꺽인 주식을 사지 않았다.</span>',
                        unsafe_allow_html=True)
        if _rf["drop70"]:
            st.markdown(tag("추가 매수 금지", "fail") +
                        ' <span class="hint">RS가 80~90권에서 70대로 내려온 첫 구간으로 본다. '
                        '이 자리에서는 절대로 물타지 않는다.</span>',
                        unsafe_allow_html=True)
        if sect and sect.get("top"):
            st.markdown('<div class="ev">선도 산업군 상위 5 · <b>'
                        + " · ".join(sect["top"][:5]) + '</b>'
                        + (" · 지금 업종이 여기 있으면 그 안에서만 고른다"
                           if sect.get("rank") and sect["rank"] <= 5
                           else " · 지금 업종은 여기 없다")
                        + '</div>', unsafe_allow_html=True)
        if _lead:
            st.markdown(tag(_lead["label"], _lead["kind"]) +
                        f' <span class="hint">{_lead["why"]}. '
                        f'FTD 이후 새 상승은 선도기업이 신고가를 먼저 만든다.</span>',
                        unsafe_allow_html=True)
        if _contra:
            _crow = [[f'{x["date"]:%Y-%m-%d}',
                      f'<span class="up">{x["stock"]:+.2f}%</span>',
                      f'<span class="down">{x["idx"]:+.2f}%</span>',
                      "거래량↑" if x["vol_up"] else "거래량 보통"]
                     for x in _contra[::-1]]
            with st.expander(f'시장 급락일에 홀로 오른 세션 {_contra[-1]["date"]:%Y-%m-%d} 포함 {len(_contra)}건'):
                st.markdown(table(["날짜", "종목", "벤치마크", "거래량"], _crow),
                            unsafe_allow_html=True)
                st.markdown('<div class="hint">벤치마크 −1.2% 이하 + 종목 +1.0% 이상. '
                            '장이 일제히 빨지는데 추세를 거스르면 선도 후보로 표시한다. '
                            '이것만으로 매수하지 않는다.</div>', unsafe_allow_html=True)
        with st.expander("RS 산정 근거 · IBD와의 괴리 (다음 수정 시 여기)"):
            st.markdown(
                "- **산식** 0.4×3개월 + 0.2×(6+9+12개월) 수익률의 유니버스 백분위. 1~99.\n"
                "- **한국** KRX 전종목 등락률, **미국** 유동성 상위군(앱 `UNIVERSE_US`). "
                "미국은 유니버스가 작아 점수가 부풀 수 있다.\n"
                "- **87 특별표시** IBD 원전 90+를 앱에서 한 칸 낮춘 값. 90을 요구하면 후보가 너무 줄어 "
                "유니버스 왜곡을 더 키운다.\n"
                "- **6~12개월 하락 금지** IBD RS선 대신 주가÷벤치마크 비율의 기울기.\n"
                "- **70대 첫 하락** 과거 RS 시계열이 없어 '현재 70~79 + 3M이 6M보다 5%p 약함 + "
                "RS선 6M 하락'을 대용한다.\n"
                f"- {IBD_ADJ}"
            )
