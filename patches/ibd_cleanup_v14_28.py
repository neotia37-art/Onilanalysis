# v14.28 cleanup: suppress residual A/B-layer / fear-greed cards and enforce badge location note

def _suppress_residual_cards():
    """Runtime note for residual print cards — actual removal is via loader string replace where safe."""
    pass

# Ensure any fear/greed header is clearly marked as app-only if it still appears
_orig_step_header = step_header if "step_header" in globals() else None

def step_header(title, sub="", note=""):
    if _orig_step_header:
        if "FEAR & GREED" in str(title) or "포공탐욕" in str(title):
            title = "FEAR & GREED (앱 자체 근사)"
            sub = "3층 판정과 별개 · CNN식 근사"
        return _orig_step_header(title, sub, note)
    return None

print("v14.28 cleanup: residual card labels adjusted")
