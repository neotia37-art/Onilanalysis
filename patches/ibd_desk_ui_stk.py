        desk = load_ibd_desk()
        volc = vol_ratio_corner(df)
        hits = fund_hits_for(TK, desk)
        blocks = block_hits_for(TK, desk)
        notes = (desk.get("notes") or {}).get(str(TK).upper(), [])
        try:
            chk = checkup_for(TK, desk)
        except Exception:
            _cr = (desk.get("checkups") or {}).get(str(TK).upper()) or []
            chk = _cr[-1] if _cr else None
        try:
            irows = inst_rows_for(TK, desk)
        except Exception:
            irows = [x for x in (desk.get("inst") or [])
                     if str(x.get("ticker", "")).upper() == str(TK).upper()]
        try:
            sc = sponsorship_score(fnd, volc, hits, blocks, notes,
                                   checkup=chk, inst_rows=irows)
        except TypeError:
            sc = sponsorship_score(fnd, volc, hits, blocks, notes)
        try:
            mh = ma_health(df, binfo["weekly"] if binfo else None)
        except Exception:
            mh = None

        if mh:
            step_header("MA · 21일 EMA · 50일 · 10주", "매수영역 안팗 · 지지/저항",
                        "IBD가 차트에서 매일 보는 세 선")
            mc = st.columns(4)
            mc[0].markdown(card("21일 EMA",
                                fmt(mh["ema21"], market) if mh.get("ema21") == mh.get("ema21") else "—",
                                (f'이격 {pct(mh.get("dist21"),2)} · '
                                 + ("위" if (mh.get("dist21") or 0) >= 0 else "아래")),
                                "up" if (mh.get("dist21") or 0) >= 0 else "down"),
                           unsafe_allow_html=True)
            mc[1].markdown(card("50일 SMA",
                                fmt(mh["sma50"], market) if mh.get("sma50") == mh.get("sma50") else "—",
                                (f'이격 {pct(mh.get("dist50"),2)}' if mh.get("dist50") is not None else "산출 전"),
                                "up" if (mh.get("dist50") or 0) >= 0 else "down"),
                           unsafe_allow_html=True)
            mc[2].markdown(card("10주 SMA",
                                fmt(mh["sma10w"], market) if mh.get("sma10w") == mh.get("sma10w") else "—",
                                (f'이격 {pct(mh.get("dist10"),2)}' if mh.get("dist10") is not None else "산출 전"),
                                "up" if (mh.get("dist10") or 0) >= 0 else "down"),
                           unsafe_allow_html=True)
            mc[3].markdown(card("정렬", mh.get("grade") or "—",
                                "21일이 50일 위에 있으면 단기 추세가 중기를 이긴다",
                                "up" if mh.get("kind") == "pass" else
                                ("amb" if mh.get("kind") == "warn" else "down")),
                           unsafe_allow_html=True)

        step_header("I · 기관보증", "거래량비율 · 펀드 수 · 블록 · Stock Checkup",
                    "자동 근사 + 구독 화면 수동 이전")
        ic = st.columns(4)
        ic[0].markdown(card("기관보증 점수",
                            f'{sc["score"]}<span style="font-size:.75rem">/100</span>',
                            f'자동 {sc["auto"]}/40 · 수동 {sc["man"]}/60 · {sc["grade"]}',
                            "up" if sc["kind"] == "pass" else
                            ("amb" if sc["kind"] == "warn" else "mut")),
                       unsafe_allow_html=True)
        if volc:
            lab, k, why = volc["flag"]
            ic[1].markdown(card("거래량비율", f'{volc["ratio"]:.2f}배',
                                f'50일평균 대비 · 5일 {volc["v5"]:.2f}배 · {lab}',
                                "up" if k == "pass" else ("down" if k == "fail" else "mut")),
                           unsafe_allow_html=True)
        else:
            ic[1].markdown(card("거래량비율", "—", "산출 불가"), unsafe_allow_html=True)
        ic[2].markdown(card("36개월 펀드 교차",
                            f'{len(hits)}건' if hits else "없음",
                            (" / ".join(f"{h[0]} {h[1]}" for h in hits[:2])
                             if hits else "펀드 코너에 이 티커가 없음"),
                            "up" if any(h[1] != "축소" for h in hits) else "mut"),
                       unsafe_allow_html=True)
        if chk:
            ic[3].markdown(card("펀드 수 추이",
                                f'+{chk.get("funds_chg")}%' if chk.get("funds_chg") is not None
                                else "—",
                                f'증가 {chk.get("funds_up_q")}기간 · A/D {chk.get("ad") or "—"}',
                                "up" if (chk.get("funds_up_q") or 0) >= 3 else "mut"),
                           unsafe_allow_html=True)
        else:
            ic[3].markdown(card("개장 블록",
                                f'{len(blocks)}건' if blocks else "없음",
                                (blocks[-1].get("side") + " · " + str(blocks[-1].get("date")))
                                if blocks else "블록 테이프에 없음",
                                "up" if blocks and "매수" in str(blocks[-1].get("side")) else "mut"),
                           unsafe_allow_html=True)
        st.markdown('<div class="hint">' + " · ".join(sc.get("why") or []) + f' · {IBD_I_ADJ}</div>',
                    unsafe_allow_html=True)
        if hits:
            st.markdown(table(["펀드", "교차", "36개월 등급"],
                              [[f'<b>{a}</b>', b, f'<span class="mono">{c or "—"}</span>']
                               for a, b, _k, c in hits]),
                        unsafe_allow_html=True)
        # Checkup 시트·일지 입력은 ibd_checkup_ui.py 한곳만. 키 중복 금지.
