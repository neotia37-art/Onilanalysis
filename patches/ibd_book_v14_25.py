# v14.25 book: Pulse 2026-10-09 + AMT/CCI 10/9 Checkup + DailyPsycho 10/09 + Weekly Review 10/9
# 원전: /IBD/20261009 (MP10092026.jpg, AMT/CCI Stock Checkup·Quote PDF, DailyPsycho_100926.pdf,
#       Your Weekly Review 10/9, Big Picture 10/09 "Stock Market Pops As AI Worries Recede")
BOOK_REV_20261009 = 25
CHECKUP_BOOK_V14_25 = True
PULSE_SEED_V14_25 = True


def _C1009(**kw):
    kw = dict(kw)
    kw.setdefault("date", "2026-10-09")
    kw.setdefault("printed", "Oct 11, 2026 05:45-05:47 AM ET (10/09/2026 Market Close)")
    kw.setdefault("ingest", "2026-10-12")
    kw.setdefault("rev", BOOK_REV_20261009)
    return _C29(**kw)


CHECKUP_BOOK_20261009_ROWS = [
    _C1009(
        ticker="AMT", name="American Tower REIT",
        group="REITS", group_rank=85, group_rs="C+",
        source="20261009_AMT_Stock Checkup - Investors.com.pdf",
        exposure=None,
        comp=70, eps=39, rs=68, smr="A", ad="C",
        price=182.24, off52=-7, vs50=5.61,
        eps_q=4, eps3=7.0, surprise=0.55, sales_q=4.65,
        eps3y=3.0, accel=1, eps_yrs=2, eps_est_q=-0.30, eps_est_y=3.22,
        funds_chg=0, funds_up_q=0, ud=0.99,
        ptm=28.6, roe=71.9, debt=1122, mcap="84.9 B", vol50="2.5 M",
        due="2026-10-27",
        inst_note="Comp70 EPS39 RS68 SMR A A/D C. 10/9 +9.30% 거래량 +271% (SpaceX 스펙트럼 뉴스에 타워주 급등, 50일·200일선 위로). 그룹 REITs 85위 C+ · 그룹 내 13위. D/E 1122%. 펀드 0% / 0q. 리더 아님. 매수 아님.",
    ),
    _C1009(
        ticker="CCI", name="Crown Castle",
        group="REITS", group_rank=85, group_rs="C+",
        source="20261009_CCI_Stock Checkup - Investors.com.pdf",
        exposure="80%-100%",
        comp=42, eps=34, rs=48, smr="D", ad="C",
        price=79.64, off52=-21, vs50=8.56,
        eps_q=11, eps3=-11.4, surprise=5.72, sales_q=-4.91,
        eps3y=-20.0, accel=3, eps_yrs=1, eps_est_q=8.69, eps_est_y=5.37,
        funds_chg=0, funds_up_q=0, ud=0.88,
        ptm=26.2, roe=0.0, debt=None, mcap="33.9 B", vol50="3.3 M",
        due="2026-10-21",
        inst_note="Comp42 EPS34 RS48 SMR D A/D C. 10/9 +15.60% 거래량 +333% (SpaceX 뉴스, 50일선 돌파). off52 -21%. 3년 EPS -20%. 그룹 REITs 85위 C+ · 그룹 내 39위. 펀드 0% / 0q. 리더 아님. 매수 아님.",
    ),
]

PULSE_20261009 = {
    "date": "2026-10-09",
    "source": "MP10092026.jpg + IBD Big Picture 10/09",
    "headline": "Stocks up as biotechs, pharma plays shine",
    "exposure": "80%-100%",
    "dist_nasdaq": 2,
    "dist_spx": 8,
    "leaders_up": ["SNOW", "GCT"],
    "leaders_down": ["CRGY", "DE"],
    "ftd": "2026-06-02",
    "note": "공식 Pulse 노출 80-100 · DD NAS 2 / SPX 8. 나스닥 4주 연속 상승·10일선 지지, 다우는 50일선 아래, 러셀2000 5주 연속 하락. 신규 추격 0.",
}

PSYCHO_20261009 = {
    "date": "2026-10-09",
    "vix": 16.5,
    "put_call": 0.82,
    "high_low": None,
    "bulls": 56.9,
    "bears": 30.9,
    "margin_yoy": None,
    "source": "DailyPsycho_100926.pdf + MP10092026",
    "note": "VIX 16.5 · P/C 0.82 · 불 56.9 / 베어 30.9 (Investors Intelligence). NYSE 공매도비율 5.08. Pulse 80-100 DD NAS2/SPX8.",
}

WEEKLY_REVIEW_20261009 = [
    {"ticker":"CRWD","name":"Crowdstrike Holdings A","group_rank":1,"price":275.04},
    {"ticker":"FTNT","name":"Fortinet Inc","group_rank":1,"price":194.75},
    {"ticker":"OKTA","name":"Okta Inc Cl A","group_rank":1,"price":232.13},
    {"ticker":"QLYS","name":"Qualys Inc","group_rank":1,"price":202.42},
    {"ticker":"TENB","name":"Tenable Holdings Inc","group_rank":1,"price":41.59},
    {"ticker":"VEEV","name":"Veeva Systems Inc Cl A","group_rank":2,"price":296.13},
    {"ticker":"MPC","name":"Marathon Petroleum","group_rank":4,"price":455.03},
    {"ticker":"VLO","name":"Valero Energy Corp","group_rank":4,"price":433.75},
    {"ticker":"WKC","name":"World Kinect","group_rank":4,"price":36.41},
    {"ticker":"DCBO","name":"Docebo Inc","group_rank":5,"price":25.47},
    {"ticker":"DDOG","name":"Datadog Inc Cl A","group_rank":5,"price":293.26},
    {"ticker":"DT","name":"Dynatrace Inc","group_rank":5,"price":63.5},
    {"ticker":"FROG","name":"Jfrog Ltd","group_rank":5,"price":102.23},
    {"ticker":"MSFT","name":"Microsoft Corp","group_rank":5,"price":535.07},
    {"ticker":"NET","name":"Cloudflare Inc Cl A","group_rank":5,"price":360.93},
    {"ticker":"NTNX","name":"Nutanix Inc Class A","group_rank":5,"price":74.63},
    {"ticker":"PAYC","name":"Paycom Software Inc","group_rank":5,"price":232.22},
    {"ticker":"PD","name":"Pagerduty Inc","group_rank":5,"price":16.16},
    {"ticker":"PLTR","name":"Palantir Technologiescla","group_rank":5,"price":209.05},
    {"ticker":"RNG","name":"Ringcentral Inc Cl A","group_rank":5,"price":79.27},
    {"ticker":"SHOP","name":"Shopify Inc Cl A","group_rank":5,"price":170.85},
    {"ticker":"SNOW","name":"Snowflake Inc Cl A","group_rank":5,"price":368.89},
    {"ticker":"TEAM","name":"Atlassian Corp Plc Cl A","group_rank":5,"price":206.79},
    {"ticker":"TWLO","name":"Twilio Inc Cl A","group_rank":5,"price":289.47},
    {"ticker":"ZBRA","name":"Zebra Technologies Corp","group_rank":6,"price":387.18},
    {"ticker":"ANET","name":"Arista Networks Inc","group_rank":7,"price":216.74},
    {"ticker":"DGII","name":"Digi International Inc","group_rank":7,"price":75.63},
    {"ticker":"BWLP","name":"Bw Lpg","group_rank":8,"price":26.0},
    {"ticker":"ECO","name":"Okeanis Eco Tankers","group_rank":8,"price":93.11},
    {"ticker":"FRO","name":"Frontline Ltd","group_rank":8,"price":56.1},
    {"ticker":"NMM","name":"Navios Maritime Partners","group_rank":8,"price":93.06},
    {"ticker":"SBLK","name":"Star Bulk Carriers Corp","group_rank":8,"price":29.7},
    {"ticker":"SHIP","name":"Seanergy Maritime Hldgs","group_rank":8,"price":17.11},
    {"ticker":"STNG","name":"Scorpio Tankers Inc","group_rank":8,"price":85.14},
    {"ticker":"TK","name":"Teekay Corp","group_rank":8,"price":15.27},
    {"ticker":"TNK","name":"Teekay Tankers Ltd Cl A","group_rank":8,"price":106.14},
    {"ticker":"ILMN","name":"Illumina Inc","group_rank":10,"price":278.17},
    {"ticker":"DHT","name":"D H T Holdings Inc","group_rank":11,"price":24.64},
    {"ticker":"INSW","name":"International Seaways","group_rank":11,"price":119.82},
    {"ticker":"LPG","name":"Dorian Lpg Ltd","group_rank":11,"price":57.64},
    {"ticker":"NVGS","name":"Navigator Holdings Ltd","group_rank":11,"price":23.93},
    {"ticker":"TEN","name":"Tsakos Energy Navigation","group_rank":11,"price":51.4},
    {"ticker":"LITE","name":"Lumentum Holdings Inc","group_rank":13,"price":1103.36},
    {"ticker":"KEYS","name":"Keysight Technologies","group_rank":14,"price":382.75},
    {"ticker":"HBB","name":"Hamilton Beach Bran Cl A","group_rank":15,"price":34.76},
    {"ticker":"PAYS","name":"Paysign Inc","group_rank":18,"price":15.37},
    {"ticker":"RELY","name":"Remitly Global Inc","group_rank":18,"price":24.13},
    {"ticker":"PTC","name":"P T C Inc","group_rank":20,"price":194.45},
    {"ticker":"APH","name":"Amphenol Corp Cl A","group_rank":21,"price":87.24},
    {"ticker":"ARW","name":"Arrow Electronics Inc","group_rank":21,"price":227.9},
    {"ticker":"KN","name":"Knowles Corporation","group_rank":21,"price":37.56},
    {"ticker":"DELL","name":"Dell Technologies Cl C","group_rank":23,"price":586.06},
    {"ticker":"NTAP","name":"Netapp Inc","group_rank":23,"price":237.15},
    {"ticker":"P","name":"Everpure","group_rank":23,"price":154.49},
    {"ticker":"EQNR","name":"Equinor Asa Adr","group_rank":25,"price":43.01},
    {"ticker":"SU","name":"Suncor Energy Inc","group_rank":25,"price":72.23},
    {"ticker":"AMD","name":"Advanced Micro Devices","group_rank":27,"price":608.1},
    {"ticker":"NVDA","name":"Nvidia Corp","group_rank":27,"price":229.28},
    {"ticker":"SMTC","name":"Semtech Corporation","group_rank":27,"price":187.3},
    {"ticker":"ADI","name":"Analog Devices Inc","group_rank":28,"price":406.19},
    {"ticker":"ASX","name":"A S E Technology Hlg Ads","group_rank":28,"price":46.43},
    {"ticker":"ROG","name":"Rogers Corp","group_rank":28,"price":147.41},
    {"ticker":"TSM","name":"Taiwan Semiconductor Adr","group_rank":28,"price":453.31},
    {"ticker":"ASML","name":"A S M L Holding N.V. Ny","group_rank":29,"price":1780.34},
    {"ticker":"FORM","name":"Formfactor Inc","group_rank":29,"price":139.67},
    {"ticker":"THC","name":"Tenet Healthcare Corp","group_rank":30,"price":263.78},
    {"ticker":"RDVT","name":"Red Violet Inc","group_rank":32,"price":79.78},
    {"ticker":"TAL","name":"T A L Education Gp A Ads","group_rank":35,"price":12.86},
    {"ticker":"CNXN","name":"P C Connection Inc","group_rank":38,"price":92.81},
    {"ticker":"GCT","name":"Gigacloud Technology Cla","group_rank":38,"price":57.26},
    {"ticker":"HPE","name":"Hewlett Packard Ent Co","group_rank":38,"price":73.46},
    {"ticker":"NSIT","name":"Insight Enterprises Inc","group_rank":38,"price":163.61},
    {"ticker":"SNX","name":"T D Synnex","group_rank":38,"price":273.37},
    {"ticker":"DDI","name":"Doubledown Interactv Ads","group_rank":39,"price":13.65},
    {"ticker":"JCI","name":"Johnson Controls Intl","group_rank":43,"price":157.44},
    {"ticker":"MLAB","name":"Mesa Laboratories","group_rank":45,"price":127.51},
    {"ticker":"EXEL","name":"Exelixis Inc","group_rank":46,"price":59.86},
    {"ticker":"HALO","name":"Halozyme Therapeutics","group_rank":46,"price":110.42},
    {"ticker":"INFU","name":"Infusystem Holdings Inc","group_rank":48,"price":13.56},
    {"ticker":"NHC","name":"National Healthcare Corp","group_rank":48,"price":227.11},
    {"ticker":"CRVL","name":"Corvel Corp","group_rank":49,"price":77.16},
    {"ticker":"WAB","name":"Wabtec Corp","group_rank":54,"price":285.43},
    {"ticker":"FFIV","name":"F 5 Inc","group_rank":56,"price":479.83},
    {"ticker":"HSTM","name":"Healthstream Inc","group_rank":58,"price":33.13},
    {"ticker":"ERO","name":"Ero Copper Corp","group_rank":60,"price":37.61},
    {"ticker":"FCX","name":"Freeport Mcmoran Inc","group_rank":60,"price":73.69},
    {"ticker":"SCCO","name":"Southern Copper Corp","group_rank":60,"price":209.21},
    {"ticker":"TECK","name":"Teck Resources Ltd","group_rank":60,"price":68.05},
    {"ticker":"JXN","name":"Jackson Financial Cl A","group_rank":69,"price":129.71},
    {"ticker":"RGA","name":"Reinsurance Grp Of Amer","group_rank":69,"price":255.98},
    {"ticker":"SAFT","name":"Safety Insurance Group","group_rank":69,"price":103.82},
    {"ticker":"TRV","name":"Travelers Companies Inc","group_rank":69,"price":368.75},
    {"ticker":"UVE","name":"Universal Insurance Hldg","group_rank":69,"price":45.85},
    {"ticker":"PRLB","name":"Proto Labs Inc","group_rank":70,"price":93.84},
    {"ticker":"DV","name":"Doubleverify Hldgs Inc","group_rank":73,"price":13.49},
    {"ticker":"MGNI","name":"Magnite Inc","group_rank":73,"price":25.4},
    {"ticker":"ESTC","name":"Elastic N.V","group_rank":74,"price":98.23},
    {"ticker":"AAMI","name":"Acadian Asset Management","group_rank":78,"price":93.71},
    {"ticker":"AMG","name":"Affiliated Managers Grp","group_rank":78,"price":387.26},
    {"ticker":"SEIC","name":"S E I Investments Co","group_rank":78,"price":104.7},
    {"ticker":"VCTR","name":"Victory Capital Hld Cl A","group_rank":78,"price":112.44},
    {"ticker":"WT","name":"Wisdomtree","group_rank":78,"price":22.61},
    {"ticker":"TRGP","name":"Targa Resources Corp","group_rank":84,"price":286.7},
    {"ticker":"NEM","name":"Newmont Corporation","group_rank":87,"price":117.84},
    {"ticker":"SSRM","name":"Ssr Mining Inc","group_rank":87,"price":35.51},
    {"ticker":"DXCM","name":"Dexcom Inc","group_rank":88,"price":84.11},
    {"ticker":"KRT","name":"Karat Packaging Inc","group_rank":91,"price":54.58},
    {"ticker":"NVT","name":"Nvent Electric Plc","group_rank":93,"price":167.43},
    {"ticker":"ACNB","name":"A C N B Corporation","group_rank":94,"price":62.29},
    {"ticker":"ATLO","name":"Ames National Corp","group_rank":94,"price":31.46},
    {"ticker":"CZFS","name":"Citizens Financial Svcs","group_rank":94,"price":78.05},
    {"ticker":"FBIZ","name":"First Business Finl Svcs","group_rank":94,"price":69.36},
    {"ticker":"FMAO","name":"Farmers & Merchants Banc","group_rank":94,"price":34.55},
    {"ticker":"GCBC","name":"Greene County Bancorp","group_rank":96,"price":33.65},
    {"ticker":"CXW","name":"Corecivic Inc","group_rank":100,"price":32.93},
    {"ticker":"GEO","name":"Geo Group Inc Reit","group_rank":100,"price":31.13},
    {"ticker":"ANF","name":"Abercrombie & Fitch Co","group_rank":101,"price":142.58},
    {"ticker":"PWR","name":"Quanta Services Inc","group_rank":120,"price":705.94},
    {"ticker":"CHEF","name":"Chefs' Warehouse Hldg","group_rank":122,"price":114.32},
    {"ticker":"IMAX","name":"Imax Corp","group_rank":128,"price":50.8},
    {"ticker":"MG","name":"Mistras Group Inc","group_rank":130,"price":20.77},
    {"ticker":"IDT","name":"I D T Corporation Cl B","group_rank":138,"price":81.49},
    {"ticker":"FIGS","name":"Figs Inc Cl A","group_rank":140,"price":15.78},
    {"ticker":"WEYS","name":"Weyco Group Inc","group_rank":140,"price":51.46},
]

_ensure_book_seed_v14_25_prev = ensure_book_seed


def ensure_book_seed(desk):
    desk = _ensure_book_seed_v14_25_prev(desk)
    changed = False
    for rec in CHECKUP_BOOK_20261009_ROWS:
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
            if int(old.get("rev") or 0) < BOOK_REV_20261009 or not old.get("items"):
                keep_manual = "수동" in str(old.get("source") or "") and int(old.get("rev") or 0) >= BOOK_REV_20261009
                if not keep_manual:
                    rows[hit] = dict(rec)
                    changed = True
        if not any(str(x.get("ticker")) == tk and str(x.get("date")) == rec["date"] for x in desk.get("inst") or []):
            desk.setdefault("inst", []).append({
                "ticker": tk, "date": rec["date"],
                "funds_chg": rec.get("funds_chg"), "funds_up_q": rec.get("funds_up_q"),
                "ad": rec.get("ad"), "ud_vol": rec.get("ud"),
                "new_flag": (rec.get("funds_chg") or 0) >= 10,
                "note": rec.get("inst_note") or "",
                "source": rec.get("source") or "Stock Checkup 20261009",
            })
            changed = True
    lists = desk.setdefault("lists", {})
    lists["market_pulse_20261009"] = PULSE_20261009
    lists["weekly_review_20261009"] = WEEKLY_REVIEW_20261009
    cur = lists.get("market_pulse_latest") or {}
    if str(cur.get("date") or "") < "2026-10-09":
        lists["market_pulse_latest"] = dict(PULSE_20261009)
        changed = True
    hist = list(lists.get("psycho_history") or [])
    by_d = {str(x.get("date") or "")[:10]: x for x in hist}
    if "2026-10-09" not in by_d:
        by_d["2026-10-09"] = dict(PSYCHO_20261009)
        lists["psycho_history"] = [by_d[k] for k in sorted(by_d)]
        changed = True
    if str((lists.get("psycho_latest") or {}).get("date") or "") < "2026-10-09":
        lists["psycho_latest"] = by_d["2026-10-09"]
        changed = True
    if changed:
        try:
            save_ibd_desk(desk)
        except Exception:
            pass
    return desk
