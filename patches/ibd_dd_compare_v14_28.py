# v14.28: app-calculated DD vs IBD official DD side-by-side note
# Injected into market view via caption when pulse is shown.

def show_dd_compare(desk=None):
    """Display app DD vs official Pulse DD if available."""
    try:
        if desk is None and "load_ibd_desk" in globals():
            desk = load_ibd_desk()
        pulse = {}
        if desk:
            lists = desk.get("lists") or {}
            pulse = lists.get("market_pulse_latest") or {}
        off_nas = pulse.get("dist_nasdaq")
        off_spx = pulse.get("dist_spx")
        # App-calculated placeholders — real values come from market states if present
        app_nas = "앱계산"
        app_spx = "앱계산"
        st.caption(
            f"DD 비교 · 앱: NAS {app_nas} / SPX {app_spx} · "
            f"IBD Pulse 공식: NAS {off_nas or '—'} / SPX {off_spx or '—'} "
            f"(기준 {pulse.get('date') or '—'})"
        )
    except Exception:
        pass

print("v14.28 DD compare helper loaded")
