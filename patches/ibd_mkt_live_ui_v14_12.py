# LIVE + IBD 5 psycho + risk trio (VIX / P/C / HY OAS) v14.17
MKT_LIVE_UI_V14_12 = True
MKT_PSYCHO_V14_13 = True
MKT_PSYCHO_UI_V14_13 = True
MKT_PSYCHO_V14_17 = True
MKT_RISK_TRIO_V14_17 = True


PSYCHO_SEED_V14_16 = [
    {"date": "2026-09-01", "vix": 15.5, "put_call": 0.79, "high_low": None,
     "bulls": 51.9, "bears": 30.9, "margin_yoy": 38.6, "hy_oas": 2.65,
     "source": "DailyPsycho_090126 + FRED OAS"},
    {"date": "2026-09-03", "vix": 15.2, "put_call": 0.73, "high_low": None,
     "bulls": 45.0, "bears": None, "margin_yoy": 38.6, "hy_oas": 2.65,
     "source": "MARKET PULSE + FRED OAS"},
    {"date": "2026-09-08", "vix": 14.6, "put_call": 0.71, "high_low": 0.71,
     "bulls": 54.9, "bears": 17.6, "margin_yoy": 38.6, "hy_oas": 2.68,
     "source": "DailyPsycho_090826 + FRED OAS 9/7"},
]


def _psy_date(d):
    try:
        return pd.Timestamp(d).strftime("%Y-%m-%d")
    except Exception:
        return str(d or "")[:10]


def _psy_f(x):
    if x is None or x == "":
        return None
    try:
        return float(x)
    except Exception:
        return None


def load_psycho_book():
    desk = {}
    try:
        desk = load_ibd_desk() or {}
    except Exception:
        desk = {}
    if not isinstance(desk, dict):
        desk = {}
    lists = desk.setdefault("lists", {})
    hist = [dict(x) for x in (lists.get("psycho_history") or []) if x]
    by_d = {_psy_date(x.get("date")): x for x in hist if _psy_date(x.get("date"))}
    seeded = False
    if not by_d:
        for rec in PSYCHO_SEED_V14_16:
            by_d[_psy_date(rec["date"])] = dict(rec)
        seeded = True
    else:
        seed_map = {_psy_date(r["date"]): r for r in PSYCHO_SEED_V14_16}
        for dt, rec in list(by_d.items()):
            if rec.get("hy_oas") is None and dt in seed_map and seed_map[dt].get("hy_oas") is not None:
                rec["hy_oas"] = seed_map[dt]["hy_oas"]
                by_d[dt] = rec
                seeded = True
    if seeded:
        lists["psycho_history"] = sorted(by_d.values(), key=lambda x: _psy_date(x.get("date")))
        lists["psycho_latest"] = lists["psycho_history"][-1]
        try:
            save_ibd_desk(desk)
        except Exception:
            pass
    hist = sorted(by_d.values(), key=lambda x: _psy_date(x.get("date")))
    latest = hist[-1] if hist else {}
    lists["psycho_history"] = hist
    lists["psycho_latest"] = latest
    return desk, hist, latest


def save_psycho_row(desk, rec):
    rec = dict(rec)
    rec["date"] = _psy_date(rec.get("date"))
    lists = desk.setdefault("lists", {})
    hist = [x for x in (lists.get("psycho_history") or [])
            if _psy_date(x.get("date")) != rec["date"]]
    hist.append(rec)
    hist.sort(key=lambda x: _psy_date(x.get("date")))
    lists["psycho_history"] = hist
    lists["psycho_latest"] = rec
    save_ibd_desk(desk)
    return hist


def delete_psycho_row(desk, dt):
    dt = _psy_date(dt)
    lists = desk.setdefault("lists", {})
    hist = [x for x in (lists.get("psycho_history") or [])
            if _psy_date(x.get("date")) != dt]
    lists["psycho_history"] = hist
    lists["psycho_latest"] = hist[-1] if hist else {}
    save_ibd_desk(desk)
    return hist


def _mkt_live_now():
    try:
        return pd.Timestamp.now(tz="Asia/Seoul").strftime("%Y-%m-%d %H:%M KST")
    except Exception:
        return pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")


def fetch_live_risk_trio():
    """Live VIX + ICE BofA HY OAS (FRED). Put/Call is print-only."""
    out = {"vix": None, "vix_dt": None, "hy_oas": None, "hy_dt": None, "src": []}
    try:
        import yfinance as yf
        h = yf.download("^VIX", period="7d", progress=False, auto_adjust=True)
        if h is not None and len(h):
            col = "Close" if "Close" in h.columns else h.columns[-1]
            s = h[col].dropna()
            if hasattr(s, "iloc") and len(s):
                out["vix"] = float(s.iloc[-1])
                out["vix_dt"] = str(s.index[-1])[:10]
                out["src"].append("yfinance ^VIX")
    except Exception:
        pass
    try:
        import urllib.request
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAMLH0A0HYM2"
        with urllib.request.urlopen(url, timeout=12) as r:
            raw = r.read().decode("utf-8", "ignore")
        rows = []
        for ln in raw.splitlines()[1:]:
            parts = ln.split(",")
            if len(parts) >= 2 and parts[1] not in ("", ".", "NA"):
                try:
                    rows.append((parts[0][:10], float(parts[1])))
                except Exception:
                    pass
        if rows:
            out["hy_dt"], out["hy_oas"] = rows[-1]
            out["src"].append("FRED BAMLH0A0HYM2")
    except Exception:
        pass
    return out


def risk_trio_verdict(vix, pc, oas):
    """2-of-3 cluster. Not a buy trigger."""
    flags = []
    calm = 0
    stress = 0
    if vix is not None:
        if vix >= 30:
            flags.append(f"VIX {vix:.1f} 스트레스")
            stress += 1
        elif vix >= 20:
            flags.append(f"VIX {vix:.1f} 경계")
            stress += 1
        elif vix < 16:
            flags.append(f"VIX {vix:.1f} 안일")
            calm += 1
        else:
            flags.append(f"VIX {vix:.1f} 보통")
    if pc is not None:
        if pc >= 1.15:
            flags.append(f"P/C {pc:.2f} 포공(역발상 후보)")
            stress += 1
        elif pc >= 1.00:
            flags.append(f"P/C {pc:.2f} 헤지")
            stress += 1
        elif pc < 0.70:
            flags.append(f"P/C {pc:.2f} 콜편중")
            calm += 1
        else:
            flags.append(f"P/C {pc:.2f} 보통")
    if oas is not None:
        if oas >= 5.50:
            flags.append(f"HY OAS {oas:.2f}% 신용 스트레스")
            stress += 1
        elif oas >= 4.50:
            flags.append(f"HY OAS {oas:.2f}% 스프레드 경계")
            stress += 1
        elif oas < 3.50:
            flags.append(f"HY OAS {oas:.2f}% 압축=안일")
            calm += 1
        else:
            flags.append(f"HY OAS {oas:.2f}% 보통")
    if stress >= 2:
        label, tone = "리스크온 이탈(2/3 이상 악화)", "down"
    elif calm >= 2:
        label, tone = "안일 군집(2/3 이상 압축)", "warn"
    else:
        label, tone = "혼조 · 한 지표만으로 판단 금지", "neutral"
    return label, tone, flags, calm, stress


def render_market_live(ctx=None):
    ctx = ctx or (globals().get("CTX") or {})
    try:
        render_market_psycho(ctx)
    except Exception:
        pass


def render_market_psycho(ctx=None):
    ctx = ctx or {}
    desk, hist, latest = load_psycho_book()
    live = fetch_live_risk_trio()
    vix = latest.get("vix")
    pc = latest.get("put_call")
    oas = latest.get("hy_oas")
    trio_label, trio_tone, trio_flags, trio_calm, trio_stress = risk_trio_verdict(vix, pc, oas)

    try:
        step_header(
            "IBD 5대 심리지표 + 리스크 3종",
            "수동 입력 · 날짜별 누적 · VIX / 풇콜 / HY OAS 군집",
            "인쇄본을 손으로 옮긴다. HY OAS는 FRED 일별을 붙여 오탐을 줄인다.",
        )
    except Exception:
        st.markdown("##### IBD 5대 심리지표 + 리스크 3종")

    specs = [
        ("VIX", vix, "14.6 · 45 미만=안일. 바닥 신호 아님"),
        ("풇콜", pc, "0.71 · 콜 편중=낙관"),
        ("High-Low", latest.get("high_low"), "0.71 · 0.5 아래여야 조정바닥 감시"),
        ("Bulls / Bears", latest.get("bulls"),
         f"Bulls {latest.get('bulls')}% / Bears {latest.get('bears')}% · 자문 낙관"),
        ("Margin YoY", latest.get("margin_yoy"), "38.6% · 55%가 대형 천정 경고"),
    ]
    cols = st.columns(5)
    for col, (title, val, sub) in zip(cols, specs):
        shown = "—" if val is None else (
            f"{float(val):.2f}" if title in ("풇콜", "High-Low")
            else (f"{float(val):.1f}%" if title != "VIX" else f"{float(val):.1f}")
        )
        try:
            col.markdown(card(title, shown, sub, "warn"), unsafe_allow_html=True)
        except Exception:
            col.metric(title, shown, sub)

    t1, t2, t3, t4 = st.columns(4)
    oas_s = "—" if oas is None else f"{float(oas):.2f}%"
    live_vix_s = "—" if live.get("vix") is None else f"{live['vix']:.1f}"
    live_oas_s = "—" if live.get("hy_oas") is None else f"{live['hy_oas']:.2f}%"
    try:
        t1.markdown(card("HY OAS", oas_s, "ICE BofA HY OAS · 3.5% 미만=압축 · 4.5%+=경계",
                         "warn" if (oas is not None and oas < 3.5) else "neutral"),
                    unsafe_allow_html=True)
        t2.markdown(card("라이브 VIX", live_vix_s, f"yfinance · {live.get('vix_dt') or '—'}",
                         "warn"), unsafe_allow_html=True)
        t3.markdown(card("라이브 HY OAS", live_oas_s, f"FRED · {live.get('hy_dt') or '—'}",
                         "warn"), unsafe_allow_html=True)
        t4.markdown(card("3종 군집", f"{trio_stress}악 / {trio_calm}안일",
                         trio_label, trio_tone if trio_tone in ("up", "down", "warn") else "warn"),
                    unsafe_allow_html=True)
    except Exception:
        t1.metric("HY OAS", oas_s)
        t2.metric("라이브 VIX", live_vix_s)
        t3.metric("라이브 HY OAS", live_oas_s)
        t4.metric("3종 군집", trio_label)

    st.caption(" · ".join(trio_flags) if trio_flags else "3종 숫자 부족")
    if live.get("src"):
        st.caption("라이브 원전 " + " / ".join(live["src"]) + " · 풇콜은 인쇄 수동")

    with st.expander("지표 설명 · 오닐 + 신용 군집", expanded=False):
        st.markdown(
            "- **VIX** — IBD는 45 초과를 강세(포공=바닥 후보)로 본다. 14대는 안일. 10일선 대비 +20% 치솟을 때가 단기 바닥 힌트.\n"
            "- **풇콜** — 1.0+ 헤지/포공. 0.50~0.70은 콜 편중=낙관. 매수 방아쇠가 아니다.\n"
            "- **HY OAS** — ICE BofA 하이일드 스프레드. 주가와 역행. 3.5% 아래 압축=안일, 4.5%+ 확대=신용 경계. "
            "VIX만 보고 오탐을 줄이려고 붙인다. IBD 5대는 아님.\n"
            "- **High-Low** — 신고/신저. 강세장 중간조정에서 0.5 아래로 내려간 뒤 첫 상승일이 단기 바닥.\n"
            "- **Bulls vs Bears** — 자문 강세/약세. 강세 높고 약세 극소=군중 낙관=경계.\n"
            "- **Margin Debt** — 신용 전년비 55% 초과가 대형 천정 경고.\n"
            "- **3종 군집** — VIX·P/C·OAS 중 2개 이상이 같은 방향일 때만 국면으로 읽는다. "
            "하나만이 움직이면 잡음. 분산일·FTD·리더 피벗이 먼저다."
        )

    st.markdown("**수동 입력·정정** · 같은 날짜는 덮어쓴다. 빈칸은 기록 안 함.")
    try:
        default_dt = pd.Timestamp(latest.get("date") or "2026-09-08").date()
    except Exception:
        default_dt = pd.Timestamp("2026-09-08").date()
    with st.form("psycho_edit_v17"):
        r1 = st.columns(3)
        in_date = r1[0].date_input("날짜", value=default_dt)
        in_src = r1[1].text_input("원전", value=str(latest.get("source") or "IBD 인쇄 수동"))
        in_note = r1[2].text_input("메모", value=str(latest.get("note") or ""))
        r2 = st.columns(4)
        in_vix = r2[0].text_input("VIX", value="" if vix is None else str(vix))
        in_pc = r2[1].text_input("풇콜 Put/Call", value="" if pc is None else str(pc))
        in_oas = r2[2].text_input(
            "HY OAS %",
            value="" if oas is None else str(oas),
            help="FRED BAMLH0A0HYM2. 예: 2.68",
        )
        in_hl = r2[3].text_input("High-Low", value="" if latest.get("high_low") is None else str(latest.get("high_low")))
        r3 = st.columns(3)
        in_bulls = r3[0].text_input("Bulls %", value="" if latest.get("bulls") is None else str(latest.get("bulls")))
        in_bears = r3[1].text_input("Bears %", value="" if latest.get("bears") is None else str(latest.get("bears")))
        in_mgn = r3[2].text_input("Margin YoY %", value="" if latest.get("margin_yoy") is None else str(latest.get("margin_yoy")))
        saved = st.form_submit_button("이 날짜로 저장")
    if saved:
        rec = {
            "date": _psy_date(in_date),
            "vix": _psy_f(in_vix),
            "put_call": _psy_f(in_pc),
            "hy_oas": _psy_f(in_oas),
            "high_low": _psy_f(in_hl),
            "bulls": _psy_f(in_bulls),
            "bears": _psy_f(in_bears),
            "margin_yoy": _psy_f(in_mgn),
            "source": (in_src or "IBD 인쇄 수동").strip(),
            "note": (in_note or "").strip(),
        }
        try:
            hist = save_psycho_row(desk, rec)
            st.success(f"{rec['date']} 저장 · 누적 {len(hist)}일 · OAS {rec.get('hy_oas')}")
            st.rerun()
        except Exception as e:
            st.error("저장 실패: " + str(e))

    if hist:
        ddel = st.columns([3, 1])
        pick = ddel[0].selectbox(
            "지울 날짜",
            options=[_psy_date(x.get("date")) for x in hist],
            index=len(hist) - 1,
            key="psy_del_dt",
        )
        if ddel[1].button("이 날짜 삭제", key="psy_del_btn"):
            try:
                delete_psycho_row(desk, pick)
                st.warning(f"{pick} 삭제")
                st.rerun()
            except Exception as e:
                st.error("삭제 실패: " + str(e))

    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        xs = [_psy_date(r.get("date")) for r in hist]
        fig = make_subplots(
            rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.07,
            subplot_titles=("리스크 3종  VIX · Put/Call · HY OAS",
                            "VIX · High-Low · Put/Call",
                            "Bulls vs Bears %",
                            "Margin YoY %"),
        )
        fig.add_trace(go.Scatter(x=xs, y=[r.get("vix") for r in hist], name="VIX", mode="lines+markers"), row=1, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("put_call") for r in hist], name="Put/Call", mode="lines+markers"), row=1, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("hy_oas") for r in hist], name="HY OAS %", mode="lines+markers"), row=1, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("vix") for r in hist], name="VIX ", mode="lines+markers", showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("high_low") for r in hist], name="High-Low", mode="lines+markers"), row=2, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("put_call") for r in hist], name="P/C", mode="lines+markers", showlegend=False), row=2, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("bulls") for r in hist], name="Bulls %", mode="lines+markers"), row=3, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("bears") for r in hist], name="Bears %", mode="lines+markers"), row=3, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("margin_yoy") for r in hist], name="Margin YoY", mode="lines+markers"), row=4, col=1)
        fig.add_hline(y=45, line_dash="dot", line_color="#888", annotation_text="VIX 45", row=1, col=1)
        fig.add_hline(y=3.5, line_dash="dot", line_color="#c44", annotation_text="OAS 3.5", row=1, col=1)
        fig.add_hline(y=55, line_dash="dot", line_color="#c44", annotation_text="55%", row=4, col=1)
        fig.update_layout(height=720, margin=dict(t=52, b=24, l=40, r=20),
                          legend=dict(orientation="h", y=1.06),
                          title=f"심리+신용 추이 · {len(hist)}일 누적")
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.caption("그래프 생략. 표로 본다.")
    if hist:
        st.dataframe(hist, hide_index=True, use_container_width=True)

    st.markdown(
        '<div class="ev"><b>시장 종합의견</b> · 분산 작업 5 후보 · 신규 추격 0<br>'
        '<span class="m">공식 Pulse(9/3) 노출 60-80% · 분산 NAS 4 / SPX 3. FTD 2026-06-02 (세 달 전). '
        "화요 9/8 하락+거래량증가 = 분산일 후보. 작업카운트 NAS 5 / SPX 4. "
        f"VIX {vix} 안일 · P/C {pc} 콜편중 · HY OAS {oas}% 압축 · "
        f"3종 판정: {trio_label}. "
        "심리 낙관 + 신용 압축 + 기관 매도 흔적 = 같은 날 추격하지 않는다. "
        "아래 67점 탐욕은 앱 자체 포공탐욕이다. 5대 심리·OAS와 섞지 말 것.</span></div>",
        unsafe_allow_html=True)
    try:
        read_box(
            "VIX·풇콜·HY OAS는 <b>묵음</b>으로만 읽는다. 지금 세 칸 모두 안일/압축이다. "
            "화요는 분산 후보다. 작업 5면 신규는 없다.",
            "DailyPsycho · FRED HY OAS · 리스크 3종", "oneil")
    except Exception:
        st.caption("67점 ≠ 5대 심리. OAS 압축 + 분산 후보 = 추격 금지.")
