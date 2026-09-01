def stock_ftd_dd_review(df, market_states=None):
    ftd = detect_stock_ftd(df)
    dd_stock = stock_distribution_days(df, min_drop=0.5)
    dd_classic = stock_distribution_days(df, min_drop=0.2)
    active_s = [x for x in dd_stock if not x.get("expired")]
    active_c = [x for x in dd_classic if not x.get("expired")]
    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) >= 2 else last
    chg = float(last["Close"] / prev["Close"] - 1) * 100 if float(prev["Close"]) else 0.0
    vol_up = float(last["Volume"]) > float(prev["Volume"]) if not pd.isna(last["Volume"]) else False
    today_dd = bool(chg <= -0.5 and vol_up)
    today_ftd = bool(ftd.get("date") is not None and ftd["date"] == df.index[-1])
    last10 = set(df.index[-10:])
    cluster = sum(1 for x in active_s if x["date"] in last10)
    n = len(active_s)
    if n >= 5:
        dd_label, dd_kind, dd_why = "분산 캠페인", "fail", f"유효 분산일 {n}개 · 10일 클러스터 {cluster}개"
    elif n >= 3:
        dd_label, dd_kind, dd_why = "상승세 압박", "warn", f"유효 분산일 {n}개 · 10일 클러스터 {cluster}개"
    else:
        dd_label, dd_kind, dd_why = "분산 관리", "pass", f"유효 분산일 {n}개 (정상 차익실현 범위)"
    stt = ftd.get("state")
    if stt == "confirmed":
        f_label, f_kind = "종목 FTD 유효", "pass"
    elif stt == "failed":
        f_label, f_kind = "종목 FTD 무효", "fail"
    elif stt == "rally_attempt":
        f_label, f_kind = "종목 램리 시도", "warn"
    else:
        f_label, f_kind = "조정 없음 (FTD 대기 국면 아님)", "idle"
    mkt = {"label": "시장 데이터 없음", "kind": "idle", "ok": None}
    if market_states:
        kinds = [s.get("kind") for s in market_states.values()]
        if kinds.count("fail") >= 2:
            mkt = {"label": "시장 조정 — 종목 FTD로 추격 금지", "kind": "fail", "ok": False}
        elif any(s.get("ftd", {}).get("state") in ("confirmed", "no_correction") for s in market_states.values()):
            mkt = {"label": "시장 FTD/상승 유효 — 종목 신호를 볼 환경", "kind": "pass", "ok": True}
        else:
            mkt = {"label": "시장 램리 미확인 — 종목 FTD는 참고만", "kind": "warn", "ok": False}
    if today_dd and n >= 3:
        act, act_k = "오늘이 분산일 + 누적 압박 — 추가 금지, 방어선 재확인", "fail"
    elif today_ftd and mkt.get("ok") is False:
        act, act_k = "종목 FTD는 떠으나 시장(M)이 확인되지 않음 — 추격 금지", "warn"
    elif today_ftd and ftd.get("quality") == "prime" and n <= 2:
        act, act_k = "품질 좋은 종목 FTD — 피벗 근처일 때만 관찰 시작", "pass"
    elif stt == "failed":
        act, act_k = "종목 FTD 실패(저점 이탈) — 새 저점부터 다시 센다", "fail"
    elif n >= 5:
        act, act_k = "분산 5개+ — 보유는 보호, 신규·추가는 없다", "fail"
    else:
        act, act_k = "관찰 유지 — 시장 FTD와 피벗을 함께 본다", "idle"
    return {"ftd": ftd, "dd_stock": dd_stock, "dd_classic": dd_classic,
            "active_n": n, "classic_n": len(active_c), "cluster10": cluster,
            "today_dd": today_dd, "today_ftd": today_ftd, "today_chg": chg,
            "dd_label": dd_label, "dd_kind": dd_kind, "dd_why": dd_why,
            "f_label": f_label, "f_kind": f_kind, "mkt": mkt, "act": act, "act_k": act_k}


def stock_ftd_chart(df, review):
    d = df.tail(180)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[.74, .26], vertical_spacing=.04)
    fig.add_trace(go.Scatter(x=d.index, y=d["Close"], mode="lines", name="종가",
                             line=dict(color=P_INK, width=1.6)), row=1, col=1)
    ftd = review["ftd"]
    active = [x for x in review["dd_stock"] if not x.get("expired") and x["date"] in d.index]
    expired = [x for x in review["dd_stock"] if x.get("expired") and x["date"] in d.index]
    if expired:
        fig.add_trace(go.Scatter(x=[x["date"] for x in expired], y=[d.loc[x["date"], "Close"] for x in expired],
                                 mode="markers", name="만료 분산일",
                                 marker=dict(color="#C8C2B8", size=7, symbol="triangle-down")), row=1, col=1)
    if active:
        fig.add_trace(go.Scatter(x=[x["date"] for x in active], y=[d.loc[x["date"], "Close"] for x in active],
                                 mode="markers", name="유효 분산일",
                                 marker=dict(color=P_DOWN, size=9, symbol="triangle-down")), row=1, col=1)
    if ftd.get("date") is not None and ftd["date"] in d.index:
        fig.add_trace(go.Scatter(x=[ftd["date"]], y=[d.loc[ftd["date"], "Close"]],
                                 mode="markers+text", name="종목 FTD", text=["FTD"],
                                 textposition="top center", textfont=dict(color=P_UP, size=11),
                                 marker=dict(color=P_UP, size=13, symbol="star")), row=1, col=1)
    if ftd.get("low_date") is not None and ftd["low_date"] in d.index:
        fig.add_vline(x=ftd["low_date"], line=dict(color=P_INK2, width=1, dash="dash"), row=1, col=1)
    if not d["Volume"].isna().all():
        colors = [P_DOWN if any(x["date"] == dt for x in active) else (P_UP if ftd.get("date") == dt else "#D5D0C6") for dt in d.index]
        fig.add_trace(go.Bar(x=d.index, y=d["Volume"], name="거래량", marker=dict(color=colors)), row=2, col=1)
    return _layout(fig, 340)
