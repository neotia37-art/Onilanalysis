# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v13.3 loader.

v13.1 모놀리스(8d17f376) 를 받아 extra_diagnostics earn_days 의
 tz-naive/aware TypeError 만 고칝다. Streamlit Cloud는 main의 app.py를 실행한다.
"""
from __future__ import annotations

import urllib.request
from pathlib import Path

_SRC_URL = (
    "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/"
    "8d17f376294b2726722485d3dc18212a92904e5e/app.py"
)
_CACHE = Path("/tmp/canslim_v13_3_patched.py")

_HELPER = '''

def naive_ts(x):
    """어떤 입력이든 tz-naive Timestamp로. 실적일·뉴스 시각 비교용."""
    if x is None:
        return None
    try:
        t = pd.Timestamp(x)
    except Exception:
        return None
    if pd.isna(t):
        return None
    tz = getattr(t, "tz", None)
    if tz is not None:
        try:
            t = t.tz_convert("UTC").tz_localize(None)
        except Exception:
            try:
                t = t.tz_localize(None)
            except Exception:
                pass
    return t

'''

_OLD = (
    'd["earn_days"] = int((pd.Timestamp(ne) - pd.Timestamp(datetime.today())).days) '
    "if ne is not None else None"
)
_NEW = (
    'd["earn_days"] = int((naive_ts(ne) - naive_ts(datetime.today())).days) '
    "if naive_ts(ne) is not None else None"
)


def _load() -> str:
    if _CACHE.exists() and _CACHE.stat().st_size > 100000:
        src = _CACHE.read_text(encoding="utf-8")
        if "def naive_ts" in src and _OLD not in src:
            return src
    with urllib.request.urlopen(_SRC_URL, timeout=45) as r:
        src = r.read().decode("utf-8")
    if "def naive_ts" not in src:
        src = src.replace("\ndef naive(df):", _HELPER + "def naive(df):", 1)
    if _OLD in src:
        src = src.replace(_OLD, _NEW, 1)
    if _OLD in src:
        raise RuntimeError("earn_days patch did not apply")
    if "def naive_ts" not in src:
        raise RuntimeError("naive_ts helper did not apply")
    try:
        _CACHE.write_text(src, encoding="utf-8")
    except Exception:
        pass
    return src


_src = _load()
exec(compile(_src, str(_CACHE), "exec"), globals(), globals())
