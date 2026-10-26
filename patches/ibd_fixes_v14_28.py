# v14.28 fixes: early seed call helper + score label note
# Call this from market tab or startup if available.

def ensure_pulse_early(desk=None):
    """Call ensure_book_seed early so market tab sees latest Pulse."""
    if desk is None:
        try:
            desk = load_ibd_desk()
        except Exception:
            return None
    try:
        return ensure_book_seed(desk)
    except Exception:
        return desk

SCORE_LABEL_NOTE = "앱 점수 = Yahoo 자체 산식 · IBD 등급 = Checkup 원전. 날짜·출처 확인 필수."

print("v14.28 fixes loaded: early seed helper ready")
