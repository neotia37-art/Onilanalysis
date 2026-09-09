# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v14.14 — force-call IBD 5 psycho on 시장 tab."""
from __future__ import annotations

import urllib.request
from pathlib import Path

_SRC_URL = (
    "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/"
    "8d17f376294b2726722485d3dc18212a92904e5e/app.py"
)
_CACHE = Path("/tmp/canslim_v14_14_patched.py")
_PATCH_BASE = "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/main/patches/"
_HOOK_MARK = "MKT_PSYCHO_HOOK_V14_14"
_HOOK_BLOCK = (
    '        try:\n'
    '            render_market_live(CTX)  # MKT_PSYCHO_HOOK_V14_14\n'
    '        except Exception:\n'
    '            try:\n'
    '                render_market_psycho(CTX)\n'
    '            except Exception as _pe:\n'
    '                st.caption("IBD 5대 심리 패널 실패: " + str(_pe))\n'
)
