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


def _es_lab_q(p):
    s = str(p).replace(" 00:00:00", "")[:19]
    try:
        t = pd.Timestamp(s)
        if pd.notna(t):
            return f"{t.year} Q{(int(t.month) - 1) // 3 + 1}"
    except Exception:
        pass
    return s[:10] if s else "—"


def _es_lab_y(p):
    s = str(p).replace(" 00:00:00", "")[:19]
    try:
        t = pd.Timestamp(s)
        if pd.notna(t):
            return f"FY{t.year}"
    except Exception:
        pass
    return ("FY" + s[:4]) if s else "—"


def _es_growth(cur, prev):
    if callable(globals().get("growth_pct")):
        try:
            return growth_pct(cur, prev)
        except Exception:
            pass
    c, p = _es_num(cur), _es_num(prev)
    if c is None or p is None:
        return None
    if p == 0:
        return 999.0 if c > 0 else None
    return (c / p - 1.0) * 100.0


def _es_from_tab(tab, lag, last, is_year=False):
    rows = []
    if tab is None or getattr(tab, "empty", True):
        return rows
    if "EPS" not in getattr(tab, "index", []):
        return rows
    cols = list(tab.columns)
    if not cols:
        return rows
    start = max(0, len(cols) - last)
    for i in range(start, len(cols)):
        per = cols[i]
        cur = _es_num(tab.loc["EPS", per])
        prev = None
        kind = "전년동기" if (not is_year and lag == 4) else "전년"
        if i - lag >= 0:
            prev = _es_num(tab.loc["EPS", cols[i - lag]])
        elif (not is_year) and i >= 1 and len(cols) < lag + 1:
            prev = _es_num(tab.loc["EPS", cols[i - 1]])
            kind = "직전분기"
        g = _es_growth(cur, prev) if (cur is not None and prev is not None) else None
        rows.append({
            "period": per,
            "label": _es_lab_y(per) if is_year else _es_lab_q(per),
            "eps": cur,
            "prev": prev,
            "growth": g,
            "kind": kind,
            "src": "손익계산서",
        })
    return rows


def _es_from_earn_hist(edf, last=6):
    rows = []
    if edf is None or getattr(edf, "empty", True):
        return rows
    df = edf.copy()
    col = None
    for c in df.columns:
        cl = str(c).strip().lower()
        if cl in ("reported eps", "eps actual", "actual eps", "reported"):
            col = c
            break
    if col is None:
        for c in df.columns:
            if "report" in str(c).lower() and "eps" in str(c).lower():
                col = c
                break
    if col is None:
        return rows
    try:
        now = pd.Timestamp.utcnow().tz_localize(None)
    except Exception:
        now = pd.Timestamp.now()
    items = []
    for idx, rec in df.iterrows():
        try:
            t = pd.Timestamp(idx)
            if getattr(t, "tz", None) is not None:
                t = t.tz_convert("UTC").tz_localize(None)
            t = t.tz_localize(None) if getattr(t, "tz", None) is not None else t
        except Exception:
            continue
        if pd.isna(t) or t > now + pd.Timedelta(days=3):
            continue
        eps = _es_num(rec.get(col))
        if eps is None:
            continue
        items.append((t, float(eps)))
    if not items:
        return rows
    items.sort(key=lambda x: x[0])
    uniq = []
    for t, eps in items:
        qkey = (int(t.year), (int(t.month) - 1) // 3 + 1)
        if uniq and uniq[-1][2] == qkey:
            uniq[-1] = (t, eps, qkey)
        else:
            uniq.append((t, eps, qkey))
    for i, (t, eps, qkey) in enumerate(uniq):
        prev = None
        for t2, e2, k2 in uniq[:i]:
            if k2[0] == qkey[0] - 1 and k2[1] == qkey[1]:
                prev = e2
        g = _es_growth(eps, prev) if prev is not None else None
        rows.append({
            "period": t,
            "label": f"{qkey[0]} Q{qkey[1]}",
            "eps": eps,
            "prev": prev,
            "growth": g,
            "kind": "전년동기",
            "src": "실적발표",
        })
    return rows[-last:] if last else rows


def _es_ok(g, bar=25):
    if g is None:
        return False
    try:
        g = float(g)
    except Exception:
        return False
    return g == 999 or g >= bar


def eps_streak_from_fnd(fnd):
    fnd = fnd or {}
    y_rows = _es_from_tab(fnd.get("y_tab"), lag=1, last=3, is_year=True)
    q_stmt = _es_from_tab(fnd.get("q_tab"), lag=4, last=6, is_year=False)
    q_earn = _es_from_earn_hist(fnd.get("earn_hist"), last=8)
    q_map = {}
    for r in q_stmt:
        q_map[r["label"]] = r
    if len([r for r in q_stmt if r.get("growth") is not None]) < 4:
        for r in q_earn:
            prev = q_map.get(r["label"])
            if prev is None or prev.get("growth") is None:
                q_map[r["label"]] = r
            elif prev.get("eps") is None and r.get("eps") is not None:
                q_map[r["label"]] = r
    q_rows = list(q_map.values())

    def _key(r):
        try:
            return pd.Timestamp(r.get("period"))
        except Exception:
            lab = str(r.get("label") or "")
            try:
                y = int(lab[:4])
                if "Q" in lab:
                    q = int(lab.split("Q")[-1])
                    return pd.Timestamp(year=y, month=3 * q, day=1)
                return pd.Timestamp(year=y, month=12, day=31)
            except Exception:
                return pd.Timestamp("1970-01-01")

    q_rows.sort(key=_key)
    q_rows = q_rows[-6:]
    y_g = [r.get("growth") for r in y_rows if r.get("growth") is not None]
    q_g = [r.get("growth") for r in q_rows if r.get("growth") is not None]
    y_n, q_n = len(y_g), len(q_g)
    y_ge25 = sum(1 for g in y_g if _es_ok(g, 25))
    y_pos = sum(1 for g in y_g if _es_ok(g, 0.0001) or (g is not None and float(g) > 0) or g == 999)
    q_ge25 = sum(1 for g in q_g if _es_ok(g, 25))
    q_pos = sum(1 for g in q_g if g == 999 or (g is not None and float(g) > 0))
    last_q = q_g[-1] if q_g else None
    last_y = y_g[-1] if y_g else None
    accel = None
    if len(q_g) >= 2:
        a, b = q_g[0], q_g[-1]
        if a != 999 and b != 999:
            accel = b > a
        elif b == 999 and a != 999:
            accel = True
        else:
            accel = False
    y_streak = (y_n >= 3 and y_ge25 == y_n)
    q_streak = (q_n >= 4 and q_ge25 == q_n and _es_ok(last_q, 25))
    priority = bool(y_streak and q_streak)
    strong_note = []
    if y_streak:
        strong_note.append("3년 연속 +25%")
    if q_n >= 4 and q_ge25 == q_n:
        strong_note.append(f"{q_n}분기 연속 +25%")
    if accel:
        strong_note.append("분기 가속")
    return {
        "y_rows": y_rows, "q_rows": q_rows, "y_g": y_g, "q_g": q_g,
        "y_n": y_n, "q_n": q_n, "y_ge25": y_ge25, "q_ge25": q_ge25,
        "y_pos": y_pos, "q_pos": q_pos, "last_q": last_q, "last_y": last_y,
        "accel": accel, "y_streak": y_streak, "q_streak": q_streak,
        "priority": priority,
        "note": " · ".join(strong_note) if strong_note else "연속 +25% 미달",
    }


def _es_fmt_eps(v):
    if v is None:
        return "—"
    av = abs(float(v))
    if av >= 100:
        return f"{v:,.1f}"
    if av >= 1:
        return f"{v:,.2f}"
    return f"{v:,.3f}"


def _es_fmt_g(g):
    if g is None:
        return "—"
    if g == 999:
        return "흑자전환"
    if callable(globals().get("pct")):
        try:
            return pct(g, 0)
        except Exception:
            pass
    return f"{g:+.0f}%"
