# TAB 11 FTD / DD drill (index M) v14.9
FTD_DRILL_TAB = True
FTD_DRILL_TAB_V14_9 = True

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

def _ftd_blend(price_df, vol_df):
    if price_df is None:
        return None
    out = price_df.copy()
    if vol_df is not None and "Volume" in vol_df.columns:
        aligned = vol_df["Volume"].reindex(out.index)
        if aligned.notna().sum() >= 20:
            out["Volume"] = aligned.fillna(out["Volume"])
            out["vol_is_proxy"] = True
        else:
            out["vol_is_proxy"] = False
    else:
        out["vol_is_proxy"] = False
    return out

def _ftd_rally_day(df):
    if df is None or len(df) < 15:
        return None
    d = df.tail(60)
    return len(d) - int(d["Close"].values.argmin())

def _ftd_chart(df, dds, ftd, title):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.72, 0.28], vertical_spacing=0.04)
    if df is None or len(df) < 5:
        fig.update_layout(title=title + " (no data)", height=460)
        return fig
    d = df.tail(90).copy()
    fig.add_trace(go.Candlestick(x=d.index, open=d["Open"], high=d["High"], low=d["Low"], close=d["Close"], name="OHLC",
                                 increasing_line_color="#14803c", decreasing_line_color="#b42318"), row=1, col=1)
    try:
        fig.add_trace(go.Scatter(x=d.index, y=d["Close"].rolling(50).mean(), name="50d",
                                 line=dict(color="#f79009", width=1.4)), row=1, col=1)
    except Exception:
        pass
    colors = ["#12b76a" if float(c) >= float(o) else "#d92d20" for o, c in zip(d["Open"], d["Close"])]
    fig.add_trace(go.Bar(x=d.index, y=d["Volume"], name="Vol", marker_color=colors), row=2, col=1)
    active = [x for x in (dds or []) if not x.get("expired")]
    if active:
        fig.add_trace(go.Scatter(x=[x["date"] for x in active], y=[x["close"] for x in active], mode="markers", name="DD",
                                 marker=dict(symbol="triangle-down", size=12, color="#d92d20")), row=1, col=1)
    if ftd and ftd.get("date") is not None:
        yv = float(df.loc[ftd["date"], "Close"]) if ftd["date"] in df.index else None
        fig.add_trace(go.Scatter(x=[ftd["date"]], y=[yv], mode="markers+text", name="FTD", text=["FTD"],
                                 textposition="top center", marker=dict(symbol="star", size=15, color="#12b76a")), row=1, col=1)
    fig.update_layout(title=title, height=500, xaxis_rangeslider_visible=False, legend=dict(orientation="h"), margin=dict(t=42, b=20, l=40, r=20))
    return fig

to_top()
with TABS[11], guard("FTD\ud6c8\ub828"):
    st.markdown('<div class="masthead"><h1>FTD / DD drill</h1><div class="sub">Pulse is source of truth. Auto detect is homework, not the answer.</div></div>', unsafe_allow_html=True)
    try:
        read_box("DD = index down <b>0.2%+</b> AND volume > prior day. FTD = after correction, rally day <b>4+</b>, NAS <b>+1.7%</b> / SPX <b>+1.25%</b> + volume up. Prime window 4-7. 0-2 healthy, 3-4 pressure, 5+ campaign. Yahoo index volume is not IBD exchange volume — use QQQ/SPY as proxy.", "IBD Learn / Big Picture / MARKET PULSE", "oneil")
    except Exception:
        st.info("DD -0.2%+vol up / FTD NAS +1.7 SPX +1.25")
    gap_rows = [
        ["DD gate", "index -0.2%", "stock -0.5%", "this tab uses -0.2%"],
        ["FTD bar", "NAS +1.7 / SPX +1.25", "stock +1.5", "follows index pick"],
        ["correction", "index -4%", "stock -8%", "drill uses -4%"],
        ["volume", "IBD exchange total", "Yahoo ^IXIC estimate", "price=index, vol=QQQ/SPY"],
        ["score", "Pulse DD + exposure", "app 65 banner", "count the candle"],
        ["layer", "M = index", "stock FTD = hint", "no chase if M is dead"],
    ]
    try:
        st.markdown(table(["cell", "IBD", "old app", "fix"], gap_rows), unsafe_allow_html=True)
    except Exception:
        st.dataframe([{"k":a,"ibd":b,"app":c,"fix":d} for a,b,c,d in gap_rows], hide_index=True)
    desk = load_ibd_desk()
    lists = desk.get("lists") or {}
    pulse = (lists.get("market_pulse_latest") or lists.get("market_pulse_20260903") or
             {"dist_nasdaq":4,"dist_spx":3,"ftd":"2026-06-02","exposure":"60%-80%","market_score":65,
              "headline":"Software rally, lower yields fuel broad-based gains",
              "leaders_up":["SNOW","HPE","DELL","MRX","ESTC","AYA"],"leaders_down":["VSXY","TDW"],"date":"2026-09-03"})
    a,b,c,d = st.columns(4)
    a.metric("Pulse NAS DD", f"{pulse.get('dist_nasdaq','?')}")
    b.metric("Pulse SPX DD", f"{pulse.get('dist_spx','?')}")
    c.metric("recorded FTD", str(pulse.get("ftd") or "-"))
    d.metric("exposure", f"{pulse.get('exposure','-')} / {pulse.get('market_score','-')}")
    st.caption(f"Pulse {pulse.get('date') or '-'} / {pulse.get('headline') or ''} / up {', '.join(pulse.get('leaders_up') or [])} / down {', '.join(pulse.get('leaders_down') or [])}")
    idx_map = {"NAS + QQQ vol":("^IXIC","QQQ","nasdaq"),"SPX + SPY vol":("^GSPC","SPY","spx"),"QQQ":("QQQ","QQQ","nasdaq"),"SPY":("SPY","SPY","spx")}
    pick = st.selectbox("index + volume proxy", list(idx_map.keys()), index=0, key="ftd_drill_sym")
    psym, vsym, kind = idx_map[pick]
    lookback = st.slider("DD window", 15, 40, 25, key="ftd_drill_lb")
    price_df = _ftd_load_index(psym)
    vol_df = _ftd_load_index(vsym) if vsym != psym else price_df
    df = _ftd_blend(price_df, vol_df)
    dds = _ftd_index_dd(df, lookback=lookback) if df is not None else []
    ftd = _ftd_index_ftd(df, which=kind) if df is not None else {"state":"no_data"}
    classic_n = len([x for x in dds if not x.get("expired")])
    today_dd, today_chg, vol_up = False, None, None
    if df is not None and len(df) >= 2:
        today_chg = float(df["Close"].iloc[-1] / df["Close"].iloc[-2] - 1) * 100
        vol_up = float(df["Volume"].iloc[-1]) > float(df["Volume"].iloc[-2])
        today_dd = bool(today_chg <= -0.2 and vol_up)
    rally_n = _ftd_rally_day(df)
    k1,k2,k3,k4,k5 = st.columns(5)
    k1.metric("active DD", f"{classic_n} / {lookback}")
    k2.metric("today", "DD" if today_dd else "no", None if today_chg is None else f"{today_chg:+.2f}%")
    k3.metric("vol vs prev", "up" if vol_up else ("down" if vol_up is False else "-"))
    k4.metric("auto FTD", ftd.get("date").strftime("%Y-%m-%d") if ftd.get("date") is not None else (ftd.get("state") or "-"))
    k5.metric("rally day", f"{rally_n}" if rally_n else "-")
    pulse_n = pulse.get("dist_nasdaq") if kind == "nasdaq" else pulse.get("dist_spx")
    if pulse_n is not None and classic_n != pulse_n:
        st.warning(f"auto DD {classic_n} != Pulse {pulse_n}. Volume source differs. Hand count wins.")
    if classic_n <= 2: st.success("0-2 healthy")
    elif classic_n <= 4: st.warning("3-4 pressure, no chase")
    else: st.error("5+ campaign")
    st.plotly_chart(_ftd_chart(df, dds, ftd, f"{pick} 50d / DD red / FTD star"), use_container_width=True)
    if dds:
        show=[]
        for x in dds[-15:]:
            dt=x.get("date")
            show.append({"date": dt.strftime("%Y-%m-%d") if hasattr(dt,"strftime") else str(dt)[:10], "chg": round(float(x.get("chg") or 0),2), "close": round(float(x.get("close") or 0),2), "volx": round(float(x.get("vol_vs_prev") or 0),2), "exp": "Y" if x.get("expired") else "N"})
        st.dataframe(show, hide_index=True, use_container_width=True)
    expos = ["0%-20%","20%-40%","40%-60%","60%-80%","80%-100%"]
    with st.form("ftd_pulse_form"):
        p1,p2,p3,p4 = st.columns(4)
        pdate = p1.text_input("Pulse date", value=str(pulse.get("date") or ""))
        pn = p2.number_input("NAS DD", value=int(pulse.get("dist_nasdaq") or 0), min_value=0, max_value=12)
        ps = p3.number_input("SPX DD", value=int(pulse.get("dist_spx") or 0), min_value=0, max_value=12)
        cur = pulse.get("exposure") if pulse.get("exposure") in expos else "60%-80%"
        pexp = p4.selectbox("exposure", expos, index=expos.index(cur))
        pftd = st.text_input("market FTD", value=str(pulse.get("ftd") or ""))
        pup = st.text_input("leaders up", value=",".join(pulse.get("leaders_up") or []))
        pdn = st.text_input("leaders down", value=",".join(pulse.get("leaders_down") or []))
        if st.form_submit_button("save Pulse"):
            desk.setdefault("lists", {})["market_pulse_latest"] = {
                "date": pdate, "dist_nasdaq": int(pn), "dist_spx": int(ps), "exposure": pexp, "ftd": pftd,
                "leaders_up": [x.strip().upper() for x in pup.split(",") if x.strip()],
                "leaders_down": [x.strip().upper() for x in pdn.split(",") if x.strip()],
                "source": "FTD drill manual Pulse", "headline": pulse.get("headline"), "market_score": pulse.get("market_score"),
            }
            save_ibd_desk(desk)
            st.success("Pulse saved. This cell beats auto count.")
    journal = list(desk.get("ftd_drill") or [])
    seed = {"date": pd.Timestamp.now().strftime("%Y-%m-%d"), "index": pick,
            "chg_pct": None if today_chg is None else round(today_chg,2),
            "vol_vs_prev": "up" if vol_up else ("down" if vol_up is False else ""),
            "hand_dd": "?", "hand_ftd": "?", "active_n": classic_n, "pulse_n": pulse_n, "rally_day": rally_n, "note": ""}
    have = any(str(x.get("date"))==seed["date"] and str(x.get("index"))==pick for x in journal)
    edited = st.data_editor(pd.DataFrame(journal if have else journal+[seed]), num_rows="dynamic", key="ftd_drill_editor", use_container_width=True)
    if st.button("save journal", key="ftd_drill_save"):
        desk["ftd_drill"] = edited.to_dict("records")
        save_ibd_desk(desk)
        st.success("saved")
    for i, line in enumerate(["NAS close chg?","exchange volume > prior?","is DD?","active DD vs Pulse?","rally day from low?","+1.7 or +1.25 today?","no chase without market FTD?"],1):
        st.checkbox(f"{i}. {line}", key=f"ftd_q_{i}")
