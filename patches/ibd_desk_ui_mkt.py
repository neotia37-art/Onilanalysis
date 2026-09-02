        step_header("IBD DESK", "첫화면 · 거래량 테이프 · 36개월 펀드",
                    "구독 화면을 옮겨 적는 칸 + 자동 지수 테이프")
        desk = load_ibd_desk()
        tape = index_tape(CTX.get("states"))
        if tape:
            trows = []
            for r in tape:
                vc = "—" if r["vol_chg"] is None else f'{r["vol_chg"]:+.1f}%'
                trows.append([
                    f'<b>{r["name"]}</b>',
                    f'<span class="mono">{r["px"]:,.2f}</span>' if r["px"] else "—",
                    f'<span class="mono {"down" if (r["chg"] or 0)<0 else "up"}>{pct(r["chg"],2)}</span>',
                    f'<span class="mono">{vc}</span>',
                    tag(r["label"], r["kind"]),
                ])
            st.markdown(table(["지수", "종가", "등락", "거래량 전일비", "국면"], trows), unsafe_allow_html=True)
        fronts = desk.get("front") or []
        if fronts:
            last = fronts[-1]
            st.markdown(
                f'<div class="ev"><b>IBD 첫화면 {last.get("date","")}</b> · '
                f'나스닥 {last.get("nasdaq","—")} ({pct(last.get("nasdaq_chg"),2)}) · '
                f'다우 {last.get("dji","—")} ({pct(last.get("dji_chg"),2)}) · '
                f'S&P {last.get("spx","—")} ({pct(last.get("spx_chg"),2)})<br>'
                f'나스닥 거래량 {last.get("nasdaq_vol","—")}Mil ({pct(last.get("nasdaq_vol_chg"),2)}) · '
                f'NYSE {last.get("nyse_vol","—")}Mil ({pct(last.get("nyse_vol_chg"),2)})<br>'
                f'<span class="m">{last.get("headline","")}</span> · {last.get("note","")}</div>',
                unsafe_allow_html=True)
        with st.expander("IBD 첫화면 기록 추가", expanded=not fronts):
            if st.button("2026-09-02 첫화면 시드 넣기", key="ibd_seed_front"):
                seed = ibd_front_seed_20260902()
                if not any(x.get("date") == seed["date"] for x in desk["front"]):
                    desk["front"].append(seed); save_ibd_desk(desk); st.success("시드 저장")
                else:
                    st.info("이미 같은 날짜")
            fc = st.columns(4)
            d0 = fc[0].text_input("날짜", value=str(datetime.today().date()), key="ibd_f_dt")
            hd = fc[1].text_input("헤드라인", value="", key="ibd_f_hd")
            nq = fc[2].number_input("나스닥 종가", value=0.0, key="ibd_f_nq")
            nqc = fc[3].number_input("나스닥 %", value=0.0, key="ibd_f_nqc")
            note = st.text_input("메모", value="", key="ibd_f_note")
            if st.button("첫화면 저장", key="ibd_f_save"):
                desk["front"].append({"date": d0, "source": "IBD 첫화면 수동", "nasdaq": nq, "nasdaq_chg": nqc, "headline": hd.strip(), "note": note.strip()})
                save_ibd_desk(desk); st.success("저장")
        step_header("FUND CORNER", "36개월 상위 펀드 · 상위10 · 신규 · 축소", "IBD Mutual Fund 코너를 보고 옮긴다")
        funds = desk.get("funds") or []
        if funds:
            for f in funds[::-1][:8]:
                st.markdown(
                    f'<div class="ev"><b>{f.get("name","")}</b> · 36개월 {f.get("grade36","—")} · {f.get("asof","")}<br>'
                    f'상위10 <b>{" · ".join(f.get("top10") or []) or "—"}</b><br>'
                    f'<span class="up">신규 {", ".join(f.get("new") or []) or "—"}</span> · '
                    f'<span class="down">축소 {", ".join(f.get("cut") or []) or "—"}</span></div>', unsafe_allow_html=True)
        with st.expander("펀드 한 개 추가"):
            nm = st.text_input("펀드명", key="ibd_fn")
            gr = st.text_input("36개월 등급", key="ibd_fg")
            asof = st.text_input("기준일", value=str(datetime.today().date()), key="ibd_fa")
            top = st.text_input("상위 10 티커 (쉼표)", key="ibd_ft")
            new = st.text_input("신규 취득 티커", key="ibd_fnew")
            cut = st.text_input("축소 티커", key="ibd_fcut")
            if st.button("펀드 저장", key="ibd_fsave") and nm.strip():
                desk["funds"].append({"name": nm.strip(), "grade36": gr.strip(), "asof": asof, "top10": tickers_from_csv(top), "new": tickers_from_csv(new), "cut": tickers_from_csv(cut)})
                save_ibd_desk(desk); st.success("저장")
        step_header("BLOCK TAPE", "개장 대규모 자금동향 (수동)", "NYSE·나스닥 개장 블록 목록")
        with st.expander("블록 한 줄 추가"):
            bc = st.columns(5)
            bt = bc[0].text_input("티커", key="ibd_bt")
            bd = bc[1].text_input("날짜", value=str(datetime.today().date()), key="ibd_bd")
            bs = bc[2].selectbox("방향", ["매수", "매도", "혼합"], key="ibd_bs")
            ba = bc[3].text_input("규모", key="ibd_ba")
            bn = bc[4].text_input("메모", key="ibd_bn")
            if st.button("블록 저장", key="ibd_bsave") and bt.strip():
                desk["block"].append({"ticker": bt.strip().upper(), "date": bd, "side": bs, "amount": ba.strip(), "note": bn.strip()})
                save_ibd_desk(desk); st.success("저장")
        if desk.get("block"):
            brows = [[b.get("date"), b.get("ticker"), b.get("side"), b.get("amount") or "—", b.get("note") or "—"] for b in desk["block"][::-1][:20]]
            st.markdown(table(["날짜", "티커", "방향", "규모", "메모"], [[f'<span class="mono">{a}</span>' for a in r] for r in brows]), unsafe_allow_html=True)
        with st.expander("기관보증을 이 앱에 담는 방식"):
            st.markdown("- 오닐의 I는 우량 펀드가 담는가이지 기관보유율 한 칸이 아니다.\n- 자동: 거래량비율, 지수 거래량 전일비, yfinance 기관보유율.\n- 수동: IBD 첫화면, 36개월 펀드, 개장 블록, 종목 분석문.\n" + f"- {IBD_I_ADJ}")
