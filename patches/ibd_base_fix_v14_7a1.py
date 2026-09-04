# v14.7 — O'Neil/IBD base lock + Checkup gate. PBF 2026-09-04 review.
# Pivot identity = exact daily left-side (or handle) high, locked after first
# close above it until an 8%+ new correction. US buy trigger = pivot + $0.10
# (How to Make Money in Stocks). KR trigger = pivot * 1.001.
# HTF only if prior run >=90% and depth <=20% and 3-6 weeks.
# Volume <1.40x average is never a valid breakout. 50-day +15% = chase ban.
# Checkup overlay is the IBD gate: Comp 90 / EPS 80 / RS 80 / SMR A-B / A-D A-B.
BASE_FIX_V14_7 = "2026-09-04-pbf-ibd"
BASE_FIX_V14_6 = BASE_FIX_V14_7  # loader compatibility


def to_weekly_locked(df):
    w = df.resample("W-FRI").agg({"Open": "first", "High": "max", "Low": "min",
                                  "Close": "last", "Volume": "sum"}).dropna()
    if w.empty:
        return w
    last_d = pd.Timestamp(df.index[-1]).normalize()
    last_w = pd.Timestamp(w.index[-1]).normalize()
    if last_d < last_w and len(w) > 4:
        w = w.iloc[:-1]
    return w


def _daily_date(dfd, week_end, kind, back=1, after=None):
    start = pd.Timestamp(week_end) - pd.Timedelta(days=7 * back)
    if after is not None and pd.Timestamp(after) > start:
        start = pd.Timestamp(after)
    seg = dfd.loc[start:week_end]
    if seg.empty:
        return week_end
    return seg["High"].idxmax() if kind == "H" else seg["Low"].idxmin()


def build_bases(dfd, zp=8.0):
    w = to_weekly_locked(dfd)
    if len(w) < 20:
        return [], w
    bases, used = [], -1
    for hp, typ, hv in zigzag(w, zp):
        if typ != "H" or hp <= used:
            continue
        after = w.iloc[hp + 1:]
        if len(after) < 3:
            break
        bo = np.where(after["Close"].values > hv)[0]
        completed = len(bo) > 0
        endpos = hp + 1 + int(bo[0]) if completed else len(w) - 1
        seg = w.iloc[hp:endpos + 1]
        lowv = float(seg["Low"].min())
        lowpos = hp + int(np.argmin(seg["Low"].values))
        depth = (hv - lowv) / hv * 100
        weeks = endpos - hp
        if depth < 7 or depth > 72 or weeks < 3:
            continue
        start_d = _daily_date(dfd, w.index[hp], "H")
        low_d = _daily_date(dfd, w.index[lowpos], "L", after=start_d)
        if pd.Timestamp(low_d) <= pd.Timestamp(start_d):
            right = dfd.loc[start_d:dfd.index[-1]]
            if len(right) < 3:
                continue
            cap = right
            if completed:
                cap = right.iloc[: max(3, int(weeks * 6))]
            low_d = cap["Low"].idxmin()
        try:
            left_high = float(dfd.loc[start_d, "High"])
        except Exception:
            left_high = float(hv)
        lowv = float(dfd.loc[low_d, "Low"]) if low_d in dfd.index else lowv
        if left_high <= 0 or lowv >= left_high:
            continue
        depth = (left_high - lowv) / left_high * 100
        end_d = dfd.index[-1]
        if completed:
            cx = dfd.loc[low_d:]
            cxi = cx.index[cx["Close"] > left_high]
            end_d = cxi[0] if len(cxi) else _daily_date(dfd, w.index[endpos], "H", after=low_d)
        if pd.Timestamp(low_d) < pd.Timestamp(start_d):
            continue
        pre = dfd.loc[:start_d].tail(160)
        prior = (left_high / float(pre["Low"].min()) - 1) * 100 if len(pre) > 30 else np.nan
        rng = left_high - lowv
        u_ratio = int((seg["Low"] <= lowv + rng * 0.33).sum()) / max(1, len(seg)) * 100
        li = max(1, lowpos - hp)
        lseg, rseg = seg.iloc[:li], seg.iloc[li:]
        lv = float(lseg["Volume"].mean()) if len(lseg) else np.nan
        vol_bal = float(rseg["Volume"].mean()) / lv if lv and lv > 0 and len(rseg) else np.nan
        bases.append({"start": start_d, "low_date": low_d, "end": end_d,
                      "left_high": left_high, "low": lowv, "depth": depth,
                      "weeks": float(weeks), "completed": completed, "prior_gain": prior,
                      "u_ratio": u_ratio, "vol_bal": vol_bal, "locked": bool(completed)})
        used = endpos
    return bases, w


def classify(dfd, base, handle):
    depth, weeks = base["depth"], base["weeks"]
    lh, low = base["left_high"], base["low"]
    rng = lh - low
    pre = dfd.loc[:base["start"]].tail(60)
    run = (lh / float(pre["Low"].min()) - 1) * 100 if len(pre) > 15 else 0
    if run >= 90 and depth <= 20 and 3 <= weeks <= 6:
        return "하이 타이트 플래그", "4~8주 +90% 이상 후 3~5주 얖은 조정. 깊이 20% 초과면 플래그가 아님"
    if run >= 60 and depth <= 25 and 2.5 <= weeks <= 8:
        return "짧은 플래그 (HTF 미달)", "선행 상승·깊이·주수가 HTF 정석에 못 미침 — 컵/조정의 짧은 형태"
    seg = dfd.loc[base["start"]:base["end"]]
    if rng > 0 and len(seg) > 20:
        lv = seg["Low"]
        isl = lv == lv.rolling(9, center=True, min_periods=9).min()
        cand = [i for i in np.where(isl.fillna(False).values)[0] if lv.iloc[i] <= low + rng * 0.40]
        merged = []
        for i in cand:
            if merged and i - merged[-1] < 6:
                if lv.iloc[i] < lv.iloc[merged[-1]]:
                    merged[-1] = i
            else:
                merged.append(i)
        if len(merged) >= 2 and merged[-1] - merged[0] >= 8:
            peak = float(seg["High"].iloc[merged[0]:merged[-1] + 1].max())
            tail = float(seg["High"].iloc[merged[-1]:].max())
            if peak >= low + rng * 0.45 and tail >= peak * 0.90 and weeks >= 6:
                return "이중 바닥 (W)", "두 번째 저점이 첫 저점을 살짧 이탈하는 형태가 정석"
    if depth <= 15 and weeks >= 5:
        return "플랫 베이스", "5주 이상 · 깊이 15% 이내. 2차 베이스로 자주 출현"
    if weeks >= 6 and handle is not None:
        return "컵 위드 핸들", "오닐 대표 패턴. 핸들 고점이 피봇"
    if weeks >= 6:
        return "컵 (핸들 미형성)", "핸들 없이 좌측 고점을 바로 치면 실패율 상승"
    if weeks >= 3:
        return "짧은 조정", "정식 베이스 기준(5주) 미달 — 신뢰도 낮음"
    return "베이스 미형성", ""


def _pick_current_base(bases, dfd):
    if not bases:
        return None
    price = float(dfd["Close"].iloc[-1])
    completed = [b for b in bases if b.get("completed")]
    if completed:
        last_c = completed[-1]
        if price >= last_c["low"] * 0.995:
            after = dfd.loc[last_c["end"]:]
            if after.empty:
                last_c = dict(last_c)
                last_c["locked"] = True
                return last_c
            peak = float(after["High"].max())
            trough = float(after["Low"].min())
            retr = (peak - trough) / peak * 100 if peak else 0
            if retr < 8:
                last_c = dict(last_c)
                last_c["locked"] = True
                return last_c
    return bases[-1]


def _buy_trigger(pivot, market):
    try:
        p = float(pivot)
    except Exception:
        return pivot
    if market == "KR":
        return p * 1.001
    return p + 0.10
