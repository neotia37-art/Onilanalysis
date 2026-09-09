# LIVE market layers v14.18 — close layer / IBD print / OAS regime
MKT_LIVE_UI_V14_12 = True
MKT_PSYCHO_V14_13 = True
MKT_PSYCHO_UI_V14_13 = True
MKT_PSYCHO_V14_17 = True
MKT_RISK_TRIO_V14_17 = True
MKT_LAYERS_V14_18 = True


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


def _mkt_live_now():
    try:
        return pd.Timestamp.now(tz="Asia/Seoul").strftime("%Y-%m-%d %H:%M KST")
    except Exception:
        return pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")


def _us_session_label():
    try:
        now = pd.Timestamp.now(tz="Asia/Seoul")
    except Exception:
        return "직전 미국 세션 종가", "close"
    hhmm = now.hour * 100 + now.minute
    wd = int(now.weekday())
    if wd >= 5:
        return "주말 · 직전 미국 세션 종가", "close"
    if 2230 <= hhmm or hhmm <= 515:
        return "미국 정규장 진행중 · 라이브 근사", "rth"
    if 1615 <= hhmm < 2230:
        return "미국 GTH · VIX만 얎은 라이브 / ETF는 종가", "gth"
    return "직전 미국 세션 종가 (한국 저녁 판정값)", "close"


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


def _yf_close_pct(tickers):
    out = {}
    try:
        import yfinance as yf
        raw = yf.download(
            tickers, period="10d", interval="1d",
            progress=False, auto_adjust=True, threads=False,
        )
    except Exception:
        return out
    if raw is None or len(raw) == 0:
        return out

    def _series(tk):
        try:
            if isinstance(raw.columns, pd.MultiIndex):
                if "Close" in raw.columns.get_level_values(0):
                    s = raw["Close"]
                    if isinstance(s, pd.DataFrame):
                        if tk in s.columns:
                            s = s[tk]
                        else:
                            s = s.iloc[:, 0]
                else:
                    s = raw.iloc[:, 0]
            else:
                s = raw["Close"] if "Close" in raw.columns else raw.iloc[:, -1]
            s = pd.to_numeric(s, errors="coerce").dropna()
            return s
        except Exception:
            return pd.Series(dtype=float)

    multi = isinstance(raw.columns, pd.MultiIndex)
    for tk in tickers:
        s = _series(tk) if (multi or len(tickers) > 1) else _series(tickers[0])
        if s is None or len(s) < 2:
            continue
        last = float(s.iloc[-1])
        prev = float(s.iloc[-2])
        out[tk] = {
            "px": last,
            "pct": (last / prev - 1.0) * 100.0 if prev else None,
            "dt": str(s.index[-1])[:10],
        }
    return out


def fetch_close_layer():
    tks = ["^VIX", "HYG", "LQD", "SPY", "IWM", "RSP"]
    got = _yf_close_pct(tks)
    vix = (got.get("^VIX") or {}).get("px")
    vix_dt = (got.get("^VIX") or {}).get("dt")
    hyg = got.get("HYG") or {}
    lqd = got.get("LQD") or {}
    spy = got.get("SPY") or {}
    iwm = got.get("IWM") or {}
    rsp = got.get("RSP") or {}
    ratio = None
    if hyg.get("px") and lqd.get("px"):
        try:
            ratio = float(hyg["px"]) / float(lqd["px"])
        except Exception:
            ratio = None
    iwm_vs = None
    rsp_vs = None
    if iwm.get("pct") is not None and spy.get("pct") is not None:
        iwm_vs = float(iwm["pct"]) - float(spy["pct"])
    if rsp.get("pct") is not None and spy.get("pct") is not None:
        rsp_vs = float(rsp["pct"]) - float(spy["pct"])
    return {
        "vix": vix, "vix_dt": vix_dt,
        "hyg_pct": hyg.get("pct"), "hyg_dt": hyg.get("dt"),
        "lqd_pct": lqd.get("pct"),
        "hyg_lqd": ratio,
        "spy_pct": spy.get("pct"), "spy_dt": spy.get("dt"),
        "iwm_pct": iwm.get("pct"), "iwm_vs_spy": iwm_vs,
        "rsp_pct": rsp.get("pct"), "rsp_vs_spy": rsp_vs,
        "ok": bool(got),
    }


def fetch_hy_oas():
    out = {"hy_oas": None, "hy_dt": None}
    try:
        import urllib.request
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=BAMLH0A0HYM2"
        with urllib.request.urlopen(url, timeout=10) as r:
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
    except Exception:
        pass
    return out


def _layer_a_flags(a):
    flags, bad, calm = [], 0, 0
    vix = a.get("vix")
    if vix is not None:
        if vix >= 20:
            flags.append("VIX %.1f 경계+" % vix); bad += 1
        elif vix < 16:
            flags.append("VIX %.1f 안일" % vix); calm += 1
        else:
            flags.append("VIX %.1f 보통" % vix)
    hp = a.get("hyg_pct")
    if hp is not None:
        if hp <= -0.60:
            flags.append("HYG %+.2f%% 신용ETF 약" % hp); bad += 1
        elif hp >= 0.40:
            flags.append("HYG %+.2f%% 신용ETF 강" % hp); calm += 1
        else:
            flags.append("HYG %+.2f%%" % hp)
    vs = a.get("iwm_vs_spy")
    rs = a.get("rsp_vs_spy")
    weak_b = 0
    if vs is not None:
        if vs <= -0.40:
            flags.append("IWM-SPY %+.2f%%p 소형 이탈" % vs); weak_b += 1
        else:
            flags.append("IWM-SPY %+.2f%%p" % vs)
    if rs is not None:
        if rs <= -0.30:
            flags.append("RSP-SPY %+.2f%%p 폭 이탈" % rs); weak_b += 1
        else:
            flags.append("RSP-SPY %+.2f%%p" % rs)
    if weak_b:
        bad += 1
    return flags, bad, calm


def _layer_b_flags(latest):
    flags, soft, hot = [], 0, 0
    pc = latest.get("put_call")
    hl = latest.get("high_low")
    if pc is not None:
        if pc < 0.70:
            flags.append("P/C %.2f 콜편중(인쇄)" % pc); hot += 1
        elif pc >= 1.00:
            flags.append("P/C %.2f 헤지(인쇄)" % pc); soft += 1
        else:
            flags.append("P/C %.2f 인쇄" % pc)
    if hl is not None:
        if hl < 0.50:
            flags.append("H/L %.2f 조정바닥 감시" % hl); soft += 1
        else:
            flags.append("H/L %.2f 인쇄" % hl)
    bulls, bears = latest.get("bulls"), latest.get("bears")
    if bulls is not None and bears is not None and bulls >= 50 and bears <= 20:
        flags.append("Bulls %.0f/Bears %.0f 군중낙관" % (bulls, bears)); hot += 1
    elif bulls is not None:
        flags.append("Bulls %.0f%%" % bulls)
    return flags, soft, hot


def combine_stance(a_bad, a_calm, b_hot, oas, pulse_dd):
    oas_tight = oas is not None and oas < 3.50
    dd = int(pulse_dd or 0)
    if a_bad >= 2 and (b_hot or oas_tight or dd >= 5):
        return "보수 · 종가층 악화 + 배경 안일/분산", "down"
    if a_bad >= 2:
        return "종가층 악화 · 추격 금지", "down"
    if dd >= 5:
        return "분산 작업 5+ · 신규 0 (배경)", "warn"
    if a_calm >= 2 and b_hot and oas_tight:
        return "3층 모두 안일 · 추격 금지", "warn"
    if a_bad == 0 and a_calm >= 1:
        return "종가층 조용 · 그래도 분산·피벗이 먼저", "warn"
    return "혼조 · 한 층만으로 사지 말 것", "neutral"


def render_market_live(ctx=None):
    ctx = ctx or (globals().get("CTX") or {})
    try:
        render_market_psycho(ctx)
    except Exception:
        pass


def render_market_layers(ctx=None):
    return render_market_psycho(ctx)


def render_market_psycho(ctx=None):
    ctx = ctx or {}
    desk, hist, latest = load_psycho_book()
    sess_lab, sess_kind = _us_session_label()
    try:
        a = fetch_close_layer()
    except Exception:
        a = {"ok": False}
    try:
        fred = fetch_hy_oas()
    except Exception:
        fred = {}
    book_oas = latest.get("hy_oas")
    live_oas = fred.get("hy_oas")
    oas = book_oas if book_oas is not None else live_oas

    pulse = {}
    try:
        lists = (desk.get("lists") if desk else None) or {}
        pulse = (lists.get("market_pulse_latest")
                 or lists.get("market_pulse_20260903") or {})
    except Exception:
        pulse = {}
    dd_n = pulse.get("dist_nasdaq") or 5

    a_flags, a_bad, a_calm = _layer_a_flags(a)
    b_flags, b_soft, b_hot = _layer_b_flags(latest)
    stance, tone = combine_stance(a_bad, a_calm, b_hot, oas, dd_n)

    st.markdown(
        '<div class="masthead"><h1>시장 3층 판정 · v14.18</h1>'
        '<div class="sub">' + sess_lab + " · " + _mkt_live_now() +
        " · A=미국 세션 종가 · B=IBD 전일 인쇄 · C=OAS 레짐</div></div>",
        unsafe_allow_html=True)
    st.caption("분 단위 폴링 없음. 한국 저녁 기본값은 막 끝난 미국 세션 종가 + 전일 인쇄 + 최신 OAS.")

    try:
        step_header("A층 · 미국 세션 종가", "VIX · HYG · IWM/RSP vs SPY",
                    "정규장 ETF·VIX. 전일 종가에 고정하지 않는다. GTH VIX는 얎음.")
    except Exception:
        st.markdown("##### A층 · 미국 세션 종가")

    def _fmt(v, kind="n"):
        if v is None:
            return "—"
        try:
            if kind == "pct":
                return "%+.2f%%" % float(v)
            if kind == "pp":
                return "%+.2f%%p" % float(v)
            if kind == "vix":
                return "%.1f" % float(v)
            return "%.3f" % float(v)
        except Exception:
            return "—"

    a_tone = "down" if a_bad >= 2 else ("warn" if a_calm >= 2 else "neutral")
    cA = st.columns(4)
    cards = [
        ("VIX 종가", _fmt(a.get("vix"), "vix"), "%s · 20+=경계 16-=안일" % (a.get("vix_dt") or "—")),
        ("HYG 종가%", _fmt(a.get("hyg_pct"), "pct"), "신용 ETF 가격. OAS가 아님. -0.6%=약"),
        ("IWM - SPY", _fmt(a.get("iwm_vs_spy"), "pp"), "IWM %s / SPY %s" % (_fmt(a.get("iwm_pct"), "pct"), _fmt(a.get("spy_pct"), "pct"))),
        ("RSP - SPY", _fmt(a.get("rsp_vs_spy"), "pp"), "동일가중 폭. -0.3%p=이탈"),
    ]
    for col, item in zip(cA, cards):
        t, v, s = item
        try:
            col.markdown(card(t, v, s, a_tone), unsafe_allow_html=True)
        except Exception:
            col.metric(t, v, s)
    st.caption("A층 " + (" · ".join(a_flags) if a_flags else "yfinance 실패 · 새로고침"))

    try:
        step_header("B층 · IBD 전일 인쇄", "P/C · High-Low · Bulls/Bears · Margin",
                    "장중 추정 금지. 인쇄본을 손으로 옮긴다.")
    except Exception:
        st.markdown("##### B층 · IBD 전일 인쇄")

    specs = [
        ("VIX 인쇄", latest.get("vix"), "IBD 칸. A층 종가와 달를 수 있음"),
        ("P/C 인쇄", latest.get("put_call"), "Cboe 장중 P/C가 아님"),
        ("High-Low 인쇄", latest.get("high_low"), "0.5 아래여야 조정바닥 감시"),
        ("Bulls / Bears", latest.get("bulls"),
         "Bulls %s%% / Bears %s%%" % (latest.get("bulls"), latest.get("bears"))),
        ("Margin YoY", latest.get("margin_yoy"), "55%가 대형 천정 경고"),
    ]
    cols = st.columns(5)
    for col, item in zip(cols, specs):
        title, val, sub = item
        shown = "—" if val is None else (
            "%.2f" % float(val) if title in ("P/C 인쇄", "High-Low 인쇄")
            else ("%.1f%%" % float(val) if title != "VIX 인쇄" else "%.1f" % float(val))
        )
        try:
            col.markdown(card(title, shown, sub, "warn"), unsafe_allow_html=True)
        except Exception:
            col.metric(title, shown, sub)
    st.caption("B층 " + (" · ".join(b_flags) if b_flags else "인쇄 숫자 없음"))

    try:
        step_header("C층 · 레짐", "HY OAS (FRED Daily Close) · 당일 경보 아님",
                    "T+1 오전에 전일 종가가 올라온다. HYG 가격과 섞지 말 것.")
    except Exception:
        st.markdown("##### C층 · 레짐")
    cC = st.columns(3)
    oas_s = "—" if oas is None else ("%.2f%%" % float(oas))
    live_s = "—" if live_oas is None else ("%.2f%%" % float(live_oas))
    ratio_s = "—" if a.get("hyg_lqd") is None else ("%.3f" % float(a["hyg_lqd"]))
    try:
        cC[0].markdown(card("HY OAS 확정", oas_s,
                            "책 %s · FRED %s %s · 3.5%% 미만=압축" % (book_oas, fred.get("hy_dt") or "—", live_s),
                            "warn" if (oas is not None and oas < 3.5) else "neutral"),
                       unsafe_allow_html=True)
        cC[1].markdown(card("HYG/LQD", ratio_s, "장중 신용 근사. OAS 대체 아님", "neutral"),
                       unsafe_allow_html=True)
        cC[2].markdown(card("3층 종합", stance,
                            "A악 %s / A안일 %s / B낙관 %s · 분산NAS %s" % (a_bad, a_calm, b_hot, dd_n),
                            tone if tone in ("up", "down", "warn") else "warn"),
                       unsafe_allow_html=True)
    except Exception:
        cC[0].metric("HY OAS", oas_s)
        cC[1].metric("HYG/LQD", ratio_s)
        cC[2].metric("종합", stance)

    with st.expander("왜 층을 나누나", expanded=False):
        st.markdown(
            "- **A층** 미국 정규장에서 계속 거래되는 값. 한국 저녁 판정은 **막 끝난 세션 종가**를 쓴다. GTH VIX는 호가가 얎다.\n"
            "- **B층** IBD 인쇄 P/C·NH-NL·자문비율·신용잔고. 전일 마감 패키지. Cboe 장중 P/C는 다른 시리즈.\n"
            "- **C층** ICE BofA HY OAS는 하루 1회 종가, FRED는 다음날 오전 게시. 당일 방아쇠가 아니다.\n"
            "- 보수 규칙: **A층이 2개 이상 악화**하거나, A가 조용해도 **분산 5 + B/C 안일**이면 신규 0."
        )

    st.markdown("**B층 수동 입력** · 같은 날짜 덮어씀. A층은 자동.")
    try:
        default_dt = pd.Timestamp(latest.get("date") or "2026-09-08").date()
    except Exception:
        default_dt = pd.Timestamp("2026-09-08").date()
    with st.form("psycho_edit_v18"):
        r1 = st.columns(3)
        in_date = r1[0].date_input("날짜", value=default_dt)
        in_src = r1[1].text_input("원전", value=str(latest.get("source") or "IBD 인쇄 수동"))
        in_note = r1[2].text_input("메모", value=str(latest.get("note") or ""))
        r2 = st.columns(4)
        in_vix = r2[0].text_input("VIX 인쇄", value="" if latest.get("vix") is None else str(latest.get("vix")))
        in_pc = r2[1].text_input("P/C 인쇄", value="" if latest.get("put_call") is None else str(latest.get("put_call")))
        in_oas = r2[2].text_input("HY OAS %", value="" if book_oas is None else str(book_oas))
        in_hl = r2[3].text_input("High-Low 인쇄", value="" if latest.get("high_low") is None else str(latest.get("high_low")))
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
            st.success("%s 저장 · 누적 %s일" % (rec["date"], len(hist)))
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
                st.warning(pick + " 삭제")
                st.rerun()
            except Exception as e:
                st.error("삭제 실패: " + str(e))

    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        xs = [_psy_date(r.get("date")) for r in hist]
        fig = make_subplots(
            rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.08,
            subplot_titles=("B층 VIX인쇄 · P/C · H/L + C층 OAS",
                            "Bulls vs Bears %", "Margin YoY %"),
        )
        fig.add_trace(go.Scatter(x=xs, y=[r.get("vix") for r in hist], name="VIX print", mode="lines+markers"), row=1, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("put_call") for r in hist], name="P/C print", mode="lines+markers"), row=1, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("high_low") for r in hist], name="H/L", mode="lines+markers"), row=1, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("hy_oas") for r in hist], name="HY OAS", mode="lines+markers"), row=1, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("bulls") for r in hist], name="Bulls %", mode="lines+markers"), row=2, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("bears") for r in hist], name="Bears %", mode="lines+markers"), row=2, col=1)
        fig.add_trace(go.Scatter(x=xs, y=[r.get("margin_yoy") for r in hist], name="Margin YoY", mode="lines+markers"), row=3, col=1)
        fig.add_hline(y=3.5, line_dash="dot", line_color="#c44", annotation_text="OAS 3.5", row=1, col=1)
        fig.add_hline(y=55, line_dash="dot", line_color="#c44", annotation_text="55%", row=3, col=1)
        fig.update_layout(height=620, margin=dict(t=48, b=24, l=40, r=20),
                          legend=dict(orientation="h", y=1.08),
                          title="B+C 추이 · %s일" % len(hist))
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.caption("그래프 생략")
    if hist:
        st.dataframe(hist, hide_index=True, use_container_width=True)

    oas_txt = "—" if oas is None else str(oas)
    st.markdown(
        '<div class="ev"><b>시장 종합 · v14.18</b> · ' + stance + "<br>"
        '<span class="m">A층 ' + str(a_bad) + "악/" + str(a_calm) + "안일 · B층 낙관 " + str(b_hot)
        + " · OAS " + oas_txt + "% · Pulse 분산 NAS " + str(dd_n)
        + " · FTD 2026-06-02 소진. A층 2악 또는 분산5+안일이면 신규 추격 0. "
        "아래 67점 탐욕은 앱 자체 점수. 3층과 섞지 말 것.</span></div>",
        unsafe_allow_html=True)
    try:
        read_box(
            "A층은 <b>종가 스냅</b>, B층은 <b>전일 인쇄</b>, C층은 <b>레짐</b>이다. "
            "HYG%와 HY OAS를 같은 칸으로 읽지 않는다.",
            "v14.18 3층 판정", "oneil")
    except Exception:
        st.caption("v14.18 · A 종가 / B 인쇄 / C OAS")
