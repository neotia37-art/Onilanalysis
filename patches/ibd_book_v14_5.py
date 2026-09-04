# v14.5 book addendum: 2026-09-04 Checkup 22 + Weekly Review + Market Pulse + pivots
# Concat after ibd_book_v14_4. Keep BOOK_REV=5 so 9/2 manual edits survive.
BOOK_REV_20260904 = 6

def _C04(**kw):
    kw = dict(kw)
    kw.setdefault("date", "2026-09-04")
    kw.setdefault("source", "20260904 Stock Checkup PDF")
    kw.setdefault("printed", "Sep 04, 2026 (Market Closed / print)")
    kw.setdefault("ingest", "2026-09-04")
    kw.setdefault("full", True)
    kw.setdefault("rev", BOOK_REV_20260904)
    kw.setdefault("comp_color", _dot_comp(kw.get("comp")))
    kw["items"] = checkup_items_from(kw)
    body = (f'Comp {kw.get("comp")} · EPS {kw.get("eps")} · RS {kw.get("rs")} · '
            f'SMR {kw.get("smr")} · A/D {kw.get("ad")}. '
            f'펀드 {kw.get("funds_chg")}% · {kw.get("funds_up_q")}분기. '
            f'고점 {kw.get("off52")}% · 50일 {kw.get("vs50")}%.')
    kw.setdefault("body", body)
    return kw

CHECKUP_BOOK_20260904 = [
    _C04(ticker="AMD", name="Advanced Micro Devices", group="COMPUTER-SEMICON", group_rs="A",
         comp=89, eps=98, rs=76, smr="A", ad="D", price=456.16, off52=-22, vs50=-8.84,
         eps_q=246, surprise=2.71, sales_q=50.11, eps3y=28.0, accel=4,
         funds_chg=15, funds_up_q=5, ud=0.82, roe=10.2, mcap="746.1 B",
         inst_note="펀드 +15% 5분기. RS 76 · 고점 -22% · A/D D."),
    _C04(ticker="APH", name="Amphenol", group="ELECTRONICS-MISC", group_rs="B",
         comp=94, eps=98, rs=76, smr="A", ad="D+", price=82.07, off52=-8, vs50=1.94,
         eps_q=67, surprise=14.74, sales_q=55.00, eps3y=46.0, accel=0,
         funds_chg=5, funds_up_q=7, ud=1.03, roe=38.1, mcap="197.4 B",
         inst_note="펀드 7분기. RS 76 · Comp 94."),
    _C04(ticker="AVGO", name="Broadcom", group="COMPUTER-SEMICON", group_rs="A",
         comp=72, eps=98, rs=34, smr="A", ad="E", price=357.16, off52=-28, vs50=-7.01,
         eps_q=96, surprise=3.25, sales_q=85.50, eps3y=32.0, accel=2,
         funds_chg=3, funds_up_q=8, ud=0.80, roe=44.3, mcap="1747.2 B",
         inst_note="RS 34 · A/D E. 후행 대형."),
    _C04(ticker="BNMR", name="BNMR", group="?", group_rs="A",
         comp=47, eps=21, rs=73, smr="C", ad="C+", price=26.45, off52=-60, vs50=45.12,
         eps_q=33, surprise=-315.52, sales_q=2, accel=1,
         funds_chg=18, funds_up_q=4, ud=1.78, roe=-151.2, mcap="13.9 B",
         inst_note="Comp 47 제외."),
    _C04(ticker="CLS", name="Celestica", group="ELECTRONICS-CONTRACT MFG", group_rs="C",
         comp=67, eps=99, rs=38, smr="A", ad="E", price=309.84, off52=-35, vs50=-5.65,
         eps_q=83, surprise=10.20, sales_q=62.39, eps3y=57.0, accel=3,
         funds_chg=13, funds_up_q=1, ud=0.92, roe=52.7, mcap="35 B",
         inst_note="RS 38 · A/D E."),
    _C04(ticker="COHR", name="Coherent", group="LASER/PHOTONICS", group_rs="B",
         comp=71, eps=97, rs=51, smr="B", ad="E", price=264.41, off52=-40, vs50=-14.60,
         eps_q=74, surprise=7.61, sales_q=33.78, eps3y=46.0, accel=2,
         funds_chg=24, funds_up_q=4, ud=0.98, roe=8.5, mcap="52.6 B",
         inst_note="펀드 +24% · 고점 -40%."),
    _C04(ticker="CRDO", name="Credo Technology", group="COMPUTER-SEMICON", group_rs="A",
         comp=70, eps=79, rs=48, smr="A", ad="E", price=164.17, off52=-47, vs50=-29.29,
         eps_q=131, surprise=2.22, sales_q=114.73, accel=0,
         funds_chg=16, funds_up_q=1, ud=0.45, roe=30.7, mcap="31.1 B",
         inst_note="U/D 0.45 분산."),
    _C04(ticker="DELL", name="Dell Technologies", group="COMPUTER-HARDWARE", group_rank=20, group_rs="A",
         comp=97, eps=99, rs=96, smr="C", ad="C", price=516.39, off52=0, vs50=18.12,
         eps_q=203, surprise=43.34, sales_q=57.75, eps3y=30.0, accel=0,
         funds_chg=12, funds_up_q=4, ud=1.16, roe=0.0, mcap="319.1 B",
         inst_note="Pulse 리더. 신고가 +50일 18%. 추격 금지."),
    _C04(ticker="HOOD", name="Robinhood Markets", group="FINANCE-INVEST BNK", group_rs="A+",
         comp=92, eps=36, rs=89, smr="A", ad="A+", price=124.72, off52=-19, vs50=22.42,
         eps_q=48, surprise=44.28, sales_q=32.25, accel=2,
         funds_chg=3, funds_up_q=1, ud=1.10, roe=23.6, mcap="96.2 B",
         inst_note="EPS Rating 36 C실격."),
    _C04(ticker="LITE", name="Lumentum", group="LASER/PHOTONICS", group_rs="C",
         comp=75, eps=99, rs=67, smr="B", ad="E", price=847.37, off52=-22, vs50=3.84,
         eps_q=267, surprise=8.80, sales_q=109.34, eps3y=34.0, accel=0,
         funds_chg=26, funds_up_q=5, ud=1.36, roe=-240.0, mcap="78.1 B",
         inst_note="펀드 +26% · ROE 적자."),
    _C04(ticker="LLY", name="Eli Lilly", group="MEDICAL-ETHICAL DRUGS", group_rs="A",
         comp=93, eps=98, rs=70, smr="A", ad="D", price=1159.60, off52=-10, vs50=-2.64,
         eps_q=33, surprise=30.92, sales_q=47.67, eps3y=79.0, accel=0,
         funds_chg=1, funds_up_q=3, ud=1.12, roe=102.4, mcap="1092 B",
         inst_note="RS 70 후행 · A/D D."),
    _C04(ticker="LRGX", name="LRGX", group="?", group_rs="C+",
         comp=79, eps=95, rs=70, smr="A", ad="E", price=292.66, off52=-33, vs50=-9.61,
         eps_q=37, surprise=7.90, sales_q=29.99, eps3y=26.0, accel=0,
         funds_chg=6, funds_up_q=6, ud=0.74, roe=65.1, mcap="360.8 B",
         inst_note="A/D E · 고점 -33%."),
    _C04(ticker="MPC", name="Marathon Petroleum", group="OIL&GAS-REFINING/MKTG", group_rank=2, group_rs="A+",
         comp=99, eps=86, rs=98, smr="B", ad="A+", price=387.71, off52=-1, vs50=21.44,
         eps_q=348, surprise=24.26, sales_q=53.48, eps3y=-24.0, accel=0,
         funds_chg=7, funds_up_q=4, ud=2.59, roe=47.9, mcap="108.7 B",
         inst_note="3년 EPS -24. 50일 +21%. 추격 금지."),
    _C04(ticker="MRVL", name="Marvell Technology", group="COMPUTER-SEMICON", group_rs="A",
         comp=86, eps=94, rs=70, smr="A", ad="E", price=208.83, off52=-37, vs50=-5.86,
         eps_q=40, surprise=0.69, sales_q=36.55, eps3y=34.0, accel=1,
         funds_chg=25, funds_up_q=3, ud=0.92, roe=16.5, mcap="181.1 B",
         inst_note="펀드 +25% · A/D E · 고점 -37%."),
    _C04(ticker="MUFG", name="Mitsubishi UFJ Financial", group="BANKS-FOREIGN", group_rank=13, group_rs="A",
         comp=98, eps=91, rs=93, smr="B", ad="C", price=24.13, off52=3, vs50=9.39,
         eps_q=25, surprise=20.60, sales_q=11.64, eps3y=14.0, accel=0,
         funds_chg=5, funds_up_q=3, ud=1.53, roe=12.5, mcap="259.6 B",
         inst_note="신고가. 매출 +12%. 50일 +9%."),
    _C04(ticker="NET", name="Cloudflare", group="COMPUTER SFTWR-SECURITY", group_rs="A+",
         comp=93, eps=96, rs=81, smr="C", ad="C", price=284.51, off52=-14, vs50=1.91,
         eps_q=38, surprise=8.04, sales_q=35.87, eps3y=43.0, accel=0,
         funds_chg=4, funds_up_q=7, ud=1.33, roe=-14.4, mcap="97.1 B",
         inst_note="RS 81 · SMR C · 50일 +1.9%."),
    _C04(ticker="PLTR", name="Palantir Technologies", group="COMPUTER SFTWR-ENTERPRISE", group_rs="A+",
         comp=99, eps=99, rs=82, smr="A", ad="A", price=182.53, off52=-12, vs50=22.88,
         eps_q=156, surprise=18.98, sales_q=92.83, eps3y=86.0, accel=2,
         funds_chg=-1, funds_up_q=0, ud=1.44, roe=38.4, mcap="407.2 B",
         inst_note="2차 182.44 통과. 펀드 -1% · RS 82."),
    _C04(ticker="PSX", name="Phillips 66", group="OIL&GAS-REFINING/MKTG", group_rs="A+",
         comp=98, eps=78, rs=97, smr="C", ad="A+", price=254.66, off52=-1, vs50=19.76,
         eps_q=295, surprise=25.46, sales_q=53.04, eps3y=-30.0, accel=1,
         funds_chg=4, funds_up_q=5, ud=1.60, roe=24.0, mcap="102.2 B",
         inst_note="EPS 78 · 3년 EPS -30."),
    _C04(ticker="RNG", name="RingCentral", group="TELECOM-SVC WIRELESS", group_rank=4, group_rs="A+",
         comp=98, eps=89, rs=99, smr="D", ad="A+", price=76.36, off52=5, vs50=41.25,
         eps_q=15, surprise=4.75, sales_q=5.90, eps3y=18.0, accel=0,
         funds_chg=12, funds_up_q=2, ud=2.66, roe=0.0, mcap="6.1 B",
         inst_note="SMR D · 매출 +6% · 50일 +41%."),
    _C04(ticker="TLN", name="Talen Energy", group="UTILITY-ELECTRIC", group_rs="D",
         comp=9, eps=16, rs=14, smr="C", ad="E", price=305.52, off52=-32, vs50=-12.60,
         eps_q=-233, surprise=-162.37, sales_q=18.57, accel=0,
         funds_chg=8, funds_up_q=2, ud=0.77, roe=-12.9, mcap="14.5 B",
         inst_note="Comp 9 제외."),
    _C04(ticker="TX", name="Ternium", group="STEEL-PRODUCERS", group_rs="A",
         comp=87, eps=49, rs=89, smr="D", ad="A", price=57.98, off52=0, vs50=17.02,
         eps_q=37, surprise=46.74, sales_q=9.96, accel=0,
         funds_chg=11, funds_up_q=3, ud=2.82, roe=5.7, mcap="11.2 B",
         inst_note="EPS 49 · SMR D."),
    _C04(ticker="WPM", name="Wheaton Precious Metals", group="MINING-GOLD/SILVER/GEMS", group_rs="B",
         comp=98, eps=99, rs=83, smr="A", ad="A", price=156.63, off52=-6, vs50=25.05,
         eps_q=90, surprise=4.52, sales_q=84.65, eps3y=61.0, accel=0,
         funds_chg=0, funds_up_q=0, ud=1.58, roe=23.6, mcap="68.4 B",
         inst_note="RS 83 · 펀드 0분기 · 50일 +25%."),
]

MARKET_PULSE_20260903 = {
    "date": "2026-09-03", "source": "MARKET PULSE.png + IBD DESK",
    "headline": "Software rally, lower yields fuel broad-based gains",
    "exposure": "60%-80%", "dist_nasdaq": 4, "dist_spx": 3,
    "leaders_up": ["SNOW", "HPE", "DELL", "MRX", "ESTC", "AYA"],
    "leaders_down": ["VSXY", "TDW"],
    "nasdaq": 26117.35, "nasdaq_chg": 0.66, "nasdaq_vol_chg": -5.88,
    "spx": 7744.92, "spx_chg": 0.51, "spx_vol_chg": 20.20,
    "dji": 54231.77, "dji_chg": 0.46, "pct_above_200": 70.5,
    "adv": 1808, "dec": 1407, "nh": 87, "nl": 19,
    "vix": 15.2, "put_call": 0.73, "bullish_advice": 45,
    "market_score": 65, "market_label": "Confirmed Uptrend · 상승 추세 약함",
    "ftd": "2026-06-02", "dist_25d": 3,
    "note": "앱 노출 40-60% vs Pulse 60-80%. 분산 나스닥 4 / S&P 3.",
}

FRONT_SEED_20260903 = {
    "date": "2026-09-03", "source": "IBD DESK + MARKET PULSE", "tag": "2026-09-03-close",
    "nasdaq": 26117.35, "nasdaq_chg": 0.66, "dji": 54231.77, "dji_chg": 0.46,
    "spx": 7744.92, "spx_chg": 0.51, "nasdaq_vol_chg": -5.88, "nyse_vol_chg": 20.20,
    "headline": "Software rally · 3지수 상승 · 나스닥 vol -5.88% / S&P +20.20%",
    "note": "Confirmed Uptrend 약함. 분산 3~4일. Pulse 노출 60-80%.",
    "market_score": 65, "exposure": "60%-80%",
}

BUY_POINTS_20260901 = [
    {"ticker": "MSFT", "name": "Microsoft", "note": "Below shelf entry at 513.73", "pivot": 513.73, "status": "피벗 아래", "action": "대기"},
    {"ticker": "PLTR", "name": "Palantir Technologies", "note": "Above secondary buy point at 182.44", "pivot": 182.44, "status": "2차 위", "action": "추가 금지"},
    {"ticker": "NOW", "name": "ServiceNow", "note": "In buy zone above 139.20 cup-base entry", "pivot": 139.20, "status": "컵 매수구간", "action": "체크업 후 관찰"},
    {"ticker": "SHOP", "name": "Shopify", "note": "Cup with handle has a 158.87 buy point", "pivot": 158.87, "status": "컵위핸들 피벗", "action": "체크업 후 관찰"},
]

LONG_TERM_LEADERS_20260811 = {
    "date": "2026-08-11", "source": "20260811_longterm.png",
    "portfolio": [
        {"ticker": "ANET", "comp": 99, "eps": 96, "eps3y": 33, "stab": 7, "est_y": 37, "est_ny": 26, "roe": 31, "debt": 0},
        {"ticker": "CAH", "comp": 91, "eps": 95, "eps3y": 21, "stab": 8, "est_y": 8, "est_ny": 13},
        {"ticker": "CDNS", "comp": 67, "eps": 92, "eps3y": 21, "stab": 3, "est_y": 14, "est_ny": 17, "roe": 22, "debt": 48},
        {"ticker": "CTAS", "comp": 93, "eps": 86, "eps3y": 15, "stab": 2, "est_y": 12, "est_ny": 11, "roe": 41, "debt": 32},
        {"ticker": "KLAC", "comp": 83, "eps": 82, "eps3y": 20, "stab": 10, "est_y": 46, "est_ny": 21, "roe": 88, "debt": 96},
        {"ticker": "MEDP", "comp": 99, "eps": 95, "eps3y": 28, "stab": 4, "est_y": 15, "est_ny": 10, "roe": 70, "debt": 25},
        {"ticker": "ORLY", "comp": 49, "eps": 77, "eps3y": 8, "stab": 2, "est_y": 11, "est_ny": 11},
        {"ticker": "STRL", "comp": 67, "eps": 99, "eps3y": 60, "stab": 9, "est_y": 80, "est_ny": 27, "roe": 30, "debt": 29},
    ],
    "watch": [
        {"ticker": "GOOGL", "comp": 73, "eps": 99, "eps3y": 48, "stab": 21, "est_y": 89, "est_ny": -27, "roe": 36, "debt": 15},
        {"ticker": "TSM", "comp": 89, "eps": 98, "eps3y": 38, "stab": 16, "est_y": 59, "est_ny": 31, "roe": 36, "debt": 17},
    ],
    "note": "8/11 print. 3 weeks stale. not a buy list.",
}

WEEKLY_REVIEW_20260903 = [
    {"ticker":"VEEV","name":"Veeva Systems","group_rank":1,"price":284.38},
    {"ticker":"MPC","name":"Marathon Petroleum","group_rank":2,"price":387.71},
    {"ticker":"VLO","name":"Valero Energy","group_rank":2,"price":370.69},
    {"ticker":"KARO","name":"Karooooo","group_rank":4,"price":65.82},
    {"ticker":"PATH","name":"UiPath","group_rank":4,"price":16.50},
    {"ticker":"PAYC","name":"Paycom Software","group_rank":4,"price":240.52},
    {"ticker":"RNG","name":"RingCentral","group_rank":4,"price":76.36},
    {"ticker":"SNOW","name":"Snowflake","group_rank":4,"price":356.95},
    {"ticker":"TEAM","name":"Atlassian","group_rank":4,"price":194.68},
    {"ticker":"TWLO","name":"Twilio","group_rank":4,"price":240.48},
    {"ticker":"PBI","name":"Pitney Bowes","group_rank":5,"price":17.58},
    {"ticker":"ZBRA","name":"Zebra Technologies","group_rank":5,"price":357.50},
    {"ticker":"ILMN","name":"Illumina","group_rank":6,"price":221.66},
    {"ticker":"BWLP","name":"BW LPG","group_rank":7,"price":24.61},
    {"ticker":"ECO","name":"Okeanis Eco Tankers","group_rank":7,"price":69.56},
    {"ticker":"FRO","name":"Frontline","group_rank":7,"price":45.42},
    {"ticker":"NMM","name":"Navios Maritime","group_rank":7,"price":91.34},
    {"ticker":"SBLK","name":"Star Bulk Carriers","group_rank":7,"price":31.87},
    {"ticker":"SHIP","name":"Seanergy Maritime","group_rank":7,"price":18.53},
    {"ticker":"TNK","name":"Teekay Tankers","group_rank":7,"price":91.83},
    {"ticker":"CRWD","name":"CrowdStrike","group_rank":10,"price":214.97},
    {"ticker":"FTNT","name":"Fortinet","group_rank":10,"price":156.36},
    {"ticker":"MITK","name":"Mitek Systems","group_rank":10,"price":18.85},
    {"ticker":"OKTA","name":"Okta","group_rank":10,"price":170.42},
    {"ticker":"QLYS","name":"Qualys","group_rank":10,"price":174.35},
    {"ticker":"INSW","name":"International Seaways","group_rank":11,"price":102.24},
    {"ticker":"LPG","name":"Dorian LPG","group_rank":11,"price":53.57},
    {"ticker":"MUFG","name":"Mitsubishi UFJ Financial","group_rank":13,"price":24.13},
    {"ticker":"RDVT","name":"Red Violet","group_rank":16,"price":76.43},
    {"ticker":"SN","name":"SharkNinja","group_rank":19,"price":175.21},
    {"ticker":"DELL","name":"Dell Technologies","group_rank":20,"price":516.39},
    {"ticker":"NTAP","name":"NetApp","group_rank":20,"price":185.38},
    {"ticker":"HALO","name":"Halozyme","group_rank":27,"price":110.76},
    {"ticker":"ANET","name":"Arista Networks","group_rank":34,"price":193.80},
    {"ticker":"WT","name":"WisdomTree","group_rank":41,"price":24.87},
    {"ticker":"CAH","name":"Cardinal Health","group_rank":55,"price":248.61},
    {"ticker":"ESTC","name":"Elastic","group_rank":71,"price":96.13},
    {"ticker":"KRT","name":"Karat Packaging","group_rank":84,"price":47.06},
]

def ensure_lists_seed(desk):
    desk.setdefault("lists", {})
    desk["lists"]["weekly_review_20260903"] = WEEKLY_REVIEW_20260903
    desk["lists"]["buy_points_20260901"] = BUY_POINTS_20260901
    desk["lists"]["long_term_leaders_20260811"] = LONG_TERM_LEADERS_20260811
    desk["lists"]["market_pulse_20260903"] = MARKET_PULSE_20260903
    return desk

_ensure_book_seed_v14_4 = ensure_book_seed

def ensure_book_seed(desk):
    desk = _ensure_book_seed_v14_4(desk)
    changed = False
    for rec in CHECKUP_BOOK_20260904:
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
            if int(old.get("rev") or 0) < BOOK_REV_20260904 or not old.get("items"):
                keep_manual = old.get("source", "").find("수동") >= 0 and int(old.get("rev") or 0) >= BOOK_REV_20260904
                if not keep_manual:
                    rows[hit] = dict(rec)
                    changed = True
        if not any(str(x.get("ticker")) == tk and str(x.get("date")) == rec["date"] for x in desk["inst"]):
            desk["inst"].append({
                "ticker": tk, "date": rec["date"],
                "funds_chg": rec.get("funds_chg"), "funds_up_q": rec.get("funds_up_q"),
                "ad": rec.get("ad"), "ud_vol": rec.get("ud"),
                "new_flag": (rec.get("funds_chg") or 0) >= 10,
                "note": rec.get("inst_note") or "",
                "source": "Stock Checkup PDF 20260904",
            })
            changed = True
    ensure_lists_seed(desk)
    fronts = desk.setdefault("front", [])
    if not any(str(x.get("date")) == "2026-09-03" for x in fronts):
        fronts.append(dict(FRONT_SEED_20260903))
        changed = True
    if changed:
        save_ibd_desk(desk)
    return desk
