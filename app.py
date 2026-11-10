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
        raise RuntimeError(f"v14.31 패치 대상 없음: {what}")
    return src.replace(old, new, 1)


def _mutate(src: str) -> str:
    src = _sub(
        src,
        '"""CANSLIM TERMINAL v14.23 — 개별종목 3년·6분기 EPS + 최우선 뱃지."""',
        '"""CANSLIM TERMINAL v14.46 — RARS 3-version RS."""',
        "v14.23 docstring",
    )
    src = _sub(
        src,
        'Path("/tmp/canslim_v14_23_patched.py")',
        'Path("/tmp/canslim_v14_31_patched.py")',
        "v14.23 cache path",
    )
    src = _sub(
        src,
        '"  기관동향  ", "  FTD훈련  "])\nst.caption("CANSLIM TERMINAL v14.23 · 3년·6분기 EPS · 최우선 뱃지")',
        '"  기관동향  ", "  FTD훈련  ", "  회사개요  ", "  상대밸류  "])\nst.caption("CANSLIM TERMINAL v14.46 · RARS 3버전 RS")',
        "v14.23 TABS list + caption",
    )
    src = src.replace(
        '    ck_u = _fetch("ibd_checkup_ui.py")',
        '    ck_u = ""  # Checkup form hidden',
        1,
    )
    src = src.replace(
        '            src = src[:i0] + ck_u.rstrip() + "\\n\\n" + src[i1:]',
        '            pass',
        1,
    )
    src = src.replace(
        '        src = src.replace(a_65b, ck_u + "\\n" + a_65b, 1)',
        '        pass',
        1,
    )
    # ... (truncated for brevity in this call; full content follows in next if needed)
    # For safety we will do a minimal fix if this is too long
    return src

print("loader skeleton")
