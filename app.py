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


def _load():
    for old in Path("/tmp").glob("canslim_v14_*_patched.py"):
        try:
            old.unlink()
        except Exception:
            pass
    with urllib.request.urlopen(_SRC_URL, timeout=45) as r:
        src = r.read().decode("utf-8")
    if "def naive_ts" not in src:
        src = src.replace("\ndef naive(df):", "\n" + _HELPER + "\ndef naive(df):", 1)
    if _OLD_EARN in src:
        src = src.replace(_OLD_EARN, _NEW_EARN, 1)
    if _OLD_TABS in src:
        src = src.replace(_OLD_TABS, _NEW_TABS, 1)
    ftd = _fetch("stock_ftd_engine.py") + "\n" + _fetch("stock_ftd_detect.py") + "\n" + _fetch("stock_ftd_review.py") + "\n"
    fui = _fetch("stock_ftd_ui.py")
    ibd_e = _fetch("ibd_proxy_engine.py")
    ibd_eb = _fetch("ibd_proxy_engine_b.py")
    ibd3 = _fetch("ibd_proxy_ui_step3.py")
    ibd5 = _fetch("ibd_proxy_ui_step5.py")
    ibdh = _fetch("ibd_proxy_ui_hold.py")
    desk_e = _fetch("ibd_desk_engine.py")
    desk_m = _fetch("ibd_desk_ui_mkt.py")
    desk_s = _fetch("ibd_desk_ui_stk.py")
    chart = _fetch("ibd_ma_chart.py")
    inst = _fetch("ibd_inst_tab.py")
    ck_e = _fetch("ibd_checkup_full.py")
    ck_u = _fetch("ibd_checkup_ui.py")
    book4 = _fetch("ibd_book_v14_4.py")
    book5 = _fetch("ibd_book_v14_5.py")
    book6 = _fetch("ibd_book_v14_6.py")
    book8 = _fetch("ibd_book_v14_8.py")
    book10 = _fetch("ibd_book_v14_10.py")
    drill = _fetch("ibd_ftd_drill_tab.py")
    _ly = _EMBEDDED_LAYERS if "시장 3층 판정" in (_EMBEDDED_LAYERS or "") else ""
    if "시장 3층 판정" not in (_ly or "") or "def render_market_psycho" not in (_ly or ""):
        for _name in (
            "ibd_mkt_layers_v14_21.py",
            "ibd_mkt_layers_v14_20.py",
            "ibd_mkt_layers_v14_18.py",
        ):
            try:
                _ly = _fetch(_name)
            except Exception:
                _ly = ""
            if "시장 3층 판정" in _ly and "def render_market_psycho" in _ly:
                break
    if "시장 3층 판정" not in (_ly or "") or "def render_market_psycho" not in (_ly or ""):
        raise RuntimeError("3-layer patch missing (embed empty + GitHub v14.21/20/18 fail)")
    mktlive = _fetch("ibd_mkt_live_v14_12.py") + "\n\n" + _ly
    basefix = (_fetch("ibd_base_fix_v14_7a1.py") + "\n"
               + _fetch("ibd_base_fix_v14_7a2.py") + "\n"
               + _fetch("ibd_base_fix_v14_7b.py"))
    book = book4 + "\n\n" + book5 + "\n\n" + book6 + "\n\n" + book8 + "\n\n" + book10
    a_idx = "def index_state(idf, min_gain, corr_pct):"
    if "def stock_distribution_days" not in src and a_idx in src:
        src = src.replace(a_idx, ftd + a_idx, 1)
    a_s7 = "        # STEP 7 종합\n        step_header(\"STEP 7\", \"종합 등급\")"
    if "STEP 6.5" not in src and a_s7 in src:
        src = src.replace(a_s7, fui + "\n" + a_s7, 1)
    a_sc = "def scenario(binfo, price, market, ma, capital, risk_pct, atrp=None):"
    if "def eps_rating_detail" not in src and a_sc in src:
        src = src.replace(a_sc, ibd_e + "\n" + ibd_eb + a_sc, 1)
    a_s4 = "        # STEP 4 밸류에이션\n        step_header(\"STEP 4\", \"재무 · 밸류에이션\")"
    if "STEP 3b" not in src and a_s4 in src:
        src = src.replace(a_s4, ibd3 + a_s4, 1)
    a_s6 = "        # STEP 6 수급 — 한국은 기관/외국인 정밀 수집"
    if "70대 진입 추정" not in src and a_s6 in src:
        src = src.replace(a_s6, ibd5 + a_s6, 1)
    a_urg = '            urgent = [r for r in ok_revs if r["kind"] == "fail"]'
    if "HOLD RS" not in src and a_urg in src:
        src = src.replace(a_urg, ibdh + a_urg, 1)
    a_sv = "def save_portfolio(p):\n    st.session_state[\"port\"] = p\n    save_json_file(PORT_FILE, p)\n"
    if "def load_ibd_desk" not in src and "def save_portfolio(p):" in src:
        src = src.replace(a_sv, a_sv + "\n" + desk_e + "\n", 1)
    a_t3 = "# TAB 3 — 개별종목"
    _ck_pre = "\n\n" + desk_e + "\n\n" + ck_e + "\n\n" + book + "\n\n"
    if a_t3 in src:
        head, tail = src.split(a_t3, 1)
        if "def checkup_for" not in head or "def checkup_rows_for" not in head:
            src = head + _ck_pre + a_t3 + tail
    a_mkt = '        states, bw = CTX["states"], CTX["bw"]'
    if "IBD DESK" not in src and a_mkt in src:
        src = src.replace(a_mkt, a_mkt + "\n" + desk_m, 1)
    src = _inject_layers_before_tab1(src, mktlive)
    src = _inject_hook(src)
    a_65 = "        # STEP 6.5 종목 FTD · 분산일 (매도일) — 시장 규칙을 이 종목에 이식"
    if "I · 기관보증" not in src and a_65 in src:
        src = src.replace(a_65, desk_s + "\n" + a_65, 1)
    a_ch = "def stock_chart(dfd, weekly, binfo, market, rsl, use_weekly):"
    if "21일 EMA" not in src and a_ch in src:
        i0 = src.find(a_ch)
        i1 = src.find("\n\ndef fx_chart(", i0)
        if i0 >= 0 and i1 > i0:
            src = src[:i0] + chart.rstrip() + "\n" + src[i1:]
    if "with TABS[10], guard(\"기관동향\")" not in src:
        src = src.rstrip() + "\n\n" + inst + "\n"
    elif "Daily Mutual 스냅샷" not in src or "ensure_book_seed" not in src:
        i0 = src.find("with TABS[10], guard(\"기관동향\")")
        if i0 < 0:
            i0 = src.find("# TAB 10")
        if i0 >= 0:
            src = src[:i0] + inst + "\n"
        else:
            src = src.rstrip() + "\n\n" + inst + "\n"
    src += "\n\n" + desk_e + "\n\n" + ck_e + "\n\n" + book + "\n"
    a_ck = '        step_header("IBD CHECKUP"'
    a_65b = "        # STEP 6.5 종목 FTD"
    if "Checkup 항목 입력" not in src and a_ck in src and a_65b in src:
        i0 = src.find(a_ck)
        i1 = src.find(a_65b)
        if 0 <= i0 < i1:
            src = src[:i0] + ck_u.rstrip() + "\n\n" + src[i1:]
    elif "Checkup 항목 입력" not in src and a_65b in src:
        src = src.replace(a_65b, ck_u + "\n" + a_65b, 1)
    if "def load_ibd_desk" not in src:
        raise RuntimeError("IBD desk engine patch did not apply")
    if "IBD DESK" not in src:
        raise RuntimeError("IBD desk market UI patch did not apply")
    if "TABS[10]" not in src:
        raise RuntimeError("institution tab did not apply")
    if "def ma_health" not in src:
        src += "\n\ndef ma_health(df, weekly=None):\n    return None\n"
    if "def checkup_for" not in src:
        src += "\n\ndef checkup_for(tk, desk):\n    rows = (desk.get('checkups') or {}).get(str(tk or '').upper()) or []\n    return rows[-1] if rows else None\n"
    if "def inst_rows_for" not in src:
        src += "\n\ndef inst_rows_for(tk, desk):\n    return [x for x in (desk.get('inst') or []) if str(x.get('ticker','')).upper() == str(tk or '').upper()]\n"
    if "with TABS[11], guard(\"FTD훈련\")" not in src:
        src = src.rstrip() + "\n\n" + drill + "\n"
    if "CHECKUP_BOOK_V14_9" not in src:
        raise RuntimeError("v14.9 checkup book 0908 did not apply")
    if "CHART_READ_V14_11" not in src:
        raise RuntimeError("v14.11 chart read did not apply")
    if "FTD_DRILL_TAB_V14_11" not in src:
        raise RuntimeError("v14.11 FTD drill did not apply")
    if "INDEX_CHART_READ_20260907" not in src:
        raise RuntimeError("v14.11 index chart gold did not apply")
    src = _inject_layers_before_tab1(src, mktlive)
    src = _inject_hook(src)
    i_def = src.find("def render_market_psycho")
    i_hook = src.find(_HOOK_MARK)
    if i_def < 0 or i_hook < 0 or i_def > i_hook:
        raise RuntimeError("v14.21 render_market_psycho must be defined BEFORE market tab hook")
    if "MKT_LIVE_V14_12" not in src:
        raise RuntimeError("v14.12 market live helpers did not apply")
    if _HOOK_MARK not in src:
        raise RuntimeError("v14.21 layer hook did not inject into market tab")
    if "시장 3층 판정" not in src or "def render_market_psycho" not in src:
        raise RuntimeError("v14.21 3-layer editor missing")
    if "psycho_edit_v21" not in src and "psycho_edit_v20" not in src and "psycho_edit_v18" not in src:
        raise RuntimeError("v14.21 psycho form missing")
    _old_fg = 'step_header("FEAR & GREED", "포공탐욕지수", "군중이 어디에 서 있는가")'
    _new_fg = 'step_header("FEAR & GREED (앱 자체)", "3층 판정과 다른 물건", "CNN식 근사. IBD 인쇄 심리가 아니다")'
    if _old_fg in src:
        src = src.replace(_old_fg, _new_fg, 1)
    if "FTD_DRILL_TAB" not in src:
        raise RuntimeError("v14.9 FTD drill tab did not apply")
    if "CHECKUP_BOOK_20260904" not in src:
        raise RuntimeError("v14.5 checkup book 22 did not apply")
    if "WEEKLY_REVIEW_20260903" not in src:
        raise RuntimeError("v14.5 weekly review list did not apply")
    if "CHECKUP_BOOK_PBF" not in src:
        raise RuntimeError("v14.7 PBF checkup book did not apply")
    src += "\n\n" + basefix + "\n"
    if "BASE_FIX_V14_7" not in src or "apply_ibd_overlay" not in src:
        raise RuntimeError("v14.7 base fix did not apply")
    a_binfo = "    binfo = analyze_base(dfd, market, zig_pct)\n"
    a_binfo2 = ("    binfo = analyze_base(dfd, market, zig_pct)\n"
                "    try:\n"
                "        _desk = load_ibd_desk() if callable(globals().get(\"load_ibd_desk\")) else None\n"
                "        binfo = apply_ibd_overlay(binfo, tk, _desk)\n"
                "        if callable(globals().get(\"apply_chart_read\")):\n"
                "            binfo = apply_chart_read(binfo, tk, _desk)\n"
                "    except Exception:\n"
                "        pass\n")
    if "apply_ibd_overlay(binfo" not in src and a_binfo in src:
        src = src.replace(a_binfo, a_binfo2, 1)
    if "def upsert_front" not in src:
        src += "\n\ndef upsert_front(desk, rec):\n    rec = dict(rec)\n    dt = str(rec.get('date') or '')\n    desk['front'] = [x for x in (desk.get('front') or []) if str(x.get('date')) != dt] + [rec]\n    save_ibd_desk(desk)\n    return desk\n\ndef delete_front(desk, dt):\n    desk['front'] = [x for x in (desk.get('front') or []) if str(x.get('date')) != str(dt)]\n    save_ibd_desk(desk)\n    return desk\n\ndef ibd_front_seed_20260902_close():\n    return {'date':'2026-09-02','source':'IBD 첫화면 수동','tag':'2026-09-02-close-ah','nasdaq':26217.83,'nasdaq_chg':0.45,'nasdaq_pts':118.05,'dji':53061.95,'dji_chg':0.56,'dji_pts':295.07,'spx':7666.60,'spx_chg':0.46,'spx_pts':35.13,'nasdaq_vol':7443.0,'nasdaq_vol_chg':10.25,'nasdaq_vol_pts':692.0,'nyse_vol':4739.0,'nyse_vol_chg':-2.43,'nyse_vol_pts':-118.0,'qqq_ah':709.24,'qqq_ah_chg':0.23,'qqq_ah_pts':1.60,'spy_ah':765.16,'spy_ah_chg':0.44,'spy_ah_pts':3.38,'dia_ah':530.62,'dia_ah_chg':0.54,'dia_ah_pts':2.87,'headline':'지수 동반 상승 · 나스닥 거래량 +10.25% / NYSE \u22122.43%','note':'종가 상승일. 나스닥 매집형 테이프. NYSE 거래량 감소.'}\n"
    try:
        compile(src, str(_CACHE), "exec")
    except SyntaxError as e:
        raise RuntimeError(
            f"assembled source SyntaxError line {e.lineno}: {e.msg}: {(e.text or '').strip()}"
        )
    _CACHE.write_text(src, encoding="utf-8")
    return src


_src = _load()
exec(compile(_src, str(_CACHE), "exec"), globals(), globals())
