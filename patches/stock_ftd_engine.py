# 엔진 ①-b 개별종목 FTD · 분산일 (매도일) — 공부용 인라인
# -----------------------------------------------------------------------------
# 오닐 원전에서 FTD·분산일은 "지수(M)" 도구다.
# 종목에 그대로 이식하면 문텀이 너무 낮아 매일 분산일로 찍힌다.
# 그래서 논리(저점→4일→대량 양봉 / 음봉+거래량 증가 / +5% 만료)는 같고
# 문텀만 종목 변동성에 맞게 올린다.
#
# 절대 규칙: 종목 FTD는 "이 종목의 조정이 끝났다"는 힌트일 뿐,
#            시장 FTD(M)를 대체하지 않는다. M이 죽으면 종목 FTD로 추격하지 않는다.
# ════════════════════════════════════════════════════════════════════════════
def stock_distribution_days(df, lookback=25, min_drop=0.5, expire_up=0.05):
    """종목 분산일(매도일) 목록.

    판정 (한 줄): 종가 하락폭 >= min_drop%  AND  당일 거래량 > 전일 거래량.
    만료: 현재가가 그 분산일 종가 × (1+expire_up) 위로 올라가면 카운트에서 제외.
          기관 매도가 '소화'됐다는 오닐의 +5% 만료 규칙과 같다.

    문텀을 나누는 이유
    - 지수 원전 min_drop=0.2 : 지수는 하루에 0.3%만 빼져도 의미가 있다.
    - 종목 기본 min_drop=0.5 : 성장주는 평소에도 1%씩 흔들린다.
    - 호출부에서 classic(0.2)과 stock(0.5)을 같이 보여 공부할 수 있게 한다.

    해석 스케일 (25거래일 창, 만료 후 잔여)
    0~2개  정상 차익실현. 상승세 유지.
    3~4개  압박. 신규 추격 금지, 손절을 숫자로 다시 적는다.
    5개+   분산 캠페인. 보유는 방어, 추가는 없다.
    """
    if df is None or len(df) < 5 or "Volume" not in df.columns:
        return []
    d = df.tail(lookback + 1).copy()
    if d["Volume"].isna().all():
        return []
    d["chg"] = d["Close"].pct_change() * 100
    last = float(d["Close"].iloc[-1])
    out = []
    for i in range(1, len(d)):
        chg = d["chg"].iloc[i]
        vol, pvol = d["Volume"].iloc[i], d["Volume"].iloc[i - 1]
        if pd.isna(chg) or pd.isna(vol) or pd.isna(pvol):
            continue
        if chg <= -abs(min_drop) and vol > pvol:
            close_i = float(d["Close"].iloc[i])
            expired = last >= close_i * (1.0 + expire_up)
            rng = float(d["High"].iloc[i] - d["Low"].iloc[i]) if "High" in d.columns else np.nan
            close_loc = (float(d["Close"].iloc[i] - d["Low"].iloc[i]) / rng) if rng and rng > 0 else np.nan
            out.append({
                "date": d.index[i],
                "chg": float(chg),
                "close": close_i,
                "vol": float(vol),
                "vol_vs_prev": float(vol / pvol) if pvol else np.nan,
                "expired": bool(expired),
                "close_loc": float(close_loc) if close_loc == close_loc else None,
            })
    return out
