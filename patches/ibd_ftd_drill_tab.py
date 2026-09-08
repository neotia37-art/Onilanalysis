# TAB 11 — FTD · 분산일 훈련 (지수 M 원전)
FTD_DRILL_TAB = True

def _ftd_index_dd(df, lookback=25):
    try:
        return stock_distribution_days(df, lookback=lookback, min_drop=0.2, expire_up=0.05)
    except Exception:
        return []

def _ftd_index_ftd(df, which="nasdaq"):
    gain = 1.7 if which == "nasdaq" else 1.25
    try:
        return detect_stock_ftd(df, min_gain=gain, corr_pct=4.0, lookback=260)
    except Exception:
        return {"state": "no_data", "date": None, "checks": []}

def _ftd_load_index(sym):
    try:
        import yfinance as yf
        df = yf.download(sym, period="18mo", interval="1d", progress=False, auto_adjust=True)
        if df is None or len(df) < 30:
            return None
        if isinstance(df.columns, tuple) or getattr(df.columns, "nlevels", 1) > 1:
            df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
        need = {"Open", "High", "Low", "Close", "Volume"}
        if not need.issubset(set(df.columns)):
            return None
        return df.dropna(subset=["Close"])
    except Exception:
        return None

def _ftd_chart(df, dds, ftd, title):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.72, 0.28], vertical_spacing=0.04)
    if df is None or len(df) < 5:
        fig.update_layout(title=title + " (no data)", height=420)
        return fig
    d = df.tail(80)
    fig.add_trace(go.Candlestick(x=d.index, open=d["Open"], high=d["High"], low=d["Low"], close=d["Close"], name="OHLC",
                                 increasing_line_color="#14803c", decreasing_line_color="#b42318"), row=1, col=1)
    fig.add_trace(go.Bar(x=d.index, y=d["Volume"], name="Vol", marker_color="#98a2b3"), row=2, col=1)
    active = [x for x in (dds or []) if not x.get("expired")]
    if active:
        fig.add_trace(go.Scatter(x=[x["date"] for x in active], y=[x["close"] for x in active], mode="markers", name="DD",
                                 marker=dict(symbol="triangle-down", size=11, color="#d92d20")), row=1, col=1)
    if ftd and ftd.get("date") is not None:
        yv = float(df.loc[ftd["date"], "Close"]) if ftd["date"] in df.index else None
        fig.add_trace(go.Scatter(x=[ftd["date"]], y=[yv], mode="markers+text", name="FTD", text=["FTD"],
                                 textposition="top center", marker=dict(symbol="star", size=14, color="#12b76a")), row=1, col=1)
    fig.update_layout(title=title, height=460, xaxis_rangeslider_visible=False, legend=dict(orientation="h"), margin=dict(t=40, b=20, l=40, r=20))
    return fig

to_top()
with TABS[11], guard("FTD훈련"):
    st.markdown('<div class="masthead"><h1>FTD · 분산일 훈련</h1><div class="sub">지수 원전 규칙. 종목 FTD는 M을 대체하지 않는다.</div></div>', unsafe_allow_html=True)
    try:
        read_box("분산일 = 지수 <b>0.2%이상 하락</b> + 거래량 <b>전일보다 많으면</b>. FTD = 조정 뒤 램리 <b>4일+</b>, 나스닥 <b>+1.7%</b> / S&P <b>+1.25%</b> + 거래량 전일비. 4~7일이 가장 강하다. 0~2 건강 · 3~4 압박 · 5+ 조정.", "IBD Learn · Big Picture", "oneil")
    except Exception:
        st.info("DD -0.2%+vol up / FTD NAS +1.7 SPX +1.25")
    gap_rows = [
        ["분산 문턱", "지수 -0.2%", "종목 -0.5%", "훈련 탭은 지수 -0.2%"],
        ["FTD 양봉", "NAS +1.7 / SPX +1.25", "종목 +1.5", "지수별 문턱"],
        ["조정", "지수 -4%", "종목 -8%", "훈련은 -4%"],
        ["거래량", "전일비면 충분", "품질만 50일", "DD는 50일 불필"],
        ["점수", "Pulse 개수", "앱 65점", "오늘 캔들을 손으로"],
        ["층위", "M=지수", "종목 FTD=힌트", "M 없으면 추격 금지"],
    ]
    try:
        st.markdown(table(["칸", "IBD", "앱", "수정"], gap_rows), unsafe_allow_html=True)
    except Exception:
        st.dataframe([{"k":a,"ibd":b,"app":c,"fix":d} for a,b,c,d in gap_rows], hide_index=True)
    desk = load_ibd_desk()
    pulse = ((desk.get("lists") or {}).get("market_pulse_20260903") or {"dist_nasdaq":4,"dist_spx":3,"ftd":"2026-06-02","exposure":"60%-80%","market_score":65})
    a,b,c,d = st.columns(4)
    a.metric("Pulse NAS DD", f"{pulse.get('dist_nasdaq','?')}")
    b.metric("Pulse SPX DD", f"{pulse.get('dist_spx','?')}")
    c.metric("recorded FTD", str(pulse.get("ftd") or "-"))
    d.metric("exposure", f"{pulse.get('exposure','-')} / {pulse.get('market_score','-')}")
    idx_map = {"NASDAQ (^IXIC)":("^IXIC","nasdaq"),"S&P 500 (^GSPC)":("^GSPC","spx"),"QQQ":("QQQ","nasdaq"),"SPY":("SPY","spx")}
    pick = st.selectbox("index", list(idx_map.keys()), index=0, key="ftd_drill_sym")
    sym, kind = idx_map[pick]
    lookback = st.slider("DD window", 15, 40, 25, key="ftd_drill_lb")
    df = _ftd_load_index(sym)
    dds = _ftd_index_dd(df, lookback=lookback) if df is not None else []
    ftd = _ftd_index_ftd(df, which=kind) if df is not None else {"state":"no_data"}
    active = [x for x in dds if not x.get("expired")]
    classic_n = len(active)
    today_dd, today_chg = False, None
    if df is not None and len(df) >= 2:
        today_chg = float(df["Close"].iloc[-1] / df["Close"].iloc[-2] - 1) * 100
        today_dd = bool(today_chg <= -0.2 and float(df["Volume"].iloc[-1]) > float(df["Volume"].iloc[-2]))
    k1,k2,k3,k4 = st.columns(4)
    k1.metric("active DD", f"{classic_n} / {lookback}")
    k2.metric("today", "DD" if today_dd else "no", None if today_chg is None else f"{today_chg:+.2f}%")
    k3.metric("auto FTD", ftd.get("date").strftime("%Y-%m-%d") if ftd.get("date") is not None else (ftd.get("state") or "-"))
    k4.metric("quality", ftd.get("quality") or "-")
    if classic_n <= 2: st.success("0-2 healthy")
    elif classic_n <= 4: st.warning("3-4 pressure, no chase")
    else: st.error("5+ campaign")
    st.plotly_chart(_ftd_chart(df, dds, ftd, f"{pick} DD red / FTD star"), use_container_width=True)
    if dds:
        show=[]
        for x in dds[-15:]:
            dt=x.get("date")
            show.append({"date": dt.strftime("%Y-%m-%d") if hasattr(dt,"strftime") else str(dt)[:10], "chg": round(float(x.get("chg") or 0),2), "close": round(float(x.get("close") or 0),2), "volx": round(float(x.get("vol_vs_prev") or 0),2), "exp": "Y" if x.get("expired") else "N"})
        st.dataframe(show, hide_index=True, use_container_width=True)
    st.markdown("### hand journal")
    journal = list(desk.get("ftd_drill") or [])
    seed = {"date": pd.Timestamp.now().strftime("%Y-%m-%d"), "index": pick, "chg_pct": None if today_chg is None else round(today_chg,2), "vol_vs_prev": "", "hand_dd": "?", "hand_ftd": "?", "active_n": classic_n, "note": ""}
    edited = st.data_editor(pd.DataFrame(journal + [seed] if not any(str(x.get("date"))==seed["date"] and str(x.get("index"))==pick for x in journal) else journal), num_rows="dynamic", key="ftd_drill_editor", use_container_width=True)
    if st.button("save journal", key="ftd_drill_save"):
        desk["ftd_drill"] = edited.to_dict("records")
        save_ibd_desk(desk)
        st.success("saved")
    for i, line in enumerate(["NAS chg?","vol > prev?","is DD?","active DD count?","rally day?","+1.7 or +1.25?","no chase without market FTD?"],1):
        st.checkbox(f"{i}. {line}", key=f"ftd_q_{i}")
