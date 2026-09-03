# v14.4 book compact seed
BOOK_REV = 5

def _dot_comp(v):
    try:
        n = float(v)
    except Exception:
        return "none"
    if n >= 90:
        return "green"
    if n >= 80:
        return "yellow"
    return "red"

def _dot_rs(v):
    try:
        n = float(v)
    except Exception:
        return "none"
    if n >= 80:
        return "green"
    if n >= 70:
        return "yellow"
    return "red"

def _dot_letter(v, good="AB", mid="C"):
    s = str(v or "").upper().replace("+", "").replace("-", "")
    if not s:
        return "none"
    if s[0] in good or s[0] in mid:
        return "green"
    if s[0] == "D":
        return "yellow"
    return "red"

def _dot_pct(v, g=25, y=0):
    try:
        n = float(str(v).replace("%", ""))
    except Exception:
        return "none"
    if n >= g:
        return "green"
    if n >= y:
        return "yellow"
    return "red"

def _dot_off52(v):
    try:
        n = float(v)
    except Exception:
        return "none"
    if n >= -15:
        return "green"
    if n >= -25:
        return "yellow"
    return "red"

def _dot_ud(v):
    try:
        n = float(v)
    except Exception:
        return "none"
    if n >= 1.2:
        return "green"
    if n >= 1.0:
        return "yellow"
    return "red"

def _dot_de(v):
    try:
        n = float(v)
    except Exception:
        return "none"
    return "red" if n >= 100 else "green"

def checkup_items_from(rec):
    g = rec.get
    def S(k, d=""):
        v = g(k)
        return d if v is None or v == "" else str(v)
    rows = [
        ("IBD Stock Checklist", "Composite Rating", S("comp"), _dot_comp(g("comp"))),
        ("General Market", "Stock Market Exposure", S("exposure"), "yellow" if g("exposure") else "none"),
        ("Industry Group", "Industry Group Rank (1 to 145)", S("group_rank"), "none"),
        ("Industry Group", "Group RS Rating", S("group_rs"), _dot_letter(g("group_rs"))),
        ("Current Earnings", "EPS Due Date", S("due"), "none"),
        ("Current Earnings", "EPS Rating", S("eps"), _dot_rs(g("eps"))),
        ("Current Earnings", "EPS % Chg (Last Qtr)", (S("eps_q")+"%") if S("eps_q") else "", _dot_pct(g("eps_q"), 25, 0)),
        ("Current Earnings", "Last 3 Qtrs Avg EPS Growth", (S("eps3")+"%") if S("eps3") else "", _dot_pct(g("eps3"), 25, 0)),
        ("Current Earnings", "# Qtrs of EPS Acceleration", S("accel"), "green" if str(g("accel") or "0") not in ("", "0") else "yellow"),
        ("Current Earnings", "EPS Est % Chg (Current Qtr)", (S("eps_est_q")+"%") if S("eps_est_q") else "", _dot_pct(g("eps_est_q"), 20, 0)),
        ("Current Earnings", "Estimate Revisions", S("est_rev"), "none"),
        ("Current Earnings", "Last Quarter % Earnings Surprise", (S("surprise")+"%") if S("surprise") else "", _dot_pct(g("surprise"), 0, -5)),
        ("Annual Earnings", "3 Yr EPS Growth Rate", (S("eps3y")+"%") if S("eps3y") else "", _dot_pct(g("eps3y"), 25, 15)),
        ("Annual Earnings", "Consecutive Yrs of Annual EPS Growth", S("eps_yrs"), "green" if str(g("eps_yrs") or "0") not in ("", "0") else "yellow"),
        ("Annual Earnings", "EPS Est % Chg for Current Year", (S("eps_est_y")+"%") if S("eps_est_y") else "", _dot_pct(g("eps_est_y"), 20, 0)),
        ("Sales, Margin, ROE", "SMR Rating", S("smr"), _dot_letter(g("smr"))),
        ("Sales, Margin, ROE", "Sales % Chg (Last Qtr)", (S("sales_q")+"%") if S("sales_q") else "", _dot_pct(g("sales_q"), 25, 10)),
        ("Sales, Margin, ROE", "3 Yr Sales Growth Rate", (S("sales3y")+"%") if S("sales3y") else "", _dot_pct(g("sales3y"), 25, 20)),
        ("Sales, Margin, ROE", "Annual Pre-Tax Margin", (S("ptm")+"%") if S("ptm") else "", _dot_pct(g("ptm"), 18, 8)),
        ("Sales, Margin, ROE", "Annual ROE", (S("roe")+"%") if S("roe") else "", _dot_pct(g("roe"), 17, 10)),
        ("Sales, Margin, ROE", "Debt/Equity Ratio", (S("debt")+"%") if S("debt") else "", _dot_de(g("debt"))),
        ("Price And Volume", "Price", ("$"+S("price")) if S("price") else "", "green"),
        ("Price And Volume", "RS Rating", S("rs"), _dot_rs(g("rs"))),
        ("Price And Volume", "% Off 52 Week High", (S("off52")+"%") if S("off52") else "", _dot_off52(g("off52"))),
        ("Price And Volume", "Price vs. 50-Day Moving Average", (S("vs50")+"%") if S("vs50") else "", "yellow"),
        ("Price And Volume", "50-Day Average Volume", S("vol50"), "green" if S("vol50") else "none"),
        ("Supply And Demand", "Market Capitalization", ("$"+S("mcap")) if S("mcap") else "", "green" if S("mcap") else "none"),
        ("Supply And Demand", "Accumulation/Distribution Rating", S("ad"), _dot_letter(g("ad"), good="ABC", mid="")),
        ("Supply And Demand", "Up/Down Volume", S("ud"), _dot_ud(g("ud"))),
        ("Supply And Demand", "% Change In Funds Owning Stock", (S("funds_chg")+"%") if S("funds_chg") not in ("",) else "", _dot_pct(g("funds_chg"), 8, 0)),
        ("Supply And Demand", "Qtrs Of Increasing Fund Ownership", S("funds_up_q"), "green" if str(g("funds_up_q") or "0") not in ("", "0") else "yellow"),
    ]
    return [{"sec": a, "label": b, "value": c, "color": d} for a, b, c, d in rows]

def _C(**kw):
    kw = dict(kw)
    kw.setdefault("date", "2026-09-02")
    kw.setdefault("source", "20260903 Stock Checkup PDF")
    kw.setdefault("ingest", "2026-09-03")
    kw.setdefault("full", True)
    kw.setdefault("rev", BOOK_REV)
    kw.setdefault("comp_color", _dot_comp(kw.get("comp")))
    kw["items"] = checkup_items_from(kw)
    kw.setdefault("body", f'Comp {kw.get("comp")} EPS {kw.get("eps")} RS {kw.get("rs")} SMR {kw.get("smr")} A/D {kw.get("ad")} funds {kw.get("funds_chg")}% {kw.get("funds_up_q")}q')
    return kw

CHECKUP_BOOK_20260902 = [
    _C(ticker="AMZN", name="Amazon.com", group="RETAIL-INTERNET", comp=83, eps=99, rs=56, smr="A", ad="E", price=254.98, off52=-11, vs50=0.85, eps_q=242, surprise=215.36, funds_chg=2, funds_up_q=8, ud=1.19, inst_note="funduc6d0 8분기. A/D E RS 56"),
    _C(ticker="ANET", name="Arista Networks", group="COMPUTER-NETWORKING", group_rank=1, comp=96, eps=96, rs=85, smr="A", ad="D", price=186.10, off52=-13, vs50=2.38, eps_q=40, surprise=15.14, funds_chg=4, funds_up_q=8, ud=1.19, inst_note="그룹 1위. 펀드 8분기"),
    _C(ticker="CRWD", name="CrowdStrike Holdings", group="COMPUTER SFTWR-SECURITY", comp=95, eps=94, rs=86, smr="C", ad="C", price=203.42, off52=-13, vs50=2.22, eps_q=33, surprise=6.33, funds_chg=8, funds_up_q=1, ud=1.06, inst_note="펀드 +8% 1분기"),
    _C(ticker="DINO", name="HF Sinclair", group="OIL&GAS-REFINING/MKTG", comp=99, eps=80, rs=98, smr="C", ad="A+", price=106.06, off52=2, vs50=22.31, eps_q=212, surprise=18.26, funds_chg=5, funds_up_q=1, ud=1.75, inst_note="A/D A+ 신고가권"),
    _C(ticker="ERO", name="Ero Copper", group="MINING-METAL ORES", exposure="40%-60%", comp=98, eps=99, rs=83, smr="A", ad="B-", price=34.76, off52=-15, vs50=15.33, eps_q=80, surprise=12.69, funds_chg=0, funds_up_q=0, ud=0.96, inst_note="펀드 증가 없음"),
    _C(ticker="ETON", name="Eton Pharmaceuticals", group="MEDICAL-DEVELOPMENT BIOTECH", comp=98, eps=82, rs=99, smr="B", ad="B", price=61.96, off52=-7, vs50=32.53, eps_q=530, surprise=126.55, funds_chg=25, funds_up_q=1, ud=2.01, inst_note="펀드 +25% 신규/대규모"),
    _C(ticker="GOOG", name="Alphabet Cl C", group="INTERNET-CONTENT", comp=69, eps=99, rs=51, smr="A", ad="E", price=333.78, off52=-17, vs50=-3.75, eps_q=294, surprise=216.66, funds_chg=1, funds_up_q=8, ud=0.64, inst_note="8분기 +1% A/D E"),
    _C(ticker="HALO", name="Halozyme Therapeutics", group="MEDICAL-PROFITABLE BIOTECH", comp=99, eps=94, rs=96, smr="A", ad="A+", price=109.66, off52=0, vs50=23.04, eps_q=48, surprise=27.58, funds_chg=0, funds_up_q=1, ud=1.68, inst_note="A/D A+ 신고가"),
    _C(ticker="META", name="Meta Platforms", group="INTERNET-CONTENT", comp=63, eps=84, rs=31, smr="A", ad="C", price=592.85, off52=-25, vs50=-0.02, eps_q=-13, surprise=-14.02, funds_chg=0, funds_up_q=0, ud=1.2, inst_note="펀드 증가 없음 EPS -13%"),
    _C(ticker="MSFT", name="Microsoft", group="COMP SFTWR-ENTERPRISE", exposure="40%-60%", comp=97, eps=93, rs=60, smr="A", ad="A+", price=496.82, off52=-10, vs50=13.34, eps_q=30, surprise=11.81, funds_chg=0, funds_up_q=0, ud=2.0, inst_note="A/D A+ UD 2.0"),
    _C(ticker="MU", name="Micron Technology", group="COMPUTER-HARDWARE/PERIP", comp=89, eps=84, rs=81, smr="A", ad="E", price=956.08, off52=-24, vs50=1.28, eps_q=1215, surprise=20.36, funds_chg=15, funds_up_q=5, ud=0.75, inst_note="펀드 +15% 5분기 A/D E"),
    _C(ticker="OMDA", name="Omada Health", group="MEDICAL-SERVICES", comp=71, eps=49, rs=85, smr="C", ad="E", price=23.31, off52=-13, vs50=3.53, eps_q=134, surprise=33.10, funds_chg=4, funds_up_q=4, ud=1.75, inst_note="펀드 4분기 Comp 71"),
    _C(ticker="SKWD", name="Skyward Specialty Ins", group="INSURANCE", comp=95, eps=96, rs=84, smr="A", ad="D", price=56.32, off52=-14, vs50=-5.21, eps_q=46, surprise=10.67, funds_chg=4, funds_up_q=1, ud=1.36, inst_note="50일 -5% A/D D"),
    _C(ticker="SNDK", name="Sandisk", group="COMPUTER-HARDWARE/PERIP", comp=83, eps=85, rs=78, smr="B", ad="E", price=1553.40, off52=-34, vs50=-1.02, eps_q=13434, surprise=12.26, funds_chg=39, funds_up_q=3, ud=0.79, inst_note="펀드 +39% 3분기 최우선"),
    _C(ticker="TSM", name="Taiwan Semiconductor ADR", group="ELEC-SEMICONDUCTOR MFG", comp=85, eps=98, rs=66, smr="A", ad="E", price=415.50, off52=-13, vs50=-1.31, eps_q=62, surprise=10.78, funds_chg=4, funds_up_q=8, ud=0.66, inst_note="펀드 8분기 A/D E"),
    _C(ticker="VLO", name="Valero Energy", group="OIL&GAS-REFINING/MKTG", comp=99, eps=85, rs=98, smr="C", ad="A+", price=366.09, off52=0, vs50=18.04, eps_q=450, surprise=24.05, funds_chg=7, funds_up_q=4, ud=1.56, inst_note="A/D A+ 펀드 4분기"),
    _C(ticker="WT", name="WisdomTree Inc.", group="FINANCE-INVESTMENT MGMT", group_rank=57, group_rs="B", exposure="40%-60%", comp=98, eps=99, rs=95, smr="A", ad="C", price=23.74, off52=-8, vs50=14.06, eps_q=72, surprise=17.30, sales_q=57.34, funds_chg=2, funds_up_q=5, ud=1, roe=18.6, debt=195, inst_note="보유 펀드 5분기 EPS 99 RS 95 A/D C"),
]

MUTUAL_SNAPS = [
    {"date": "2026-07-17", "asof": "Thursday, July 16, 2026", "source": "20260903_DailyMutualData_20260717_26.pdf",
     "headline": "36개월 Fidelity Select Semicnd A+ / Energy A-",
     "etf": [{"etf": "SPYG", "tk": "NVDA", "w": 15.02}, {"etf": "SPYG", "tk": "MSFT", "w": 6.81}, {"etf": "SPYG", "tk": "META", "w": 5.18}, {"etf": "SPYG", "tk": "AAPL", "w": 4.93}],
     "funds": [{"name": "Fidelity Sel Semicnd", "grade36": "A+", "ytd": 51}, {"name": "Fidelity Sel Energy", "grade36": "A-", "ytd": 51}],
     "note": "7월 중순. 반도체·에너지 Select가 36개월 A권."},
    {"date": "2026-09-01", "asof": "Monday, August 31, 2026 (paper Tue Sep 1)", "source": "20260902_DailyMutualData_090126.pdf",
     "headline": "36개월 A+ Sel Technlgy / Tech Hardware / Adv Semicnd",
     "etf": [{"etf": "SPYG", "tk": "NVDA", "w": 15.02}, {"etf": "IUSG", "tk": "NVDA", "w": 14.23}, {"etf": "IUSV", "tk": "XOM", "w": 1.83}],
     "funds": [{"name": "Fidelity Sel Technlgy", "grade36": "A+", "ytd": 22, "aum": "26.4B"}, {"name": "Fidelity Sel Tech Hardware", "grade36": "A+", "ytd": 20, "aum": "3.57B"}, {"name": "Fidelity Adv Semicnd", "grade36": "A+", "ytd": 17, "aum": "3.42B"}, {"name": "Fidelity Sel Energy", "grade36": "A-", "ytd": 42, "aum": "2.46B"}],
     "sectors": [{"name": "TechHardware", "ytd": 68, "w4": 2}, {"name": "Energy", "ytd": 51, "w4": 8}, {"name": "Wireless", "ytd": 26, "w4": 3}, {"name": "BioTech", "ytd": 26, "w4": 9}, {"name": "Industrial", "ytd": 20, "w4": 0}, {"name": "Gold", "ytd": 19, "w4": 32}, {"name": "SW & ITSvc", "ytd": 6, "w4": 10}],
     "note": "9/1 지면. 하드웨어·에너지 선두. SNDK/ETON/MU 펀드 급증과 맞물림."},
]

QUALITY_FUNDS_SEED = [
    {"name": "IBD New Buys of top-performing funds", "grade36": "—", "date": "2026-08-10", "new": ["SIMO", "DELL", "CHEF"], "top10": ["SIMO", "DELL"], "cut": ["SAN"], "source": "TopBuys Aug 10"},
    {"name": "Fidelity Sel Technlgy", "grade36": "A+", "date": "2026-09-01", "ytd": 22, "new": ["NVDA", "MU", "SNDK", "TSM"], "top10": ["NVDA", "MSFT", "AAPL"], "cut": [], "source": "DailyMutual 0901"},
    {"name": "Fidelity Sel Tech Hardware", "grade36": "A+", "date": "2026-09-01", "ytd": 20, "new": ["SNDK", "DELL", "MU"], "top10": ["AAPL", "MU"], "cut": [], "source": "DailyMutual 0901"},
    {"name": "Fidelity Adv Semicnd", "grade36": "A+", "date": "2026-09-01", "ytd": 17, "new": ["TSM", "MU", "NVDA"], "top10": ["NVDA", "TSM"], "cut": [], "source": "DailyMutual 0901"},
    {"name": "Fidelity Sel Energy", "grade36": "A-", "date": "2026-09-01", "ytd": 42, "new": ["VLO", "DINO", "XOM"], "top10": ["XOM"], "cut": [], "source": "DailyMutual 0901"},
]

def upsert_mutual(desk, rec):
    rec = dict(rec)
    dt = str(rec.get("date") or "")
    rows = desk.setdefault("mutual", [])
    desk["mutual"] = [x for x in rows if str(x.get("date")) != dt] + [rec]
    save_ibd_desk(desk)
    return desk

def checkup_history(tk, desk):
    rows = list((desk.get("checkups") or {}).get(str(tk or "").upper()) or [])
    rows.sort(key=lambda x: str(x.get("date") or ""))
    return rows

def checkup_delta(rows):
    if len(rows) < 2:
        return None
    a, b = rows[-2], rows[-1]
    def n(x, k):
        try:
            return float(x.get(k))
        except Exception:
            return None
    out = {}
    for k in ("comp", "eps", "rs", "funds_chg", "funds_up_q", "off52", "vs50"):
        va, vb = n(a, k), n(b, k)
        out[k] = None if va is None or vb is None else vb - va
    out["from"] = a.get("date")
    out["to"] = b.get("date")
    return out

def ensure_book_seed(desk):
    desk.setdefault("checkups", {})
    desk.setdefault("notes", {})
    desk.setdefault("inst", [])
    desk.setdefault("mutual", [])
    desk.setdefault("funds", [])
    changed = False
    for rec in CHECKUP_BOOK_20260902:
        tk = rec["ticker"]
        rows = desk["checkups"].setdefault(tk, [])
        hit = None
        for i, x in enumerate(rows):
            if str(x.get("date")) == rec["date"]:
                hit = i
                break
        if hit is None:
            rows.append(dict(rec))
            changed = True
        else:
            old = rows[hit]
            if int(old.get("rev") or 0) < BOOK_REV or not old.get("items"):
                keep_manual = old.get("source", "").find("수동") >= 0 and int(old.get("rev") or 0) >= BOOK_REV
                if not keep_manual:
                    rows[hit] = dict(rec)
                    changed = True
        if not any(str(x.get("ticker")) == tk and str(x.get("date")) == rec["date"] for x in desk["inst"]):
            desk["inst"].append({
                "ticker": tk, "date": rec["date"],
                "funds_chg": rec.get("funds_chg"), "funds_up_q": rec.get("funds_up_q"),
                "ad": rec.get("ad"), "ud_vol": rec.get("ud") or rec.get("ud_vol"),
                "new_flag": (rec.get("funds_chg") or 0) >= 10,
                "note": rec.get("inst_note") or "",
                "source": "Stock Checkup PDF",
            })
            changed = True
    for snap in MUTUAL_SNAPS:
        if not any(str(x.get("date")) == snap["date"] for x in desk["mutual"]):
            desk["mutual"].append(dict(snap))
            changed = True
    for f in QUALITY_FUNDS_SEED:
        if not any(x.get("name") == f["name"] and str(x.get("date")) == f["date"] for x in desk["funds"]):
            desk["funds"].append(dict(f))
            changed = True
    if changed:
        save_ibd_desk(desk)
    return desk
