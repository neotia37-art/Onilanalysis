"""Load sector helpers from the current file, not a stale imported copy."""
from __future__ import annotations

import importlib


def module():
    import selfdesk.sectors as mod

    if not hasattr(mod, "sector_for_stock"):
        mod = importlib.reload(mod)
    return mod


def load_sector_ranks():
    return module().load_sector_ranks()


def clear_sector_cache() -> None:
    fn = getattr(module(), "clear_sector_cache", None)
    if fn:
        fn()


def sector_for_stock(sector):
    fn = getattr(module(), "sector_for_stock", None)
    if fn is None:
        return None
    return fn(sector)
