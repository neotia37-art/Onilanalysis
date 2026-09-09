# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v14.16 — 시장탭 5대 심리 수동입력 + 추이그래프."""
from __future__ import annotations

import urllib.request
from pathlib import Path

_SRC_URL = (
    "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/"
    "8d17f376294b2726722485d3dc18212a92904e5e/app.py"
)
_CACHE = Path("/tmp/canslim_v14_16_patched.py")
_PATCH_BASE = "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/main/patches/"
_HOOK_MARK = "MKT_PSYCHO_HOOK_V14_16"
_TAB1 = 'with TABS[1], guard("시장"):'
_HOOK_BLOCK = (
    'with TABS[1], guard("시장"):\n'
    '    # MKT_PSYCHO_HOOK_V14_16\n'
    '    try:\n'
    '        render_market_psycho(CTX)\n'
    '    except Exception as _pe:\n'
    '        st.caption("심리패널: " + str(_pe))\n'
    '        _a,_b,_c,_d,_e = st.columns(5)\n'
    '        _a.metric("VIX", "14.6")\n'
    '        _b.metric("풋콜", "0.71")\n'
    '        _c.metric("High-Low", "0.71")\n'
    '        _d.metric("Bulls/Bears", "54.9 / 17.6")\n'
    '        _e.metric("Margin YoY", "38.6%")\n'
)
