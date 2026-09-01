        # STEP 6.5 종목 FTD · 분산일 (매도일) — 시장 규칙을 이 종목에 이식
        step_header("STEP 6.5", "종목 FTD · 분산일 (매도일)",
                    "시장 규칙을 이 종목 차트에 그대로 적용해 공부한다")
        _rev = stock_ftd_dd_review(df, CTX.get("states"))
        _f = _rev["ftd"]
        rc = st.columns(4)
        rc[0].markdown(card("종목 FTD",
                            f'<span class="{"up" if _rev["f_kind"]=="pass" else ("amb" if _rev["f_kind"]=="warn" else "down")}">{_rev["f_label"]}</span>',
                            (f'{_f["date"]:%Y-%m-%d} · 저점 {_f.get("day","?")}일차 {pct(_f.get("gain"),2)}'
                             f'<br>품질 {_f.get("quality") or "—"} · 이후 {pct(_f.get("ret_since"))}'
                             if _f.get("date") is not None else
                             (f'램리 {_f.get("rally_day","?")}일차 · 저점 {_f["low_date"]:%Y-%m-%d}'
                              if _f.get("state") == "rally_attempt" and _f.get("low_date") is not None else
                              f'최대 낙폭 {pct(_f.get("max_dd"))}')),
                            "up" if _rev["f_kind"] == "pass" else ("amb" if _rev["f_kind"] == "warn" else ("down" if _rev["f_kind"] == "fail" else "mut"))),
                       unsafe_allow_html=True)
        rc[1].markdown(card("유효 분산일",
                            f'{_rev["active_n"]}<span style="font-size:.85rem">개 / 25일</span>',
                            f'{_rev["dd_label"]} · 10일 클러스터 {_rev["cluster10"]}개<br>원전 문텀(−0.2%)이면 {_rev["classic_n"]}개',
                            "down" if _rev["dd_kind"] == "fail" else ("amb" if _rev["dd_kind"] == "warn" else "up")),
                       unsafe_allow_html=True)
        rc[2].markdown(card("오늘 캔들",
                            ("분산일" if _rev["today_dd"] else ("종목 FTD" if _rev["today_ftd"] else "해당 없음")),
                            f'등락 {pct(_rev["today_chg"],2)} · ' + ("종가↓ + 거래량↑" if _rev["today_dd"] else "분산일 조건 미충족"),
                            "down" if _rev["today_dd"] else ("up" if _rev["today_ftd"] else "mut")),
                       unsafe_allow_html=True)
        rc[3].markdown(card("시장(M) 대조", _rev["mkt"]["label"], "종목 FTD는 M을 대체하지 않는다",
                            "up" if _rev["mkt"]["kind"] == "pass" else ("amb" if _rev["mkt"]["kind"] == "warn" else ("down" if _rev["mkt"]["kind"] == "fail" else "mut"))),
                       unsafe_allow_html=True)
        st.markdown(f'{tag(_rev["act"], _rev["act_k"])}', unsafe_allow_html=True)
        st.plotly_chart(stock_ftd_chart(df, _rev), use_container_width=True)
        _chk_rows = []
        for title, ok, note in (_f.get("checks") or []):
            _chk_rows.append([title, verdict(ok), f'<span class="m">{note}</span>'])
        _chk_rows.append(["오늘이 종목 분산일인가", verdict(_rev["today_dd"]), f'하락 {_rev["today_chg"]:+.2f}% + 거래량 전일비'])
        _chk_rows.append(["유효 분산일 ≤ 2 (건강)", verdict(_rev["active_n"] <= 2), _rev["dd_why"]])
        _chk_rows.append(["10일 클러스터 ≤ 2", verdict(_rev["cluster10"] <= 2), f'{_rev["cluster10"]}개 — 한 주에 몰리면 매도 캠페인'])
        _chk_rows.append(["시장 FTD/상승이 먼저인가", verdict(_rev["mkt"].get("ok") is True), _rev["mkt"]["label"]])
        st.markdown(table(["체크 (공부)", "판정", "근거"], _chk_rows), unsafe_allow_html=True)
        if _rev["dd_stock"]:
            with st.expander(f'분산일 원장 — 종목 문텀 −0.5% ({_rev["active_n"]}개 유효 / {len(_rev["dd_stock"])}개 탐지)'):
                _dd_rows = []
                for r in _rev["dd_stock"][::-1]:
                    _dd_rows.append([f'{r["date"]:%Y-%m-%d}', f'<span class="down">{r["chg"]:+.2f}%</span>',
                                     f'{r["vol_vs_prev"]:.2f}배' if r.get("vol_vs_prev") else "—",
                                     "만료(+5% 소화)" if r.get("expired") else tag("유효", "fail"),
                                     f'{r["close_loc"]*100:.0f}%' if r.get("close_loc") is not None else "—"])
                st.markdown(table(["날짜", "등락", "거래량/전일", "상태", "종가위치(하단=강한 매도)"], _dd_rows), unsafe_allow_html=True)
        else:
            st.markdown('<div class="hint">종목 문텀(−0.5%)으로 본 유효 분산일이 없습니다.</div>', unsafe_allow_html=True)
        read_box(
            '종목 FTD·분산일은 <b>지수 규칙을 이 종목 일봉에 그대로 엎은 공부 도구</b>입니다. '
            '오닐 원전은 이 두 신호를 지수에만 쓰였습니다. 종목에 쓸 때는 문텀만 올립니다.<br><br>'
            '<b>① 종목 FTD</b> — 고점 대비 8% 이상 밀린 뒤, 저점에서 4일 이상 지나 종가가 +1.5% 이상 오르고 거래량이 전일보다 큰 첫날. '
            '4~7일차 + 50일평균 거래량 이상이면 품질 <b>prime</b>. 그 이후 저점을 종가로 깨면 무효.<br>'
            '<b>② 종목 분산일(매도일)</b> — 종가 −0.5% 이하 + 거래량 전일비 증가. +5% 회복 시 만료. 25일 유효 5개면 분산 캠페인.<br>'
            '<b>③ 시장(M)이 먼저</b> — 종목 FTD가 떠도 지수 FTD가 없으면 추격하지 않습니다.<br><br>'
            f'오늘 이 종목: <b>{_rev["act"]}</b>',
            "종목 FTD · 분산일을 이렇게 읽는다", "oneil")
