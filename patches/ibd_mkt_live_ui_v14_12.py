# LIVE + IBD 5 psycho editor v14.16
MKT_LIVE_UI_V14_12 = True
MKT_PSYCHO_V14_13 = True
MKT_PSYCHO_UI_V14_13 = True

PSYCHO_SEED_V14_16 = [
    {"date": "2026-09-01", "vix": 15.5, "put_call": 0.79, "high_low": None,
     "bulls": 51.9, "bears": 30.9, "margin_yoy": 38.6, "source": "DailyPsycho_090126"},
    {"date": "2026-09-03", "vix": 15.2, "put_call": 0.73, "high_low": None,
     "bulls": 45.0, "bears": None, "margin_yoy": 38.6, "source": "MARKET PULSE"},
    {"date": "2026-09-08", "vix": 14.6, "put_call": 0.71, "high_low": 0.71,
     "bulls": 54.9, "bears": 17.6, "margin_yoy": 38.6, "source": "DailyPsycho_090826"},
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
    if not by_d:
        for rec in PSYCHO_SEED_V14_16:
            by_d[_psy_date(rec["date"])] = dict(rec)
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


def render_market_live(ctx=None):
    ctx = ctx or (globals().get("CTX") or {})
    try:
        render_market_psycho(ctx)
    except Exception:
        pass


def render_market_psycho(ctx=None):
    ctx = ctx or {}
    desk, hist, latest = load_psycho_book()
    try:
        step_header("IBD 5대 심리지표", "수동 입력 · 날짜별 누적 · 추이 그래프",
                    "인쇄본 숫자를 손으로 옮긴다. 아래 67점 공포탐욕과 다른 물건.")
    except Exception:
        st.markdown("##### IBD 5대 심리지표")
    specs = [
        ("VIX", latest.get("vix"), "45 미만=안일"),
        ("풋콜", latest.get("put_call"), "콜 편중=낙관"),
        ("High-Low", latest.get("high_low"), "0.5 아래여야 바닥감시"),
        ("Bulls / Bears", latest.get("bulls"),
         f"Bulls {latest.get('bulls')}% / Bears {latest.get('bears')}%"),
        ("Margin YoY", latest.get("margin_yoy"), "55%가 한계"),
    ]
    cols = st.columns(5)
    for col, (title, val, sub) in zip(cols, specs):
        shown = "—" if val is None else (f"{float(val):.2f}" if title in ("풋콜", "High-Low")
                                         else (f"{float(val):.1f}%" if title != "VIX" else f"{float(val):.1f}"))
        try:
            col.markdown(card(title, shown, sub, "warn"), unsafe_allow_html=True)
        except Exception:
            col.metric(title, shown, sub)
    with st.expander("지표 설명", expanded=False):
        st.markdown("- VIX 45+가 공포(바닥 후보). 14대는 안일.\n- 풋콜 1.0+ 헤지. 0.50~0.70 콜편중.\n- High-Low 0.5 아래 다음 상승일이 조정 바닥 힌트.\n- Bulls 높고 Bears 극소=군중 낙관.\n- Margin 55%+ 대형 천정 경고.\n- 다섯을 평균 내서 사지 않는다.")
    st.markdown("**수동 입력·정정** · 같은 날짜는 덮어쓴다. 빈칸은 기록 안 함.")
    try:
        default_dt = pd.Timestamp(latest.get("date") or "2026-09-08").date()
    except Exception:
        default_dt = pd.Timestamp("2026-09-08").date()
    with st.form("psycho_edit_v16"):
        r1 = st.columns(3)
        in_date = r1[0].date_input("날짜", value=default_dt)
        in_src = r1[1].text_input("원전", value=str(latest.get("source") or "IBD 인쇄 수동"))
        in_note = r1[2].text_input("메모", value=str(latest.get("note") or ""))
        r2 = st.columns(3)
        in_vix = r2[0].text_input("VIX", value="" if latest.get("vix") is None else str(latest.get("vix")))
        in_pc = r2[1].text_input("풋콜 Put/Call", value="" if latest.get("put_call") is None else str(latest.get("put_call")))
        in_hl = r2[2].text_input("High-Low", value="" if latest.get("high_low") is None else str(latest.get("high_low")))
        r3 = st.columns(3)
        in_bulls = r3[0].text_input("Bulls %", value="" if latest.get("bulls") is None else str(latest.get("bulls")))
        in_bears = r3[1].text_input("Bears %", value="" if latest.get("bears") is None else str(latest.get("bears")))
        in_mgn = r3[2].text_input("Margin YoY %", value="" if latest.get("margin_yoy") is None else str(latest.get("margin_yoy")))
        saved = st.form_submit_button("이 날짜로 저장")
    if saved:
        rec = {
            "date": _psy_date(in_date),
            "vix": _psy_f(in_vix), "put_call": _psy_f(in_pc), "high_low": _psy_f(in_hl),
            "bulls": _psy_f(in_bulls), "bears": _psy_f(in_bears), "margin_yoy": _psy_f(in_mgn),
            "source": (in_src or "IBD 인쇄 수동").strip(), "note": (in_note or "").strip(),
        }
        try:
            hist = save_psycho_row(desk, rec)
            st.success(f"{rec['date']} 저장 · 누적 {len(hist)}일")
            st.rerun()
        except Exception as e:
            st.error("저장 실패: " + str(e))
    if hist:
        ddel = st.columns([3, 1])
        pick = ddel[0].selectbox("지울 날짜", options=[_psy_date(x.get("date")) for x in hist],
                                 index=len(hist) - 1, key="psy_del_dt")
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
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.08,
                            subplot_titles=("VIX · High-Low · Put/Call", "Bulls vs Bears %", "Margin YoY %"))
        fig.add_trace(go.Scatter(x=xs, y=[r.get("vix") for r in hist], name="VIX", mode="lines+markers"), row=1, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("high_low") for r in hist], name="High-Low", mode="lines+markers"), row=1, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("put_call") for r in hist], name="Put/Call", mode="lines+markers"), row=1, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("bulls") for r in hist], name="Bulls %", mode="lines+markers"), row=2, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("bears") for r in hist], name="Bears %", mode="lines+markers"), row=2, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("margin_yoy") for r in hist], name="Margin YoY", mode="lines+markers"), row=3, col=1)
        fig.add_hline(y=55, line_dash="dot", line_color="#c44", annotation_text="55%", row=3, col=1)
        fig.add_hline(y=45, line_dash="dot", line_color="#888", annotation_text="VIX 45", row=1, col=1)
        fig.update_layout(height=580, margin=dict(t=48, b=24, l=40, r=20),
                          legend=dict(orientation="h", y=1.08),
                          title=f"심리지표 추이 · {len(hist)}일 누적")
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.caption("그래프 생략. 표로 본다.")
    if hist:
        st.dataframe(hist, hide_index=True, use_container_width=True)
