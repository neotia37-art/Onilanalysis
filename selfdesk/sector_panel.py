"""Market-tab sector board. Does not replace the rest of the market tab."""
from __future__ import annotations

import inspect

import streamlit as st

from selfdesk.sectors import load_sector_ranks


@st.cache_data(ttl=1800, show_spinner=False)
def _ranks():
    return load_sector_ranks()


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
        "미국 SPDR 11섹터입니다. 순위는 6개월 수익률이고, 같으면 3개월, 그다음 1개월입니다. "
        "사이드바 종목이 한국이어도 이 표는 미국 업종입니다. 매수 순위가 아닙니다."
    )
    if st.button("섹터 다시 받기", key="self_sector_refresh"):
        _ranks.clear()
    try:
        board = _ranks()
    except Exception as exc:
        st.warning(f"섹터 순위를 받지 못했습니다: {exc}")
        return
    if step_header:
        step_header("SECTOR", "6개월 수익률 순위", f"자료 기준 {board.get('asof') or '—'}")
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
            [
                dict(zip(headers, row))
                for row in body
            ],
            hide_index=True,
            use_container_width=True,
        )
    if board.get("errors"):
        st.caption("빠진 섹터: " + " · ".join(board["errors"][:4]))
    st.divider()
