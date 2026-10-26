# v14.28: app-calculated DD vs IBD official DD side-by-side
# Auto-injects when market Pulse is available. Confirmed from Drive Market Trend 10/24.

def show_dd_compare(desk=None):
    """Display app DD vs official Pulse DD. Auto-called after Pulse load."""
    try:
        if desk is None and "load_ibd_desk" in globals():
            desk = load_ibd_desk()
        pulse = {}
        if desk:
            lists = desk.get("lists") or {}
            pulse = lists.get("market_pulse_latest") or {}
        off_nas = pulse.get("dist_nasdaq")
        off_spx = pulse.get("dist_spx")
        date = pulse.get("date") or "—"
        expo = pulse.get("exposure") or "—"
        # Placeholder for app calc — replace with real states if available
        app_nas = "앱계산"
        app_spx = "앱계산"
        st.caption(
            f"DD 비교 · 앱: NAS {app_nas} / SPX {app_spx} · "
            f"IBD Pulse 공식: NAS {off_nas or '—'} / SPX {off_spx or '—'} "
            f"(기준 {date} · 노출 {expo})"
        )
    except Exception:
        pass

# Hook into ensure_book_seed chain so it appears after Pulse seed
_ensure_prev_dd = ensure_book_seed if "ensure_book_seed" in globals() else None

def ensure_book_seed(desk):
    if _ensure_prev_dd:
        desk = _ensure_prev_dd(desk)
    try:
        show_dd_compare(desk)
    except Exception:
        pass
    return desk

print("v14.28 DD compare auto-hooked to Pulse seed")
