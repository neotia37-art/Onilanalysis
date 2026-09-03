# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v14.3 — v13.1 base + FTD + IBD-proxy + desk + MA + inst tab."""
from __future__ import annotations

import urllib.request
from pathlib import Path

_SRC_URL = (
    "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/"
    "8d17f376294b2726722485d3dc18212a92904e5e/app.py"
)
_CACHE = Path("/tmp/canslim_v14_3_patched.py")
_PATCH_BASE = "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/main/patches/"

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
                "  기관동향  "])'''


def _fetch(name):
    with urllib.request.urlopen(_PATCH_BASE + name, timeout=45) as r:
        return r.read().decode("utf-8")


def _load():
    if _CACHE.exists() and _CACHE.stat().st_size > 100000:
        src = _CACHE.read_text(encoding="utf-8")
        if ("TABS[10]" in src and "CHECKUP_REV" in src and "checkup_blank_items" in src and "Checkup 항목 입력" in src):
            return src
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
    if "IBD DESK" not in src and a_t3 in src:
        src = src.replace(a_t3, desk_m + "\n" + a_t3, 1)
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
    src += "\n\n" + desk_e + "\n\n" + ck_e + "\n"
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
    if "def upsert_front" not in src:
        src += "\n\ndef upsert_front(desk, rec):\n    rec = dict(rec)\n    dt = str(rec.get('date') or '')\n    desk['front'] = [x for x in (desk.get('front') or []) if str(x.get('date')) != dt] + [rec]\n    save_ibd_desk(desk)\n    return desk\n\ndef delete_front(desk, dt):\n    desk['front'] = [x for x in (desk.get('front') or []) if str(x.get('date')) != str(dt)]\n    save_ibd_desk(desk)\n    return desk\n\ndef ibd_front_seed_20260902_close():\n    return {'date':'2026-09-02','source':'IBD 첫화면 수동','tag':'2026-09-02-close-ah','nasdaq':26217.83,'nasdaq_chg':0.45,'nasdaq_pts':118.05,'dji':53061.95,'dji_chg':0.56,'dji_pts':295.07,'spx':7666.60,'spx_chg':0.46,'spx_pts':35.13,'nasdaq_vol':7443.0,'nasdaq_vol_chg':10.25,'nasdaq_vol_pts':692.0,'nyse_vol':4739.0,'nyse_vol_chg':-2.43,'nyse_vol_pts':-118.0,'qqq_ah':709.24,'qqq_ah_chg':0.23,'qqq_ah_pts':1.60,'spy_ah':765.16,'spy_ah_chg':0.44,'spy_ah_pts':3.38,'dia_ah':530.62,'dia_ah_chg':0.54,'dia_ah_pts':2.87,'headline':'3지수 동반 상승 · 나스닥 거래량 +10.25% / NYSE \u22122.43%','note':'종가 상승일. 나스닥 매집형 테이프. NYSE 거래량 감소.'}\n"
    _CACHE.write_text(src, encoding="utf-8")
    return src


_src = _load()
exec(compile(_src, str(_CACHE), "exec"), globals(), globals())
