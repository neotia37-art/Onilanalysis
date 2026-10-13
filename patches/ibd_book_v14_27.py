# v14.27 book: Market Pulse 2026-10-12 (Monday) from Drive MP10192026.jpg
# OCR RapidOCR 2026-10-13. Current outlook 칸에 레짐 문구 없이 Exposure만 표기.
# 심리(DailyPsycho) 10/12 숫자는 원전 위젯 미수록 → 10/9 유지.
BOOK_REV_20261012_MON = 27
CHECKUP_BOOK_V14_27 = True
PULSE_SEED_V14_27 = True

PULSE_20261012 = {
    "date": "2026-10-12",
    "source": "MP10192026.jpg (Drive CANSLIM/IBD, modified 2026-10-13)",
    "headline": "Stocks mixed as bank earnings loom",
    "exposure": "80%-100%",
    "dist_nasdaq": 2,
    "dist_spx": 8,
    "leaders_up": ["ECO", "FRO", "DHT", "HAFN", "FIGS", "TEN"],
    "leaders_down": ["LITE", "SMTC"],
    "ftd": "2026-06-02",
    "note": "공식 Pulse(월요) 노출 80-100 · DD NAS 2 / SPX 8. 리더 상승 ECO·FRO·DHT·HAFN·FIGS·TEN / 하락 LITE·SMTC. 레짐 문구는 카드에 없음(Exposure만). 심리 인쇄는 10/9 유지. 신규 추격 0.",
}

_ensure_book_seed_v14_27_prev = ensure_book_seed


def ensure_book_seed(desk):
    desk = _ensure_book_seed_v14_27_prev(desk)
    lists = desk.setdefault("lists", {})
    changed = False
    lists["market_pulse_20261012"] = dict(PULSE_20261012)
    cur = lists.get("market_pulse_latest") or {}
    if str(cur.get("date") or "") < "2026-10-12":
        lists["market_pulse_latest"] = dict(PULSE_20261012)
        changed = True
    elif str(cur.get("date") or "") == "2026-10-12":
        if cur.get("leaders_up") != PULSE_20261012["leaders_up"] or cur.get("headline") != PULSE_20261012["headline"]:
            lists["market_pulse_latest"] = dict(PULSE_20261012)
            changed = True
    if changed:
        try:
            save_ibd_desk(desk)
        except Exception:
            pass
    return desk
