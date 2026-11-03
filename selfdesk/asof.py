"""One collection-date line at the top of every tab. No extra network calls."""
from __future__ import annotations

import inspect
from datetime import datetime, timedelta, timezone
from html import escape

_KST = timezone(timedelta(hours=9))
_NOTE = {
    "시장": "섹터 순위의 기준일은 섹터 표에 적는다.",
    "환율": "환율 시계열의 마지막 날은 아래 차트의 끝이다.",
    "뉴스": "기사 시각은 각 줄의 날짜다. 이 줄에서 뉴스를 다시 받지 않는다.",
    "기관동향": "13F 보고일은 아래 표의 보고일이다. 보유 비중은 개별종목 탭과 같은 조회다.",
    "사용 가이드": "이 탭은 시세를 새로 받지 않는다.",
    "FTD훈련": "연습 화면이다. 아래 날짜가 있으면 그때의 시세다.",
    "회사개요": "사업 설명은 수록 자료다. 시세 날짜만 여기 적는다.",
}


def _app_globals():
    frame = inspect.currentframe()
    while frame:
        if "CTX" in frame.f_globals or "TABS" in frame.f_globals:
            return frame.f_globals
        frame = frame.f_back
    return {}


def _day(value) -> str | None:
    if value is None:
        return None
    text = str(value).replace(" 00:00:00", "")
    return text[:10]


def _last_index(frame) -> str | None:
    try:
        if frame is None or len(frame.index) == 0:
            return None
        return _day(frame.index[-1])
    except Exception:
        return None


def _last_column(frame) -> str | None:
    try:
        if frame is None or len(getattr(frame, "columns", [])) == 0:
            return None
        return _day(frame.columns[-1])
    except Exception:
        return None


def asof_parts(section: str, g: dict | None = None) -> list[str]:
    g = g if g is not None else {}
    ctx = g.get("CTX") or {}
    parts = []
    opened = datetime.now(_KST).strftime("%Y-%m-%d %H:%M KST")
    parts.append(f"화면 {opened}")
    ticker = str(g.get("TK") or "").strip()
    if ticker:
        parts.append(f"종목 {ticker}")
    price_day = _last_index(ctx.get("df"))
    if price_day:
        parts.append(f"종목 시세 {price_day}")
    states = ctx.get("states") or {}
    for name, state in states.items():
        day = _last_index((state or {}).get("df"))
        if day:
            parts.append(f"{name} {day}")
    fnd = ctx.get("fnd") or {}
    q_day = _last_column(fnd.get("q_tab"))
    if q_day:
        parts.append(f"분기 실적표 {q_day}")
    y_day = _last_column(fnd.get("y_tab"))
    if y_day:
        parts.append(f"연간 실적표 {y_day}")
    note = _NOTE.get(section)
    if note:
        parts.append(note)
    return parts


def show_tab_asof(section: str) -> None:
    import streamlit as st

    parts = asof_parts(section, _app_globals())
    st.markdown(
        '<div class="hint"><b>자료 기준</b> · ' + " · ".join(escape(part) for part in parts) + "</div>",
        unsafe_allow_html=True,
    )
