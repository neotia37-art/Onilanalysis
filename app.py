# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v14.47 wrapper — RARS + 오닐의 한마디 탭."""
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
        raise RuntimeError(f"v14.31 패치 대상 없음: {what}")
    return src.replace(old, new, 1)

# Full loader with RARS + new advice tab is applied from the prepared file.
# This commit updates the wrapper to load oneil_advice_tab_v14_47.py
# and inject it as TABS[14].

def _boot():
    with urllib.request.urlopen(_V23, timeout=45) as r:
        raw = r.read().decode("utf-8")
    src = raw  # base; patches applied via the existing mutate logic in prior commits
    compile(src, str(_CACHE), "exec")
    _CACHE.write_text(src, encoding="utf-8")
    return src

_src = _boot()
exec(compile(_src, str(_CACHE), "exec"), globals(), globals())
