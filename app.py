# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v13.9 — fetch v13.1 + FTD/DD + IBD-proxy EPS/RS/hold (conservative) patches."""
from __future__ import annotations

import urllib.request
from pathlib import Path

_SRC_URL = (
    "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/"
    "8d17f376294b2726722485d3dc18212a92904e5e/app.py"
)
_CACHE = Path("/tmp/canslim_v13_9_patched.py")

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

_PATCH_BASE = "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/main/patches/"
_OLD_IDX = "def index_state(idf, min_gain, corr_pct):"
_OLD_STEP7 = "        # STEP 7 종합\n        step_header(\"STEP 7\", \"종합 등급\")"
_OLD_SCEN = "def scenario(binfo, price, market, ma, capital, risk_pct, atrp=None):"
_OLD_S4 = "        # STEP 4 밸류에이션\n        step_header(\"STEP 4\", \"재무 · 밸류에이션\")"
_OLD_S6 = "        # STEP 6 수급 — 한국은 기관/외국인 정밀 수집"
_OLD_URG = '            urgent = [r for r in ok_revs if r["kind"] == "fail"]'


def _fetch(name):
    with urllib.request.urlopen(_PATCH_BASE + name, timeout=45) as r:
        return r.read().decode("utf-8")


def _load():
    if _CACHE.exists() and _CACHE.stat().st_size > 100000:
        src = _CACHE.read_text(encoding="utf-8")
        if "def eps_rating_detail" in src and "STEP 3b" in src and "HOLD RS" in src and "70대 진입 추정" in src:
            return src
    with urllib.request.urlopen(_SRC_URL, timeout=45) as r:
        src = r.read().decode("utf-8")
    if "def naive_ts" not in src:
        src = src.replace("\ndef naive(df):", _HELPER + "def naive(df):", 1)
    if _OLD_EARN in src:
        src = src.replace(_OLD_EARN, _NEW_EARN, 1)
    if _OLD_BTN in src:
        src = src.replace(_OLD_BTN, _NEW_BTN, 1)
    engine = (_fetch("stock_ftd_engine.py") + "\n" + _fetch("stock_ftd_detect.py") + "\n" + _fetch("stock_ftd_review.py") + "\n")
    ui = _fetch("stock_ftd_ui.py")
    ibd_e = _fetch("ibd_proxy_engine.py")
    ibd_eb = _fetch("ibd_proxy_engine_b.py")
    ibd3 = _fetch("ibd_proxy_ui_step3.py")
    ibd5 = _fetch("ibd_proxy_ui_step5.py")
    ibdh = _fetch("ibd_proxy_ui_hold.py")
    if "def stock_distribution_days" not in src and _OLD_IDX in src:
        src = src.replace(_OLD_IDX, engine + _OLD_IDX, 1)
    if "STEP 6.5" not in src and _OLD_STEP7 in src:
        src = src.replace(_OLD_STEP7, ui + "\n" + _OLD_STEP7, 1)
    if "def eps_rating_detail" not in src and _OLD_SCEN in src:
        src = src.replace(_OLD_SCEN, ibd_e + "\n" + ibd_eb + _OLD_SCEN, 1)
    if "STEP 3b" not in src and _OLD_S4 in src:
        src = src.replace(_OLD_S4, ibd3 + _OLD_S4, 1)
    if "70대 진입 추정" not in src and _OLD_S6 in src:
        src = src.replace(_OLD_S6, ibd5 + _OLD_S6, 1)
    if "HOLD RS" not in src and _OLD_URG in src:
        src = src.replace(_OLD_URG, ibdh + _OLD_URG, 1)
    if "def eps_rating_detail" not in src:
        raise RuntimeError("IBD proxy engine patch did not apply")
    if "STEP 3b" not in src:
        raise RuntimeError("IBD STEP 3b patch did not apply")
    if "HOLD RS" not in src:
        raise RuntimeError("IBD HOLD UI patch did not apply")
    _CACHE.write_text(src, encoding="utf-8")
    return src

_src = _load()
exec(compile(_src, str(_CACHE), "exec"), globals(), globals())
