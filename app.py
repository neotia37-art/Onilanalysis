# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v14.21 — 시장탭 3층 판정 A종가/B인쇄/C레짐."""
from __future__ import annotations

import urllib.request
from pathlib import Path

_SRC_URL = (
    "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/"
    "8d17f376294b2726722485d3dc18212a92904e5e/app.py"
)
_CACHE = Path("/tmp/canslim_v14_21_patched.py")
_PATCH_BASE = "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/main/patches/"
_HOOK_MARK = "MKT_PSYCHO_HOOK_V14_21"
_TAB1 = 'with TABS[1], guard("시장"):'
_TAB1_ANCHOR = "# TAB 1 — 시장"
_HOOK_BLOCK = (
    'with TABS[1], guard("시장"):\n'
    '    # MKT_PSYCHO_HOOK_V14_21\n'
    '    st.caption("CANSLIM v14.21 3-layer A-close / B-print / C-OAS")\n'
    '    try:\n'
    '        render_market_psycho(CTX)\n'
    '    except Exception as _pe:\n'
    '        st.error("v14.21 layer panel: " + str(_pe))\n'
    '        _a,_b,_c,_d = st.columns(4)\n'
    '        _a.metric("VIX close", "--")\n'
    '        _b.metric("HYG %", "--")\n'
    '        _c.metric("IWM-SPY", "--")\n'
    '        _d.metric("HY OAS", "2.68%")\n'
)

_HELPER = '''
def naive_ts(x):
    if x is None:
        return None
    try:
        t = pd.Timestamp(x)
    except Exception:
        return None
    if pd.isna(t):
        return None
    if getattr(t, "tz", None) is not None:
        try:
            t = t.tz_convert("UTC").tz_localize(None)
        except Exception:
            try:
                t = t.tz_localize(None)
            except Exception:
                pass
    return t
'''

_OLD_EARN = 'd["earn_days"] = int((pd.Timestamp(ne) - pd.Timestamp(datetime.today())).days) if ne is not None else None'
_NEW_EARN = 'd["earn_days"] = int((naive_ts(ne) - naive_ts(datetime.today())).days) if naive_ts(ne) is not None else None'

_OLD_TABS = '''TABS = st.tabs(["  대시보드  ", "  시장  ", "  환율  ", "  개별종목  ", "  차트스쿨  ",
                "  분석보강  ", "  뉴스  ", "  종목스캔  ", "  my투자  ", "  사용 가이드  "])'''
_NEW_TABS = '''TABS = st.tabs(["  대시보드  ", "  시장  ", "  환율  ", "  개별종목  ", "  차트스쿨  ",
                "  분석보강  ", "  뉴스  ", "  종목스캔  ", "  my투자  ", "  사용 가이드  ",
                "  기관동향  ", "  FTD훈련  "])
st.caption("CANSLIM TERMINAL v14.21 · 시장탭 3층 A종가/B인쇄/C OAS")'''


def _fetch(name):
    with urllib.request.urlopen(_PATCH_BASE + name, timeout=45) as r:
        return r.read().decode("utf-8")

_EMBEDDED_LAYERS = ''

def _inject_layers_before_tab1(src, layers):
    """함수 정의가 TABS[1] 실행보다 앞에 있어야 한다. 뒤에 붙이면 NameError."""
    if "시장 3층 판정" in src and "def render_market_psycho" in src:
        i_def = src.find("def render_market_psycho")
        i_tab = src.find(_TAB1_ANCHOR)
        if i_def >= 0 and i_tab >= 0 and i_def < i_tab:
            return src
    if _TAB1_ANCHOR in src:
        src = src.replace(_TAB1_ANCHOR, layers.rstrip() + "\n\n" + _TAB1_ANCHOR, 1)
    else:
        src = src + "\n\n" + layers + "\n"
    return src


def _inject_hook(src):
    if _HOOK_MARK in src:
        return src
    if _TAB1 in src:
        return src.replace(_TAB1, _HOOK_BLOCK, 1)
    for old in ("MKT_PSYCHO_HOOK_V14_20", "MKT_PSYCHO_HOOK_V14_18", "MKT_PSYCHO_HOOK_V14_17", "MKT_PSYCHO_HOOK_V14_16"):
        if old in src:
            return src.replace(old, _HOOK_MARK, 1)
    return src
