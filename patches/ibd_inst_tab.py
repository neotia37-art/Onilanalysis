# TAB 10 — 기관동향
to_top()
with TABS[10], guard("기관동향"):
    st.markdown('<div class="masthead"><h1>기관투자동향 (I)</h1><div class="sub">'
                "Daily Mutual 스냅샷 · 36개월 펀드 · Checkup 추이 · 수동 누적</div></div>",
                unsafe_allow_html=True)
    desk = load_ibd_desk()
    try:
        ensure_book_seed(desk)
    except Exception:
        pass
    try:
        ensure_wt_full_checkup(desk)
    except Exception:
        pass
    read_box(
        "오닐의 I는 기관보유율 한 칸이 아니다. "
        "<b>① 우량 펀드가 새로 새었는가</b> "
        "<b>② 기존 보유가 추가했는가</b> "
        "<b>③ 그 펀드의 신규 상위 3~4인가</b> "
        "<b>④ 펀드 수 자체가 몇 분기 늘었는가</b>. "
        "날짜별로 쌓고 아래에서 고친다.",
        "오닐 I — How to Make Money in Stocks", "oneil")
    rows = desk.get("inst") or []
    chks = desk.get("checkups") or {}
    snaps = sorted(desk.get("mutual") or [], key=lambda x: str(x.get("date") or ""))
    funds = desk.get("funds") or []
    def _chg(x):
        try:
            return float(x)
        except Exception:
            return -999
    def _q(x):
        try:
            return int(x)
        except Exception:
            return 0
    ranked = sorted(rows, key=lambda r: (_chg(r.get("funds_chg")), _q(r.get("funds_up_q"))), reverse=True)
    new_buys = [r for r in ranked if _chg(r.get("funds_chg")) >= 8]
    steady = [r for r in ranked if _q(r.get("funds_up_q")) >= 3]
    top34 = ranked[:4]
    c = st.columns(4)
    c[0].markdown(card("신규·대규모", f"{len(new_buys)}", "펀드보유 변화 +8% 이상", "up" if new_buys else "mut"), unsafe_allow_html=True)
    c[1].markdown(card("펀드 수 연속증가", f"{len(steady)}", "3분기 이상", "up" if steady else "mut"), unsafe_allow_html=True)
    c[2].markdown(card("신규매입 상위", " · ".join(r.get("ticker") for r in top34) or "—", "펀드% 기준 3~4", "amb"), unsafe_allow_html=True)
    c[3].markdown(card("Mutual 스냅샷", f"{len(snaps)}일", "7/17 · 9/1 시드 후 누적", "up" if snaps else "mut"), unsafe_allow_html=True)
    step_header("MUTUAL DESK", "Daily Mutual Data · 날짜별 누적", "090126 = 8/31 종가 지면 · 0717 = 7/16 종가 지면")
    if snaps:
        sdates = [str(s.get("date")) for s in snaps]
        pick = st.selectbox("스냅샷 날짜", sdates[::-1], key="mut_pick")
        snap = next((s for s in snaps if str(s.get("date")) == pick), snaps[-1])
        st.markdown(f'<div class="ev"><b>{snap.get("date")}</b> · {snap.get("asof") or ""} · {snap.get("source") or ""}<br><span class="m">{snap.get("headline") or ""} {snap.get("note") or ""}</span></div>', unsafe_allow_html=True)
        if snap.get("sectors"):
            st.markdown(table(["Fidelity Select", "YTD%", "4주%"], [[f'<b>{x.get("name")}</b>', x.get("ytd"), x.get("w4")] for x in snap["sectors"]]), unsafe_allow_html=True)
        if snap.get("funds"):
            st.markdown(table(["36개월 펀드", "등급", "YTD", "AUM"], [[f'<b>{x.get("name")}</b>', x.get("grade36") or "—", x.get("ytd") if x.get("ytd") is not None else "—", x.get("aum") or "—"] for x in snap["funds"]]), unsafe_allow_html=True)
        if snap.get("etf"):
            st.markdown(table(["ETF", "보유", "비중%"], [[x.get("etf"), f'<b>{x.get("tk")}</b>', x.get("w")] for x in snap["etf"][:12]]), unsafe_allow_html=True)
    else:
        st.markdown('<div class="hint">Mutual 스냅샷이 없습니다. 아래에서 날짜를 추가하세요.</div>', unsafe_allow_html=True)
    with st.expander("Mutual 스냅샷 입력 · 정정"):
        mc = st.columns(3)
        md = mc[0].text_input("날짜", value=str(datetime.today().date()), key="mut_d")
        masof = mc[1].text_input("기준", key="mut_asof")
        mhead = mc[2].text_input("헤드라인", key="mut_head")
        mnote = st.text_area("메모", height=80, key="mut_note")
        if st.button("Mutual 스냅샷 저장", key="mut_save") and md.strip():
            rec = {"date": md.strip(), "asof": masof.strip(), "headline": mhead.strip(), "note": mnote.strip(), "source": "수동", "funds": [], "etf": [], "sectors": []}
            old = next((x for x in desk.get("mutual") or [] if str(x.get("date")) == md.strip()), None)
            if old:
                rec["funds"] = old.get("funds") or []
                rec["etf"] = old.get("etf") or []
                rec["sectors"] = old.get("sectors") or []
                rec["source"] = old.get("source") or "수동"
            if "upsert_mutual" in dir():
                upsert_mutual(desk, rec)
            else:
                desk["mutual"] = [x for x in desk.get("mutual") or [] if str(x.get("date")) != md.strip()] + [rec]
                save_ibd_desk(desk)
            st.success(f"Mutual {md} 저장")
            st.rerun()
    if top34:
        step_header("TOP NEW", "펀드보유 변화 상위", "차트·A/D를 같이 본다")
        trows = []
        for r in top34:
            tk = r.get("ticker")
            hist = checkup_history(tk, desk) if "checkup_history" in dir() else (chks.get(tk) or [])
            chk = hist[-1] if hist else {}
            dlt = checkup_delta(hist) if "checkup_delta" in dir() else None
            trows.append([f"<b>{tk}</b>", f'{r.get("funds_chg")}%', f'{r.get("funds_up_q")}분기', chk.get("ad") or r.get("ad") or "—", chk.get("rs") or "—", chk.get("comp") or "—", (f'Δ펀드 {dlt["funds_chg"]:+.0f}' if dlt and dlt.get("funds_chg") is not None else r.get("note") or "")])
        st.markdown(table(["티커", "펀드%", "증가분기", "A/D", "RS", "Comp", "추이/메모"], trows), unsafe_allow_html=True)
    step_header("BOARD", "관찰 종목 전체", "Checkup 시드 + 수동 행 · 날짜 누적")
    if ranked:
        brows = []
        for r in ranked:
            tk = r.get("ticker")
            chk = (checkup_history(tk, desk) if "checkup_history" in dir() else (chks.get(tk) or []) or [{}])[-1]
            flag = []
            if _chg(r.get("funds_chg")) >= 10:
                flag.append("신규/대량")
            if _q(r.get("funds_up_q")) >= 3:
                flag.append("연속증가")
            ad = str(r.get("ad") or chk.get("ad") or "")
            if ad in ("D", "E"):
                flag.append("분산A/D")
            brows.append([f"<b>{tk}</b>", r.get("date") or "—", f'{r.get("funds_chg")}%', f'{r.get("funds_up_q")}', ad or "—", chk.get("rs") or "—", chk.get("comp") or "—", " · ".join(flag) or "—"])
        st.markdown(table(["티커", "기준일", "펀드%", "증가분기", "A/D", "RS", "Comp", "태그"], brows), unsafe_allow_html=True)
    with st.expander("기관 행 추가 · 정정"):
        ic = st.columns(5)
        itk = ic[0].text_input("티커", key="inst_tk")
        idt = ic[1].text_input("날짜", value=str(datetime.today().date()), key="inst_dt")
        ich = ic[2].number_input("펀드보유 %변화", value=0.0, key="inst_ch")
        iq = ic[3].number_input("증가 분기", value=0, step=1, key="inst_q")
        iad = ic[4].text_input("A/D", key="inst_ad")
        inote = st.text_input("메모", key="inst_note")
        if st.button("기관 행 저장", key="inst_save") and itk.strip():
            tkU = itk.strip().upper()
            desk["inst"] = [x for x in desk.get("inst") or [] if not (str(x.get("ticker")) == tkU and str(x.get("date")) == idt)]
            desk["inst"].append({"ticker": tkU, "date": idt, "funds_chg": ich, "funds_up_q": int(iq), "ad": iad.strip(), "new_flag": ich >= 10, "note": inote.strip(), "source": "수동"})
            save_ibd_desk(desk)
            st.success(f"{tkU} {idt} 저장")
            st.rerun()
    step_header("QUALITY FUNDS", "36개월 상위 펀드의 신규 3~4", "Mutual 시드 + 수동")
    if funds:
        bag = {}
        for f in funds:
            for t in f.get("new") or []:
                bag.setdefault(t, []).append((f.get("name"), f.get("grade36"), "신규"))
            for t in f.get("top10") or []:
                bag.setdefault(t, []).append((f.get("name"), f.get("grade36"), "상위10"))
            for t in f.get("cut") or []:
                bag.setdefault(t, []).append((f.get("name"), f.get("grade36"), "축소"))
        if bag:
            frows = [[f"<b>{t}</b>", str(sum(1 for h in hs if h[2] == "신규")), ", ".join(f"{a}({c}/{b or '—'})" for a, b, c in hs[:4])] for t, hs in bag.items()]
            frows.sort(key=lambda r: -int(r[1]))
            st.markdown(table(["티커", "신규펀드 수", "교차"], frows), unsafe_allow_html=True)
        st.markdown(table(["펀드", "36개월", "날짜", "신규", "상위10"], [[f'<b>{f.get("name")}</b>', f.get("grade36") or "—", f.get("date") or "—", ", ".join(f.get("new") or []) or "—", ", ".join(f.get("top10") or []) or "—"] for f in funds]), unsafe_allow_html=True)
    with st.expander("36개월 펀드 입력 · 정정"):
        fc = st.columns(4)
        fn = fc[0].text_input("펀드명", key="qf_n")
        fg = fc[1].text_input("36개월 등급", key="qf_g")
        fd = fc[2].text_input("날짜", value=str(datetime.today().date()), key="qf_d")
        fy = fc[3].number_input("YTD%", value=0.0, key="qf_y")
        fnew = st.text_input("신규 티커 (쉼표)", key="qf_new")
        ftop = st.text_input("상위10 티커 (쉼표)", key="qf_top")
        if st.button("펀드 저장", key="qf_save") and fn.strip():
            recf = {"name": fn.strip(), "grade36": fg.strip(), "date": fd.strip(), "ytd": fy, "new": [x.strip().upper() for x in fnew.split(",") if x.strip()], "top10": [x.strip().upper() for x in ftop.split(",") if x.strip()], "cut": [], "source": "수동"}
            desk["funds"] = [x for x in desk.get("funds") or [] if not (x.get("name") == recf["name"] and str(x.get("date")) == recf["date"])] + [recf]
            save_ibd_desk(desk)
            st.success(f'{recf["name"]} {recf["date"]} 저장')
            st.rerun()
    step_header("CHECKUP BOOK", "17종 Stock Checkup · 날짜 추이", "PDF 시드 후 개별종목 탭에서 날짜별로 정정")
    book = []
    for tk, lst in sorted(chks.items()):
        hist = sorted(lst, key=lambda x: str(x.get("date") or ""))
        c0 = hist[-1]
        dlt = checkup_delta(hist) if "checkup_delta" in dir() else None
        trend = "—"
        if dlt and dlt.get("funds_chg") is not None:
            trend = f'{dlt["from"]}->{dlt["to"]} 펀드 {dlt["funds_chg"]:+.0f} RS {dlt.get("rs") or 0:+.0f}'
        elif len(hist) == 1:
            trend = "1일"
        book.append([f"<b>{tk}</b>", c0.get("name") or "", c0.get("comp") or "—", c0.get("eps") or "—", c0.get("rs") or "—", f'{c0.get("smr") or "—"}/{c0.get("ad") or "—"}', f'{c0.get("funds_chg")}% / {c0.get("funds_up_q")}q', c0.get("date") or "", trend])
    if book:
        st.markdown(table(["티커", "이름", "Comp", "EPS", "RS", "SMR/AD", "펀드%/분기", "기준일", "추이"], book), unsafe_allow_html=True)
    read_box(
        "9/2 Checkup. <b>SNDK(+39%·3q)</b> · <b>ETON(+25%·1q)</b> · <b>MU(+15%·5q)</b> 가 신규/대규모 후보. "
        "SNDK 고점 −34%·A/D E, ETON 50일 +33%, MU A/D E — I만 보고 사지 않는다. "
        "보유 WT는 펀드 5분기 · EPS 99 · RS 95, A/D C · 부채 195%. "
        "다음 지면은 날짜를 바꿔 저장하면 추이 칸이 생긴다.",
        "오늘 스냅샷에서 보이는 것")
