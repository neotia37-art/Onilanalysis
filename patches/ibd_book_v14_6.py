# v14.6 book addendum: PBF IBD Checkup 2026-09-04 print + overlay hook
BOOK_REV_20260904_PBF = 7
CHECKUP_BOOK_PBF = True

def _pbf_rec():
    return _C04(
        ticker="PBF", name="PBF Energy",
        group="OIL&GAS-REFINING/MKTG", group_rank=2, group_rs="A+",
        about="Operates as petroleum refiners and suppliers",
        printed="5:24 AM ET, Friday, September 04, 2026",
        source="20260904_PBF_Stock Checkup - Investors.com.pdf",
        rev=BOOK_REV_20260904_PBF,
        comp=97, eps=72, rs=99, smr="D", ad="A",
        price=75.33, off52=-3, vs50=19.07,
        due="2026-10-29",
        eps_q=704, eps3=297.6, accel=1, eps_est_q=1705.24, surprise=49.93,
        eps3y=None, eps_yrs=0, eps_est_y=519.20,
        sales_q=56.23, sales3y=-10.0, ptm=10.5, roe=23.6, debt=51,
        vol50="3.1 Mil", mcap="8.9 B",
        funds_chg=9, funds_up_q=4, ud=1.68,
        inst_note="그룹 2위 A+. SMR D · EPS 72 · 50일 +19%. 3년 EPS 연속 0. 고점 추격 금지.",
        body=("Comp 97 · EPS 72 · RS 99 · SMR D · A/D A. "
              "분기 EPS +704% / 3년 연속 0년 · 매출 3년 -10%. "
              "50일 +19.07% · 고점 -3%. 펀드 +9% 4분기. 추격 금지."),
    )


CHECKUP_BOOK_20260904_PBF = [_pbf_rec()]

_ensure_book_seed_v14_5 = ensure_book_seed


def ensure_book_seed(desk):
    desk = _ensure_book_seed_v14_5(desk)
    changed = False
    for rec in CHECKUP_BOOK_20260904_PBF:
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
            if int(old.get("rev") or 0) < BOOK_REV_20260904_PBF or not old.get("items"):
                keep_manual = old.get("source", "").find("수동") >= 0 and int(old.get("rev") or 0) >= BOOK_REV_20260904_PBF
                if not keep_manual:
                    rows[hit] = dict(rec)
                    changed = True
        if not any(str(x.get("ticker")) == tk and str(x.get("date")) == rec["date"]
                   for x in desk["inst"]):
            desk["inst"].append({
                "ticker": tk, "date": rec["date"],
                "funds_chg": rec.get("funds_chg"), "funds_up_q": rec.get("funds_up_q"),
                "ad": rec.get("ad"), "ud_vol": rec.get("ud"),
                "new_flag": False,
                "note": rec.get("inst_note") or "",
                "source": "Stock Checkup PDF 20260904 PBF",
            })
            changed = True
    if changed:
        save_ibd_desk(desk)
    return desk
