# v14.29: Load Pulse from data/market_pulse.json (bot-committed daily).
# Do not gate buys on stale Checkup; prefer latest IBD data only.

import json
from pathlib import Path

def _load_pulse_json():
    """Load latest Pulse from repo data/market_pulse.json."""
    try:
        # In Streamlit Cloud the file is in the repo root relative to app
        candidates = [
            Path("data/market_pulse.json"),
            Path("/mount/src/onilanalysis/data/market_pulse.json"),
            Path("/app/data/market_pulse.json"),
        ]
        for p in candidates:
            if p.exists():
                with p.open(encoding="utf-8") as f:
                    data = json.load(f)
                return data.get("latest") or (data.get("history") or [{}])[0]
    except Exception:
        pass
    return None

def ensure_pulse_from_json(desk):
    """Override market_pulse_latest with JSON if newer."""
    latest = _load_pulse_json()
    if not latest:
        return desk
    lists = desk.setdefault("lists", {})
    cur = lists.get("market_pulse_latest") or {}
    if str(latest.get("date") or "") >= str(cur.get("date") or ""):
        lists["market_pulse_latest"] = dict(latest)
        try:
            save_ibd_desk(desk)
        except Exception:
            pass
    return desk

# Chain into ensure_book_seed
_ensure_prev_json = ensure_book_seed if "ensure_book_seed" in globals() else None

def ensure_book_seed(desk):
    if _ensure_prev_json:
        desk = _ensure_prev_json(desk)
    return ensure_pulse_from_json(desk)

def show_inst_trend_real(tk, desk=None):
    """Show date-based institutional trend graph when ticker clicked."""
    st.subheader(f"{tk} 기관동향 일자별 추이")
    st.caption("최신 Daily Mutual 기반. Grok 봇이 업데이트한 자료를 사용.")
    try:
        if desk is None and "load_ibd_desk" in globals():
            desk = load_ibd_desk()
        rows = []
        if desk:
            for x in (desk.get("inst") or []):
                if str(x.get("ticker", "")).upper() == str(tk or "").upper():
                    rows.append(x)
        if not rows:
            st.info("이 종목의 기관 누적 데이터가 아직 없습니다. 최신 Mutual PDF를 봇이 수록하면 그래프가 나옵니다.")
            return
        import pandas as pd
        df = pd.DataFrame(rows)
        if "date" in df.columns:
            df = df.sort_values("date")
            # Simple funds count or AUM proxy if present
            ycol = "funds" if "funds" in df.columns else (df.columns[-1] if len(df.columns) > 1 else None)
            if ycol:
                st.line_chart(df.set_index("date")[ycol])
            else:
                st.dataframe(df)
        else:
            st.dataframe(df)
    except Exception as e:
        st.caption(f"그래프 준비: {e}")

print("v14.29 Pulse JSON loader + real inst trend graph ready")
