# IBD Stock Checkup full sheet with green/yellow/red dots
CHECKUP_REV = 3


def ibd_dot(color):
    c = str(color or "").lower()
    hex_ = {"green": "#16A34A", "g": "#16A34A", "pass": "#16A34A",
            "yellow": "#EAB308", "y": "#EAB308", "warn": "#EAB308", "amber": "#EAB308",
            "red": "#DC2626", "r": "#DC2626", "fail": "#DC2626",
            "none": "#D4D0C8", "": "#D4D0C8"}.get(c, "#D4D0C8")
    lab = {"#16A34A": "ok", "#EAB308": "watch", "#DC2626": "fail"}.get(hex_, "")
    return (f'<span title="{lab}" style="display:inline-block;width:11px;height:11px;'
            f'border-radius:50%;background:{hex_};border:1px solid rgba(0,0,0,.12);'
            f'vertical-align:middle;margin-left:.35rem"></span>')


def ibd_dot_tag(color):
    c = str(color or "").lower()
    if c in ("green", "g", "pass"):
        return tag("ok", "pass") + " " + ibd_dot("green")
    if c in ("yellow", "y", "warn", "amber"):
        return tag("watch", "warn") + " " + ibd_dot("yellow")
    if c in ("red", "r", "fail"):
        return tag("fail", "fail") + " " + ibd_dot("red")
    return tag("-", "idle")


def checkup_blank_items():
    return [
        {"sec": "IBD Stock Checklist", "label": "Composite Rating", "value": "", "color": "none"},
        {"sec": "General Market", "label": "Stock Market Exposure", "value": "", "color": "none"},
        {"sec": "Industry Group", "label": "Industry Group Rank (1 to 145)", "value": "", "color": "none"},
        {"sec": "Industry Group", "label": "Group RS Rating", "value": "", "color": "none"},
        {"sec": "Current Earnings", "label": "EPS Due Date", "value": "", "color": "none"},
        {"sec": "Current Earnings", "label": "EPS Rating", "value": "", "color": "none"},
        {"sec": "Current Earnings", "label": "EPS % Chg (Last Qtr)", "value": "", "color": "none"},
        {"sec": "Current Earnings", "label": "Last 3 Qtrs Avg EPS Growth", "value": "", "color": "none"},
        {"sec": "Current Earnings", "label": "# Qtrs of EPS Acceleration", "value": "", "color": "none"},
        {"sec": "Current Earnings", "label": "EPS Est % Chg (Current Qtr)", "value": "", "color": "none"},
        {"sec": "Current Earnings", "label": "Estimate Revisions", "value": "", "color": "none"},
        {"sec": "Current Earnings", "label": "Last Quarter % Earnings Surprise", "value": "", "color": "none"},
        {"sec": "Annual Earnings", "label": "3 Yr EPS Growth Rate", "value": "", "color": "none"},
        {"sec": "Annual Earnings", "label": "Consecutive Yrs of Annual EPS Growth", "value": "", "color": "none"},
        {"sec": "Annual Earnings", "label": "EPS Est % Chg for Current Year", "value": "", "color": "none"},
        {"sec": "Sales, Margin, ROE", "label": "SMR Rating", "value": "", "color": "none"},
        {"sec": "Sales, Margin, ROE", "label": "Sales % Chg (Last Qtr)", "value": "", "color": "none"},
        {"sec": "Sales, Margin, ROE", "label": "3 Yr Sales Growth Rate", "value": "", "color": "none"},
        {"sec": "Sales, Margin, ROE", "label": "Annual Pre-Tax Margin", "value": "", "color": "none"},
        {"sec": "Sales, Margin, ROE", "label": "Annual ROE", "value": "", "color": "none"},
        {"sec": "Sales, Margin, ROE", "label": "Debt/Equity Ratio", "value": "", "color": "none"},
        {"sec": "Price And Volume", "label": "Price", "value": "", "color": "none"},
        {"sec": "Price And Volume", "label": "RS Rating", "value": "", "color": "none"},
        {"sec": "Price And Volume", "label": "% Off 52 Week High", "value": "", "color": "none"},
        {"sec": "Price And Volume", "label": "Price vs. 50-Day Moving Average", "value": "", "color": "none"},
        {"sec": "Price And Volume", "label": "50-Day Average Volume", "value": "", "color": "none"},
        {"sec": "Supply And Demand", "label": "Market Capitalization", "value": "", "color": "none"},
        {"sec": "Supply And Demand", "label": "Accumulation/Distribution Rating", "value": "", "color": "none"},
        {"sec": "Supply And Demand", "label": "Up/Down Volume", "value": "", "color": "none"},
        {"sec": "Supply And Demand", "label": "% Change In Funds Owning Stock", "value": "", "color": "none"},
        {"sec": "Supply And Demand", "label": "Qtrs Of Increasing Fund Ownership", "value": "", "color": "none"},
    ]


def wt_checkup_full_20260902():
    items = [
        ("IBD Stock Checklist", "Composite Rating", "98", "green"),
        ("General Market", "Stock Market Exposure", "40%-60%", "yellow"),
        ("Industry Group", "Industry Group Rank (1 to 145)", "57", "yellow"),
        ("Industry Group", "Group RS Rating", "B", "yellow"),
        ("Current Earnings", "EPS Due Date", "2026-10-23", "none"),
        ("Current Earnings", "EPS Rating", "99", "green"),
        ("Current Earnings", "EPS % Chg (Last Qtr)", "72%", "green"),
        ("Current Earnings", "Last 3 Qtrs Avg EPS Growth", "70.5%", "green"),
        ("Current Earnings", "# Qtrs of EPS Acceleration", "1", "green"),
        ("Current Earnings", "EPS Est % Chg (Current Qtr)", "29.81%", "green"),
        ("Current Earnings", "Estimate Revisions", "", "green"),
        ("Current Earnings", "Last Quarter % Earnings Surprise", "17.30%", "green"),
        ("Annual Earnings", "3 Yr EPS Growth Rate", "57.0%", "green"),
        ("Annual Earnings", "Consecutive Yrs of Annual EPS Growth", "3", "green"),
        ("Annual Earnings", "EPS Est % Chg for Current Year", "38.04%", "green"),
        ("Sales, Margin, ROE", "SMR Rating", "A", "green"),
        ("Sales, Margin, ROE", "Sales % Chg (Last Qtr)", "57.34%", "green"),
        ("Sales, Margin, ROE", "3 Yr Sales Growth Rate", "22.0%", "red"),
        ("Sales, Margin, ROE", "Annual Pre-Tax Margin", "33.1%", "green"),
        ("Sales, Margin, ROE", "Annual ROE", "18.6%", "green"),
        ("Sales, Margin, ROE", "Debt/Equity Ratio", "195%", "red"),
        ("Price And Volume", "Price", "$23.74", "green"),
        ("Price And Volume", "RS Rating", "95", "green"),
        ("Price And Volume", "% Off 52 Week High", "-8%", "green"),
        ("Price And Volume", "Price vs. 50-Day Moving Average", "14.06%", "green"),
        ("Price And Volume", "50-Day Average Volume", "2.7 Mil", "green"),
        ("Supply And Demand", "Market Capitalization", "$3.7 B", "green"),
        ("Supply And Demand", "Accumulation/Distribution Rating", "C", "green"),
        ("Supply And Demand", "Up/Down Volume", "1", "yellow"),
        ("Supply And Demand", "% Change In Funds Owning Stock", "2%", "green"),
        ("Supply And Demand", "Qtrs Of Increasing Fund Ownership", "5", "green"),
    ]
    return {
        "ticker": "WT", "date": "2026-09-02", "name": "WisdomTree Inc.",
        "group": "FINANCE-INVESTMENT MGMT",
        "about": "Operates as a ETP sponsor and asset management company",
        "printed": "11:33 PM ET, Wednesday, September 02, 2026 (Market Closed)",
        "ingest": "2026-09-03",
        "source": "20260903_WT_Stock Checkup - Investors.com.pdf",
        "comp": "98", "comp_color": "green",
        "eps": "99", "rs": "95", "smr": "A", "ad": "C",
        "price": 23.74, "off52": -8, "vs50": 14.06,
        "eps_q": 72, "surprise": 17.30, "sales_q": 57.34,
        "funds_chg": 2, "funds_up_q": 5, "ud_vol": 1.0,
        "group_rank": 57, "group_rs": "B", "exposure": "40%-60%",
        "vol50": "2.7 Mil", "mcap": "3.7B", "roe": 18.6, "debt": 195,
        "due": "2026-10-23",
        "added_lists": "Added to My Stock Lists 09/02/26",
        "chart_asof": "09/02/2026 (Market Close)",
        "rev": CHECKUP_REV,
        "leaders": {
            "Composite": [("1", "SEIC", "SEI Investments Co."), ("2", "VCTR", "Victory Capital Holdings Inc. Cl A"), ("3", "WT", "WisdomTree Inc."), ("4", "JBAXY", "Julius Baer Group AG ADR"), ("5", "STT", "State Street Corp.")],
            "Relative Strength": [("1", "RFL", "Rafael Holdings Inc."), ("2", "BVC", "BitVentures Ltd."), ("3", "VCTR", "Victory Capital Holdings Inc. Cl A"), ("4", "WT", "WisdomTree Inc. (Added to My Stock Lists 09/02/26)"), ("5", "AAMI", "Acadian Asset Management Inc.")],
            "EPS Rating": [("1", "WT", "WisdomTree Inc. (Added to My Stock Lists 09/02/26)"), ("2", "SII", "Sprott Inc."), ("3", "IVZ", "INVESCO Ltd."), ("4", "AAMI", "Acadian Asset Management Inc."), ("5", "AMG", "Affiliated Managers Group Inc.")],
            "Acc/Dis": [("1", "VTS", "Vitesse Energy Inc."), ("2", "CNNE", "Cannae Holdings Inc."), ("3", "OFS", "OFS Capital Corp."), ("4", "FSK", "FS KKR Capital Corp."), ("33", "WT", "WisdomTree (Added to My Stock Lists 09/02/26)")],
            "SMR Rating": [("1", "BX", "Blackstone Inc."), ("2", "BAM", "Brookfield Asset Management Ltd. Cl A"), ("3", "HLNE", "Hamilton Lane Inc. Cl A"), ("4", "VCTR", "Victory Capital Holdings Inc. Cl A"), ("5", "WT", "WisdomTree (Added to My Stock Lists 09/02/26)")],
        },
        "items": [{"sec": a, "label": b, "value": c, "color": d} for a, b, c, d in items],
        "articles": [{"title": "A WisdomTree Covered Call Can Cultivate A Bountiful Yield", "source": "Investor's Business Daily", "when": "08/04/2026 01:43 PM ET"}],
        "body": "Comp 98 G / EPS 99 G / RS 95 G / SMR A G / AD C G. Exposure 40-60 Y. Group 57 RS B Y. 3y sales 22 R. DE 195 R. UD 1.0 Y. Funds +2 5q G. Comp #3 EPS #1 SMR #5 AD #33. Added 09/02/26.",
        "full": True,
    }


def checkup_rows_for(tk, desk):
    tk = str(tk or "").upper()
    rows = list((desk.get("checkups") or {}).get(tk) or [])
    rows.sort(key=lambda x: str(x.get("date") or ""))
    return rows


def checkup_for(tk, desk, date=None):
    rows = checkup_rows_for(tk, desk)
    if not rows:
        return None
    if date:
        hits = [x for x in rows if str(x.get("date")) == str(date)]
        return hits[-1] if hits else rows[-1]
    return rows[-1]


def upsert_checkup(desk, rec):
    rec = dict(rec)
    tk = str(rec.get("ticker") or "").upper()
    dt = str(rec.get("date") or "")
    rec["ticker"] = tk
    rec["full"] = True
    rec.setdefault("rev", CHECKUP_REV)
    rows = desk.setdefault("checkups", {}).setdefault(tk, [])
    desk["checkups"][tk] = [x for x in rows if str(x.get("date")) != dt] + [rec]
    nts = desk.setdefault("notes", {}).setdefault(tk, [])
    nts = [x for x in nts if not (str(x.get("date")) == dt and "Stock Checkup" in str(x.get("title") or ""))]
    nts.append({"date": dt, "eps": rec.get("eps"), "rs": rec.get("rs"), "smr": f'{rec.get("smr") or ""} / {rec.get("ad") or ""}'.strip(" /"), "comp": rec.get("comp"), "title": "IBD Stock Checkup", "body": rec.get("body") or ""})
    desk["notes"][tk] = nts
    try:
        inst = desk.setdefault("inst", [])
        inst = [x for x in inst if not (str(x.get("ticker")) == tk and str(x.get("date")) == dt)]
        inst.append({"ticker": tk, "date": dt, "funds_chg": rec.get("funds_chg"), "funds_up_q": rec.get("funds_up_q"), "ad": rec.get("ad"), "ud_vol": rec.get("ud_vol"), "new_flag": False, "note": rec.get("body") or "", "source": rec.get("source") or "Stock Checkup"})
        desk["inst"] = inst
    except Exception:
        pass
    save_ibd_desk(desk)
    return desk


def ensure_wt_full_checkup(desk):
    seed = wt_checkup_full_20260902()
    desk.setdefault("checkups", {})
    rows = desk["checkups"].setdefault("WT", [])
    kept, found = [], False
    for x in rows:
        if str(x.get("date")) == seed["date"]:
            old_rev = int(x.get("rev") or 0)
            kept.append(x if (x.get("full") and x.get("items") and old_rev >= CHECKUP_REV) else seed)
            found = True
        else:
            kept.append(x)
    if not found:
        kept.append(seed)
    desk["checkups"]["WT"] = kept
    nts = desk.setdefault("notes", {}).setdefault("WT", [])
    if not any(str(n.get("date")) == seed["date"] and "Stock Checkup" in str(n.get("title") or "") for n in nts):
        nts.append({"date": seed["date"], "eps": seed["eps"], "rs": seed["rs"], "smr": f'{seed["smr"]} / {seed["ad"]}', "comp": seed["comp"], "title": "IBD Stock Checkup", "body": seed["body"]})
    inst = desk.setdefault("inst", [])
    if not any(str(x.get("ticker")) == "WT" and str(x.get("date")) == seed["date"] for x in inst):
        inst.append({"ticker": "WT", "date": seed["date"], "funds_chg": 2, "funds_up_q": 5, "ad": "C", "ud_vol": 1.0, "new_flag": False, "note": seed["body"], "source": "Stock Checkup PDF"})
    save_ibd_desk(desk)
    return desk


def _leader_rows(rows):
    out = []
    for row in rows or []:
        if isinstance(row, (list, tuple)) and len(row) >= 3:
            out.append((str(row[0]), str(row[1]), str(row[2])))
        elif isinstance(row, dict):
            out.append((str(row.get("rank") or ""), str(row.get("ticker") or ""), str(row.get("name") or "")))
    return out


def render_checkup_sheet(chk):
    if not chk:
        return
    items = chk.get("items") or []
    n_g = sum(1 for x in items if str(x.get("color", "")).lower() in ("green", "g", "pass"))
    n_y = sum(1 for x in items if str(x.get("color", "")).lower() in ("yellow", "y", "warn", "amber"))
    n_r = sum(1 for x in items if str(x.get("color", "")).lower() in ("red", "r", "fail"))
    st.markdown(f'<div class="masthead"><h1>IBD STOCK CHECKUP <span class="mono">{chk.get("ticker") or ""}</span></h1><div class="sub">{chk.get("name") or ""} · {chk.get("date") or ""} · {chk.get("printed") or chk.get("source") or ""}</div></div>', unsafe_allow_html=True)
    top = st.columns(4)
    top[0].markdown(card("Composite", str(chk.get("comp") or "-"), "IBD Stock Checklist" + ibd_dot(chk.get("comp_color") or "green"), "up"), unsafe_allow_html=True)
    top[1].markdown(card("G / Y / R", f"{n_g} · {n_y} · {n_r}", f'{ibd_dot("green")} {ibd_dot("yellow")} {ibd_dot("red")}', "up" if n_r == 0 else ("amb" if n_r <= 2 else "down")), unsafe_allow_html=True)
    top[2].markdown(card("Group", str(chk.get("group") or "-"), f'rank {chk.get("group_rank") or "-"} / 145 · RS {chk.get("group_rs") or "-"}', "amb"), unsafe_allow_html=True)
    top[3].markdown(card("Price", str(chk.get("price") or "-"), f'52w {chk.get("off52")}% · 50d {chk.get("vs50")}%', "up"), unsafe_allow_html=True)
    if chk.get("about"):
        st.markdown(f'<div class="hint">ABOUT {chk.get("ticker") or ""}: {chk.get("about")}</div>', unsafe_allow_html=True)
    extra = []
    if chk.get("added_lists"):
        extra.append(chk["added_lists"])
    if chk.get("chart_asof"):
        extra.append("chart " + str(chk["chart_asof"]))
    if chk.get("ingest"):
        extra.append("ingest " + str(chk["ingest"]))
    if extra:
        st.caption(" · ".join(extra))
    leaders = chk.get("leaders") or {}
    if leaders:
        with st.expander("RANK WITHIN GROUP · Composite / RS / EPS / Acc-Dis / SMR", expanded=True):
            cols = st.columns(min(3, max(1, len(leaders))))
            for i, (k, rows) in enumerate(leaders.items()):
                body = "".join(f'<div class="ev"><b>{a}</b> {b} · {c}</div>' for a, b, c in _leader_rows(rows))
                cols[i % len(cols)].markdown(f'<div class="card"><div class="k">{k}</div>{body}</div>', unsafe_allow_html=True)
    if items:
        last_sec = None
        rows_html = []
        for it in items:
            sec = it.get("sec") or ""
            if sec != last_sec:
                rows_html.append(f'<tr><td colspan="3" style="background:#F3F0EA;font-family:IBM Plex Mono,monospace;font-size:.63rem;letter-spacing:.12em;text-transform:uppercase;color:#7A828B;padding:.4rem .7rem">{sec}</td></tr>')
                last_sec = sec
            rows_html.append(f'<tr><td style="padding:.38rem .7rem;border-bottom:1px solid #E2DED5">{it.get("label")}</td><td class="mono" style="padding:.38rem .7rem;border-bottom:1px solid #E2DED5;text-align:right;font-weight:600">{it.get("value") or "-"}</td><td style="padding:.38rem .7rem;border-bottom:1px solid #E2DED5;width:70px">{ibd_dot(it.get("color"))}</td></tr>')
        st.markdown('<table class="chk" style="width:100%;border-collapse:collapse;background:#fff;border:1px solid #E2DED5"><thead><tr style="background:#F3F0EA"><th style="text-align:left;padding:.45rem .7rem;font-size:.63rem;letter-spacing:.1em;text-transform:uppercase;color:#7A828B">item</th><th style="text-align:right;padding:.45rem .7rem;font-size:.63rem;letter-spacing:.1em;text-transform:uppercase;color:#7A828B">value</th><th style="padding:.45rem .7rem;font-size:.63rem;letter-spacing:.1em;text-transform:uppercase;color:#7A828B">dot</th></tr></thead><tbody>' + "".join(rows_html) + '</tbody></table>', unsafe_allow_html=True)
        st.caption("green = pass · yellow = watch · red = fail · gray = no dot")
    for a in chk.get("articles") or []:
        st.markdown(f'<div class="ev"><b>IBD ARTICLES</b> · {a.get("when") or ""}<br><span class="m">{a.get("title") or ""} · {a.get("source") or ""}</span></div>', unsafe_allow_html=True)
    if chk.get("body"):
        read_box(chk["body"], "summary")
