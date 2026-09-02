# 엔진 ⑤-b2 RS·선도·보유 순위 (보수 조정) — 다음 수정 시 IBD_ADJ와 같이 고쳐라
# 3) RS: IBD 12개월 상대수익 백분위. 앱 0.4×3M+0.2×(6+9+12). 주도 문택 90→87.
# 4) RS선: 주가÷벤치 6M·12M 기울기. 둘 다 음수면 절대 매수 금지.
# 5) 80~90→70 첫 하락: 시계열 없음. 현재 70~79 + 3M이 6M보다 5%p 약 + 6M 기울기 음수.
# 6) 업종 RS: 미국 섹터 ETF 6M 상위 5만 선도 산업군. 한국은 유도하지 않음.
# 7) FTD 이후 선도: 시장 FTD 확정(45일 안) + 52주고 -5% + RS 80+.
# 8) 반시장 상승: 벤치 -1.2% 이하인 날 종목 +1.0% 이상.
# 9) 매도 순위: 계좌 안 1개월·1분기 수익률 오름차순. 약한 것 먼저.


def rs_line_slopes(line):
    if line is None or len(line) < 70:
        return {"s3": None, "s6": None, "s12": None}

    def sl(n):
        if len(line) <= n:
            return None
        a, b = float(line.iloc[-n - 1]), float(line.iloc[-1])
        if a == 0:
            return None
        return (b / a - 1) * 100

    return {"s3": sl(63), "s6": sl(126), "s12": sl(252)}


def rs_proxy_flags(rating, rets, slopes):
    r3 = _g((rets or {}).get("r3"))
    r6 = _g((rets or {}).get("r6"))
    s6, s12 = slopes.get("s6"), slopes.get("s12")
    elite = rating is not None and rating >= 87
    pass80 = rating is not None and rating >= 80
    trend_down = (s6 is not None and s6 < 0) and (s12 is not None and s12 < 0)
    drop70 = (rating is not None and 70 <= rating <= 79
              and r3 is not None and r6 is not None and r3 <= r6 - 5
              and s6 is not None and s6 < 0)
    flags = []
    if elite:
        flags.append(("RS 87+ 주도 후보", "pass",
                      "IBD는 90+ 선호. 앱 유니버스가 작아 87로 낮춤"))
    elif pass80:
        flags.append(("RS 80+ 통과", "pass", "오닐 최소선. 돌파 품질은 90에 가까울수록 좋다"))
    if trend_down:
        flags.append(("RS선 6·12개월 하락 · 절대 매수 금지", "fail",
                      f"6M {s6:+.1f}% / 12M {s12:+.1f}%"))
    if drop70:
        flags.append(("RS 70대 진입 추정 · 추가 매수 금지", "fail",
                      "80~90권에서 내려온 대용. 첫 70대에서 물타지 않는다"))
    if rating is not None and rating < 70:
        flags.append(("RS 70 미만 · 후보 제외", "fail", "오닐은 80 미만을 빨라고 했다"))
    return {"elite": elite, "pass80": pass80, "trend_down": trend_down, "drop70": drop70,
            "buy_ban": bool(trend_down),
            "add_ban": bool(drop70 or trend_down or (rating is not None and rating < 80)),
            "flags": flags, "s6": s6, "s12": s12}


def contra_thrust_days(df, bench, lookback=80):
    if df is None or bench is None or len(df) < 30:
        return []
    j = df[["Close", "Volume"]].join(
        bench[["Close"]].rename(columns={"Close": "Ix"}), how="inner")
    if len(j) < 20:
        return []
    j = j.tail(lookback + 1).copy()
    j["s"] = j["Close"].pct_change() * 100
    j["i"] = j["Ix"].pct_change() * 100
    j["vup"] = j["Volume"] > j["Volume"].shift(1)
    out = []
    for dt, row in j.iloc[1:].iterrows():
        if row["i"] <= -1.2 and row["s"] >= 1.0:
            out.append({"date": dt, "stock": float(row["s"]), "idx": float(row["i"]),
                        "vol_up": bool(row["vup"])})
    return out[-8:]


def ftd_leader_tag(ctx, rating, gap52):
    states = (ctx or {}).get("states") or {}
    confirmed = []
    for nm, s in states.items():
        f = s.get("ftd") or {}
        if f.get("state") == "confirmed" and (f.get("since") or 99) <= 45:
            confirmed.append((nm, f.get("since"), f.get("date")))
    if not confirmed:
        return None
    nm, since, dt = sorted(confirmed, key=lambda x: x[1] or 99)[0]
    near = gap52 is not None and gap52 >= -5
    strong = rating is not None and rating >= 80
    if near and strong:
        return {"kind": "pass", "label": "FTD 이후 선도 신고가권",
                "why": f"{nm} FTD 후 {since}일 · 52주 고점 {gap52:+.1f}% · RS {rating}"}
    if near:
        return {"kind": "warn", "label": "FTD 이후 고점권 (RS 미달)",
                "why": f"{nm} FTD 후 {since}일 · 고점은 가깝지만 RS가 선도를 확인 못 함"}
    return {"kind": "idle", "label": "시장 FTD는 유효 · 이 종목은 아직 후행",
            "why": f"{nm} FTD 후 {since}일 · 선도는 신고가를 먼저 만든다"}


def period_ret(df, n):
    if df is None or len(df) <= n:
        return None
    a, b = float(df["Close"].iloc[-n - 1]), float(df["Close"].iloc[-1])
    if a == 0:
        return None
    return (b / a - 1) * 100


def rank_holdings_by_period(ok_revs):
    rows = []
    for r in ok_revs:
        df = None
        try:
            df, _, _, _ = load_price(r["ticker"])
        except Exception:
            df = None
        rows.append({**r, "m1": period_ret(df, 21), "q1": period_ret(df, 63)})

    def km(x):
        return 999 if x["m1"] is None else x["m1"]

    def kq(x):
        return 999 if x["q1"] is None else x["q1"]

    by_m = sorted(rows, key=km)
    by_q = sorted(rows, key=kq)
    rm = {id(x): i + 1 for i, x in enumerate(by_m)}
    rq = {id(x): i + 1 for i, x in enumerate(by_q)}
    out = []
    for x in rows:
        out.append({**x, "rank_m": rm[id(x)], "rank_q": rq[id(x)],
                    "sell_first": rm[id(x)] == 1 or rq[id(x)] == 1})
    return sorted(out, key=lambda z: (z["rank_m"], z["rank_q"]))


def ca_rs_opinion(h, df, market, uni, bench, fnd=None):
    rating, rets = rs_rating(df, uni) if df is not None else (None, {})
    line, _ = (rs_line(df, bench) if (df is not None and bench is not None) else (None, None))
    sl = rs_line_slopes(line)
    flags = rs_proxy_flags(rating, rets, sl)
    q_g = y_g = roe = None
    if fnd:
        q_g = growth_pct(fnd.get("q_eps"), fnd.get("q_eps_prev"))
        y_g = growth_pct(fnd.get("y_eps"), fnd.get("y_eps_prev2"))
        roe = _g(fnd.get("roe"))
    c_ok = q_g is not None and (q_g == 999 or q_g >= 25)
    a_ok = (y_g is not None and (y_g == 999 or y_g >= 25)) or (roe or 0) >= 17
    snap = (h or {}).get("snap") or {}
    notes = []
    if c_ok:
        notes.append(f"C 유지 (분기 EPS {pct(q_g)})")
    elif q_g is not None:
        notes.append(f"C 약화 (분기 EPS {pct(q_g)} · 25% 미달)")
    else:
        notes.append("C 미수집")
    if a_ok:
        notes.append(f"A 유지 (연 EPS {pct(y_g)} · ROE {pct(roe, 0, False)})")
    else:
        notes.append(f"A 약화 (연 EPS {pct(y_g)} · ROE {pct(roe, 0, False)})")
    if rating is not None:
        notes.append(f"RS {rating}")
        if snap.get("rs") is not None:
            dlt = rating - int(snap["rs"])
            notes.append(f"매수 시점 RS {int(snap['rs'])} → {rating} ({dlt:+d})")
    for lab, k, _w in flags["flags"]:
        if k == "fail":
            notes.append(lab)
    if flags["trend_down"]:
        opinion, kind = "상대강도 추세 하락 · 추가 매수 금지. 보유는 방어선만 본다.", "fail"
    elif flags["drop70"]:
        opinion, kind = "RS 70대 진입 추정 · 절대로 추가 매수하지 않는다.", "fail"
    elif (not c_ok) and (not a_ok):
        opinion, kind = "C·A 동시 약화 · 비중 축소·매도 순위를 본다.", "fail"
    elif not c_ok:
        opinion, kind = "C가 먼저 죽었다. 차트를 느슨하게 보지 않는다.", "warn"
    elif flags["elite"] and c_ok and a_ok:
        opinion, kind = "C·A·RS가 같이 버티는 자리. 추격만 하지 않으면 보유 유지.", "pass"
    else:
        opinion, kind = "누적 점수는 관리 구간. 피벗·방어선을 숫자로 유지한다.", "idle"
    new_snap = {"rs": rating, "c": q_g, "a": y_g, "roe": roe,
                "at": str(datetime.today().date())}
    return {"rating": rating, "q_g": q_g, "y_g": y_g, "roe": roe,
            "c_ok": c_ok, "a_ok": a_ok, "flags": flags, "notes": notes,
            "opinion": opinion, "kind": kind, "snap": new_snap, "old_snap": snap}
