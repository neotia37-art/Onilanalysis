"""Market-tab sector board. One request, shared with the stock tab."""
from __future__ import annotations

import inspect

import streamlit as st

from selfdesk.sector_lookup import clear_sector_cache, load_sector_ranks


def _ui():
    frame = inspect.currentframe()
    while frame:
        if "table" in frame.f_globals and "card" in frame.f_globals:
            return frame.f_globals
        frame = frame.f_back
    return {}


def _pct(value):
    if value is None:
        return "—"
    return f"{value:+.1f}%"


def render_sector_ranks() -> None:
    ui = _ui()
    table = ui.get("table")
    step_header = ui.get("step_header")
    st.subheader("섹터 순위")
    st.caption(
        "미국 SPDR 11섹터입니다. 순위는 6개월 가격 수익률이고, 같으면 3개월, 그다음 1개월입니다. "
        "시세는 한 번만 받습니다. 개별종목 탭의 업종 순위도 이 표와 같은 기준입니다. "
        "사이드바 종목이 한국이어도 이 표는 미국 업종입니다. 매수 순위가 아닙니다."
    )
    if st.button("섹터 다시 받기", key="self_sector_refresh"):
        clear_sector_cache()
    try:
        board = load_sector_ranks()
    except Exception as exc:
        st.warning(f"섹터 순위를 받지 못했습니다. 아래 시장 판단은 그대로 둡니다: {exc}")
        return
    if step_header:
        step_header("SECTOR", "6개월 가격 수익률", f"자료 기준 {board.get('asof') or '—'}")
    else:
        st.caption(f"자료 기준 {board.get('asof') or '—'}")
    body = [
        [
            str(row["rank"]),
            row["name"],
            row["etf"],
            _pct(row["r6"]),
            _pct(row["r3"]),
            _pct(row["r1"]),
            row["date"],
        ]
        for row in board["rows"]
    ]
    headers = ["순위", "섹터", "ETF", "6개월", "3개월", "1개월", "마지막 봉"]
    if table:
        st.markdown(table(headers, body), unsafe_allow_html=True)
    else:
        st.dataframe(
            [dict(zip(headers, row)) for row in body],
            hide_index=True,
            use_container_width=True,
        )
    st.divider()
