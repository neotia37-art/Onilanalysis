# v14.8 book: 2026-09-07/08 Checkup + list-change article
BOOK_REV_20260908 = 8
CHECKUP_BOOK_20260908 = True

def _C08(**kw):
    kw = dict(kw)
    kw.setdefault("date", "2026-09-08")
    kw.setdefault("source", "20260907/08 Stock Checkup PDF")
    kw.setdefault("printed", "Sep 07-08, 2026")
    kw.setdefault("ingest", "2026-09-08")
    kw.setdefault("full", True)
    kw.setdefault("rev", BOOK_REV_20260908)
    kw.setdefault("comp_color", _dot_comp(kw.get("comp")))
    kw["items"] = checkup_items_from(kw)
    body = (f'Comp {kw.get("comp")} · EPS {kw.get("eps")} · RS {kw.get("rs")} · '
            f'SMR {kw.get("smr")} · A/D {kw.get("ad")}. '
            f'펀드 {kw.get("funds_chg")}% · {kw.get("funds_up_q")}분기. '
            f'고점 {kw.get("off52")}% · 50일 {kw.get("vs50")}%.')
    kw.setdefault("body", body)
    return kw

CHECKUP_BOOK_20260908_ROWS = [
    _C08(ticker="ANET", name="Arista Networks", group="COMPUTER-NETWORKING", group_rank=25, group_rs="A",
         source="20260907_ANET_Stock Checkup - Investors.com.pdf",
         comp=97, eps=96, rs=86, smr="A", ad="D", price=193.78, off52=-10, vs50=5.93,
         eps_q=40, surprise=15.14, sales_q=37.69, eps3y=33.0, accel=3,
         funds_chg=4, funds_up_q=8, ud=1.35, roe=31.5, debt=0, mcap="244.4 B", due="2026-11-02",
         inst_note="그룹 25. RS 86 · A/D D. 50일 +5.9%."),
    _C08(ticker="NOW", name="ServiceNow", group="COMPUTER SFTWR-ENTERPRISE", group_rank=8, group_rs="A+",
         source="20260907_NOW_Stock Checkup - Investors.com.pdf",
         comp=94, eps=91, rs=60, smr="A", ad="A+", price=141.26, off52=-27, vs50=20.71,
         eps_q=10, surprise=4.39, sales_q=24.01, eps3y=27.0, accel=0,
         funds_chg=-3, funds_up_q=0, ud=1.47, roe=14.2,
         inst_note="피벗 139.20 위. RS 60 · 펀드 -3% · 50일 +20.7%."),
    _C08(ticker="PBF", name="PBF Energy", group="OIL&GAS-REFINING/MKTG", group_rank=1, group_rs="A+",
         source="20260907_PBF_Stock Checkup - Investors.com.pdf",
         comp=97, eps=72, rs=99, smr="D", ad="A", price=74.34, off52=-5, vs50=16.33,
         eps_q=704, surprise=49.93, sales_q=56.23, accel=1,
         funds_chg=8, funds_up_q=4, ud=1.69, roe=23.6, debt=51, mcap="8.8 B", due="2026-10-29",
         inst_note="SMR D · EPS 72 · 50일 +16.3%. 추가 금지."),
    _C08(ticker="SHOP", name="Shopify", group="RETAIL-INTERNET", group_rank=8, group_rs="A+",
         source="20260907_SHOP_Stock Checkup - Investors.com.pdf",
         comp=96, eps=96, rs=70, smr="A", ad="B", price=145.09, off52=-20, vs50=8.15,
         eps_q=51, surprise=38.91, sales_q=33.69, eps3y=61.0, accel=0,
         funds_chg=-4, funds_up_q=0, ud=1.36, roe=15.5, debt=1, mcap="186.6 B", due="2026-10-22",
         inst_note="피벗 158.87 미달. RS 70 · 펀드 -4%."),
    _C08(ticker="SNOW", name="Snowflake", group="COMPUTER SFTWR-ENTERPRISE", group_rank=8, group_rs="A+",
         source="20260907_SNOW_Stock Checkup - Investors.com.pdf",
         comp=97, eps=96, rs=95, smr="C", ad="B", price=337.18, off52=-12, vs50=13.41,
         eps_q=77, surprise=38.76, sales_q=35.09, eps3y=28.0, accel=2,
         funds_chg=11, funds_up_q=1, ud=1.57, roe=-48.2, debt=140, mcap="116.9 B", due="2026-12-02",
         inst_note="Pulse 리더. SMR C · ROE 적자 · 50일 +13.4%."),
    _C08(ticker="VEEV", name="Veeva Systems", group="MEDICAL-SYST/SOFTWR", group_rank=5, group_rs="A+",
         source="20260907_VEEV_Stock Checkup - Investors.com.pdf",
         comp=99, eps=91, rs=87, smr="A", ad="A+", price=275.09, off52=-11, vs50=25.04,
         eps_q=18, surprise=5.49, sales_q=17.60, eps3y=27.0, accel=1,
         funds_chg=5, funds_up_q=1, ud=2.63, roe=14.4, debt=1, mcap="44.5 B", due="2026-12-09",
         inst_note="Comp 99 A/D A+. RS 87 · 50일 +25%."),
    _C08(ticker="FIVE", name="Five Below", group="RETAIL-DISCOUNT", group_rank=136, group_rs="E",
         source="20260908_FIVE_Stock Checkup - Investors.com.pdf",
         comp=92, eps=97, rs=84, smr="A", ad="C+", price=252.20, off52=-4, vs50=15.60,
         eps_q=107, surprise=19.82, sales_q=22.85, eps3y=18.0, accel=0,
         funds_chg=9, funds_up_q=6, ud=1.27, roe=28.3, debt=79, mcap="13.9 B", due="2026-12-02",
         inst_note="IBD50 신규. 그룹 136 E. RS 84 · 50일 +15.6%."),
    _C08(ticker="IOT", name="Samsara", group="COMPUTER SFTWR-ENTERPRISE", group_rank=8, group_rs="A+", exposure="60%-80%",
         source="20260908_IOT_Stock Checkup - Investors.com.pdf",
         comp=82, eps=64, rs=70, smr="B", ad="C+", price=40.20, off52=-15, vs50=6.82,
         eps_q=67, surprise=25.00, sales_q=29.88, accel=1,
         funds_chg=7, funds_up_q=1, ud=1.73, roe=6.4, debt=4, mcap="23.5 B", due="2026-11-26",
         inst_note="Comp 82 RS 70 EPS 64. 문턱 미달."),
]

LIST_CHANGES_20260904 = {
    "date": "2026-09-04",
    "source": "20260908 article",
    "ibd50_add": ["ELF", "ERO", "FIVE", "MU", "RBRK"],
    "ibd50_cut": ["ADPT", "DXCM", "FLYW", "LB", "PLTR"],
    "sector_add": ["TAL"],
    "sector_cut": ["AU", "PLTR", "SKWD"],
    "bigcap_add": ["AMP", "MSFT", "TWLO", "ZBRA"],
    "bigcap_cut": ["FNV", "RJF", "RPRX", "SNOW"],
    "ipo_add": ["YSWY"],
    "notable_add": ["DELL", "DHT", "EQNR", "FRO", "HSHP", "PSX", "SLAB", "TRMD"],
    "notable_cut": ["ECO", "HRMY", "INCY", "LPG", "MPC", "SNOW", "WHD", "WT"],
    "note": "list add != buy. WT cut from Notable.",
}

_ensure_book_seed_prev = ensure_book_seed

def ensure_book_seed(desk):
    desk = _ensure_book_seed_prev(desk)
    changed = False
    for rec in CHECKUP_BOOK_20260908_ROWS:
        tk = rec["ticker"]
        rows = desk["checkups"].setdefault(tk, [])
        hit = None
        for i, x in enumerate(rows):
            if str(x.get("date")) == rec["date"]:
                hit = i
                break
        if hit is None:
            rows.append(dict(rec)); changed = True
        else:
            old = rows[hit]
            if int(old.get("rev") or 0) < BOOK_REV_20260908 or not old.get("items"):
                keep_manual = old.get("source", "").find("수동") >= 0 and int(old.get("rev") or 0) >= BOOK_REV_20260908
                if not keep_manual:
                    rows[hit] = dict(rec); changed = True
        if not any(str(x.get("ticker")) == tk and str(x.get("date")) == rec["date"] for x in desk.get("inst") or []):
            desk.setdefault("inst", []).append({
                "ticker": tk, "date": rec["date"],
                "funds_chg": rec.get("funds_chg"), "funds_up_q": rec.get("funds_up_q"),
                "ad": rec.get("ad"), "ud_vol": rec.get("ud"),
                "new_flag": (rec.get("funds_chg") or 0) >= 10,
                "note": rec.get("inst_note") or "",
                "source": rec.get("source") or "Stock Checkup 20260908",
            })
            changed = True
    desk.setdefault("lists", {})["list_changes_20260904"] = LIST_CHANGES_20260904
    if changed:
        try: save_ibd_desk(desk)
        except Exception: pass
    return desk
