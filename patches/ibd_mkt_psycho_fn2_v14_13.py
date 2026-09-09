# psycho comment v14.13
MKT_PSYCHO_FN2_V14_13 = True


def psycho_composite(latest):
    latest = latest or {}
    bits = []
    for key, label, field in (("vix", "VIX", "vix"), ("put_call", "P/C", "put_call"), ("high_low", "H/L", "high_low"), ("bulls", "Bulls", "bulls"), ("bears", "Bears", "bears"), ("margin", "Margin", "margin_yoy")):
        lab, _ = _psycho_read_one(key, latest.get(field))
        raw = latest.get(field)
        shown = "—" if raw is None else raw
        extra = "%" if key in ("bulls", "bears", "margin") and raw is not None else ""
        bits.append(f"{label} {shown}{extra} ({lab})")
    return bits


def market_comment_today(pulse=None, latest=None, states=None, bw=None):
    pulse = pulse or {}
    latest = latest or {}
    bw = bw or {}
    off_n = pulse.get("dist_nasdaq_official") or pulse.get("dist_nasdaq") or 4
    off_s = pulse.get("dist_spx_official") or pulse.get("dist_spx") or 3
    work_n = pulse.get("working_dist_nasdaq") or off_n
    work_s = pulse.get("working_dist_spx") or off_s
    ftd = pulse.get("ftd") or "2026-06-02"
    exp = pulse.get("exposure") or "60%-80%"
    cand = pulse.get("candidate_dd_20260908") or {}
    stance = "현금 비중 유지 · 신규 추격 0"
    if int(work_n or 0) >= 5:
        stance = "분산 작업카운트 5 · 신규 금지 · 보유만 방어선"
    elif int(work_n or 0) >= 3:
        stance = "분산 3~4(작업 5 후보) · 추격 금지 · 피벗 대기만"
    lines = [
        f"<b>오늘 종합 (인쇄 {latest.get('date') or '—'} · Pulse 공식 {pulse.get('official_date') or pulse.get('date') or '—'})</b>",
        f"공식 Pulse 노출 <b>{exp}</b> · 공식 분산 NAS {off_n} / SPX {off_s}. 마지막 시장 FTD는 <b>{ftd}</b> (세 달 전). 새 FTD는 아직 없다.",
    ]
    if cand:
        lines.append(
            f"2026-09-08 화요 테이프: 다우 {cand.get('dji_close')} ({cand.get('dji_chg_pts')}pt) · 나스닥 {cand.get('nasdaq_close')} ({cand.get('nasdaq_chg_pts')}pt) · S&P {cand.get('spx_chg_pts')}pt. NYSE vol {cand.get('nyse_vol')} vs 금 {cand.get('nyse_vol_prev')} · NAS vol {cand.get('nasdaq_vol')} vs 금 {cand.get('nasdaq_vol_prev')}. 상승 {cand.get('adv')} / 하락 {cand.get('dec')}. <b>하락+거래량증가 = 분산일 후보</b>. 작업카운트 NAS {work_n} / SPX {work_s}. FTD훈련 탭에서 0.2%·전일거래량으로 손계산해 확정한다."
        )
    lines.append(
        f"심리 5종: VIX {latest.get('vix')} (45 미만=안일), P/C {latest.get('put_call')} (콜 편중), H/L {latest.get('high_low')} (0.5 문턱 위), Bulls {latest.get('bulls')}% / Bears {latest.get('bears')}% (자문 낙관), Margin {latest.get('margin_yoy')}% YoY (55% 아래)."
    )
    lines.append(
        f"읽기: 군중은 아직 편하다. 공식 분산 3~4일에 화요 후보를 더하면 작업 5. 심리 낙관 + 기관 매도 흔적 = 같은 날 추격하지 않는다. 적합도 {bw.get('score') if bw.get('score') is not None else '—'} · {stance}."
    )
    lines.append("보유 WT·PBF는 추가 금지. 정유 신고가(VLO DINO PSX MPC)와 LITE +62%·NVDA 베이스이탈은 리스트 공부일 뿐 매수 창이 아니다.")
    return "<br>".join(lines), stance
