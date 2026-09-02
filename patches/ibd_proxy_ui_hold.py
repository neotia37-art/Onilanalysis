            step_header("HOLD RS·C·A", "보유 종목 상대강도·실적 누적 관리",
                        "매수한 뒤에도 C·A·RS를 매일 다시 적는다")
            _ranked = rank_holdings_by_period(ok_revs)
            _rr = []
            for x in _ranked:
                _rr.append([
                    f'<b>{x["name"]}</b>',
                    f'<span class="mono">{pct(x["m1"])}</span>',
                    f'<span class="mono">{x["rank_m"]}</span>',
                    f'<span class="mono">{pct(x["q1"])}</span>',
                    f'<span class="mono">{x["rank_q"]}</span>',
                    tag("매도 우선", "fail") if x["sell_first"] else tag("대기", "idle"),
                ])
            st.markdown(table(["종목", "1개월", "월 순위", "1분기", "분기 순위", "매도 우선"], _rr),
                        unsafe_allow_html=True)
            st.markdown('<div class="hint">순위는 <b>계좌 안 상대 비교</b>다. '
                        '오닐은 같은 기간에 덜 오른 종목을 먼저 판다. '
                        '1개월·1분기 중 1위(가장 약함)에 매도 우선 표시. '
                        '절대 수익률이 플러스여도 계좌 안에서 꼬찌면 먼저 점검한다.</div>',
                        unsafe_allow_html=True)

            _uni_cache, _bench_cache, _fnd_cache = {}, {}, {}
            _op_rows = []
            dirty = False
            for r in ok_revs:
                h = r["h"]
                mk = r["market"]
                try:
                    hdf, _, _, _ = load_price(h["ticker"])
                except Exception:
                    hdf = None
                if mk not in _uni_cache:
                    _uni_cache[mk] = load_rs_universe(mk)
                if mk not in _bench_cache:
                    _bench_cache[mk] = CTX.get("bench") if mk == CTX.get("market") else None
                if h["ticker"] not in _fnd_cache:
                    try:
                        if mk == "KR":
                            _fnd_cache[h["ticker"]] = load_kr_fund_all(h["ticker"], kr_segment(h["ticker"]))
                        else:
                            px0 = float(hdf["Close"].iloc[-1]) if hdf is not None else 0
                            _fnd_cache[h["ticker"]] = load_us_fund(h["ticker"], px0)
                    except Exception:
                        _fnd_cache[h["ticker"]] = None
                op = ca_rs_opinion(h, hdf, mk, _uni_cache[mk], _bench_cache[mk],
                                   _fnd_cache[h["ticker"]])
                r["ca_op"] = op
                if not h.get("snap") and op.get("snap"):
                    h["snap"] = op["snap"]
                    dirty = True
                _op_rows.append([
                    f'<b>{r["name"]}</b>',
                    f'<span class="mono">{op["rating"] if op["rating"] is not None else "—"}</span>',
                    verdict(op["c_ok"]),
                    verdict(op["a_ok"]),
                    tag(op["opinion"], op["kind"]),
                ])
            if dirty:
                save_portfolio(port)
            st.markdown(table(["종목", "RS", "C", "A", "의견"], _op_rows),
                        unsafe_allow_html=True)
            for r in ok_revs:
                op = r.get("ca_op")
                if not op:
                    continue
                st.markdown(
                    f'<div class="ev"><b>{r["name"]}</b> · '
                    + " · ".join(op["notes"])
                    + f'<br><span class="m">{op["opinion"]}</span></div>',
                    unsafe_allow_html=True)
            with st.expander("보유 C·A·RS 관리 근거"):
                st.markdown(
                    "- 매수 시점 `snap`(RS·C·A·ROE)을 일지에 남기고 오늘 값과 비교한다.\n"
                    "- C는 분기 EPS +25%, A는 연 EPS +25% 또는 ROE 17%.\n"
                    "- RS선 6·12개월 하락이거나 70대 진입 추정이면 추가 매수 금지 의견을 강제한다.\n"
                    "- 재무를 못 가져오면 C·A는 미수집으로 두고 RS 의견만 남긴다."
                )
