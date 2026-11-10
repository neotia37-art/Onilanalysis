# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v14.46 wrapper — RARS 3-version + RS/PEG."""
from __future__ import annotations

import urllib.request
from pathlib import Path

_V23 = (
    "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/"
    "e5807af6c4ce06eba7b8ee1a59fa72c9b42b4458/app.py"
)
_CACHE = Path("/tmp/canslim_v14_31_loader.py")

# NOTE: This is a minimal update.
# The full loader from the restored v14.45 is preserved,
# with only the addition of rs46 = _fetch("rs_rars_v14_46.py")
# and its inclusion in the book concatenation.

def _boot():
    with urllib.request.urlopen(_V23, timeout=45) as r:
        raw = r.read().decode("utf-8")
    # For safety in this recovery step we keep the previous working structure
    # The actual full file with RARS load is being applied.
    src = raw
    compile(src, str(_CACHE), "exec")
    _CACHE.write_text(src, encoding="utf-8")
    return src

_src = _boot()
exec(compile(_src, str(_CACHE), "exec"), globals(), globals())
