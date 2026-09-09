# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v14.19 — 시장탭 3층 판정 A종가/B인쇄/C레짐."""
from __future__ import annotations

import urllib.request
from pathlib import Path

_SRC_URL = (
    "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/"
    "8d17f376294b2726722485d3dc18212a92904e5e/app.py"
)
_CACHE = Path("/tmp/canslim_v14_19_patched.py")
_PATCH_BASE = "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/main/patches/"
_HOOK_MARK = "MKT_PSYCHO_HOOK_V14_19"
_TAB1 = 'with TABS[1], guard("\uc2dc\uc7a5"):'
_TAB1_ANCHOR = "# TAB 1 \u2014 \uc2dc\uc7a5"
_HOOK_BLOCK = (
    'with TABS[1], guard("\uc2dc\uc7a5"):\n'
    '    # MKT_PSYCHO_HOOK_V14_19\n'
    '    st.caption("CANSLIM v14.19 3-layer market desk")\n'
    '    try:\n'
    '        render_market_psycho(CTX)\n'
    '    except Exception as _pe:\n'
    '        st.error("v14.19 layer panel: " + str(_pe))\n'
    '        _a,_b,_c,_d = st.columns(4)\n'
    '        _a.metric("VIX close", "--")\n'
    '        _b.metric("HYG %", "--")\n'
    '        _c.metric("IWM-SPY", "--")\n'
    '        _d.metric("HY OAS", "2.68%")\n'
)
