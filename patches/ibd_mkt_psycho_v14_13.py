# 시장 탭 5대 심리지표 + 누적 추이 + FTD/분산 종합코멘트 v14.13
MKT_PSYCHO_V14_13 = True

# IBD Psychological Market Indicators (원전 인쇄본을 손으로 옮긴다)
# 1 VIX  2 Put/Call  3 High-Low Ratio  4 Bulls vs Bears  5 Margin Debt YoY
PSYCHO_SEED_HISTORY = [
    {
        "date": "2026-09-01",
        "source": "DailyPsycho_090126",
        "vix": 15.5, "put_call": 0.79, "high_low": None,
        "bulls": 51.9, "bears": 30.9, "margin_yoy": 38.6,
        "note": "월요 인쇄. VIX 15.5 · P/C 0.79 · 불 51.9/베어 30.9.",
    },
    {
        "date": "2026-09-03",
        "source": "MARKET PULSE.png + book v14.5",
        "vix": 15.2, "put_call": 0.73, "high_low": None,
        "bulls": 45.0, "bears": None, "margin_yoy": 38.6,
        "note": "Pulse 노출 60-80% · NAS DD 4 / SPX 3 · FTD 2026-06-02.",
    },
    {
        "date": "2026-09-08",
        "source": "DailyPsycho_090826 + IBD Psychological pages",
        "vix": 14.6, "put_call": 0.71, "high_low": 0.71,
        "bulls": 54.9, "bears": 17.6, "margin_yoy": 38.6,
        "pc_web": 0.72,
        "note": "화요 종가. VIX 14.6 · P/C 0.71(웹 0.72) · H/L 0.71 · 불 54.9/베어 17.6 · 마진 38.6%(7월).",
    },
]

PSYCHO_EXPLAIN = {
    "vix": (
        "CBOE VIX (S&P 500 옵션 내재변동성). IBD 인쇄는 '45 초과가 강세(공포=바닥 후보)'다. "
        "VIX가 10일선 대비 +20% 이상 치솟으면 단기 바닥 확인에 쓴다. "
        "14~16은 안일·저변동. 추격 허가 신호가 아니다."
    ),
    "put_call": (
        "풋 거래량 / 콜 거래량. 1.0 근처·이상은 헤지·공포(역발상 매수 후보). "
        "0.50~0.70은 콜 편중=낙관. 오닐은 이걸 매수 방아쇠로 쓰지 않는다."
    ),
    "high_low": (
        "IBD High-Low Ratio = 신고가/신저가. 강세장 중간조정에서 0.5 아래로 내려간 뒤 "
        "첫 상승일이 단기 바닥 힌트. 약세장(200일선 아래)은 문턱이 0.1로 내려간다. "
        "0.71은 문턱 위라 '반등 트리거'가 아니다."
    ),
    "bulls_bears": (
        "Investors Intelligence 투자자문 강세/약세 %. 강세가 높고 약세가 극단적으로 낮으면 "
        "군중 낙관=경계. 약세가 치솟을 때가 역발상 바닥 쪽이다."
    ),
    "margin": (
        "신용잔고 전년비. 55%를 넘으면 1970년대 이후 대형 천정 경고로 본다. "
        "월간 지표라 매일 안 바뀐다. 지금은 38.6%(2026-07)로 경고선 아래."
    ),
}
