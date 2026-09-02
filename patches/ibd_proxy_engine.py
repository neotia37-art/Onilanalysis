# IBD proxy engine A — conservative EPS rating
IBD_ADJ = (
    "이 패널의 숫자는 IBD 원점이 아니다. 앱 근사 + 보수 조정이다. "
    "EPS는 유니버스 백분위 대신 성장률 곡선(상한 깎음), RS 주도 문텀은 90→87, "
    "RS 70 하락·6~12개월 하락 금지는 RS선 기울기 대용, 업종 상위 5는 미국 섹터 ETF만."
)

def _g(v):
    if v is None or (isinstance(v, float) and (np.isnan(v) or np.isinf(v))):
        return None
    return float(v)

def _tab_growth(tab, col):
    if tab is None or tab.empty or col not in tab.columns:
        return []
    return [float(x) for x in tab[col].tolist() if x is not None and not (isinstance(x, float) and np.isnan(x))]

def _roe_path(fnd):
    cur = _g((fnd or {}).get("roe"))
    prev, delta = None, None
    yt = (fnd or {}).get("y_tab")
    if yt is not None and not yt.empty and "ROE" in getattr(yt, "index", []):
        vals = [_g(yt.loc["ROE", c]) for c in list(yt.columns)]
        vals = [v for v in vals if v is not None]
        if vals:
            cur = vals[-1]
        if len(vals) >= 2:
            prev, delta = vals[-2], vals[-1] - vals[-2]
    return cur, prev, delta

def eps_rating_detail(fnd, q_g, y_g):
    FH = fin_history(fnd or {})
    q_sales = _tab_growth(FH.get("q"), "매출액증감")
    y_sales = _tab_growth(FH.get("y"), "매출액증감")
    q_eps = _tab_growth(FH.get("q"), "EPS증감")
    y_eps = _tab_growth(FH.get("y"), "EPS증감")
    y_ni = _tab_growth(FH.get("y"), "순이익증감")
    last_q_sales = q_sales[-1] if q_sales else _g((fnd or {}).get("q_sales"))
    last_y_sales = y_sales[-1] if y_sales else None
    last_y_ni = y_ni[-1] if y_ni else y_g
    roe, roe_prev, roe_d = _roe_path(fnd)
    raw = eps_rating(200 if q_g == 999 else q_g, 200 if y_g == 999 else y_g)
    q_ok = q_g is not None and (q_g == 999 or q_g >= 25)
    y_ok = y_g is not None and (y_g == 999 or y_g >= 25)
    capped, cap_why = raw, "상한 없음 (C·A 둘 다 25%+ 또는 흑자전환)"
    if raw is not None and not (q_ok and y_ok):
        capped = min(raw, 80)
        cap_why = "C 또는 A가 25% 미만 → EPS 근사 상한 80"
    y_profit = last_y_ni if last_y_ni is not None else y_g
    elite = bool((y_profit is not None and y_profit >= 30) and (roe is not None and roe >= 17))
    rows = [
        ("분기 매출 증가율", last_q_sales, "+25%", last_q_sales is not None and last_q_sales >= 25),
        ("연간 매출 증가율", last_y_sales, "+25%", last_y_sales is not None and last_y_sales >= 25),
        ("분기 EPS 증가율", q_g, "+25%", q_ok),
        ("연간 EPS 증가율", y_g, "+25%", y_ok),
        ("연간 순이익 증가율", last_y_ni, "+30% 특별", last_y_ni is not None and last_y_ni >= 30),
        ("ROE 수준", roe, "17%+", roe is not None and roe >= 17),
        ("ROE 증감(p)", roe_d, "상승", roe_d is not None and roe_d > 0),
    ]
    return {"raw": raw, "rating": capped, "cap_why": cap_why, "elite": elite,
            "q_sales": last_q_sales, "y_sales": last_y_sales, "y_profit": y_profit,
            "roe": roe, "roe_prev": roe_prev, "roe_d": roe_d,
            "q_sales_hist": q_sales, "y_sales_hist": y_sales,
            "q_eps_hist": q_eps, "y_eps_hist": y_eps, "y_ni_hist": y_ni,
            "rows": rows, "q_ok": q_ok, "y_ok": y_ok}
