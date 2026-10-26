# v14.28 book: Market Pulse latest 2026-10-23
BOOK_REV_20261023 = 28
CHECKUP_BOOK_V14_28 = True
PULSE_SEED_V14_28 = True

PULSE_20261023 = {
    "date": "2026-10-23",
    "source": "MP10232026.jpg (latest known)",
    "headline": "Exposure cut — 20-40%",
    "exposure": "20%-40%",
    "dist_nasdaq": 3,
    "dist_spx": 6,
    "leaders_up": [],
    "leaders_down": [],
    "ftd": "2026-06-02",
    "note": "공식 Pulse 노출 20-40% · DD NAS 3 / SPX 6. 이전 10/12 80-100 고정 해제. 신규 추격 0.",
}

_ensure_book_seed_v14_28_prev = ensure_book_seed

def ensure_book_seed(desk):
    desk = _ensure_book_seed_v14_28_prev(desk)
    lists = desk.setdefault("lists", {})
    lists["market_pulse_20261023"] = dict(PULSE_20261023)
    cur = lists.get("market_pulse_latest") or {}
    if str(cur.get("date") or "") < "2026-10-23":
        lists["market_pulse_latest"] = dict(PULSE_20261023)
        try:
            save_ibd_desk(desk)
        except Exception:
            pass
    return desk
