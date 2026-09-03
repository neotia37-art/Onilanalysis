# TAB 10 — 기관동향
# ════════════════════════════════════════════════════════════════
    to_top()
with TABS[10], guard("기관동향"):
    st.markdown('<div class="masthead"><h1>기관투자동향 (I)</h1><div class="sub">'
                "신규취득 · 펀드 수 증가 · Stock Checkup · 36개월 펀드</div></div>",
                unsafe_allow_html=True)
    desk = load_ibd_desk()
    read_box(
        "오닐의 I는 기관보유율 한 칸이 아니다. "
        "<b>① 최근 분기에 우량 펀드 한두 곳이 새로 새는가</b> "
        "<b>② 기존 보유 펀드가 대규모로 추가했는가</b> "
        "<b>③ 그 펀드의 신규매입 상위 3~4 종목인가</b> "
        "<b>④ 지난 몇 분기 이 주식을 산 펀드 수 자체가 꾸준히 늘었는가</b>. "
        "질이 나쁘 펀드 100곳보다 36개월 상위 펀드 2곳의 신규 편입이 더 중요하다. "
        "펀드 수가 줄면 매수 리스트에서 뻔다.",
        "오닐 I — How to Make Money in Stocks", "oneil")

    rows = desk.get("inst") or []
    chks = desk.get("checkups") or {}
    if not rows:
        for tk, lst in chks.items():
            if lst:
                c = lst[-1]
                rows.append({
                    "ticker": tk, "date": c.get("date"),
                    "funds_chg": c.get("funds_chg"), "funds_up_q": c.get("funds_up_q"),
                    "ad": c.get("ad"), "ud_vol": c.get("ud_vol"),
                    "new_flag": (c.get("funds_chg") or 0) >= 10,
                    "note": c.get("inst_note") or "",
                })

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

    ranked = sorted(rows, key=lambda r: (_chg(r.get("funds_chg")), _q(r.get("funds_up_q"))),
                    reverse=True)
    new_buys = [r for r in ranked if _chg(r.get("funds_chg")) >= 8]
    steady = [r for r in ranked if _q(r.get("funds_up_q")) >= 3]
    top34 = ranked[:4]

    c = st.columns(3)
    c[0].markdown(card("신규·대규모 추가 후보",
                       f"{len(new_buys)}",
                       "펀드보유 변화 +8% 이상 — 최근 분기 신규/추가",
                       "up" if new_buys else "mut"), unsafe_allow_html=True)
    c[1].markdown(card("펀드 수 연속 증가",
                       f"{len(steady)}",
                       "3분기 이상 펀드 수가 늘어난 종목",
                       "up" if steady else "mut"), unsafe_allow_html=True)
    c[2].markdown(card("신규매입 상위 3~4",
                       " · ".join(r.get("ticker") for r in top34) or "—",
                       "펀드보유 %변화 기준",
                       "amb"), unsafe_allow_html=True)

    if top34:
        step_header("TOP NEW", "펀드보유 변화 상위 — 오닐의 신규매입 3~4",
                    "숫자가 크다고 바로 사지 않는다. 차트·A/D를 같이 본다")
        trows = []
        for r in top34:
            tk = r.get("ticker")
            chk = (chks.get(tk) or [None])[-1]
            trows.append([
                f"<b>{tk}</b>",
                f'{r.get("funds_chg")}%',
                f'{r.get("funds_up_q")}분기',
                (chk or {}).get("ad") or r.get("ad") or "—",
                (chk or {}).get("rs") or "—",
                (chk or {}).get("comp") or "—",
                r.get("note") or (chk or {}).get("inst_note") or "",
            ])
        st.markdown(table(["티커", "펀드%", "증가분기", "A/D", "RS", "Comp", "메모"], trows),
                    unsafe_allow_html=True)

    step_header("BOARD", "관찰 종목 전체", "Stock Checkup 시드 + 수동 행")
    if ranked:
        brows = []
        for r in ranked:
            tk = r.get("ticker")
            chk = (chks.get(tk) or [None])[-1] or {}
            flag = []
            if _chg(r.get("funds_chg")) >= 10:
                flag.append("신규/대량")
            if _q(r.get("funds_up_q")) >= 3:
                flag.append("연속증가")
            ad = str(r.get("ad") or chk.get("ad") or "")
            if ad in ("D", "E"):
                flag.append("분산A/D")
            brows.append([
                f"<b>{tk}</b>",
                r.get("date") or "—",
                f'{r.get("funds_chg")}%',
                f'{r.get("funds_up_q")}',
                ad or "—",
                chk.get("rs") or "—",
                chk.get("comp") or "—",
                " · ".join(flag) or "—",
            ])
        st.markdown(table(["티커", "기준일", "펀드%", "증가분기", "A/D", "RS", "Comp", "태그"],
                          brows), unsafe_allow_html=True)
    else:
        st.markdown('<div class="hint">아직 기관 행이 없습니다. '
                    "개별종목 탭 Checkup을 저장하거나 아래에서 한 줄을 추가하세요.</div>",
                    unsafe_allow_html=True)

    with st.expander("기관 행 추가 · 정정"):
        ic = st.columns(5)
        itk = ic[0].text_input("티커", key="inst_tk")
        idt = ic[1].text_input("날짜", value=str(datetime.today().date()), key="inst_dt")
        ich = ic[2].number_input("펀드보유 %변화", value=0.0, key="inst_ch")
        iq = ic[3].number_input("증가 분기", value=0, step=1, key="inst_q")
        iad = ic[4].text_input("A/D", key="inst_ad")
        inote = st.text_input("메모 (신규 펀드명, 규모)", key="inst_note")
        if st.button("기관 행 저장", key="inst_save") and itk.strip():
            tkU = itk.strip().upper()
            desk["inst"] = [x for x in desk.get("inst") or []
                            if not (str(x.get("ticker")) == tkU and str(x.get("date")) == idt)]
            desk["inst"].append({
                "ticker": tkU, "date": idt, "funds_chg": ich,
                "funds_up_q": int(iq), "ad": iad.strip(),
                "new_flag": ich >= 10, "note": inote.strip(),
                "source": "수동",
            })
            save_ibd_desk(desk)
            st.success(f"{tkU} {idt} 저장")
            st.rerun()

    funds = desk.get("funds") or []
    step_header("QUALITY FUNDS", "36개월 상위 펀드의 신규 3~4",
                "펀드 코너에 적은 신규 취득이 여기로 모인다")
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
            frows = []
            for t, hs in bag.items():
                frows.append([
                    f"<b>{t}</b>",
                    str(sum(1 for h in hs if h[2] == "신규")),
                    ", ".join(f"{a}({c}/{b or '—'})" for a, b, c in hs[:4]),
                ])
            frows.sort(key=lambda r: -int(r[1]))
            st.markdown(table(["티커", "신규펀드 수", "교차"], frows),
                        unsafe_allow_html=True)
        else:
            st.markdown('<div class="hint">펀드는 있으나 신규/상위10 티커가 비어 있습니다.</div>',
                        unsafe_allow_html=True)
    else:
        st.markdown('<div class="hint">시장 탭 FUND CORNER에 36개월 상위 펀드를 한 개라도 옮기면 '
                    "그 펀드의 신규 3~4 종목이 이 표에 모인다.</div>",
                    unsafe_allow_html=True)

    step_header("CHECKUP BOOK", "오늘 올린 Stock Checkup 17종",
                "이후 자료는 개별종목 탭에서 날짜별로 정정")
    book = []
    for tk, lst in sorted(chks.items()):
        c0 = lst[-1]
        book.append([
            f"<b>{tk}</b>",
            c0.get("name") or "",
            c0.get("comp") or "—",
            c0.get("eps") or "—",
            c0.get("rs") or "—",
            f'{c0.get("smr") or "—"}/{c0.get("ad") or "—"}',
            f'{c0.get("funds_chg")}% / {c0.get("funds_up_q")}q',
            c0.get("date") or "",
        ])
    if book:
        st.markdown(table(["티커", "이름", "Comp", "EPS", "RS", "SMR/AD", "펀드%/분기", "기준일"],
                          book), unsafe_allow_html=True)
    read_box(
        "체크리스트. <b>SNDK(+39%·3분기)</b> · <b>ETON(+25%·1분기)</b> · "
        "<b>MU(+15%·5분기)</b> 가 신규/대규모 추가 후보. "
        "다만 SNDK는 고점 −34%·A/D E, ETON은 50일선 +33%, MU는 A/D E 라 "
        "I만 보고 사면 안 된다. "
        "보유 WT는 펀드 5분기 증가·EPS 99·RS 95, A/D C·부채 195%. "
        "21일선 지지와 A/D 개선을 추가 매수 조건으로 둔다.",
        "오늘 스냅샷에서 보이는 것")
