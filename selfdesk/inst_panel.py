"""기관동향 탭. 사이드바에서 고른 종목만 본다. IBD 수동 입력은 쓰지 않는다."""
from __future__ import annotations

import inspect
from html import escape

import streamlit as st

from selfdesk.inst import load_us, fetch_kr, resolve_kind, ownership_band, explain_filed_gap


@st.cache_data(ttl=1800, show_spinner=False)
def _load_us(symbol: str):
    return load_us(symbol)


@st.cache_data(ttl=1800, show_spinner=False)
def _load_kr(code: str):
    return fetch_kr(code)


def _ui():
    frame = inspect.currentframe()
    while frame:
        if "card" in frame.f_globals and "table" in frame.f_globals:
            return frame.f_globals
        frame = frame.f_back
    return {}


def _pct(value, digits=1):
    if value is None:
        return "—"
    return f"{value:.{digits}f}%"


def _signed(value):
    if value is None:
        return "—"
    return f"{value:+,}"


def _won(value):
    if value is None:
        return "—"
    sign = "+" if value > 0 else ""
    return f"{sign}{value / 100_000_000:,.1f}억"


def _shares(value):
    if value is None:
        return "—"
    return f"{value:,}"


def _act(tag, action):
    if tag is None:
        return escape(action)
    kind = {"확대": "pass", "축소": "fail", "유지": "idle"}.get(action, "idle")
    return tag(action, kind)


def render_self_inst() -> None:
    ui = _ui()
    card, table = ui.get("card"), ui.get("table")
    step_header, read_box = ui.get("step_header"), ui.get("read_box")
    tag = ui.get("tag")
    symbol = str(st.session_state.get("tk_active") or "").strip()
    if not symbol:
        g = ui or {}
        symbol = str(g.get("TK") or "").strip()
    market = str(st.session_state.get("tk_market") or "")
    name = str(st.session_state.get("tk_name") or "")
    where = "한국 거래원 순매수" if market == "KR" or (symbol.isdigit() and len(symbol) == 6) else "미국 13F · 상위 뮤추얼펀드"
    st.markdown(
        '<div class="masthead"><h1>기관투자동향 (I)</h1><div class="sub">'
        "사이드바에서 조회한 종목 · IBD 입력 없음</div></div>",
        unsafe_allow_html=True,
    )
    if not symbol:
        st.info("사이드바에서 종목을 조회하면 이 탭에 기관 변화가 나옵니다.")
        return
    st.markdown(
        f'<div class="ev"><b>{escape(symbol)}</b> {escape(name)} · {where}</div>',
        unsafe_allow_html=True,
    )
    st.caption("코드를 다시 넣지 않습니다. 사이드바 종목을 바꾸면 이 탭도 같이 바뀝니다.")
    if st.button("이 종목 다시 받기", key="self_inst_refresh"):
        _load_us.clear()
        _load_kr.clear()
    try:
        kind, code = resolve_kind(symbol, market)
        with st.spinner(f"{code} 기관 자료를 가져오는 중"):
            if kind == "KR":
                _render_kr(code, card, table, step_header, read_box, tag)
            else:
                _render_us(code, card, table, step_header, read_box, tag, _stock_inst_pct(ui))
    except Exception as exc:
        st.warning(f"{symbol} 기관 자료를 받지 못했습니다: {exc}")


def _stock_inst_pct(ui) -> float | None:
    """The individual-stock card reads CTX fnd.inst. Use that exact figure."""
    ctx = (ui or {}).get("CTX") or {}
    fnd = ctx.get("fnd") or {}
    value = fnd.get("inst")
    try:
        if value is None or value != value:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _render_us(symbol, card, table, step_header, read_box, tag, shown_pct=None) -> None:
    snap = _load_us(symbol)
    judge = snap["judge"]
    yahoo = snap.get("yahoo") or {}
    shown = shown_pct if shown_pct is not None else yahoo.get("own_pct")
    filed = snap.get("own_pct")
    net = None
    if snap.get("new") is not None and snap.get("sold") is not None:
        net = snap["new"] - snap["sold"]
    own_tone = "up" if shown is not None and 15 <= shown <= 90 else "mut"
    specs = [
        ("기관 보유 비중", _pct(shown, 1), ownership_band(shown), own_tone),
        ("보고 기관", f"{snap['holders']:,}" if snap.get("holders") is not None else "—", "이번 분기 13F 건수", ""),
        ("신규 − 청산", _signed(net), f"신규 {snap.get('new') if snap.get('new') is not None else '—'} · 청산 {snap.get('sold') if snap.get('sold') is not None else '—'}", ""),
        ("확대 / 축소", f"{snap.get('increased') if snap.get('increased') is not None else '—'} / {snap.get('decreased') if snap.get('decreased') is not None else '—'}", "지분을 늘린 곳 / 줄인 곳", ""),
    ]
    if card:
        cols = st.columns(4)
        for col, (k, v, d, cls) in zip(cols, specs):
            col.markdown(card(k, v, d, cls), unsafe_allow_html=True)
    else:
        for k, v, d, _cls in specs:
            st.write(f"{k}: {v} · {d}")
    if read_box:
        read_box("<br>".join(escape(line) for line in judge["notes"]), judge["stance"], "oneil")
    else:
        st.subheader(judge["stance"])
        for line in judge["notes"]:
            st.caption(line)
    st.caption(explain_filed_gap(shown, filed))
    if step_header:
        step_header("13F", "보유 상위", "지수 운용과 그 밖을 가른다. 상위만이고 전체가 아니다.")
    st.caption("Vanguard · BlackRock · State Street · Geode · Northern Trust · Schwab 은 지수 운용으로 봅니다.")
    rows = [
        [
            f"<b>{escape(row['name'])}</b>",
            escape(row["date"] or "—"),
            _shares(row["shares"]),
            _signed(row["change"]),
            _pct(row["change_pct"], 2),
            "지수" if row["indexer"] else "일반",
            _act(tag, row["action"]),
        ]
        for row in snap.get("rows") or []
    ]
    if table and rows:
        st.markdown(table(["기관", "보고일", "보유", "변화(주)", "변화%", "구분", "움직임"], rows), unsafe_allow_html=True)
    if step_header:
        step_header("FUND", "상위 뮤추얼펀드", snap["funds_judge"]["text"])
    else:
        st.caption(snap["funds_judge"]["text"])
    funds = yahoo.get("funds") or []
    if table and funds:
        st.markdown(
            table(
                ["펀드", "보고일", "보유비중", "주식변화", "움직임"],
                [
                    [
                        f"<b>{escape(row['name'])}</b>",
                        escape(row["date"] or "—"),
                        _pct(row["pct_held"], 2),
                        _pct(row["change_pct"], 2),
                        _act(tag, row["action"]),
                    ]
                    for row in funds
                ],
            ),
            unsafe_allow_html=True,
        )
    elif yahoo.get("error"):
        st.caption("펀드 목록을 받지 못했습니다.")
    st.caption(
        "이번 분기 신규·청산·확대만 말합니다. 몇 분기 연속인지, 그 펀드 안의 신규 상위 3~4인지는 이 자료에 없습니다. "
        "13F는 분기 말 기준이고 보통 45일 뒤에 공개됩니다. 매수 신호가 아닙니다."
    )


def _render_kr(code, card, table, step_header, read_box, tag) -> None:
    flow = _load_kr(code)
    judge = flow["judge"]
    tone = "down" if "매도" in judge["stance"] else ("up" if "매수" in judge["stance"] else "mut")
    specs = [
        (f"최근 {flow['days']}거래일 기관", _won(flow.get("recent_inst")), "거래소 순매수", tone),
        ("직전 20거래일 기관", _won(flow.get("prior_inst")), "바로 앞 구간", ""),
        (f"최근 {flow['days']}거래일 외국인", _won(flow.get("recent_foreign")), "기관과 별도", ""),
    ]
    if card:
        cols = st.columns(3)
        for col, (k, v, d, cls) in zip(cols, specs):
            col.markdown(card(k, v, d, cls), unsafe_allow_html=True)
    if read_box:
        read_box("<br>".join(escape(line) for line in judge["notes"]), judge["stance"], "oneil")
    else:
        st.subheader(judge["stance"])
    if step_header:
        step_header("수급", "최근 거래일", "금액은 억원. 미국 13F가 아니다.")
    if table and flow.get("tail"):
        st.markdown(
            table(
                ["날짜", "기관", "외국인"],
                [[escape(row["date"]), _won(row["inst"]), _won(row["foreign"])] for row in flow["tail"]],
            ),
            unsafe_allow_html=True,
        )
