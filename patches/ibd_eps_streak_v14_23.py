# v14.23 — 개별종목 최근 3년 · 6분기 EPS 증가율 + 최우선 뱃지
# 오닐 C(분기 전년동기) · A(연간 연속). 손익계산서 열이 짧으면 실적발표 EPS로 보충.
EPS_STREAK_V14_23 = True


def _es_num(v):
    if v is None:
        return None
    try:
        if isinstance(v, float) and (np.isnan(v) or np.isinf(v)):
            return None
    except Exception:
        pass
    try:
        f = float(v)
    except Exception:
        return None
    if f != f or abs(f) == float("inf"):
        return None
    return f
