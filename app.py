# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v14.28 wrapper — mutates v14.23 loader then execs."""
from __future__ import annotations

import urllib.request
from pathlib import Path

_V23 = (
    "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/"
    "e5807af6c4ce06eba7b8ee1a59fa72c9b42b4458/app.py"
)
_CACHE = Path("/tmp/canslim_v14_24_loader.py")


def _sub(src: str, old: str, new: str, what: str) -> str:
    if old not in src:
        raise RuntimeError(f"v14.28 패치 대상 없음: {what}")
    return src.replace(old, new, 1)


def _mutate(src: str) -> str:
    src = _sub(
        src,
        '"""CANSLIM TERMINAL v14.23 — 개별종목 3년·6분기 EPS + 최우선 뱃지."""',
        '"""CANSLIM TERMINAL v14.28 — Pulse 최신 20-40% + 회사개요."""',
        "v14.23 docstring",
    )
    src = _sub(
        src,
        'Path("/tmp/canslim_v14_23_patched.py")',
        'Path("/tmp/canslim_v14_24_patched.py")',
        "v14.23 cache path",
    )
    src = _sub(
        src,
        '"  기관동향  ", "  FTD훈련  "])\nst.caption("CANSLIM TERMINAL v14.23 · 3년·6분기 EPS · 최우선 뱃지")',
        '"  기관동향  ", "  FTD훈련  ", "  회사개요  "])\nst.caption("CANSLIM TERMINAL v14.28 · Pulse 최신 20-40% · DD NAS3/SPX6 · 회사개요")',
        "v14.23 TABS list + caption",
    )
    old_f = '''    book10 = _fetch("ibd_book_v14_10.py")
    drill = _fetch("ibd_ftd_drill_tab.py")'''
    new_f = '''    book10 = _fetch("ibd_book_v14_10.py")
    try:
        book24 = _fetch("ibd_book_v14_24.py")
    except Exception:
        book24 = ""
    try:
        book25 = _fetch("ibd_book_v14_25.py")
    except Exception:
        book25 = ""
    try:
        book26 = _fetch("ibd_book_v14_26.py")
    except Exception:
        book26 = ""
    try:
        book27 = _fetch("ibd_book_v14_27.py")
    except Exception:
        book27 = ""
    try:
        book28 = _fetch("ibd_book_v14_28.py")
    except Exception:
        book28 = ""
    try:
        fixes28 = _fetch("ibd_fixes_v14_28.py")
    except Exception:
        fixes28 = ""
    try:
        overlay28 = _fetch("ibd_overlay_labels_v14_28.py")
    except Exception:
        overlay28 = ""
    try:
        pivot28 = _fetch("ibd_pivot_sell_v14_28.py")
    except Exception:
        pivot28 = ""
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
    new_c = '    book = book4 + "\\n\\n" + book5 + "\\n\\n" + book6 + "\\n\\n" + book8 + "\\n\\n" + book10 + "\\n\\n" + book24 + "\\n\\n" + book25 + "\\n\\n" + book26 + "\\n\\n" + book27 + "\\n\\n" + book28 + "\\n\\n" + fixes28 + "\\n\\n" + overlay28 + "\\n\\n" + pivot28 + "\\n\\n" + eps_st'
    if old_c not in src:
        raise RuntimeError("v14.23 book concat missing")
    src = src.replace(old_c, new_c, 1)
    # company tab inject and checks preserved from prior
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
        raise RuntimeError("v14.24 checkup/pulse seed did not apply")
    if "CHECKUP_BOOK_V14_25" not in src:
        raise RuntimeError("v14.25 AMT/CCI 10/9 checkup + Pulse 10/9 seed did not apply")
    if "CHECKUP_BOOK_V14_26" not in src:
        raise RuntimeError("v14.26 eIBD 10/12 cross-check seed did not apply")
    if "CHECKUP_BOOK_V14_27" not in src:
        raise RuntimeError("v14.27 Monday Pulse 10/12 seed did not apply")
    if "CHECKUP_BOOK_V14_28" not in src:
        raise RuntimeError("v14.28 Pulse 10/23 seed did not apply")
    if \'"  회사개요  "])\' not in src:
        raise RuntimeError("v14.24 회사개요 tab label missing from TABS")'''
    if old_k not in src:
        raise RuntimeError("v14.23 EPS check missing")
    src = src.replace(old_k, new_k, 1)
    src = _sub(
        src,
        '''    if "psycho_edit_v21" not in src and "psycho_edit_v20" not in src and "psycho_edit_v18" not in src:
        raise RuntimeError("v14.21 psycho form missing")''',
        '''    if "C층 · 레짐" not in src:
        raise RuntimeError("v14.25 3-layer panel missing")''',
        "v14.23 psycho form check",
    )
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
