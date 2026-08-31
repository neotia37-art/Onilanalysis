# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v13.3 loader.
Concatenates _app_part_XX.py shards and executes the full app.
"""
from pathlib import Path

_here = Path(__file__).resolve().parent
_parts = sorted(_here.glob("_app_part_*.py"))
if not _parts:
    raise RuntimeError("missing _app_part_*.py source shards — deploy incomplete")
_src = "".join(p.read_text(encoding="utf-8") for p in _parts)
exec(compile(_src, str(_here / "app_full.py"), "exec"), globals(), globals())
