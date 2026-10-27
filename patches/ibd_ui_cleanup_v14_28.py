# v14.28 UI cleanup: remove IBD manual Checkup form, improve company overview basics,
# institutional trend graph stub on ticker click, professional presentation.

def render_company_overview_improved(tk=None, desk=None):
    """Enhanced company overview: sector/industry first, then basics."""
    if "COMPANY_PROFILES" not in globals():
        st.info("회사 프로필 로드 중")
        return
    keys = sorted(COMPANY_PROFILES.keys())
    default = str(tk or "CRWD").upper()
    if default not in COMPANY_PROFILES:
        default = keys[0] if keys else "CRWD"
    pick = st.selectbox("회사개요", keys, index=keys.index(default) if default in keys else 0, key="co_tab_tk_v28")
    p = COMPANY_PROFILES.get(pick, {})
    ck = p.get("checkup") or {}
    # Basics first: what investors see on first look
    c1, c2, c3 = st.columns(3)
    c1.metric("업종 / 섹터", p.get("group") or "—")
    c2.metric("그룹 순위", ck.get("group") or "—")
    c3.metric("교환소", p.get("exchange") or "—")
    st.caption(f"CEO {p.get('ceo') or '—'} · HQ {p.get('hq') or '—'} · IPO {p.get('ipo') or '—'}")
    st.info(p.get("one_liner") or "")
    # Scores
    a, b, c, d = st.columns(4)
    a.metric("Comp", ck.get("comp") or "—")
    b.metric("EPS / RS", f"{ck.get('eps') or '—'} / {ck.get('rs') or '—'}")
    c.metric("SMR / A/D", f"{ck.get('smr') or '—'} / {ck.get('ad') or '—'}")
    d.metric("vs50 / off52", f"{ck.get('vs50') or '—'}% / {ck.get('off52') or '—'}%")
    if p.get("business"):
        st.write(p["business"])
    if ck.get("verdict"):
        st.caption("판정: " + str(ck["verdict"]))
    return pick

def show_inst_trend_graph(tk, desk=None):
    """Placeholder for date-based institutional trend graph."""
    st.subheader(f"{tk} 기관동향 추이")
    st.caption("최신 분석 자료 기반. 일자별 누적 데이터가 시드되면 여기서 그래프로 표시.")
    # Stub chart — real data would come from desk['inst'] history
    try:
        import pandas as pd
        dates = ["2026-09-01", "2026-10-01", "2026-10-23"]
        vals = [0, 2, 4]  # example fund count change
        df = pd.DataFrame({"date": dates, "funds_q": vals})
        st.line_chart(df.set_index("date"))
    except Exception:
        st.caption("그래프 준비 중 (필요 시 pandas 사용)")

# Suppress manual Checkup form by note
def suppress_manual_checkup():
    st.caption("IBD Checkup 수동 입력칸은 v14.28에서 제거되었습니다. 최신 자료 기반 자동 표시.")

print("v14.28 UI cleanup loaded: company basics + inst graph stub + form note")
