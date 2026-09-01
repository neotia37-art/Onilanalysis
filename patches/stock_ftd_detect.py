def detect_stock_ftd(df, min_gain=1.5, corr_pct=8.0, lookback=260):
    """종목 Follow-Through Day. 지수 FTD와 같은 뼈대. corr -8%, +1.5%, day>=4, vol>prev."""
    empty = {"state": "no_data", "date": None, "low_date": None, "checks": []}
    if df is None or len(df) < 30:
        return empty
    d = df.tail(lookback).copy()
    d["chg"] = d["Close"].pct_change() * 100
    novol = d["Volume"].isna().all()
    dd = (d["Close"] / d["Close"].cummax() - 1) * 100
    below = (dd <= -abs(corr_pct)).values
    if not below.any():
        return {"state": "no_correction", "max_dd": float(dd.min()), "date": None,
                "cur_dd": float(dd.iloc[-1]), "low_date": None, "quality": None,
                "checks": [("조정 존재 (-8% 이상)", False, f'최대 낙폭 {float(dd.min()):+.1f}%')]}
    s = int(np.where(below)[0][-1])
    while s > 0 and dd.values[s - 1] < -0.5:
        s -= 1
    low_pos = s + int(np.argmin(d["Close"].values[s:]))
    low_close = float(d["Close"].iloc[low_pos])
    vma50 = d["Volume"].rolling(50).mean()
    ftd, i = None, low_pos + 1
    while i < len(d):
        if d["Close"].iloc[i] < low_close:
            low_pos, low_close = i, float(d["Close"].iloc[i])
            i += 1
            continue
        n = i - low_pos + 1
        volok = True if novol else bool(d["Volume"].iloc[i] > d["Volume"].iloc[i - 1])
        if n >= 4 and d["chg"].iloc[i] >= min_gain and volok:
            v50 = float(vma50.iloc[i]) if i < len(vma50) and not pd.isna(vma50.iloc[i]) else np.nan
            vol = float(d["Volume"].iloc[i]) if not pd.isna(d["Volume"].iloc[i]) else np.nan
            above_avg = bool(vol == vol and v50 == v50 and vol >= v50)
            quality = "prime" if 4 <= n <= 7 and above_avg else ("late" if 8 <= n <= 10 else "weak")
            ftd = {"date": d.index[i], "gain": float(d["chg"].iloc[i]), "day": n,
                   "low_date": d.index[low_pos], "low_close": low_close,
                   "vol_vs_prev": (float(d["Volume"].iloc[i] / d["Volume"].iloc[i - 1]) if not novol and d["Volume"].iloc[i - 1] else np.nan),
                   "vol_vs_avg50": (float(vol / v50) if vol == vol and v50 == v50 and v50 else np.nan),
                   "quality": quality}
            break
        i += 1
    if ftd is None:
        return {"state": "rally_attempt", "low_date": d.index[low_pos], "date": None,
                "low_close": low_close, "rally_day": int(len(d) - low_pos),
                "max_dd": float(dd.min()), "cur_dd": float(dd.iloc[-1]), "quality": None,
                "checks": [("조정 존재", True, f'저점 {d.index[low_pos]:%Y-%m-%d} {low_close:.2f}'),
                            ("저점 후 4일+", len(d) - low_pos >= 4, f'램리 {len(d) - low_pos}일차'),
                            ("FTD 양봉+거래량", False, "아직 조건 미충족")]}
    post = d.loc[ftd["date"]:]
    failed = bool((post["Close"] < ftd["low_close"]).any())
    ftd.update({"state": "failed" if failed else "confirmed",
                "since": int((d.index[-1] - ftd["date"]).days),
                "ret_since": float(d["Close"].iloc[-1] / d.loc[ftd["date"], "Close"] - 1) * 100,
                "max_dd": float(dd.min()), "cur_dd": float(dd.iloc[-1]),
                "checks": [("조정 존재 (-8% 이상)", True, f'최대 낙폭 {float(dd.min()):+.1f}%'),
                            ("저점 후 4일+", ftd["day"] >= 4, f'{ftd["day"]}일차'),
                            (f'당일 +{min_gain:.1f}% 이상', ftd["gain"] >= min_gain, f'{ftd["gain"]:+.2f}%'),
                            ("거래량 > 전일", True, f'{ftd.get("vol_vs_prev") or 0:.2f}배'),
                            ("거래량 ≥ 50일평균 (품질)", (ftd.get("vol_vs_avg50") or 0) >= 1.0, f'{ftd.get("vol_vs_avg50") or 0:.2f}배'),
                            ("이후 저점 유지", not failed, "저점 이탈 → FTD 무효" if failed else "저점 유지")]})
    return ftd
