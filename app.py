# -*- coding: utf-8 -*-
"""자체 시장 데스크. IBD 입력·Pulse·Checkup 화면은 없다."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from selfdesk.engine import compose_market, make_entry, score_index, verify_entry
from selfdesk.yahoo import fetch_daily

ROOT = Path(__file__).resolve().parent
LEDGER_PATH = ROOT / "data" / "dd_ledger.json"
INDEXES = [("^IXIC", "나스닥 종합"), ("^GSPC", "S&P 500")]


def load_ledger() -> dict:
    if not LEDGER_PATH.exists():
        return {"entries": []}
    try:
        doc = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"entries": []}
    if not isinstance(doc, dict) or not isinstance(doc.get("entries"), list):
        return {"entries": []}
    return doc


def save_ledger(doc: dict) -> bool:
    try:
        LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        LEDGER_PATH.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except Exception:
        return False


def merge_today(bars_by_symbol: dict[str, list]) -> tuple[dict, bool]:
    doc = load_ledger()
    saved_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    changed = False
    for symbol, bars in bars_by_symbol.items():
        entry = make_entry(symbol, bars, saved_at)
        exists = any(
            e.get("symbol") == entry["symbol"] and e.get("sessionDate") == entry["sessionDate"]
            for e in doc["entries"]
        )
        if not exists:
            doc["entries"].append(entry)
            changed = True
    if changed:
        save_ledger(doc)
    return doc, changed


@st.cache_data(ttl=1800, show_spinner=False)
def load_indexes():
    return {symbol: fetch_daily(symbol, "1y") for symbol, _label in INDEXES}


st.set_page_config(page_title="자체 시장 데스크", layout="wide")
st.title("자체 시장 데스크")
st.caption(
    "IBD 자료 입력·Pulse·Checkup 표시는 제거했습니다. "
    "나스닥과 S&P 일봉으로 분산일을 계산하고, 세션마다 저장한 뒤 같은 봉으로 다시 검증합니다. "
    "분산이 쌓이면 시장 점수는 원점수가 높아도 상한에 묶입니다. 매수 권유가 아닙니다."
)

if st.button("지수 다시 받기"):
    load_indexes.clear()

try:
    bars_by = load_indexes()
except Exception as exc:
    st.error(f"시세를 받지 못했습니다: {exc}")
    st.stop()

scores = {symbol: score_index(symbol, bars) for symbol, bars in bars_by.items()}
market = compose_market(scores["^IXIC"], scores["^GSPC"])
ledger, wrote = merge_today(bars_by)

c1, c2, c3 = st.columns(3)
c1.metric("억제 후 시장 점수", market["published"], delta=f"원점수 {market['raw']} · 상한 {market['ceiling']}")
c2.metric("입장", market["stance"])
c3.metric("노출", market["exposure"])
if market["aggressive_blocked"]:
    st.warning("적극 매수 구간은 닫혀 있습니다. 두 지수 분산이 각 1개 이하이고 오늘 분산이 없으며 둘 다 이평 위일 때만 열립니다.")
else:
    st.info("제한적 적극만 허용됩니다. 돌파 확인 없는 추격은 포함하지 않습니다.")
for cap in market["caps"]:
    st.caption(cap["reason"])
if wrote:
    st.caption("오늘 세션을 장부에 새로 저장했습니다.")

tab_m, tab_l = st.tabs(["지수", "분산일 장부"])
with tab_m:
    left, right = st.columns(2)
    for col, (symbol, label) in zip((left, right), INDEXES):
        sc = scores[symbol]
        with col:
            st.subheader(label)
            st.write(
                f"{sc['session_date']} 종가 {sc['close']:,.2f} ({sc['chg_pct']:+.2f}%) · "
                f"유효 분산 {sc['active_count']} · 10일 밀집 {sc['cluster10']}"
            )
            st.write(f"원점수 {sc['raw']} → 표시 {sc['published']} · 상한 {sc['ceiling']}")
            for cap in sc["caps"]:
                st.caption(cap["reason"])
            if sc["active"]:
                st.dataframe(
                    [
                        {
                            "날짜": d["date"],
                            "등락%": d["chg_pct"],
                            "거래량배": d["vol_vs_prev"],
                            "만료": "아니오",
                        }
                        for d in sc["active"]
                    ],
                    hide_index=True,
                    use_container_width=True,
                )
            else:
                st.caption("유효 분산일이 없습니다.")

with tab_l:
    st.write("규칙: 종가 -0.2% 이하, 거래량 증가, 최근 25거래일, 이후 +5%면 만료. 저장본과 재계산이 다르면 불일치입니다.")
    rows = []
    for entry in reversed(ledger["entries"][-40:]):
        bars = bars_by.get(entry.get("symbol"))
        verdict = verify_entry(entry, bars) if bars else {"ok": False, "issues": ["수신 범위 밖"], "liveCount": None}
        rows.append(
            {
                "세션": entry.get("sessionDate"),
                "지수": "나스닥" if entry.get("symbol") == "^IXIC" else "S&P",
                "저장": entry.get("activeCount"),
                "재계산": verdict["liveCount"],
                "검증": "일치" if verdict["ok"] else "불일치",
                "내용": "" if verdict["ok"] else " · ".join(verdict["issues"]),
            }
        )
    st.dataframe(rows, hide_index=True, use_container_width=True)
    st.caption("클라우드에서는 장부 파일이 재시작 때 저장소 버전으로 돌아갈 수 있습니다. 화면의 검증은 매번 실제 일봉으로 다시 셉니다.")
