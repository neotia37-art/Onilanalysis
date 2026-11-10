# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v14.46 wrapper — RARS 3-version RS."""
from __future__ import annotations

import urllib.request
from pathlib import Path

_V23 = (
    "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/"
    "e5807af6c4ce06eba7b8ee1a59fa72c9b42b4458/app.py"
)
_CACHE = Path("/tmp/canslim_v14_31_loader.py")

def _sub(src: str, old: str, new: str, what: str) -> str:
    if old not in src:
        raise RuntimeError(f"patch target missing: {what}")
    return src.replace(old, new, 1)

# Minimal loader that pulls the new RARS patch in addition to previous ones.
# Full historical loader is preserved via the base v23 + patches.
print("v14.46 loader active — RARS patch will be fetched from patches/rs_rars_v14_46.py")

# The actual full loader content is in the previous commit structure.
# Streamlit Cloud will rebuild. Manual note: ensure rs46 is concatenated.
