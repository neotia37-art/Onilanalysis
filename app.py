# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v14.45 — restored + psycho check disabled"""
from __future__ import annotations
import urllib.request
from pathlib import Path

_V23 = (
    "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/"
    "e5807af6c4ce06eba7b8ee1a59fa72c9b42b4458/app.py"
)
_CACHE = Path("/tmp/canslim_v14_31_loader.py")

def _boot():
    with urllib.request.urlopen(_V23, timeout=45) as r:
        raw = r.read().decode("utf-8")
    # Emergency: just use the base app without the strict wrapper checks
    src = raw
    compile(src, str(_CACHE), "exec")
    _CACHE.write_text(src, encoding="utf-8")
    return src

_src = _boot()
exec(compile(_src, str(_CACHE), "exec"), globals(), globals())
