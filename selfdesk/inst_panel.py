"""기관동향 탭 맨 위. IBD 수동 입력은 그대로 둔다."""
from __future__ import annotations

import streamlit as st

from selfdesk.inst import load_us, fetch_kr, split_query


@st.cache_data(ttl=1800, show_spinner=False)
def _load_us(symbol: str):
    return load_us(symbol)


@st.cache_data(ttl=1800, show_spinner=False)
def _load_kr(code: str):
    return fetch_kr(code)


def _won(value):
    if value is None:
        return "—"
    sign = "+" if value > 0 else ""
    return f"{sign}{value / 100_000_000:,.1f}억"


def _pct(value, digits=1):
    if value is None:
        return "—"
    return f"{value:.{digits}f}%"


def _signed(value):
    if value is None:
        return "—"
    return f"{value:+,}"


def render_self_inst() -> None:
    st.subheader("자체 기관 · IBD 밖")
    st.caption(
        "미국은 Nasdaq 13F 집계(전체 기관의 신규·청산·확대·축소)와 Yahoo 상위 뮤추얼펀드다. "
        "한국 6자리는 거래소 투자자 순매수다. 분기 보고이지 오늘 매매가 아니고, 매수 신호가 아니다. "
        "아래 Mutual·Checkup·수동 입력은 그대로 둔다."
    )
    left, right = st.columns([3, 1])
    left.text_input("티커", key="self_inst_tk", placeholder="HCSG · AAPL · 005930")
    go = right.button("조회", key="self_inst_go", use_container_width=True)
    if go:
        st.session_state["self_inst_q"] = st.session_state.get("self_inst_tk") or ""
    if st.button("기관 자료 다시 받기", key="self_inst_refresh"):
        _load_us.clear()
        _load_kr.clear()
    query = (st.session_state.get("self_inst_q") or "").strip()
    if not query:
        st.info("티커를 넣고 조회하면 이 종목의 기관 변화를 계산합니다.")
        st.divider()
        return
    try:
        kind, symbol = split_query(query)
    except ValueError as exc:
        st.warning(str(exc))
        st.divider()
        return
    try:
        if kind == "KR":
            _render_kr(symbol)
        else:
            _render_us(symbol)
    except Exception as exc:
        st.warning(f"{symbol} 기관 자료를 받지 못했습니다: {exc}")
    st.divider()


def _render_us(symbol: str) -> None:
    snap = _load_us(symbol)
    judge = snap["judge"]
    yahoo = snap.get("yahoo") or {}
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("기관 보유율", _pct(snap.get("own_pct")))
    c2.metric("보고 기관", f"{snap['holders']:,}" if snap.get("holders") is not None else "—")
    net = None
    if snap.get("new") is not None and snap.get("sold") is not None:
        net = snap["new"] - snap["sold"]
    c3.metric("신규 − 청산", _signed(net), delta=f"신규 {snap.get('new') or '—'} · 청산 {snap.get('sold') or '—'}")
    c4.metric(
        "확대 vs 축소",
        f"{snap.get('increased') or '—'} / {snap.get('decreased') or '—'}",
    )
    if judge["stance"] == "이번 분기 보증 축소":
        st.warning(judge["stance"])
    elif judge["stance"] == "이번 분기 보증 확대":
        st.success(judge["stance"])
    else:
        st.info(judge["stance"])
    for line in judge["notes"]:
        st.caption(line)
    if yahoo.get("own_pct") is not None and snap.get("own_pct") is not None:
        gap = abs(yahoo["own_pct"] - snap["own_pct"])
        if gap >= 5:
            st.caption(
                f"보유율은 출처가 다릅니다. Nasdaq {_pct(snap['own_pct'])}, "
                f"Yahoo {_pct(yahoo['own_pct'])}."
            )
    st.markdown("**13F 보유 상위**")
    st.caption("Vanguard·BlackRock·State Street·Geode·Northern Trust·Schwab 은 지수 운용으로 분류합니다. 그 안의 액티브 펀드까지 구분하지는 않습니다.")
    st.dataframe(
        [
            {
                "기관": row["name"],
                "보고일": row["date"],
                "보유": f"{row['shares']:,}" if row["shares"] is not None else "—",
                "변화(주)": _signed(row["change"]),
                "변화%": _pct(row["change_pct"], 2),
                "구분": "지수" if row["indexer"] else "일반",
                "움직임": row["action"],
            }
            for row in snap.get("rows") or []
        ],
        hide_index=True,
        use_container_width=True,
    )
    st.markdown("**상위 뮤추얼펀드**")
    st.caption(snap["funds_judge"]["text"])
    funds = yahoo.get("funds") or []
    if funds:
        st.dataframe(
            [
                {
                    "펀드": row["name"],
                    "보고일": row["date"],
                    "보유비중": _pct(row["pct_held"], 2),
                    "주식변화": _pct(row["change_pct"], 2),
                    "움직임": row["action"],
                }
                for row in funds
            ],
            hide_index=True,
            use_container_width=True,
        )
    elif yahoo.get("error"):
        st.caption("펀드 목록 실패: " + str(yahoo["error"]))
    with st.expander("오닐 I 네 질문 중 여기서 답하는 것", expanded=False):
        st.markdown(
            "1. **우량 펀드가 새로 샀는가** — 상위 13F에서 지수 운용사를 뺀 이름의 지분 증가만 본다. "
            "36개월 등급은 없어서 우량이라고 부르지 않는다.\n"
            "2. **기존 보유가 추가했는가** — 이번 분기 확대 기관 수와 축소 기관 수.\n"
            "3. **그 펀드의 신규 상위 3~4인가** — 말하지 않는다. 펀드 포트폴리오 순위가 없다.\n"
            "4. **펀드 수가 몇 분기 늘었는가** — 이번 분기 신규에서 청산을 뺀 수만 말한다. 연속 분기는 없다."
        )
        st.caption("13F는 분기 말 기준이고 보통 45일 뒤에 공개된다. 보고일이 보유자마다 다를 수 있다.")


def _render_kr(code: str) -> None:
    flow = _load_kr(code)
    judge = flow["judge"]
    c1, c2, c3 = st.columns(3)
    c1.metric(f"최근 {flow['days']}거래일 기관", _won(flow.get("recent_inst")))
    c2.metric("직전 20거래일 기관", _won(flow.get("prior_inst")))
    c3.metric(f"최근 {flow['days']}거래일 외국인", _won(flow.get("recent_foreign")))
    if "매도" in judge["stance"]:
        st.warning(judge["stance"])
    elif "매수" in judge["stance"]:
        st.success(judge["stance"])
    else:
        st.info(judge["stance"])
    for line in judge["notes"]:
        st.caption(line)
    if flow.get("tail"):
        st.dataframe(
            [
                {
                    "날짜": row["date"],
                    "기관(억)": _won(row["inst"]),
                    "외국인(억)": _won(row["foreign"]),
                }
                for row in flow["tail"]
            ],
            hide_index=True,
            use_container_width=True,
        )
