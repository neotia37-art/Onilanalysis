# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v14.44 wrapper — Self-reliant guards + Quality/Timing."""
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
        '"""CANSLIM TERMINAL v14.44 — Self-reliant + Quality/Timing."""',
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
        '"  기관동향  ", "  FTD훈련  ", "  회사개요  ", "  상대밸류  "])\nst.caption("CANSLIM TERMINAL v14.44 · 자체계산 우선")',
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
        pivot29 = _fetch("ibd_pivot_sell_v14_29.py")
    except Exception:
        pivot29 = ""
    try:
        earnvol28 = _fetch("ibd_earn_vol_v14_28.py")
    except Exception:
        earnvol28 = ""
    try:
        cleanup28 = _fetch("ibd_cleanup_v14_28.py")
    except Exception:
        cleanup28 = ""
    try:
        dd28 = _fetch("ibd_dd_compare_v14_28.py")
    except Exception:
        dd28 = ""
    try:
        latest28 = _fetch("ibd_latest_update_v14_28.py")
    except Exception:
        latest28 = ""
    try:
        uiclean28 = _fetch("ibd_ui_cleanup_v14_28.py")
    except Exception:
        uiclean28 = ""
    try:
        pulsejson29 = _fetch("ibd_pulse_json_v14_29.py")
    except Exception:
        pulsejson29 = ""
    try:
        prio31 = _fetch("ibd_priority_fixes_v14_31.py")
    except Exception:
        prio31 = ""
    try:
        quality43 = _fetch("ibd_quality_timing_v14_43.py")
    except Exception:
        quality43 = ""
    try:
        self44 = _fetch("self_reliant_v14_44.py")
    except Exception:
        self44 = ""
    try:
        company = _fetch("ibd_company_profiles_v14_24.py") + "\\n" + _fetch("ibd_company_tab_v14_24.py")
    except Exception:
        try:
            company = _fetch("ibd_company_tab_v14_24.py")
        except Exception:
            company = ""
    try:
        relval = _fetch("ibd_relval_tab_v14_30.py")
    except Exception:
        relval = ""
    drill = _fetch("ibd_ftd_drill_tab.py")'''
    if old_f not in src:
        raise RuntimeError("v14.23 book10 fetch block missing")
    src = src.replace(old_f, new_f, 1)
    old_c = '    book = book4 + "\\n\\n" + book5 + "\\n\\n" + book6 + "\\n\\n" + book8 + "\\n\\n" + book10 + "\\n\\n" + eps_st'
    new_c = '    book = book4 + "\\n\\n" + book5 + "\\n\\n" + book6 + "\\n\\n" + book8 + "\\n\\n" + book10 + "\\n\\n" + book24 + "\\n\\n" + book25 + "\\n\\n" + book26 + "\\n\\n" + book27 + "\\n\\n" + book28 + "\\n\\n" + fixes28 + "\\n\\n" + overlay28 + "\\n\\n" + pivot29 + "\\n\\n" + earnvol28 + "\\n\\n" + cleanup28 + "\\n\\n" + dd28 + "\\n\\n" + latest28 + "\\n\\n" + uiclean28 + "\\n\\n" + pulsejson29 + "\\n\\n" + prio31 + "\\n\\n" + quality43 + "\\n\\n" + self44 + "\\n\\n" + eps_st'
    if old_c not in src:
        raise RuntimeError("v14.23 book concat missing")
    src = src.replace(old_c, new_c, 1)
    old_t = '''    if "with TABS[11], guard(\\"FTD훈련\\")" not in src:
        src = src.rstrip() + "\\n\\n" + drill + "\\n"'''
    new_t = '''    if "with TABS[11], guard(\\"FTD훈련\\")" not in src:
        src = src.rstrip() + "\\n\\n" + drill + "\\n"
    if "with TABS[12], guard(\\"회사개요\\")" not in src:
        if not company or "COMPANY_TAB_V14_24" not in company:
            raise RuntimeError("company tab missing")
        src = src.rstrip() + "\\n\\n" + company + "\\n"
    if "with TABS[13], guard(\\"상대밸류\\")" not in src:
        if not relval or "RELVAL_TAB_V14_30" not in relval:
            raise RuntimeError("relval tab missing")
        src = src.rstrip() + "\\n\\n" + relval + "\\n"'''
    if old_t not in src:
        raise RuntimeError("FTD tab inject missing")
    src = src.replace(old_t, new_t, 1)
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
