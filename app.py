# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v13.6 — fetch v13.1 monolith, apply tz + journal + stock FTD/DD study patches."""
from __future__ import annotations

import urllib.request
from pathlib import Path

_SRC_URL = (
    "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/"
    "8d17f376294b2726722485d3dc18212a92904e5e/app.py"
)
_CACHE = Path("/tmp/canslim_v13_6_patched.py")

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
