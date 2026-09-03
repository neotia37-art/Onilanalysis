# IBD Stock Checkup full sheet
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
        return tag("pass", "pass") + " " + ibd_dot("green")
    if c in ("yellow", "y", "warn", "amber"):
        return tag("watch", "warn") + " " + ibd_dot("yellow")
    if c in ("red", "r", "fail"):
        return tag("fail", "fail") + " " + ibd_dot("red")
    return tag("-", "idle")


def wt_checkup_full_20260902():
    items = [
        ("MKT", "Stock Market Exposure", "40%-60%", "yellow"),
        ("GRP", "Industry Group Rank (1 to 145)", "57", "yellow"),
        ("GRP", "Group RS Rating", "B", "yellow"),
        ("EPS", "EPS Due Date", "2026-10-23", "none"),
        ("EPS", "EPS Rating", "99", "green"),
        ("EPS", "EPS % Chg (Last Qtr)", "72%", "green"),
        ("EPS", "Last 3 Qtrs Avg EPS Growth", "70.5%", "green"),
        ("EPS", "# Qtrs of EPS Acceleration", "1", "green"),
        ("EPS", "EPS Est % Chg (Current Qtr)", "29.81%", "green"),
        ("EPS", "Estimate Revisions", "green-dot no value", "green"),
        ("EPS", "Last Quarter % Earnings Surprise", "17.30%", "green"),
        ("ANN", "3 Yr EPS Growth Rate", "57.0%", "green"),
        ("ANN", "Consecutive Yrs of Annual EPS Growth", "3", "green"),
        ("ANN", "EPS Est % Chg for Current Year", "38.04%", "green"),
        ("SMR", "SMR Rating", "A", "green"),
        ("SMR", "Sales % Chg (Last Qtr)", "57.34%", "green"),
        ("SMR", "3 Yr Sales Growth Rate", "22.0%", "red"),
        ("SMR", "Annual Pre-Tax Margin", "33.1%", "green"),
        ("SMR", "Annual ROE", "18.6%", "green"),
        ("SMR", "Debt/Equity Ratio", "195%", "red"),
        ("PX", "Price", "$23.74", "green"),
        ("PX", "RS Rating", "95", "green"),
        ("PX", "% Off 52 Week High", "-8%", "green"),
        ("PX", "Price vs. 50-Day Moving Average", "14.06%", "green"),
        ("PX", "50-Day Average Volume", "2.7 Mil", "green"),
        ("SUP", "Market Capitalization", "$3.7 B", "green"),
        ("SUP", "Accumulation/Distribution Rating", "C", "green"),
        ("SUP", "Up/Down Volume", "1", "yellow"),
        ("SUP", "% Change In Funds Owning Stock", "2%", "green"),
        ("SUP", "Qtrs Of Increasing Fund Ownership", "5", "green"),
    ]
    return {
        "ticker": "WT", "date": "2026-09-02", "name": "WisdomTree",
        "group": "FINANCE-INVESTMENT MGMT",
        "about": "Operates as a ETP sponsor and asset management company",
        "printed": "11:33 PM ET, Wednesday, September 02, 2026 (Market Closed)",
        "source": "IBD Stock Checkup PDF 2026-09-02",
        "comp": "98", "comp_color": "green",
        "eps": "99", "rs": "95", "smr": "A", "ad": "C",
        "price": 23.74, "off52": -8, "vs50": 14.06,
        "eps_q": 72, "surprise": 17.30, "sales_q": 57.34,
        "funds_chg": 2, "funds_up_q": 5, "ud_vol": 1.0,
        "group_rank": 57, "group_rs": "B", "exposure": "40%-60%",
        "vol50": "2.7 Mil", "mcap": "3.7B", "roe": 18.6, "debt": 195,
        "due": "2026-10-23",
        "leaders": {
            "Composite": [("1","SEIC","SEI Investments Co."),("2","VCTR","Victory Capital"),("3","WT","WisdomTree Inc."),("4","JBAXY","Julius Baer ADR"),("5","STT","State Street")],
            "Relative Strength": [("1","RFL","Rafael Holdings"),("2","BVC","BitVentures"),("3","VCTR","Victory Capital"),("4","WT","WisdomTree Inc."),("5","AAMI","Acadian")],
            "EPS Rating": [("1","WT","WisdomTree Inc."),("2","SII","Sprott"),("3","IVZ","INVESCO"),("4","AAMI","Acadian"),("5","AMG","Affiliated Managers")],
            "Acc/Dis": [("1","VTS","Vitesse Energy"),("2","CNNE","Cannae"),("3","OFS","OFS Capital"),("4","FSK","FS KKR"),("33","WT","WisdomTree")],
            "SMR Rating": [("1","BX","Blackstone"),("2","BAM","Brookfield AM"),("3","HLNE","Hamilton Lane"),("4","VCTR","Victory Capital"),("5","WT","WisdomTree")],
        },
        "items": [{"sec": a, "label": b, "value": c, "color": d} for a, b, c, d in items],
        "articles": [{"title": "A WisdomTree Covered Call Can Cultivate A Bountiful Yield", "source": "Investor's Business Daily", "when": "2026-08-04 13:43 ET"}],
        "body": "Comp 98 G / EPS 99 G / RS 95 G / SMR A G / AD C G. Exposure 40-60 Y. Group 57 RS B Y. 3y sales 22 R. DE 195 R. UD 1.0 Y. Funds +2 5q G.",
        "full": True,
    }


def ensure_wt_full_checkup(desk):
    seed = wt_checkup_full_20260902()
    desk.setdefault("checkups", {})
    rows = desk["checkups"].setdefault("WT", [])
    kept, found = [], False
    for x in rows:
        if str(x.get("date")) == seed["date"]:
            kept.append(x if (x.get("full") and x.get("items")) else seed)
            found = True
        else:
            kept.append(x)
    if not found:
        kept.append(seed)
    desk["checkups"]["WT"] = kept
    save_ibd_desk(desk)
    return desk


def render_checkup_sheet(chk):
    if not chk:
        return
    items = chk.get("items") or []
    n_g = sum(1 for x in items if str(x.get("color","")).lower() in ("green","g","pass"))
    n_y = sum(1 for x in items if str(x.get("color","")).lower() in ("yellow","y","warn","amber"))
    n_r = sum(1 for x in items if str(x.get("color","")).lower() in ("red","r","fail"))
    st.markdown(f'<div class="masthead"><h1>IBD Stock Checkup <span class="mono">{chk.get("ticker") or ""}</span></h1><div class="sub">{chk.get("name") or ""} · {chk.get("date") or ""} · {chk.get("printed") or chk.get("source") or ""}</div></div>', unsafe_allow_html=True)
    top = st.columns(4)
    top[0].markdown(card("Composite", str(chk.get("comp") or "-"), "IBD Stock Checklist" + ibd_dot(chk.get("comp_color") or "green"), "up"), unsafe_allow_html=True)
    top[1].markdown(card("G / Y / R", f"{n_g} · {n_y} · {n_r}", f'{ibd_dot("green")} {ibd_dot("yellow")} {ibd_dot("red")}', "up" if n_r == 0 else ("amb" if n_r <= 2 else "down")), unsafe_allow_html=True)
    top[2].markdown(card("Group", str(chk.get("group") or "-"), f'rank {chk.get("group_rank") or "-"} / 145 · RS {chk.get("group_rs") or "-"}', "amb"), unsafe_allow_html=True)
    top[3].markdown(card("Price", str(chk.get("price") or "-"), f'52w {chk.get("off52")}% · 50d {chk.get("vs50")}%', "up"), unsafe_allow_html=True)
    if chk.get("about"):
        st.markdown(f'<div class="hint">{chk.get("about")}</div>', unsafe_allow_html=True)
    leaders = chk.get("leaders") or {}
    if leaders:
        with st.expander("Group leaders Composite / RS / EPS / AD / SMR", expanded=False):
            cols = st.columns(min(3, max(1, len(leaders))))
            for i, (k, rows) in enumerate(leaders.items()):
                body = "".join(f'<div class="ev"><b>{a}</b> {b} · {c}</div>' for a, b, c in rows)
                cols[i % len(cols)].markdown(f'<div class="card"><div class="k">{k}</div>{body}</div>', unsafe_allow_html=True)
    if items:
        last_sec = None
        rows_html = []
        for it in items:
            sec = it.get("sec") or ""
            if sec != last_sec:
                rows_html.append(f'<tr><td colspan="3" style="background:#F3F0EA;font-family:IBM Plex Mono,monospace;font-size:.63rem;letter-spacing:.12em;text-transform:uppercase;color:#7A828B;padding:.4rem .7rem">{sec}</td></tr>')
                last_sec = sec
            rows_html.append(f'<tr><td style="padding:.38rem .7rem;border-bottom:1px solid #E2DED5">{it.get("label")}</td><td class="mono" style="padding:.38rem .7rem;border-bottom:1px solid #E2DED5;text-align:right;font-weight:600">{it.get("value")}</td><td style="padding:.38rem .7rem;border-bottom:1px solid #E2DED5;width:70px">{ibd_dot(it.get("color"))}</td></tr>')
        st.markdown('<table class="chk" style="width:100%;border-collapse:collapse;background:#fff;border:1px solid #E2DED5"><thead><tr style="background:#F3F0EA"><th style="text-align:left;padding:.45rem .7rem;font-size:.63rem;letter-spacing:.1em;text-transform:uppercase;color:#7A828B">item</th><th style="text-align:right;padding:.45rem .7rem;font-size:.63rem;letter-spacing:.1em;text-transform:uppercase;color:#7A828B">value</th><th style="padding:.45rem .7rem;font-size:.63rem;letter-spacing:.1em;text-transform:uppercase;color:#7A828B">dot</th></tr></thead><tbody>' + "".join(rows_html) + '</tbody></table>', unsafe_allow_html=True)
    for a in chk.get("articles") or []:
        st.markdown(f'<div class="ev"><b>IBD article</b> · {a.get("when") or ""}<br><span class="m">{a.get("title") or ""} · {a.get("source") or ""}</span></div>', unsafe_allow_html=True)
    if chk.get("body"):
        read_box(chk["body"], "summary")
