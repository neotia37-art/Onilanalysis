# v14.24 book: Pulse 2026-09-28 + CRWD 9/29 Checkup + ANET/NVDA 9/28 refresh
BOOK_REV_20260929 = 24
CHECKUP_BOOK_V14_24 = True
PULSE_SEED_V14_24 = True

def _C29(**kw):
    kw = dict(kw)
    kw.setdefault("date", "2026-09-29")
    kw.setdefault("source", "20260930 Stock Checkup PDF")
    kw.setdefault("printed", "Sep 30, 2026 08:28 ET (price 1:00 PM EST 9/29)")
    kw.setdefault("ingest", "2026-09-30")
    kw.setdefault("full", True)
    kw.setdefault("rev", BOOK_REV_20260929)
    kw.setdefault("comp_color", _dot_comp(kw.get("comp")))
    kw["items"] = checkup_items_from(kw)
    body = (
        f'Comp {kw.get("comp")} / EPS {kw.get("eps")} / RS {kw.get("rs")} / '
        f'SMR {kw.get("smr")} / A/D {kw.get("ad")}. '
        f'펌드 {kw.get("funds_chg")}% / {kw.get("funds_up_q")}q. '
        f'off52 {kw.get("off52")}% / vs50 {kw.get("vs50")}%.'
    )
    kw.setdefault("body", body)
    return kw


def _C28(**kw):
    rec = _C29(**kw)
    rec["date"] = kw.get("date") or "2026-09-28"
    rec.setdefault("printed", "Sep 28, 2026 Market Close")
    rec.setdefault("ingest", "2026-09-29")
    return rec


CHECKUP_BOOK_20260929_ROWS = [
    _C29(
        ticker="CRWD", name="CrowdStrike Holdings",
        group="COMPUTER SFTWR-SECURITY", group_rank=2, group_rs="A+",
        source="20260930_CRWD_Stock Checkup - Investors.com.pdf",
        exposure="80%-100%",
        comp=99, eps=94, rs=99, smr="C", ad="A+",
        price=262.74, off52=0, vs50=22.18,
        eps_q=33, eps3=30.9, surprise=6.33, sales_q=25.83,
        eps3y=18.0, accel=0, eps_yrs=0, eps_est_q=29.65, eps_est_y=34.36,
        funds_chg=9, funds_up_q=7, ud=1.0,
        ptm=-2.6, roe=-4.2, debt=18, mcap="269 B", vol50="10.0 M",
        due="2026-12-01",
        inst_note="Comp99 RS99 A/D A+ vs50 +22.18 off52 0. SMR C GAAP ROE -4.2. chase ban +15% vs pivot 227.60. not a buy.",
    ),
    _C28(
        ticker="ANET", name="Arista Networks",
        group="COMPUTER-NETWORKING", group_rank=22, group_rs="A",
        source="20260929 ANET Checkup 9/28 close",
        date="2026-09-28", exposure="80%-100%",
        comp=99, eps=96, rs=94, smr="A", ad="C",
        price=204.92, off52=-4.64, vs50=7.31,
        eps_q=40, eps3=33.2, surprise=15.14, sales_q=37.69,
        eps3y=33.0, accel=3, eps_yrs=5, eps_est_q=43.58, eps_est_y=37.86,
        funds_chg=4, funds_up_q=5, ud=1.42,
        ptm=47.2, roe=31.4, debt=0, mcap="260.5 B", vol50="6.3 M",
        due="2026-11-02",
        inst_note="Comp99 RS94 SMR A A/D C vs50 +7.3 off52 -4.6. app pivot 206.23 -0.6% fake BO 0.70x 9/25. grade P not a buy.",
    ),
    _C28(
        ticker="NVDA", name="NVIDIA",
        group="COMPUTER-SEMICON", group_rank=16, group_rs="A",
        source="20260929 NVDA Checkup 9/28 close",
        date="2026-09-28", exposure="80%-100%",
        comp=99, eps=99, rs=88, smr="A", ad="C-",
        price=228.86, off52=-3, vs50=5.71,
        funds_chg=2, funds_up_q=8, ud=1.1,
        roe=None, mcap="5.52 T",
        inst_note="Comp99 EPS99 RS88 SMR A A/D C- funds +2%/8q vs50 +5.7 off52 -3. app CANSLIM45 pivot 236.10 -3.1. not a buy.",
    ),
]

PULSE_20260928 = {
    "date": "2026-09-28",
    "source": "MP09282026.jpg + IBD Weekly 9/25-28 pack",
    "headline": "Broad selling · Monday Pulse after week of software/AI tape",
    "exposure": "80%-100%",
    "dist_nasdaq": 3,
    "dist_spx": 6,
    "leaders_up": ["APH", "MU", "TSM", "PANW", "ANET", "LITE"],
    "leaders_down": ["META"],
    "ftd": "2026-06-02",
    "market_score": 55,
    "note": "공식 Pulse 노출 80-100 · DD NAS 3 / SPX 6. FTD 2026-06-02 실효 논쟁. 공통6은 공부 교차표이지 매수 명단이 아님. 신규 추격 0.",
}

PSYCHO_20260928 = {
    "date": "2026-09-28",
    "vix": None,
    "put_call": None,
    "high_low": None,
    "bulls": None,
    "bears": None,
    "source": "Pulse 9/28 print (psycho print not re-keyed)",
    "note": "Pulse 80-100 / NAS3 / SPX6. 개별 심리 숫자는 9/15 인쇄(VIX 18.2 P/C 0.78)가 마지막 원전.",
}

COMMON6_20260929 = {
    "date": "2026-09-29",
    "source": "20260929_수록교차_공통기업분석.xlsx",
    "tickers": ["APH", "MU", "TSM", "PANW", "ANET", "LITE"],
    "note": "주간 패키지 교차 공통6. 공부 명단. 매수 0.",
}

_ensure_book_seed_v14_24_prev = ensure_book_seed


def ensure_book_seed(desk):
    desk = _ensure_book_seed_v14_24_prev(desk)
    changed = False
    for rec in CHECKUP_BOOK_20260929_ROWS:
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
            if int(old.get("rev") or 0) < BOOK_REV_20260929 or not old.get("items"):
                keep_manual = "수동" in str(old.get("source") or "") and int(old.get("rev") or 0) >= BOOK_REV_20260929
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
                "source": rec.get("source") or "Stock Checkup 20260929",
            })
            changed = True
    lists = desk.setdefault("lists", {})
    lists["market_pulse_20260928"] = PULSE_20260928
    lists["common6_20260929"] = COMMON6_20260929
    cur = lists.get("market_pulse_latest") or {}
    if str(cur.get("date") or "") < "2026-09-28":
        lists["market_pulse_latest"] = dict(PULSE_20260928)
        changed = True
    hist = list(lists.get("psycho_history") or [])
    by_d = {str(x.get("date") or "")[:10]: x for x in hist}
    if "2026-09-28" not in by_d:
        by_d["2026-09-28"] = dict(PSYCHO_20260928)
        lists["psycho_history"] = [by_d[k] for k in sorted(by_d)]
        changed = True
    if changed:
        try:
            save_ibd_desk(desk)
        except Exception:
            pass
    return desk
