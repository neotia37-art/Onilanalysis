# -*- coding: utf-8 -*-
"""CANSLIM TERMINAL v14.13 boot — bust v14.12 cache, rebuild with inline 5 psycho."""
from pathlib import Path
import urllib.request

for p in Path("/tmp").glob("canslim_v14_*_patched.py"):
    try:
        p.unlink()
    except Exception:
        pass

raw = urllib.request.urlopen(
    "https://raw.githubusercontent.com/neotia37-art/Onilanalysis/"
    "cdc81f4d6591016d216b3d3e5b6c0a8243bae459/app.py",
    timeout=45,
).read().decode("utf-8")
raw = raw.replace(
    "/tmp/canslim_v14_12_patched.py",
    "/tmp/canslim_v14_13_patched.py",
)
raw = raw.replace(
    'and "render_market_live(" in src\n                and "TABS[11]" in src)',
    'and "render_market_live(" in src\n                and "render_market_psycho(" in src\n                and "TABS[11]" in src)',
)
exec(compile(raw, "app_boot_v14_13", "exec"), globals(), globals())
