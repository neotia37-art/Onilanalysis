# TAB 11 FTD drill v14.11 — index volume only. QQQ/SPY is reference, never the verdict.
FTD_DRILL_TAB = True
FTD_DRILL_TAB_V14_9 = True
FTD_DRILL_TAB_V14_10 = True
FTD_DRILL_TAB_V14_11 = True

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
        if not {"Open","High","Low","Close","Volume"}.issubset(set(df.columns)):
            return None
        return df.dropna(subset=["Close"])
    except Exception:
        return None

def _ftd_vol_sane(df, kind="nasdaq"):
    if df is None or "Volume" not in df.columns or len(df) < 5:
        return False
    med = float(df["Volume"].tail(20).median())
    return med >= (1.5e9 if kind == "nasdaq" else 8e8)

def _ftd_corr_rally(df):
    if df is None or len(df) < 30:
        return None, None
    import numpy as _np
    d = df.tail(260).copy()
    dd = (d["Close"] / d["Close"].cummax() - 1) * 100
    below = (dd <= -4.0).values
    if not below.any():
        return None, None
    s = int(_np.where(below)[0][-1])
    while s > 0 and dd.values[s - 1] < -0.5:
        s -= 1
    low_pos = s + int(_np.argmin(d["Close"].values[s:]))
    return len(d) - low_pos, d.index[low_pos]

def _ftd_hand_map(desk):
    gold = ((desk or {}).get("lists") or {}).get("index_chart_read_20260907") or {}
    return dict(gold.get("hand_verdict") or {})

def _ftd_vol_rows(price_df, etf_df, lookback=25, hand_map=None, ix_ok=True):
    if price_df is None or len(price_df) < 5:
        return []
    d = price_df.tail(lookback + 1).copy()
    ev = etf_df["Volume"].reindex(d.index) if etf_df is not None and "Volume" in etf_df.columns else None
    last = float(d["Close"].iloc[-1])
    hand_map = hand_map or {}
    out = []
    for i in range(1, len(d)):
        chg = float(d["Close"].iloc[i] / d["Close"].iloc[i - 1] - 1) * 100
        ix0, ix1 = float(d["Volume"].iloc[i - 1]), float(d["Volume"].iloc[i])
        ix_x = (ix1 / ix0) if ix0 else None
        et_x = None
        if ev is not None and pd.notna(ev.iloc[i]) and pd.notna(ev.iloc[i - 1]) and float(ev.iloc[i - 1]):
            et_x = float(ev.iloc[i]) / float(ev.iloc[i - 1])
        dd_ix = bool(ix_ok and chg <= -0.2 and ix_x is not None and ix_x > 1.0)
        dd_et = bool(chg <= -0.2 and et_x is not None and et_x > 1.0)
        dt = d.index[i]
        ds = dt.strftime("%Y-%m-%d") if hasattr(dt, "strftime") else str(dt)[:10]
        hand = hand_map.get(ds)
        if hand:
            if str(hand).startswith("아님"):
                tag, dd_ix = "손표시:아님", False
            elif str(hand).startswith("후보") or str(hand).startswith("분산"):
                tag, dd_ix = "손표시:분산후보", True
            else:
                tag = "손표시:" + str(hand)
        elif not ix_ok:
            tag, dd_ix = "지수Vol신뢰낮음", False
        elif dd_ix:
            tag = "분산(지수거래량)"
        elif dd_et:
            tag = "프록시만(비원전)"
        elif chg <= -0.2:
            tag = "하락·거래량감소"
        else:
            continue
        close_i = float(d["Close"].iloc[i])
        out.append({"date": dt, "chg": chg, "close": close_i, "ix_x": ix_x, "et_x": et_x,
                    "dd_ix": dd_ix, "tag": tag, "expired": (last >= close_i * 1.05) if dd_ix else False})
    return out

def _ftd_chart(df, dds, ftd, title):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.72, 0.28], vertical_spacing=0.04)
    if df is None or len(df) < 5:
        fig.update_layout(title=title + " (no data)", height=460)
        return fig
    d = df.tail(90).copy()
    fig.add_trace(go.Candlestick(x=d.index, open=d["Open"], high=d["High"], low=d["Low"], close=d["Close"],
                                 name="OHLC", increasing_line_color="#14803c", decreasing_line_color="#b42318"), row=1, col=1)
    try:
        fig.add_trace(go.Scatter(x=d.index, y=d["Close"].rolling(50).mean(), name="50d",
                                 line=dict(color="#f79009", width=1.4)), row=1, col=1)
    except Exception:
        pass
    colors = ["#12b76a" if float(c) >= float(o) else "#d92d20" for o, c in zip(d["Open"], d["Close"])]
    fig.add_trace(go.Bar(x=d.index, y=d["Volume"], name="Vol", marker_color=colors), row=2, col=1)
    real = [x for x in (dds or []) if x.get("dd_ix") and not x.get("expired")]
    fake = [x for x in (dds or []) if "프록시" in str(x.get("tag") or "") or str(x.get("tag") or "").startswith("손표시:아님")]
    if real:
        fig.add_trace(go.Scatter(x=[x["date"] for x in real], y=[x["close"] for x in real], mode="markers",
                                 name="DD-index", marker=dict(symbol="triangle-down", size=12, color="#d92d20")), row=1, col=1)
    if fake:
        fig.add_trace(go.Scatter(x=[x["date"] for x in fake], y=[x["close"] for x in fake], mode="markers",
                                 name="proxy-reject", marker=dict(symbol="x", size=9, color="#98a2b3")), row=1, col=1)
    if ftd and ftd.get("date") is not None:
        fd = ftd["date"]
        try:
            yv = float(df.loc[fd, "Close"]) if fd in df.index else None
        except Exception:
            yv = None
        fig.add_trace(go.Scatter(x=[fd], y=[yv], mode="markers+text", name="FTD", text=["FTD"],
                                 textposition="top center", marker=dict(symbol="star", size=15, color="#12b76a")), row=1, col=1)
    fig.update_layout(title=title, height=500, xaxis_rangeslider_visible=False, legend=dict(orientation="h"),
                      margin=dict(t=42, b=20, l=40, r=20))
    return fig

to_top()
with TABS[11], guard("FTD훈련"):
    st.markdown('<div class="masthead"><h1>FTD · 분산일 훈련</h1><div class="sub">Pulse가 원전. QQQ/SPY 거래량은 판정에 쓰지 않는다.</div></div>', unsafe_allow_html=True)
    try:
        read_box("분산일 = 지수 0.2%+ 하락 + 지수(거래소) 거래량 전일비 증가. FTD = -4% 조정 후 4~7일, NAS +1.7 / SPX +1.25 + 거래량. 배너=Pulse.", "IBD Pulse · 20260907 index charts", "oneil")
    except Exception:
        st.info("DD 0.2%+index vol / FTD 1.7·1.25 / banner=Pulse")
    desk = load_ibd_desk()
    try:
        desk = ensure_book_seed(desk)
    except Exception:
        pass
    lists = desk.get("lists") or {}
    pulse = lists.get("market_pulse_latest") or lists.get("market_pulse_20260903") or {
        "dist_nasdaq": 4, "dist_spx": 3, "ftd": "2026-06-02", "exposure": "60%-80%",
        "date": "2026-09-03", "headline": "Software rally, lower yields fuel broad-based gains"}
    iread = lists.get("index_chart_read_20260907") or {}
    nas_p = iread.get("nasdaq") or {}
    a,b,c,d = st.columns(4)
    a.metric("Pulse NAS DD", f"{pulse.get('dist_nasdaq','?')}")
    b.metric("Pulse SPX DD", f"{pulse.get('dist_spx','?')}")
    c.metric("market FTD", str(pulse.get("ftd") or "-"))
    d.metric("exposure", str(pulse.get("exposure") or "-"))
    st.caption(f"Pulse {pulse.get('date')} · {pulse.get('headline') or ''}")
    if nas_p:
        st.caption(f"IBD 09/07 NAS {nas_p.get('close')} vol {nas_p.get('vol_bil')}B ({nas_p.get('vol_vs_50')}% vs 50d) · {nas_p.get('tape') or ''}")
    idx_map = {
        "NAS price + NAS vol (source)": ("^IXIC", "QQQ", "nasdaq"),
        "SPX price + SPX vol (source)": ("^GSPC", "SPY", "spx"),
        "QQQ only (do not score)": ("QQQ", "QQQ", "nasdaq"),
        "SPY only (do not score)": ("SPY", "SPY", "spx"),
    }
    pick = st.selectbox("index", list(idx_map.keys()), index=0, key="ftd_drill_sym_v11")
    psym, vsym, kind = idx_map[pick]
    lookback = st.slider("window", 15, 40, 25, key="ftd_drill_lb_v11")
    proxy_only_pick = psym in ("QQQ", "SPY")
    price_df = _ftd_load_index(psym)
    etf_df = _ftd_load_index(vsym) if vsym != psym else None
    ix_ok = (not proxy_only_pick) and _ftd_vol_sane(price_df, kind)
    hand_map = _ftd_hand_map(desk)
    rows = _ftd_vol_rows(price_df, etf_df, lookback=lookback, hand_map=hand_map, ix_ok=ix_ok)
    classic_n = len([x for x in rows if x.get("dd_ix") and not x.get("expired")])
    proxy_n = len([x for x in rows if "프록시" in str(x.get("tag") or "")])
    ftd = _ftd_index_ftd(price_df, which=kind) if price_df is not None else {"state": "no_data"}
    rally_n, _low = _ftd_corr_rally(price_df)
    last_dt = price_df.index[-1] if price_df is not None and len(price_df) else None
    last_s = last_dt.strftime("%Y-%m-%d") if last_dt is not None and hasattr(last_dt, "strftime") else "-"
    today_chg = today_dd_ix = today_dd_et = None
    if price_df is not None and len(price_df) >= 2:
        today_chg = float(price_df["Close"].iloc[-1] / price_df["Close"].iloc[-2] - 1) * 100
        ix_up = float(price_df["Volume"].iloc[-1]) > float(price_df["Volume"].iloc[-2])
        today_dd_ix = bool(ix_ok and today_chg <= -0.2 and ix_up)
        if last_s in hand_map and str(hand_map[last_s]).startswith("아님"):
            today_dd_ix = False
        if etf_df is not None and len(etf_df) >= 2:
            try:
                e1 = float(etf_df["Volume"].reindex(price_df.index).iloc[-1])
                e0 = float(etf_df["Volume"].reindex(price_df.index).iloc[-2])
                today_dd_et = bool(today_chg <= -0.2 and e1 > e0)
            except Exception:
                today_dd_et = None
    k1,k2,k3,k4,k5 = st.columns(5)
    k1.metric("index DD", f"{classic_n}/{lookback}")
    k2.metric("last session", last_s, None if today_chg is None else f"{today_chg:+.2f}%")
    k3.metric("last verdict", "DD" if today_dd_ix else ("proxy-only" if today_dd_et else "no"))
    k4.metric("auto FTD", ftd.get("date").strftime("%Y-%m-%d") if ftd.get("date") is not None else (ftd.get("state") or "-"))
    k5.metric("rally day", f"{rally_n}" if rally_n else "-")
    if proxy_only_pick:
        st.error("Do not count DD on QQQ/SPY alone.")
    if not ix_ok and not proxy_only_pick:
        st.warning("Yahoo index volume is not exchange-scale. Ignore auto count. Use Pulse.")
    pulse_n = pulse.get("dist_nasdaq") if kind == "nasdaq" else pulse.get("dist_spx")
    n_banner = pulse_n if pulse_n is not None else classic_n
    if pulse_n is not None and classic_n != pulse_n:
        st.warning(f"auto {classic_n} != Pulse {pulse_n}. proxy-only {proxy_n}. Banner follows Pulse.")
    if n_banner <= 2:
        st.success("Pulse 0-2 healthy")
    elif n_banner <= 4:
        st.warning("Pulse 3-4 pressure. no chase.")
    else:
        st.error("Pulse 5+ campaign.")
    st.plotly_chart(_ftd_chart(price_df, rows, ftd, f"{pick} last {last_s}"), use_container_width=True)
    if rows:
        show = []
        for x in rows[-18:]:
            dt = x.get("date")
            show.append({"date": dt.strftime("%Y-%m-%d") if hasattr(dt, "strftime") else str(dt)[:10],
                         "chg": round(float(x["chg"]), 2),
                         "ix_volx": None if x.get("ix_x") is None else round(float(x["ix_x"]), 2),
                         "etf_volx": None if x.get("et_x") is None else round(float(x["et_x"]), 2),
                         "tag": x.get("tag"), "exp": "Y" if x.get("expired") else "-"})
        st.dataframe(show, hide_index=True, use_container_width=True)
    st.markdown("### hand verdict calendar")
    hv = dict(hand_map)
    hv_df = pd.DataFrame([{"date": k, "verdict": v} for k, v in sorted(hv.items())] or [{"date": "", "verdict": ""}])
    hv_ed = st.data_editor(hv_df, num_rows="dynamic", key="ftd_hand_map_v11", use_container_width=True)
    if st.button("save hand verdicts", key="ftd_hand_save_v11"):
        gold = dict(lists.get("index_chart_read_20260907") or {})
        gold["hand_verdict"] = {str(r.get("date")): str(r.get("verdict")) for r in hv_ed.to_dict("records") if str(r.get("date") or "").strip()}
        desk.setdefault("lists", {})["index_chart_read_20260907"] = gold
        save_ibd_desk(desk)
        st.success("saved")
    expos = ["0%-20%", "20%-40%", "40%-60%", "60%-80%", "80%-100%"]
    with st.form("ftd_pulse_form_v11"):
        p1,p2,p3,p4 = st.columns(4)
        pdate = p1.text_input("Pulse date", value=str(pulse.get("date") or ""))
        pn = p2.number_input("NAS DD", value=int(pulse.get("dist_nasdaq") or 0), min_value=0, max_value=12)
        ps = p3.number_input("SPX DD", value=int(pulse.get("dist_spx") or 0), min_value=0, max_value=12)
        cur = pulse.get("exposure") if pulse.get("exposure") in expos else "60%-80%"
        pexp = p4.selectbox("exposure", expos, index=expos.index(cur))
        pftd = st.text_input("market FTD", value=str(pulse.get("ftd") or "2026-06-02"))
        if st.form_submit_button("save Pulse"):
            desk.setdefault("lists", {})["market_pulse_latest"] = {
                "date": pdate, "dist_nasdaq": int(pn), "dist_spx": int(ps),
                "exposure": pexp, "ftd": pftd, "source": "FTD drill Pulse",
                "headline": pulse.get("headline")}
            save_ibd_desk(desk)
            st.success("Pulse saved")
    journal = list(desk.get("ftd_drill") or [])
    seed = {"date": last_s, "index": pick,
            "chg_pct": None if today_chg is None else round(today_chg, 2),
            "hand_dd": "분산일" if today_dd_ix else "아님",
            "hand_ftd": "아님", "auto_n": classic_n, "pulse_n": pulse_n}
    have = any(str(x.get("date")) == seed["date"] and str(x.get("index")) == pick for x in journal)
    edited = st.data_editor(pd.DataFrame(journal if have else journal + [seed]), num_rows="dynamic",
                            key="ftd_drill_editor_v11", use_container_width=True)
    if st.button("save journal", key="ftd_drill_save_v11"):
        desk["ftd_drill"] = edited.to_dict("records")
        save_ibd_desk(desk)
        st.success("saved")
    for i, line in enumerate(["NAS close chg?", "exchange volume > prior (not QQQ)?", "is DD?",
                              "Pulse count?", "rally day from -4% low?", "+1.7 or +1.25 today?",
                              "no chase without market FTD?"], 1):
        st.checkbox(f"{i}. {line}", key=f"ftd_q_v11_{i}")
    st.markdown("### next charts to attach")
    st.markdown("- daily: Big Picture / Market Pulse (NAS+SPX DD count, exposure, FTD date)\n- daily close: NASDAQ Composite + S&P 500 IBD daily with volume print\n- weekly: same three indexes weekly + NYSE/NASDAQ exchange volume\n- holdings: WT and PBF daily+weekly printed the same Market Close date\n- skip: QQQ/SPY-only charts, Yahoo index volume screens, after-hours quotes")
