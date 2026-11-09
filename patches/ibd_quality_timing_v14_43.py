# v14.43 — Quality Score (Comp-like) vs Timing/Buy Checklist Score
# Based on 2026-11-06 30-name comparison: separate leadership quality from "is it buyable now"
# Quality: less market/base penalty, closer to IBD Comp ranking
# Timing: existing checklist (market + base/pivot readiness)
# A/D proxy improved with 13-week up/down volume ratio

import pandas as pd
import numpy as np

def compute_quality_score(ctx, df=None):
    """Approximate Comp-like quality (0-100). Minimizes M and base readiness penalties."""
    if df is None:
        df = ctx.get("df") if isinstance(ctx, dict) else None
    if df is None or len(df) < 60 or "Close" not in df.columns:
        return None, "데이터 부족"

    try:
        close = df["Close"].dropna()
        vol = df["Volume"].dropna() if "Volume" in df.columns else None
        score = 50.0
        notes = []

        # RS proxy (1y return) — weight high
        if len(close) >= 252:
            ret1y = (close.iloc[-1] / close.iloc[-252] - 1) * 100
            rs_pts = max(0, min(30, 15 + ret1y / 4))
            score += rs_pts
            notes.append(f"RS대리 {int(50+ret1y/2)}")
        elif len(close) >= 126:
            ret6m = (close.iloc[-1] / close.iloc[-126] - 1) * 100
            score += max(0, min(20, 10 + ret6m / 5))
            notes.append("6m RS")

        # Price vs 50/200 (trend quality)
        if len(close) >= 50:
            ma50 = close.rolling(50).mean().iloc[-1]
            if close.iloc[-1] > ma50:
                score += 8
                notes.append("50선위")
        if len(close) >= 200:
            ma200 = close.rolling(200).mean().iloc[-1]
            if close.iloc[-1] > ma200:
                score += 6
                notes.append("200선위")

        # A/D proxy: 13-week (65 sessions) up-volume vs down-volume
        if vol is not None and len(vol) >= 65 and len(close) >= 65:
            recent = df.tail(65)
            up_days = recent["Close"] > recent["Close"].shift(1)
            down_days = recent["Close"] < recent["Close"].shift(1)
            up_vol = recent.loc[up_days, "Volume"].sum()
            down_vol = recent.loc[down_days, "Volume"].sum()
            if down_vol > 0:
                ratio = up_vol / down_vol
                if ratio > 1.4:
                    score += 12
                    notes.append("A/D A")
                elif ratio > 1.1:
                    score += 6
                    notes.append("A/D B")
                elif ratio > 0.9:
                    score += 2
                    notes.append("A/D C")
                else:
                    score -= 4
                    notes.append("A/D D")
            else:
                notes.append("A/D ?")

        # Off 52w high (closer = better for leaders)
        if len(close) >= 252:
            high52 = close.iloc[-252:].max()
            off = (close.iloc[-1] / high52 - 1) * 100
            if off > -5:
                score += 8
            elif off > -15:
                score += 3
            else:
                score -= 2

        # Cap and grade
        score = max(0, min(100, round(score)))
        if score >= 85:
            grade = "A"
        elif score >= 70:
            grade = "B"
        elif score >= 55:
            grade = "C"
        elif score >= 40:
            grade = "D"
        else:
            grade = "E"
        return score, grade, " · ".join(notes) if notes else "기본"
    except Exception as e:
        return None, "계산오류", str(e)


def improved_ad_label(df):
    """Return A/D letter from 13w volume ratio."""
    if df is None or len(df) < 65 or "Close" not in df.columns or "Volume" not in df.columns:
        return "—"
    try:
        recent = df.tail(65)
        up = recent["Close"] > recent["Close"].shift(1)
        down = recent["Close"] < recent["Close"].shift(1)
        uv = recent.loc[up, "Volume"].sum()
        dv = recent.loc[down, "Volume"].sum()
        if dv <= 0:
            return "—"
        r = uv / dv
        if r >= 1.5:
            return "A"
        if r >= 1.2:
            return "B"
        if r >= 0.95:
            return "C"
        if r >= 0.75:
            return "D"
        return "E"
    except Exception:
        return "—"


# Hook into sticky_bar (chains with v14.31)
_orig_sticky_bar_q43 = sticky_bar if "sticky_bar" in globals() else None

def sticky_bar(ctx, D, extra=""):
    if _orig_sticky_bar_q43:
        _orig_sticky_bar_q43(ctx, D, extra)
    if not isinstance(ctx, dict) or not ctx.get("ok"):
        return
    df = ctx.get("df")
    q = compute_quality_score(ctx, df)
    if q and q[0] is not None:
        score, grade, note = q
        st.markdown(f"**Quality Score (Comp 근사)** : {score} / {grade}  ·  {note}")
        st.caption("Quality = 리더십·질 (C/A/RS/A-D/그룹 대리). 시장·베이스 페널티 거의 없음. IBD Comp와 순위 상관을 높이는 쪽.")
    ad = improved_ad_label(df)
    if ad != "—":
        st.caption(f"A/D 대리 (13주 업/다운 거래량비): {ad}")
    # Existing timing score is already shown by prior code; label it clearly
    st.caption("Timing / Buy Checklist Score (기존 CANSLIM 점수) = 지금 살 자리인지 (시장 상태 + 베이스·피벗 준비도 포함). 우량주라도 자리가 아니면 낮게 나옵니다.")
    st.info("앱은 시장 국면·RS·매수 타이밍 확인에 쓸 만합니다. 우량주 선별(Comp)은 IBD Checkup과 함께 보세요. 기관 보유·공식 RS·공식 DD/FTD는 아직 없습니다.")


print("v14.43 Quality vs Timing scores loaded")
