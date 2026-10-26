# v14.28 latest Drive update: 10/23-24 Pulse + recent top10 note for company/inst
# Source: Google Drive IBD_오늘기사_20261024_심층분석.md + MP10232026.jpg

LATEST_PULSE_CONFIRMED = {
    "date": "2026-10-23",
    "exposure": "20%-40%",
    "dist_nasdaq": 3,
    "dist_spx": 6,
    "source": "Drive Market Trend 10/24 + MP10232026.jpg",
    "note": "유가 100달러 돌파 · 노출 20-40% 유지 · DD NAS3/SPX6. 방어 우선.",
}

RECENT_TOP10_20261023 = ["HALO", "HAS", "DOCU", "ADP", "RNR", "HURN", "NTAP", "VEEV", "P", "ESTC"]

def ensure_latest_from_drive(desk):
    """Seed latest confirmed Pulse and note recent leaders."""
    lists = desk.setdefault("lists", {})
    lists["market_pulse_latest"] = dict(LATEST_PULSE_CONFIRMED)
    lists["recent_top10_20261023"] = RECENT_TOP10_20261023
    try:
        save_ibd_desk(desk)
    except Exception:
        pass
    return desk

# Chain after existing ensure_book_seed
_ensure_prev_latest = ensure_book_seed if "ensure_book_seed" in globals() else None

def ensure_book_seed(desk):
    if _ensure_prev_latest:
        desk = _ensure_prev_latest(desk)
    return ensure_latest_from_drive(desk)

print("v14.28 Drive latest update loaded: Pulse 10/23 + top10 note")
