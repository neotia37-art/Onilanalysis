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


def _mutate(src: str) -> str:
    src = _sub(
        src,
        '"""CANSLIM TERMINAL v14.23 — 개별종목 3년·6분기 EPS + 최우선 뱃지."""',
        '"""CANSLIM TERMINAL v14.45 — RS/PEG always-on."""',
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
        '"  기관동향  ", "  FTD훈련  ", "  회사개요  ", "  상대밸류  "])\nst.caption("CANSLIM TERMINAL v14.45 · RS/PEG 항상 표시")',
        "v14.23 TABS list + caption",
    )
    # Completely suppress Checkup manual form injection
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
        rs45 = _fetch("rs_peg_v14_45.py")
    except Exception:
        rs45 = ""
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
    new_c = '    book = book4 + "\\n\\n" + book5 + "\\n\\n" + book6 + "\\n\\n" + book8 + "\\n\\n" + book10 + "\\n\\n" + book24 + "\\n\\n" + book25 + "\\n\\n" + book26 + "\\n\\n" + book27 + "\\n\\n" + book28 + "\\n\\n" + fixes28 + "\\n\\n" + overlay28 + "\\n\\n" + pivot29 + "\\n\\n" + earnvol28 + "\\n\\n" + cleanup28 + "\\n\\n" + dd28 + "\\n\\n" + latest28 + "\\n\\n" + uiclean28 + "\\n\\n" + pulsejson29 + "\\n\\n" + prio31 + "\\n\\n" + quality43 + "\\n\\n" + self44 + "\\n\\n" + rs45 + "\\n\\n" + eps_st'
    if old_c not in src:
        raise RuntimeError("v14.23 book concat missing")
    src = src.replace(old_c, new_c, 1)
    # company tab inject and checks preserved from prior + relval
    old_t = '''    if "with TABS[11], guard(\\"FTD훈련\\")" not in src:
        src = src.rstrip() + "\\n\\n" + drill + "\\n"'''
    new_t = '''    if "with TABS[11], guard(\\"FTD훈련\\")" not in src:
        src = src.rstrip() + "\\n\\n" + drill + "\\n"
    if "with TABS[12], guard(\\"회사개요\\")" not in src:
        if not company or "COMPANY_TAB_V14_24" not in company:
            raise RuntimeError("v14.24 company overview tab patch missing")
        src = src.rstrip() + "\\n\\n" + company + "\\n"
    if "with TABS[13], guard(\\"상대밸류\\")" not in src:
        if not relval or "RELVAL_TAB_V14_30" not in relval:
            raise RuntimeError("v14.30 relative valuation tab patch missing")
        src = src.rstrip() + "\\n\\n" + relval + "\\n"'''
    if old_t not in src:
        raise RuntimeError("v14.23 FTD tab inject missing")
    src = src.replace(old_t, new_t, 1)
    old_k = '''    if "EPS_STREAK_V14_23" not in src or "def render_eps_streak" not in src:
        raise RuntimeError("v14.23 EPS 3y/6q streak panel did not apply")'''
    new_k = '''    if "EPS_STREAK_V14_23" not in src or "def render_eps_streak" not in src:
        raise RuntimeError("v14.23 EPS 3y/6q streak panel did not apply")
    if "COMPANY_TAB_V14_24" not in src or "render_company" not in src:
        raise RuntimeError("v14.39 company tab did not apply")
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
    if "  회사개요  " not in src:
        raise RuntimeError("v14.24 회사개요 tab label missing from TABS")
    if "  상대밸류  " not in src:
        raise RuntimeError("v14.30 상대밸류 tab label missing from TABS")
    if "RELVAL_TAB_V14_30" not in src or "def render_relval_tab" not in src:
        raise RuntimeError("v14.30 relative valuation tab did not apply")
    if "compute_quality_score" not in src:
        raise RuntimeError("v14.43 quality score patch did not apply")
    if "better_rs_proxy" not in src:
        raise RuntimeError("v14.45 RS/PEG patch did not apply")'''
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
    src = _sub(
        src,
        "'        render_market_psycho(CTX)\\n'",
        "'        from selfdesk.panel import render_self_market\\n'\n"
        "    '        render_self_market()\\n'\n"
        "    '    except Exception as _sem:\\n'\n"
        "    '        st.warning(\"자체 분산일: \" + str(_sem))\\n'\n"
        "    '    try:\\n'\n"
        "    '        from selfdesk.sector_panel import render_sector_ranks\\n'\n"
        "    '        render_sector_ranks()\\n'\n"
        "    '    except Exception as _sse:\\n'\n"
        "    '        st.warning(\"섹터 순위: \" + str(_sse))\\n'\n"
        "    '    try:\\n'\n"
        "    '        render_market_psycho(CTX)\\n'",
        "self market hook",
    )
    src = _sub(
        src,
        "    try:\n        compile(src, str(_CACHE), \"exec\")\n",
        "    from pathlib import Path as _AsOfPath\n"
        "    _asof_root = _AsOfPath(__file__).resolve().parent\n"
        "    if not (_asof_root / \"selfdesk\" / \"guard_old.txt\").exists():\n"
        "        _asof_root = _AsOfPath.cwd()\n"
        "    _guard_old = (_asof_root / \"selfdesk\" / \"guard_old.txt\").read_text(encoding=\"utf-8\")\n"
        "    _guard_new = (_asof_root / \"selfdesk\" / \"guard_new.txt\").read_text(encoding=\"utf-8\")\n"
        "    if _guard_old not in src:\n"
        "        raise RuntimeError(\"v14.38 자료 기준일 패치 대상 없음\")\n"
        "    src = src.replace(_guard_old, _guard_new, 1)\n"
        "    _sec_old = (_asof_root / \"selfdesk\" / \"sector_fn_old.txt\").read_text(encoding=\"utf-8\")\n"
        "    _sec_new = (_asof_root / \"selfdesk\" / \"sector_fn_new.txt\").read_text(encoding=\"utf-8\")\n"
        "    if _sec_old not in src:\n"
        "        raise RuntimeError(\"v14.39 업종 순위 함수 대상 없음\")\n"
        "    src = src.replace(_sec_old, _sec_new, 1)\n"
        "    _old_card = 'c[3].markdown(card(\"업종 순위\", \"—\", \"업종 데이터 미수집(국내 미지원)\"), unsafe_allow_html=True)'\n"
        "    _new_card = 'c[3].markdown(card(\"업종 순위\", \"—\", \"미국 11섹터에 이 업종 이름이 없거나 시세를 못 받았습니다. 시장 탭 섹터 표를 봅니다.\"), unsafe_allow_html=True)'\n"
        "    if _old_card not in src:\n"
        "        raise RuntimeError(\"v14.39 업종 카드 대상 없음\")\n"
        "    src = src.replace(_old_card, _new_card, 1)\n"
        "    _gate_old = (_asof_root / \"selfdesk\" / \"gate_old.txt\").read_text(encoding=\"utf-8\")\n"
        "    _gate_new = (_asof_root / \"selfdesk\" / \"gate_new.txt\").read_text(encoding=\"utf-8\")\n"
        "    if _gate_old not in src:\n"
        "        raise RuntimeError(\"v14.42 짧은 이력 분기 대상 없음\")\n"
        "    src = src.replace(_gate_old, _gate_new, 1)\n"
        "    _dash_old = (_asof_root / \"selfdesk\" / \"dash_old.txt\").read_text(encoding=\"utf-8\")\n"
        "    _dash_new = (_asof_root / \"selfdesk\" / \"dash_new.txt\").read_text(encoding=\"utf-8\")\n"
        "    if _dash_old not in src:\n"
        "        raise RuntimeError(\"v14.42 대시보드 문구 대상 없음\")\n"
        "    src = src.replace(_dash_old, _dash_new, 1)\n"
        "    _short_old = \"        chg = (price / float(df[\\\"Close\\\"].iloc[-2]) - 1) * 100\\n        if CTX.get(\\\"price_chk\\\", {}).get(\\\"ok\\\") is False:\\n\"\n"
        "    _short_new = \"        chg = (price / float(df[\\\"Close\\\"].iloc[-2]) - 1) * 100\\n        if len(df) < 120:\\n            st.info(f\\\"거래일 {len(df)}일입니다. 시세는 정상입니다. 120일이 안 되어 200일선과 12개월 RS는 비거나 약합니다.\\\")\\n        if CTX.get(\\\"price_chk\\\", {}).get(\\\"ok\\\") is False:\\n\"\n"
        "    if _short_old not in src:\n"
        "        raise RuntimeError(\"v14.42 짧은 이력 안내 대상 없음\")\n"
        "    src = src.replace(_short_old, _short_new, 1)\n"
        "    try:\n        compile(src, str(_CACHE), \"exec\")\n",
        "asof guard",
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
