
def apply_ibd_overlay(binfo, tk=None, desk=None):
    """IBD Stock Checkup is the gate. Chart kind=pass is not enough."""
    if not binfo:
        return binfo
    chk = _lookup_checkup(tk, desk)
    flaws = list(binfo.get("flaws") or [])
    gates = []

    def _set(kind, stage):
        rank = {"pass": 0, "idle": 1, "warn": 2, "fail": 3}
        if rank.get(kind, 0) >= rank.get(binfo.get("kind"), 0):
            binfo["kind"] = kind
            binfo["stage"] = stage

    if chk:
        smr = str(chk.get("smr") or "").upper()[:1]
        eps = _num(chk.get("eps"))
        rs = _num(chk.get("rs"))
        comp = _num(chk.get("comp"))
        vs50 = _num(chk.get("vs50"))
        off52 = _num(chk.get("off52"))
        ad = _ad_letter(chk.get("ad"))
        eps_yrs = _num(chk.get("eps_yrs"))
        eps3y = _num(chk.get("eps3y"))
        sales3y = _num(chk.get("sales3y"))

        if comp is not None and comp < 90:
            flaws.append(("IBD Composite", str(int(comp)), "90+"))
            gates.append("Comp")
            _set("fail" if comp < 80 else "warn",
                 "IBD Composite 미달 — 매수 보류")
        if eps is not None and eps < 80:
            flaws.append(("IBD EPS Rating", str(int(eps)), "80+ (90+ 선호)"))
            gates.append("EPS")
            _set("fail", "IBD EPS 80 미만 — 후보 제외")
        elif eps is not None and eps < 90:
            flaws.append(("IBD EPS Rating", str(int(eps)), "90+ 선호"))
        if rs is not None and rs < 80:
            flaws.append(("IBD RS", str(int(rs)), "80 미만 제외"))
            gates.append("RS")
            _set("fail", "IBD RS 80 미만 — 후보 제외")
        if smr in ("D", "E"):
            flaws.append(("IBD SMR", smr, "A 또는 B. D/E는 질 미달"))
            gates.append("SMR")
            _set("fail", "IBD SMR 미달 — 매수 금지")
        elif smr == "C":
            flaws.append(("IBD SMR", smr, "A 또는 B"))
            gates.append("SMR")
            _set("warn", "IBD SMR C — 질 주의")
        if ad in ("D", "D+", "E", "E+"):
            flaws.append(("IBD A/D", ad, "A 또는 B"))
            gates.append("A/D")
            _set("fail", "IBD 매집 미달 — 매수 금지")
        elif ad in ("C", "C+"):
            flaws.append(("IBD A/D", ad, "A 또는 B 선호"))
        if vs50 is not None and vs50 >= 15:
            flaws.append(("IBD 50일 이격", f"{vs50:.1f}%", "+15%면 추격"))
            gates.append("50일")
            _set("fail", "IBD 50일 +15% — 추격 금지")
        if off52 is not None and off52 >= -5 and (vs50 is not None and vs50 >= 10):
            flaws.append(("52주 고점 접근", f"{off52:.0f}%", "고점 추격 금지"))
        if eps_yrs is not None and eps_yrs <= 0:
            flaws.append(("연간 EPS 연속성장", "0년", "C 항목 3년 성장"))
            gates.append("C-연간")
            if binfo.get("kind") == "pass":
                _set("warn", "연간 EPS 성장 0년 — C 미달")
        if eps3y is not None and eps3y < 0:
            flaws.append(("3년 EPS", f"{eps3y:.0f}%", "양수 성장"))
        if sales3y is not None and sales3y < 0:
            flaws.append(("3년 매출", f"{sales3y:.1f}%", "양수 성장"))
        binfo["ibd_chk"] = {
            "comp": chk.get("comp"), "eps": chk.get("eps"), "rs": chk.get("rs"),
            "smr": chk.get("smr"), "ad": chk.get("ad"), "vs50": chk.get("vs50"),
        }
    if gates and binfo.get("kind") == "pass":
        _set("warn", "IBD Checkup 미달 — 매수 보류")
    binfo["flaws"] = flaws
    binfo["ibd_gates"] = gates
    return binfo


_buy_window_v14 = buy_window


def buy_window(states, breadth=None):
    out = _buy_window_v14(states, breadth)
    if not out:
        return out
    dd_avg = float(np.mean([s["dd_n"] for s in states.values()])) if states else 0
    sinces = [s["ftd"].get("since") for s in states.values()
              if s.get("ftd", {}).get("state") == "confirmed" and s["ftd"].get("since") is not None]
    late = bool(sinces and min(sinces) > 70)
    if dd_avg >= 3 and out["score"] >= 75:
        out["score"] = min(int(out["score"]), 68)
        out["grade"] = "선별 매수 · 분산 주의"
        out["kind"] = "warn"
    elif late and out["score"] >= 75:
        out["score"] = min(int(out["score"]), 72)
        out["grade"] = "후반 상승 · 선별"
        out["kind"] = "warn"
    return out


def sticky_bar(ctx, D, extra=""):
    if not ctx.get("ok"):
        return
    m, price = ctx["market"], ctx["price"]
    df = ctx["df"]
    chg = (price / float(df["Close"].iloc[-2]) - 1) * 100
    bw, binfo = ctx.get("bw"), ctx.get("binfo")
    cls = "up" if chg >= 0 else "down"
    parts = [f'<span class="nm">{ctx["name"].split(" (")[0]}</span>',
             f'<span class="px {cls}">{fmt(price, m)}{unit(m)} {pct(chg,2)}</span>']
    _sec2 = ctx.get("sec_hint") or ("ETF" if ctx.get("etf", {}).get("is_etf") else None)
    if m == "KR":
        _lbl = f'코스닥 · {_sec2 or "주식"}' if ctx.get("seg") == "KOSDAQ" \
            else f'코스피 · {_sec2 or "주식"}'
        parts.append('<span class="it">' +
                     tag(_lbl, "info" if _sec2 in ("ETF", "ETN") else "idle") + '</span>')
    else:
        parts.append('<span class="it">' + tag("해외 · 주식", "idle") + '</span>')
    if ctx.get("etf", {}).get("lev_inv"):
        parts.append('<span class="it">' + tag("레버리지/인버스", "fail") + '</span>')
    if bw:
        k = "up" if bw["kind"] == "pass" else ("amb" if bw["kind"] == "warn" else "down")
        g = bw["grade"]
        if binfo and binfo.get("kind") != "pass":
            g = g + " · 종목비허가"
        parts.append(f'<span class="it">시장 <b class="{k}">{bw["score"]}점 {g}</b></span>')
    if binfo:
        k = "up" if binfo["kind"] == "pass" else ("amb" if binfo["kind"] == "warn" else "down")
        lock = "잠금 " if binfo.get("locked") else ""
        parts.append(f'<span class="it">{lock}피봇 <b>{fmt(binfo["pivot"], m)}</b> '
                     f'<span class="{k}">{pct(binfo["gap"])}</span></span>')
        if binfo.get("buy_px") and abs(float(binfo["buy_px"]) - float(binfo["pivot"])) >= 0.05:
            parts.append(f'<span class="it">매수점 <b>{fmt(binfo["buy_px"], m)}</b></span>')
        if binfo.get("fake_bo"):
            parts.append('<span class="it">' + tag("가짜돌파 위험", "fail") + '</span>')
        elif binfo["kind"] == "fail":
            parts.append('<span class="it">' + tag("추격 매수 금지", "fail") + '</span>')
        if binfo.get("ibd_gates"):
            parts.append('<span class="it">' + tag("IBD " + "/".join(binfo["ibd_gates"][:3]), "fail") + '</span>')
    if D:
        parts.append(f'<span class="it">CANSLIM <b>{D["score"]}</b>/100 '
                     f'· RS <b>{ctx.get("rating") or "—"}</b></span>')
        sk = "down" if D["sp"]["score"] >= 45 else "up"
        parts.append(f'<span class="it">매도압력 <b class="{sk}">{D["sp"]["score"]}</b></span>')
    if extra:
        parts.append(f'<span class="it">{extra}</span>')
    parts.append(f'<span class="sp">{df.index[-1]:%Y-%m-%d} 종가</span>')
    st.markdown('<div class="stickybar">' + "".join(parts) + '</div>', unsafe_allow_html=True)
