
def analyze_base(dfd, market, zp=8.0):
    bases, w = build_bases(dfd, zp)
    if not bases:
        return None
    bases = count_bases(bases)
    cur = _pick_current_base(bases, dfd)
    handle = detect_handle(dfd, cur) if not cur["completed"] else None
    btype, note = classify(dfd, cur, handle)
    flaws = base_flaws(cur, handle, btype)
    if handle is None and ("핸들 미형성" in (btype or "") or cur.get("completed")):
        if not any(x[0] == "핸들 미형성" for x in flaws):
            flaws.append(("핸들 미형성", "없음", "핸들 후 돌파가 정석 — 없으면 가짜돌파 기본값"))
    if btype == "짧은 플래그 (HTF 미달)":
        flaws.append(("HTF 미달", btype, "선행 +90%·깊이 ≤20%·3~5주"))
    if cur.get("count", 1) >= 3:
        if not any(x[0] == "후기 베이스" for x in flaws):
            flaws.append(("후기 베이스", f'{cur.get("count")}차', "1~2차만 신규"))
    if handle and handle["ok_depth"] and handle["ok_pos"] and not handle["wedge"]:
        pv_raw, pv_src = handle["high"], "핸들 고점"
    else:
        pv_raw, pv_src = cur["left_high"], "베이스 좌측 고점(일봉 High)"
    pivot = float(pv_raw)
    buy_px = float(_buy_trigger(pivot, market))
    price = float(dfd["Close"].iloc[-1])
    gap = (price / pivot - 1) * 100 if pivot else 0.0
    gap_buy = (price / buy_px - 1) * 100 if buy_px else gap
    since_end = (dfd.index[-1] - pd.Timestamp(cur["end"])).days
    ma50 = dfd["Close"].rolling(50).mean()
    vs50 = None
    try:
        vs50 = (price / float(ma50.iloc[-1]) - 1) * 100
    except Exception:
        vs50 = None
    if cur["completed"] and since_end > 5:
        stage, kind = "직전 베이스 돌파 완료 — 신규 매수 구간 아님", "fail"
    elif vs50 is not None and vs50 >= 15:
        stage, kind = "50일선 +15% 이상 — IBD 추격 금지", "fail"
        flaws.append(("50일선 이격", f"{vs50:.1f}%", "피벗 0~5% 또는 50일 근처"))
    elif gap_buy < -10:
        stage, kind = "베이스 형성 중 — 관망", "idle"
    elif gap_buy < -1:
        stage, kind = "피봇 접근 — 돌파 대기", "warn"
    elif gap_buy <= 5:
        stage, kind = "매수 가능 구간", "pass"
    else:
        stage, kind = "연장(Extended) — 추격 금지", "fail"
    vma = dfd["Volume"].rolling(50).mean()
    bo_day, bo_vol = None, None
    look = dfd.loc[cur["low_date"]:]
    if len(look) >= 2:
        for i in range(1, len(look)):
            prev_c = float(look["Close"].iloc[i - 1])
            cur_c = float(look["Close"].iloc[i])
            if cur_c > pivot >= prev_c:
                bo_day = look.index[i]
                try:
                    v = float(vma.loc[bo_day])
                except Exception:
                    v = np.nan
                if v and v == v and v > 0:
                    bo_vol = float(look["Volume"].iloc[i]) / v
                else:
                    bo_vol = np.nan
                break
    fake_bo = bool(bo_day is not None and (bo_vol is None or (isinstance(bo_vol, float) and (np.isnan(bo_vol) or bo_vol < 1.4))))
    if fake_bo:
        if not any(x[0].startswith("돌파 거래량") for x in flaws):
            flaws.append(("돌파 거래량 부족", f'{bo_vol:.2f}배' if bo_vol == bo_vol else "—",
                          "50일 평균 +40%(1.4배) — 구간이어도 보류"))
        stage, kind = "거래량 부족 돌파 — 가짜돌파 위험 (보류)", "warn"
    elif handle is None and kind == "pass":
        stage, kind = "매수 가능 구간 · 핸들 없음 (포지션 축소)", "warn"
    if cur.get("locked") and cur.get("completed") and kind == "pass":
        stage, kind = "잠긴 피벗 — 이미 돌파됨 · 신규 금지", "fail"
    if cur.get("count", 1) >= 3 and kind == "pass":
        stage, kind = "3차 이상 후기 베이스 — 신규 금지", "fail"
    wins, tries = 0, 0
    for b in bases[:-1]:
        if not b["completed"]:
            continue
        after = dfd.loc[b["end"]:].head(120)
        if len(after) < 10:
            continue
        tries += 1
        if float(after["Close"].max()) / b["left_high"] - 1 >= 0.20:
            wins += 1
    return {"bases": bases, "cur": cur, "handle": handle, "type": btype, "note": note,
            "flaws": flaws, "pivot": pivot, "buy_px": buy_px, "pivot_src": pv_src,
            "gap": gap, "gap_buy": gap_buy, "stage": stage,
            "kind": kind, "bo_day": bo_day, "bo_vol": bo_vol, "fake_bo": fake_bo,
            "weekly": w, "win": (wins, tries), "vs50": vs50,
            "locked": bool(cur.get("locked"))}


def _num(x):
    if x is None or x == "":
        return None
    try:
        return float(str(x).replace("%", "").replace("+", "").replace(",", "").strip())
    except Exception:
        return None


def _ad_letter(x):
    s = str(x or "").upper().replace(" ", "")
    if not s:
        return ""
    return s[:2] if s[:2] in ("A+", "B+", "C+", "D+", "E+") else s[:1]


def _lookup_checkup(tk, desk):
    if not tk:
        return None
    fn = globals().get("checkup_for")
    if callable(fn) and desk is not None:
        try:
            chk = fn(tk, desk)
            if chk:
                return chk
        except Exception:
            pass
    if not desk:
        return None
    try:
        rows = list((desk.get("checkups") or {}).get(str(tk).upper()) or [])
        rows.sort(key=lambda x: str(x.get("date") or ""))
        return rows[-1] if rows else None
    except Exception:
        return None
