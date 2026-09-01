# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v13.4 — fetch v13.1 monolith, apply tz + journal patches."""
from __future__ import annotations

import urllib.request
from pathlib import Path

_SRC_URL = (
    "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/"
    "8d17f376294b2726722485d3dc18212a92904e5e/app.py"
)
_CACHE = Path("/tmp/canslim_v13_4_patched.py")

_HELPER = '''

def naive_ts(x):
    """어떤 입력이든 tz-naive Timestamp로. 실적일·뉴스 시각 비교용."""
    if x is None:
        return None
    try:
        t = pd.Timestamp(x)
    except Exception:
        return None
    if pd.isna(t):
        return None
    tz = getattr(t, "tz", None)
    if tz is not None:
        try:
            t = t.tz_convert("UTC").tz_localize(None)
        except Exception:
            try:
                t = t.tz_localize(None)
            except Exception:
                pass
    return t

'''

_OLD_EARN = 'd["earn_days"] = int((pd.Timestamp(ne) - pd.Timestamp(datetime.today())).days) if ne is not None else None'
_NEW_EARN = 'd["earn_days"] = int((naive_ts(ne) - naive_ts(datetime.today())).days) if naive_ts(ne) is not None else None'

_OLD_BTN = 'if st.button("일지 종목 불러오기 (WT·NTAP·HNGE)", key="p_seed_blog"):'
_NEW_BTN = 'if st.button("일지 종목 불러오기 (WT·NTAP 보유 / HNGE 8/31 매도)", key="p_seed_blog"):'

_OLD_SEEDS = '''            seeds = [
                {"ticker": "WT", "date": "2026-08-05", "price": 21.715, "qty": 60,
                 "memo": "8/5·8/6 평균 · 방어선 20.0 · 20% 계획 26.06"},
                {"ticker": "NTAP", "date": "2026-08-11", "price": 197.00, "qty": 5,
                 "memo": "거래량 경고 무시 예외 · 방어선 181"},
                {"ticker": "HNGE", "date": "2026-08-20", "price": 87.84, "qty": 15,
                 "memo": "피벗 전 진입 예외 · 방어선 80.8"},
            ]'''

_NEW_SEEDS = '''            seeds = [
                {"ticker": "WT", "date": "2026-08-05", "price": 21.715, "qty": 60,
                 "memo": "8/5·8/6 평균 · 방어선 20.0 · 20% 계획 26.06 · 8/28 신고가 분산 1회"},
                {"ticker": "NTAP", "date": "2026-08-11", "price": 197.00, "qty": 5,
                 "memo": "가짜돌파 예외 · 방어 181 · 피벗 192.35 · 스트리트 목표 189.19(8/31) · C 25% 미달 · 추가금지"},
            ]
            closed_seed = {
                "id": "HNGE-SEED-2026-08-20",
                "ticker": "HNGE", "date": "2026-08-20", "price": 87.8367,
                "qty": 15, "sell_date": "2026-08-31", "sell_price": 91.53,
                "pnl": 52.96, "ret": 4.01,
                "memo": "피벗 전 예외 청산 · 8/27 피벗 도달 다음날 대량 하락 후 8/31 반등에서 정리",
            }'''

_OLD_HAVE = '''            have = {(x.get("ticker"), str(x.get("date")), float(x.get("price") or 0))
                    for x in port["open"]}
            added = 0
            for sd in seeds:
                key = (sd["ticker"], sd["date"], sd["price"])
                if key in have:
                    continue
                port["open"].append({"id": f'{sd["ticker"]}-SEED-{sd["date"]}', **sd})
                added += 1
            save_portfolio(port)
            if added:
                st.success(f"일지 종목 {added}건을 추가했습니다. 시세는 자동 갱신됩니다.")
            else:
                st.info("이미 들어 있는 일지 종목입니다.")'''

_NEW_HAVE = '''            have = {(x.get("ticker"), str(x.get("date")), float(x.get("price") or 0))
                    for x in port["open"]}
            added = 0
            for sd in seeds:
                key = (sd["ticker"], sd["date"], sd["price"])
                if key in have:
                    continue
                port["open"].append({"id": f'{sd["ticker"]}-SEED-{sd["date"]}', **sd})
                added += 1
            have_c = {x.get("id") for x in port.get("closed") or []}
            if closed_seed["id"] not in have_c:
                port.setdefault("closed", []).append(closed_seed)
                added += 1
            port["open"] = [x for x in port["open"]
                            if not (str(x.get("ticker","")).upper() == "HNGE"
                                    and str(x.get("date","")).startswith("2026-08-20"))]
            save_portfolio(port)
            if added:
                st.success(f"일지 {added}건 반영 · WT·NTAP 보유, HNGE는 8/31 매도 기록")
            else:
                st.info("이미 들어 있는 일지 종목입니다.")'''


def _load() -> str:
    if _CACHE.exists() and _CACHE.stat().st_size > 100000:
        src = _CACHE.read_text(encoding="utf-8")
        if "def naive_ts" in src and _OLD_EARN not in src and "closed_seed" in src:
            return src
    with urllib.request.urlopen(_SRC_URL, timeout=45) as r:
        src = r.read().decode("utf-8")
    if "def naive_ts" not in src:
        src = src.replace("\ndef naive(df):", _HELPER + "def naive(df):", 1)
    if _OLD_EARN in src:
        src = src.replace(_OLD_EARN, _NEW_EARN, 1)
    if _OLD_BTN in src:
        src = src.replace(_OLD_BTN, _NEW_BTN, 1)
    if _OLD_SEEDS in src:
        src = src.replace(_OLD_SEEDS, _NEW_SEEDS, 1)
    if _OLD_HAVE in src:
        src = src.replace(_OLD_HAVE, _NEW_HAVE, 1)
    if _OLD_EARN in src:
        raise RuntimeError("earn_days patch did not apply")
    if "def naive_ts" not in src:
        raise RuntimeError("naive_ts helper did not apply")
    if "closed_seed" not in src:
        raise RuntimeError("journal v13.4 seed patch did not apply")
    _CACHE.write_text(src, encoding="utf-8")
    return src

_src = _load()
exec(compile(_src, str(_CACHE), "exec"), globals(), globals())
