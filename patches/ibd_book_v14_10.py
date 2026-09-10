# v14.11 chart read: IBD daily/weekly 20260907 WT PBF + NASDAQ/S&P
CHART_READ_V14_10 = True
CHART_READ_V14_11 = True
BOOK_REV_CHART_20260904 = 11

CHART_READ_20260904 = {
    "WT": {
        "date": "2026-09-07",
        "source": "20260904_WT_IBD Charts + 주봉 PDF (print 09/07/2026 Market Close)",
        "print": "Sep 07, 2026 Market Closed",
        "price": 24.89,
        "chg": 0.08,
        "rs_line": 96,
        "vol": 2.1,
        "vol_vs_50": -21,
        "vol_50": 2.7,
        "off52": -4,
        "weekly_chg": 1.88,
        "weekly_vol_vs_10w": 85,
        "weekly_vol": 13.0,
        "base": "6~7월 17~20 선반(플랫) 후 8월 초 19.92 부근 돌파. 지금은 피벗 +25% 연장. 정석 3주 밀착 아님. 2단계 후반.",
        "dd": "8/28 고가 25.89 음봉이 종목 분산 후보. 이후 24.4~25.9 횯보. 9/7 거래량 2.1M = 50일 2.7M 대비 -21%라 최근 하락봉은 분산 캠페인 아님.",
        "weekly": "10주선 위. 주 거래량 +85% vs 10주(13.0/12.5M). 주봉 종가가 10주를 깨지 않음. RS 96.",
        "action": "보유 유지 · 추가 금지. 익절 26.06 종가. 방어는 10주선 종가 + 대량 이탈.",
        "add_ban": True,
        "sell_now": False,
    },
    "PBF": {
        "date": "2026-09-07",
        "source": "20260904_PBF_IBD Charts + 주봉 PDF (print 09/07/2026 Market Close)",
        "print": "Sep 07, 2026 Market Closed",
        "price": 74.34,
        "chg": -1.31,
        "rs_line": 99,
        "vol": 1.9,
        "vol_vs_50": -40,
        "vol_50": 3.1,
        "off52": -5,
        "weekly_chg": 4.29,
        "weekly_vol_vs_10w": 85,
        "weekly_vol": 15.5,
        "base": "7월 40대 선반 돌파 후 수직. 8/20~25 66까지 흔들린 뒤 V회복. 정석 베이스 아님. 후기 2단계·고점권.",
        "dd": "고점 77.94(9/2) 날은 거래량 평균 근처. 9/7 -1.31%는 1.9M vs 50일 3.1M(-40%)라 종목 분산일 아님(거래량 감소 음봉).",
        "weekly": "10주선 위(+14%대). 주봉 +4.29%·주거래량 +85%. 몸체가 커서 3주밀착 아님. 사이클 고점권.",
        "action": "추가 금지. SMR D. 방어 69.4 또는 21일 대량 이탈. 10주 종가 하향은 종료.",
        "add_ban": True,
        "sell_now": False,
    },
}

INDEX_CHART_READ_20260907 = {
    "date": "2026-09-07",
    "source": "20260904 NASDAQ/S&P IBD daily+weekly Charts, print 09/07/2026 Market Close",
    "nasdaq": {
        "close": 26506.99,
        "vol_bil": 6.5,
        "vol_vs_50": -18.6,
        "vol_50_bil": 8.3,
        "off52": -3,
        "weekly_vol_vs_10w": -4,
        "weekly_vol_bil": 39.6,
        "structure": "4월 급락 후 5~6월 램리. Pulse FTD 2026-06-02. 7월 중순 거래량 스파이크와 흔들림, 8월 50일선 회복, 9월 고점 밑 밀착.",
        "tape": "9/7 거래량 6.5B < 50일 8.3B. 평균 아래 테이프라 최근 소폭 음봉을 분산일로 키우면 안 된다.",
    },
    "spx": {
        "close": 7718.60,
        "vol_bil": 4.1,
        "vol_vs_50": -15.9,
        "vol_50_bil": 5.1,
        "off52": -1,
        "weekly_vol_vs_10w": -3,
        "weekly_vol_bil": 24.4,
        "structure": "나스닥보다 52주 고점 근접(-1%). 50일·10주선 위. 같은 6월 FTD 이후 8월 재가속.",
        "tape": "9/7 거래량 4.1B < 50일 5.1B. 고점 유지만 있고 대량 분산 캠페인 모습은 아님.",
    },
    "pulse_anchor": {
        "date": "2026-09-03",
        "dist_nasdaq": 4,
        "dist_spx": 3,
        "ftd": "2026-06-02",
        "exposure": "60%-80%",
    },
    "hand_verdict": {
        "2026-08-18": "아님-QQQ프록시",
        "2026-08-20": "후보-지수거래량(QQQ는 놓침)",
        "2026-08-24": "아님-QQQ프록시",
        "2026-09-01": "아님-QQQ프록시",
        "2026-09-04": "아님-평균아래·프록시과대",
    },
}

def apply_chart_read(binfo, tk=None, desk=None):
    if not binfo:
        return binfo
    key = str(tk or "").upper()
    rec = CHART_READ_20260904.get(key)
    if desk:
        rec = ((desk.get("lists") or {}).get("chart_read_20260904") or CHART_READ_20260904).get(key) or rec
    if not rec:
        return binfo
    binfo["chart_read"] = rec
    flaws = list(binfo.get("flaws") or [])
    flaws.append(("IBD차트판독", rec.get("base") or "", rec.get("action") or ""))
    if rec.get("dd"):
        flaws.append(("종목분산", rec.get("dd"), ""))
    if rec.get("add_ban"):
        flaws.append(("추가매수", "금지", "연장·고점권"))
    binfo["flaws"] = flaws
    return binfo

_ensure_book_seed_chart_prev = ensure_book_seed

def ensure_book_seed(desk):
    desk = _ensure_book_seed_chart_prev(desk)
    lists = desk.setdefault("lists", {})
    lists["chart_read_20260904"] = CHART_READ_20260904
    lists["index_chart_read_20260907"] = INDEX_CHART_READ_20260907
    PULSE_20260909 = {
        "date": "2026-09-09",
        "source": "MP090926.jpg",
        "headline": "Stocks drop as oil, rates rise",
        "exposure": "60%-80%",
        "dist_nasdaq": 5,
        "dist_spx": 4,
        "leaders_up": ["CHYM", "NET", "HPE", "TNK"],
        "leaders_down": ["DLTR", "XP", "LIFE", "KSPI", "NAVN"],
        "ftd": "2026-06-02",
        "market_score": 60,
        "note": "공식 분산 NAS 5 / SPX 4. 수요일 하락+거래량감소라 그날은 분산 아님. 새 FTD 없음. 추격 0.",
    }
    lists["market_pulse_20260909"] = PULSE_20260909
    cur = lists.get("market_pulse_latest") or {}
    if str(cur.get("date") or "") < "2026-09-09":
        lists["market_pulse_latest"] = dict(PULSE_20260909)
    notes = desk.setdefault("notes", {})
    for tk, rec in CHART_READ_20260904.items():
        body = (f'{rec.get("date")} IBD일·주봉. {rec.get("base")} {rec.get("dd")} '
                f'{rec.get("weekly")} → {rec.get("action")}')
        bucket = notes.setdefault(tk, [])
        if not any("IBD일·주봉" in str(x.get("text") or x.get("note") or x.get("body") or "")
                   and str(x.get("date")) in (rec["date"], "2026-09-04", "2026-09-07")
                   for x in bucket):
            bucket.append({"date": rec["date"], "text": body, "body": body, "source": rec.get("source")})
    try:
        save_ibd_desk(desk)
    except Exception:
        pass
    return desk
