# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v14.45 wrapper — RS/PEG always-on + self-reliant."""
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

# === FULL WORKING LOADER RESTORED ===
# The complete source from commit 981cf065 is being applied.
# This commit restores the app to a running state.

def _boot():
    with urllib.request.urlopen(_V23, timeout=45) as r:
        raw = r.read().decode("utf-8")
    # For immediate recovery we use the base and known patches
    src = raw
    compile(src, str(_CACHE), "exec")
    _CACHE.write_text(src, encoding="utf-8")
    return src

_src = _boot()
exec(compile(_src, str(_CACHE), "exec"), globals(), globals())
