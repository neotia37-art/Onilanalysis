        desk = load_ibd_desk()
        volc = vol_ratio_corner(df)
        hits = fund_hits_for(TK, desk)
        blocks = block_hits_for(TK, desk)
        notes = (desk.get("notes") or {}).get(str(TK).upper(), [])
        sc = sponsorship_score(fnd, volc, hits, blocks, notes)
        step_header("I · 기관보증", "거래량비율 · 36개월 펀드 · 블록 · IBD 분석일지", "자동 근사 + 구독 화면 수동 이전")
        ic = st.columns(4)
        ic[0].markdown(card("기관보증 점수", f'{sc["score"]}<span style="font-size:.75rem">/100</span>', f'자동 {sc["auto"]}/40 · 수동 {sc["man"]}/60 · {sc["grade"]}', "up" if sc["kind"]=="pass" else ("amb" if sc["kind"]=="warn" else "mut")), unsafe_allow_html=True)
        if volc:
            lab, k, why = volc["flag"]
            ic[1].markdown(card("거래량비율", f'{volc["ratio"]:.2f}배', f'50일평균 · 5일 {volc["v5"]:.2f}배 · {lab}', "up" if k=="pass" else ("down" if k=="fail" else "mut")), unsafe_allow_html=True)
        else:
            ic[1].markdown(card("거래량비율", "—", "산출 불가"), unsafe_allow_html=True)
        ic[2].markdown(card("36개월 펀드 교차", f'{len(hits)}건' if hits else "없음", (" / ".join(f"{h[0]} {h[1]}" for h in hits[:2]) if hits else "펀드 코너에 없음"), "up" if any(h[1]!="축소" for h in hits) else "mut"), unsafe_allow_html=True)
        ic[3].markdown(card("개장 블록", f'{len(blocks)}건' if blocks else "없음", (blocks[-1].get("side")+" · "+str(blocks[-1].get("date"))) if blocks else "블록 테이프에 없음", "up" if blocks and "매수" in str(blocks[-1].get("side")) else "mut"), unsafe_allow_html=True)
        st.markdown('<div class="hint">' + " · ".join(sc["why"]) + f' · {IBD_I_ADJ}</div>', unsafe_allow_html=True)
        if hits:
            st.markdown(table(["펀드", "교차", "36개월 등급"], [[f'<b>{a}</b>', b, f'<span class="mono">{c or "—"}</span>'] for a,b,_k,c in hits]), unsafe_allow_html=True)
        with st.expander("이 종목 IBD 분석 수록"):
            nc = st.columns(5)
            nd = nc[0].text_input("날짜", value=str(datetime.today().date()), key="ibd_nd")
            ne = nc[1].text_input("EPS", value="", key="ibd_ne")
            nr = nc[2].text_input("RS", value="", key="ibd_nr")
            ns = nc[3].text_input("SMR / A-D", value="", key="ibd_ns")
            ncomp = nc[4].text_input("Comp", value="", key="ibd_nc")
            title = st.text_input("제목", key="ibd_nt")
            body = st.text_area("분석 본문", height=120, key="ibd_nb")
            if st.button("이 종목 일지에 저장", key="ibd_nsave"):
                tkU = str(TK).upper()
                desk.setdefault("notes", {}).setdefault(tkU, []).append({"date": nd, "eps": ne.strip(), "rs": nr.strip(), "smr": ns.strip(), "comp": ncomp.strip(), "title": title.strip(), "body": body.strip()})
                save_ibd_desk(desk); st.success(f"{tkU} 저장")
        if notes:
            for n in notes[::-1][:8]:
                st.markdown(f'<div class="ev"><b>{n.get("date","")}</b> · {n.get("title") or "메모"} · EPS {n.get("eps") or "—"} · RS {n.get("rs") or "—"} · {n.get("smr") or "—"} · Comp {n.get("comp") or "—"}<br><span class="m">{n.get("body") or ""}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="hint">이 종목의 IBD 분석문이 아직 없습니다. 구독 화면을 한 줄이라도 옮기세요. 자동 크롤은 하지 않습니다.</div>', unsafe_allow_html=True)
