# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v14.24 wrapper — mutates v14.23 loader then execs."""
from __future__ import annotations

import urllib.request
from pathlib import Path

_V23 = (
    "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/"
    "e5807af6c4ce06eba7b8ee1a59fa72c9b42b4458/app.py"
)
_CACHE = Path("/tmp/canslim_v14_24_loader.py")


def _mutate(src: str) -> str:
    src = src.replace(
        '"""CANSLIM TERMINAL v14.23 — 개별종목 3년·6분기 EPS + 최우선 뱇지."""',
        '"""CANSLIM TERMINAL v14.24 — 회사개요 탭 + CRWD 9/29 + Pulse 9/28."""',
        1,
    )
    src = src.replace(
        'Path("/tmp/canslim_v14_23_patched.py")',
        'Path("/tmp/canslim_v14_24_patched.py")',
        1,
    )
    src = src.replace(
        '"  기관동향  ", "  FTD훈련  "])\nst.caption("CANSLIM TERMINAL v14.23 · 3년·6분기 EPS · 최우선 뱇지")',
        '"  기관동향  ", "  FTD훈련  ", "  회사개요  "])\nst.caption("CANSLIM TERMINAL v14.24 · 회사개요 · Pulse 9/28 · CRWD 9/29")',
        1,
    )
    old_f = '''    book10 = _fetch("ibd_book_v14_10.py")
    drill = _fetch("ibd_ftd_drill_tab.py")'''
    new_f = '''    book10 = _fetch("ibd_book_v14_10.py")
    try:
        book24 = _fetch("ibd_book_v14_24.py")
    except Exception:
        book24 = ""
    try:
        company = _fetch("ibd_company_profiles_v14_24.py") + "\\n" + _fetch("ibd_company_tab_v14_24.py")
    except Exception:
        try:
            company = _fetch("ibd_company_tab_v14_24.py")
        except Exception:
            company = ""
    drill = _fetch("ibd_ftd_drill_tab.py")'''
    if old_f not in src:
        raise RuntimeError("v14.23 book10 fetch block missing")
    src = src.replace(old_f, new_f, 1)
    old_c = '    book = book4 + "\\n\\n" + book5 + "\\n\\n" + book6 + "\\n\\n" + book8 + "\\n\\n" + book10 + "\\n\\n" + eps_st'
    new_c = '    book = book4 + "\\n\\n" + book5 + "\\n\\n" + book6 + "\\n\\n" + book8 + "\\n\\n" + book10 + "\\n\\n" + book24 + "\\n\\n" + eps_st'
    if old_c not in src:
        raise RuntimeError("v14.23 book concat missing")
    src = src.replace(old_c, new_c, 1)
    old_t = '''    if "with TABS[11], guard(\\"FTD훈련\\")" not in src:
        src = src.rstrip() + "\\n\\n" + drill + "\\n"'''
    new_t = '''    if "with TABS[11], guard(\\"FTD훈련\\")" not in src:
        src = src.rstrip() + "\\n\\n" + drill + "\\n"
    if "with TABS[12], guard(\\"회사개요\\")" not in src:
        if not company or "COMPANY_TAB_V14_24" not in company:
            raise RuntimeError("v14.24 company overview tab patch missing")
        src = src.rstrip() + "\\n\\n" + company + "\\n"'''
    if old_t not in src:
        raise RuntimeError("v14.23 FTD tab inject missing")
    src = src.replace(old_t, new_t, 1)
    old_k = '''    if "EPS_STREAK_V14_23" not in src or "def render_eps_streak" not in src:
        raise RuntimeError("v14.23 EPS 3y/6q streak panel did not apply")'''
    new_k = '''    if "EPS_STREAK_V14_23" not in src or "def render_eps_streak" not in src:
        raise RuntimeError("v14.23 EPS 3y/6q streak panel did not apply")
    if "COMPANY_TAB_V14_24" not in src or "def render_company_overview" not in src:
        raise RuntimeError("v14.24 company overview tab did not apply")
    if "CHECKUP_BOOK_V14_24" not in src:
        raise RuntimeError("v14.24 checkup/pulse seed did not apply")'''
    if old_k not in src:
        raise RuntimeError("v14.23 EPS check missing")
    src = src.replace(old_k, new_k, 1)
    return src


def _boot():
    with urllib.request.urlopen(_V23, timeout=45) as r:
        raw = r.read().decode("utf-8")
    src = _mutate(raw)
    compile(src, str(_CACHE), "exec")
    _CACHE.write_text(src, encoding="utf-8")
    return src


_src = _boot()
exec(compile(_src, str(_CACHE), "exec"), globals(), globals())
