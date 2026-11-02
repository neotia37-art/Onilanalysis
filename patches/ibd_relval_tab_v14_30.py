"""CANSLIM TERMINAL v14.30 — Relative Valuation Tab (auto-update on earnings)

RELVAL_TAB_V14_30
"""
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

def get_valuation_metrics(ticker):
    try:
        t = yf.Ticker(ticker)
        info = t.info
        return {
            "price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "fwd_pe": info.get("forwardPE"),
            "fwd_ps": info.get("priceToSalesTrailing12Months"),
            "peg": info.get("pegRatio"),
            "growth": info.get("earningsGrowth") or info.get("revenueGrowth"),
            "margin": info.get("grossMargins") or info.get("operatingMargins"),
        }
    except Exception:
        return {}

def render_relval_tab():
    st.header("상대 밸류에이션 분석 (자동 업데이트)")
    st.caption("실적 발표 후 yfinance 데이터 기반으로 스프레드·시나리오가 갱신됩니다. 캐시 새로고침 시 최신 반영.")

    pairs = [
        ("LITE", "COHR"),
        ("NVDA", "AMD"),
        ("NVDA", "AVGO"),
        ("NVDA", "MRVL"),
        ("PLTR", "NOW"),
        ("GOOGL", "META"),
        ("MSFT", "GOOGL"),
        ("AMZN", "GOOGL"),
        ("TSLA", "NVDA"),
    ]

    if st.button("최신 데이터 새로고침"):
        st.cache_data.clear()

    @st.cache_data(ttl=3600)
    def load_pair(a, b):
        ma = get_valuation_metrics(a)
        mb = get_valuation_metrics(b)
        return ma, mb

    rows = []
    for a, b in pairs:
        ma, mb = load_pair(a, b)
        if not ma or not mb:
            continue
        pe_spread = (ma.get("fwd_pe") or 0) - (mb.get("fwd_pe") or 0)
        ps_spread = (ma.get("fwd_ps") or 0) - (mb.get("fwd_ps") or 0)
        rows.append({
            "비교": f"{a} vs {b}",
            "주가A": ma.get("price"),
            "주가B": mb.get("price"),
            "Fwd PE A": ma.get("fwd_pe"),
            "Fwd PE B": mb.get("fwd_pe"),
            "PE 스프레드": pe_spread,
            "Fwd PS A": ma.get("fwd_ps"),
            "Fwd PS B": mb.get("fwd_ps"),
            "PS 스프레드": ps_spread,
            "PEG A": ma.get("peg"),
            "성장A": ma.get("growth"),
        })

    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df.style.format({
            "주가A": "{:.1f}", "주가B": "{:.1f}",
            "Fwd PE A": "{:.1f}", "Fwd PE B": "{:.1f}", "PE 스프레드": "{:.1f}",
            "Fwd PS A": "{:.1f}", "Fwd PS B": "{:.1f}", "PS 스프레드": "{:.1f}",
            "PEG A": "{:.2f}", "성장A": "{:.1%}",
        }), use_container_width=True)

    st.subheader("PLTR 반증 조건 시나리오 (예시)")
    st.markdown("""
- **Bull**: 미국 상업 성장 ≥50% 유지 → 멀티플 유지
- **Base**: 40~50% → 멀티플 압축 시작
- **Bear**: <42% 2분기 연속 → AIP 엔진 약화
- **Severe**: 전체 성장 <25% 2분기 연속 → 고성장 스토리 종료
    """)
    st.info("실적 발표 후 이 탭을 새로고침하면 최신 컨센서스 기반 스프레드가 자동 반영됩니다.")

# Tab injection marker
if "RELVAL_TAB_V14_30" not in globals():
    pass
