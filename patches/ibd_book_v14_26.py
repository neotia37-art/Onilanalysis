# v14.26 book: eIBD 10/12판 (WEEK OF OCTOBER 12, 2026) 교차검증
# 원전: /IBD/20261009/eIBD_101226.pdf (pdftotext). 이 판의 MARKET PULSE·심리지표는 "Friday's action" = 10/9 장마감 기준.
# 10/12(월) 장 데이터는 원전에 없음 → 수치는 10/9 값 유지, 날짜 10/9로 표기.
BOOK_REV_20261012 = 26
CHECKUP_BOOK_V14_26 = True

EIBD_20261012_CHECK = {
    "edition": "eIBD WEEK OF OCTOBER 12, 2026 (VOL.43 NO.28)",
    "source": "eIBD_101226.pdf",
    "data_as_of": "2026-10-09",
    "outlook": "Market uptrend under pressure",  # eIBD 10/12 DDOG IBD Stock Checklist
    "exposure": "80%-100%",                     # Market Pulse + B6 Market Exposure
    "dist_nasdaq": 2, "dist_spx": 8,
    "leaders_up": ["SNOW", "GCT"], "leaders_down": ["CRGY", "DE"],
    "vix": 16.5, "put_call": 0.82, "bulls": 56.9, "bears": 30.9, "nyse_short_ratio": 5.08,
    "note": "eIBD 10/12판 확인: 시장 상태 '업트렌드 압력(uptrend under pressure)'·노출 80-100·DD NAS 2/SPX 8·VIX 16.5·P/C 0.82·불 56.9/베어 30.9 — 모두 10/9 장마감 기준(10/9 값과 동일). 10/12 장 데이터 원전에 없음.",
}

_ensure_book_seed_v14_26_prev = ensure_book_seed


def ensure_book_seed(desk):
    desk = _ensure_book_seed_v14_26_prev(desk)
    lists = desk.setdefault("lists", {})
    changed = False
    if lists.get("eibd_20261012_check") != EIBD_20261012_CHECK:
        lists["eibd_20261012_check"] = dict(EIBD_20261012_CHECK)
        changed = True
    cur = lists.get("market_pulse_latest") or {}
    if str(cur.get("date") or "") == "2026-10-09" and cur.get("outlook") != EIBD_20261012_CHECK["outlook"]:
        cur = dict(cur)
        cur["outlook"] = EIBD_20261012_CHECK["outlook"]
        cur["confirmed_by"] = "eIBD 10/12판"
        lists["market_pulse_latest"] = cur
        changed = True
    if changed:
        try:
            save_ibd_desk(desk)
        except Exception:
            pass
    return desk
