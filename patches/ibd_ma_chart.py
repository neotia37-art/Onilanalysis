def stock_chart(dfd, weekly, binfo, market, rsl, use_weekly):
    """일봉: 21 EMA + 50 SMA + 200 SMA / 주봉: 10주 SMA + 30주 SMA."""
    src = weekly if use_weekly else dfd
    d = src.tail(160 if use_weekly else 320)
    rows = 3 if rsl is not None else 2
    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True,
                        row_heights=[.60, .18, .22] if rows == 3 else [.76, .24],
                        vertical_spacing=.035)
    fig.add_trace(go.Candlestick(x=d.index, open=d["Open"], high=d["High"], low=d["Low"],
                                 close=d["Close"], name="주가",
                                 increasing=dict(line=dict(color=P_UP), fillcolor=P_UP),
                                 decreasing=dict(line=dict(color=P_DOWN), fillcolor=P_DOWN)),
                  row=1, col=1)
    if use_weekly:
        mas = [(10, P_ACC, 1.7, "10주"), (30, P_INFO, 1.1, "30주")]
        for p, c, w, nm in mas:
            if len(src) >= p:
                fig.add_trace(go.Scatter(x=d.index, y=src["Close"].rolling(p).mean().loc[d.index],
                                         mode="lines", name=nm,
                                         line=dict(color=c, width=w)), row=1, col=1)
    else:
        ema21 = src["Close"].ewm(span=21, adjust=False).mean()
        fig.add_trace(go.Scatter(x=d.index, y=ema21.loc[d.index],
                                 mode="lines", name="21일 EMA",
                                 line=dict(color=P_ACC, width=1.7)), row=1, col=1)
        if len(src) >= 50:
            fig.add_trace(go.Scatter(x=d.index, y=src["Close"].rolling(50).mean().loc[d.index],
                                     mode="lines", name="50일",
                                     line=dict(color=P_INFO, width=1.3)), row=1, col=1)
        if len(src) >= 200:
            fig.add_trace(go.Scatter(x=d.index, y=src["Close"].rolling(200).mean().loc[d.index],
                                     mode="lines", name="200일",
                                     line=dict(color="#7A5C9E", width=1.0)), row=1, col=1)
    if binfo:
        b, pv = binfo["cur"], binfo["pivot"]
        fig.add_vrect(x0=b["start"], x1=b["end"], fillcolor="rgba(138,90,0,.06)",
                      line_width=0, row=1, col=1)
        fig.add_vline(x=b["low_date"], line=dict(color=P_INK2, width=1, dash="dot"), row=1, col=1)
        fig.add_hline(y=pv, line=dict(color=P_ACC, width=1.5),
                      annotation_text=f"피봇 {fmt(pv, market)}", annotation_position="right",
                      annotation_font=dict(color=P_ACC, size=10), row=1, col=1)
        fig.add_hrect(y0=pv, y1=pv * 1.05, fillcolor="rgba(138,90,0,.13)", line_width=0, row=1, col=1)
        fig.add_hline(y=pv * 0.92, line=dict(color=P_DOWN, width=1, dash="dot"),
                      annotation_text="-8% 손절", annotation_position="right",
                      annotation_font=dict(color=P_DOWN, size=10), row=1, col=1)
        if binfo["handle"]:
            fig.add_vrect(x0=binfo["handle"]["start"], x1=d.index[-1],
                          fillcolor="rgba(11,122,82,.07)", line_width=0, row=1, col=1)
    vma = src["Volume"].rolling(10 if use_weekly else 50).mean().loc[d.index]
    fig.add_trace(go.Bar(x=d.index, y=d["Volume"], name="거래량",
                         marker=dict(color=[P_UP if c >= o else P_DOWN
                                            for c, o in zip(d["Close"], d["Open"])], opacity=.35)),
                  row=2, col=1)
    fig.add_trace(go.Scatter(x=d.index, y=vma, mode="lines", name="거래량 평균",
                             line=dict(color=P_ACC, width=1.1)), row=2, col=1)
    if rsl is not None:
        r = rsl.loc[rsl.index.intersection(d.index)]
        fig.add_trace(go.Scatter(x=r.index, y=r.values, mode="lines", name="RS 라인(지수 대비)",
                                 line=dict(color=P_INFO, width=1.3)), row=3, col=1)
    return _layout(fig, 600 if rows == 3 else 480)
