# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v13.3 loader — inflate app_src_*.b64 shards."""
from pathlib import Path
import base64
import zlib

_here = Path(__file__).resolve().parent
_parts = sorted(_here.glob("app_src_*.b64"))
if not _parts:
    raise RuntimeError("missing app_src_*.b64 shards — deploy incomplete")
_b64 = "".join(p.read_text(encoding="ascii") for p in _parts).encode("ascii")
_src = zlib.decompress(base64.b64decode(_b64)).decode("utf-8")
exec(compile(_src, str(_here / "app_full.py"), "exec"), globals(), globals())
