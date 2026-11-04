"""Company tab for the sidebar ticker only. Long-term and near-term CANSLIM, no IBD sheets."""
from __future__ import annotations

import inspect
from html import escape

import streamlit as st

from selfdesk.profile import clear_profile_cache, fetch_profile


def _ui():
    frame = inspect.currentframe()
    while frame:
        g = frame.f_globals
        if "CTX" in g or "TK" in g or "card" in g:
            return g
        frame = frame.f_back
    return {}


def _num(value, digits=1, suffix=""):
    if value is None:
        return "—"
    try:
        return f"{float(value):,.{digits}f}{suffix}"
    except Exception:
        return str(value)


def _pct(value):
    if value is None:
        return "—"
    return f"{float(value):+.1f}%"


def _ma_gap(df, price, window):
    try:
        close = df["Close"].astype(float)
        if len(close) < window or not price:
            return None, None
        ma = float(close.rolling(window).mean().iloc[-1])
        if not ma:
            return None, None
        return ma, (float(price) / ma - 1.0) * 100.0
    except Exception:
        return None, None


def render_company() -> None:
    g = _ui()
    ctx = g.get("CTX") or {}
    tk = str(g.get("TK") or st.session_state.get("tk_active") or "").strip()
    name = ctx.get("name") or st.session_state.get("tk_name") or tk
    market = ctx.get("market") or st.session_state.get("tk_market")
    fnd = ctx.get("fnd") or {}
    card = g.get("card")
    step_header = g.get("step_header")
    read_box = g.get("read_box")

    st.markdown(
        f'<div class="masthead"><h1>{escape(str(name))}</h1><div class="sub">{escape(str(tk or "종목 없음"))}'
        " · 사이드바에서 연 종목만 봅니다. 다른 회사 목록은 없습니다.</div></div>",
        unsafe_allow_html=True,
    )
    if not tk:
        st.warning("사이드바에서 종목을 먼저 조회하세요.")
        return
    if st.button("이 회사 다시 받기", key="co_live_refresh"):
        clear_profile_cache()
    try:
        prof = fetch_profile(tk, market)
    except Exception as exc:
        st.warning(f"회사 설명을 받지 못했습니다: {exc}")
        prof = {}

    quote_at = prof.get("quote_at") or "시세 시각 없음"
    fetched = prof.get("fetched_at") or ""
    st.caption(f"자료 기준 · 시세 {quote_at} · 회사 설명 조회 {fetched} · {prof.get('symbol') or tk}")

    if step_header:
        step_header("사업", "무엇을 하는 회사인가", prof.get("industry") or "")
    summary = prof.get("summary") or "사업 설명을 받지 못했습니다."
    st.write(summary[:900])
    facts = [
        f"섹터 {prof.get('sector') or fnd.get('sector') or '—'}",
        f"산업 {prof.get('industry') or fnd.get('industry') or '—'}",
        f"CEO {prof.get('ceo') or '—'}",
        f"직원 {_num(prof.get('employees'), 0)}",
        f"{prof.get('city') or ''} {prof.get('country') or ''}".strip() or "본사 —",
    ]
    st.caption(" · ".join(facts))
    if prof.get("website"):
        st.caption(prof["website"])

    sector_name = fnd.get("sector") or prof.get("sector")
    sect = None
    try:
        from selfdesk.sector_lookup import sector_for_stock
        sect = sector_for_stock(sector_name)
    except Exception:
        sect = None
    price = ctx.get("price") or prof.get("price")
    df = ctx.get("df")
    _, gap50 = _ma_gap(df, price, 50)
    _, gap200 = _ma_gap(df, price, 200)
    hi52 = fnd.get("hi52")
    off52 = None
    if hi52 and price:
        try:
            off52 = (float(price) / float(hi52) - 1.0) * 100.0
        except Exception:
            off52 = None
    roe = fnd.get("roe") if fnd.get("roe") is not None else prof.get("roe")
    opm = fnd.get("opm") if fnd.get("opm") is not None else prof.get("operating_margin")
    debt = fnd.get("debt") if fnd.get("debt") is not None else prof.get("debt_to_equity")

    if step_header:
        step_header("장기", "C · A — 이 회사를 몇 년 들고 갈 이야기", "성장이 25%를 넘고 이익의 질이 남는지")
    long_rows = [
        ("매출 성장", _pct(prof.get("revenue_growth")), "야후가 준 최근 매출 성장"),
        ("이익 성장", _pct(prof.get("earnings_growth")), "야후가 준 최근 이익 성장"),
        ("ROE", _num(roe, 1, "%"), "개별종목과 같은 값이면 그 값을 씀"),
        ("영업이익률", _num(opm, 1, "%"), "높을수록 본업이 돈을 남김"),
        ("부채비율", _num(debt, 1), "몇 년새 불어나면 이익의 질을 의심"),
    ]
    cols = st.columns(5)
    for col, (title, value, note) in zip(cols, long_rows):
        if card:
            col.markdown(card(title, value, note), unsafe_allow_html=True)
        else:
            col.metric(title, value, note)
    rev, earn = prof.get("revenue_growth"), prof.get("earnings_growth")
    if rev is not None and earn is not None and rev >= 25 and earn >= 25:
        long_line = "최근 매출과 이익 성장이 모두 25%를 넘습니다. 오닐이 장기에서 찾는 속도입니다."
    elif rev is not None or earn is not None:
        long_line = "최근 성장률이 25%에 못 미치거나 한쪽만 있습니다. 개별종목 탭의 3년·6분기 표로 한 번이 아닌지 확인합니다."
    else:
        long_line = "성장률을 받지 못했습니다. 개별종목 탭의 실적표를 봅니다."
    long_text = (
        "오닐의 장기 칸은 올해 한 분기 실적이 아닙니다. 연간 이익이 계속 늘고, 매출도 같이 늘며, "
        "증가율이 25% 위에 있는 회사인지입니다. "
        + long_line
        + " PER이 높다는 이유만으로 지우지 않습니다. 3년 연속은 이 문장이 아니라 개별종목 실적표가 맞습니다."
    )
    if read_box:
        read_box(long_text, "장기 · C와 A", "oneil")
    else:
        st.info(long_text)

    if step_header:
        step_header("단기", "N · S · L — 오늘 이 자리에서 쫓아도 되는가", "고점 이격, 이평선, 업종 순위")
    short_rows = [
        ("50일선", _pct(gap50) if gap50 is not None else "—", "위면 양수"),
        ("200일선", _pct(gap200) if gap200 is not None else "—", "아래면 방어"),
        ("52주 고점", _pct(off52) if off52 is not None else "—", "0%에 가까울수록 고점"),
        ("업종 순위", f'{sect["rank"]}위/{sect["total"]}' if sect else "—",
         sect["label"] if sect else "미국 11섹터에 없으면 시장 탭"),
        ("다음 실적", prof.get("next_earnings") or "—", "실적 직전 추격은 별도 위험"),
    ]
    cols = st.columns(5)
    for col, (title, value, note) in zip(cols, short_rows):
        if card:
            col.markdown(card(title, value, note), unsafe_allow_html=True)
        else:
            col.metric(title, value)
    bits = []
    if off52 is not None and off52 >= -8:
        bits.append("주가가 52주 고점 근처입니다. 오닐은 여기서 피벗 돌파를 보되, 이미 멀리 달린 자리는 쫓지 않습니다.")
    elif off52 is not None and off52 <= -20:
        bits.append("고점에서 20% 넘게 내려와 있습니다. 회사 이야기가 좋아도 단기 매수 자리는 아닙니다.")
    if gap50 is not None and gap50 < 0:
        bits.append("50일선 아래입니다. 상승 추세의 눌림이 아니라 추세가 깨진 쪽에 가깝습니다.")
    if gap200 is not None and gap200 < 0:
        bits.append("200일선 아래입니다. 장기 이야기가 있어도 단기에는 방어입니다.")
    if sect and sect["rank"] <= 4:
        bits.append(f"업종은 {sect['rank']}위로 앞쪽입니다. 주도 그룹에 속해 있습니다.")
    elif sect:
        bits.append(f"업종은 {sect['rank']}위입니다. 종목만 세고 그룹이 처져 있으면 오닐은 피했습니다.")
    if prof.get("short_pct") is not None:
        bits.append(f"공매도 비중 {prof['short_pct']:.1f}%.")
    bits.append("시장이 닫혀 있으면 이 회사가 좋아도 사지 않습니다. 시장은 시장 탭에서 봅니다.")
    short_text = " ".join(bits)
    if read_box:
        read_box(short_text, "단기 · 자리", "oneil")
    else:
        st.info(short_text)
    st.caption("매수 지시가 아닙니다. IBD 등급이나 수록 회사 목록은 이 탭에 넣지 않습니다.")
