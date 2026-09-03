        step_header("IBD CHECKUP", "구독 Stock Checkup 전문 · 녹/노/빨",
                    "PDF를 그대로 옮긴다. 같은 날짜는 정정, 이후는 수동 또는 Grok에게 요청")
        try:
            ensure_wt_full_checkup(desk)
        except Exception:
            pass
        tkU = str(TK).upper()
        all_rows = checkup_rows_for(tkU, desk) if "checkup_rows_for" in dir() else (
            (desk.get("checkups") or {}).get(tkU) or [])
        dates = [str(x.get("date") or "") for x in all_rows if x.get("date")]
        pick = None
        if dates:
            pick = st.selectbox(
                "수록 날짜 (최신이 기본)",
                options=dates[::-1],
                index=0,
                key="ibd_cdatepick")
        try:
            chk = checkup_for(TK, desk, date=pick) if pick else checkup_for(TK, desk)
        except TypeError:
            chk = checkup_for(TK, desk)

        if chk and (chk.get("items") or chk.get("full")):
            render_checkup_sheet(chk)
        elif chk:
            st.markdown(
                f'<div class="ev"><b>{chk.get("ticker")} {chk.get("name") or ""}</b> · '
                f'{chk.get("date")} · Comp {chk.get("comp") or "—"} · EPS {chk.get("eps") or "—"} · '
                f'RS {chk.get("rs") or "—"} · SMR {chk.get("smr") or "—"} · A/D {chk.get("ad") or "—"}<br>'
                f'<span class="m">{chk.get("body") or ""}</span></div>',
                unsafe_allow_html=True)
            st.markdown('<div class="hint">이 날짜는 요약만 있습니다. 아래 편집기에서 항목·색점을 채우면 '
                        'PDF와 같은 시트가 됩니다.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="hint">이 종목 Stock Checkup이 없습니다. 아래 칸에 PDF 항목을 넣거나 '
                        'WT라면 「PDF 다시 넣기」를 누르세요. 이후 날짜는 앱에서 직접 입력하거나 '
                        'Grok에게 PDF를 주시면 옮겨 드립니다.</div>', unsafe_allow_html=True)

        with st.expander("Checkup 항목 입력 · 정정 (색점 포함)", expanded=not bool(chk and chk.get("items"))):
            cur = chk or {}
            hc = st.columns(4)
            cd = hc[0].text_input("날짜", value=str(cur.get("date") or datetime.today().date()),
                                  key="ibd_cd")
            cname = hc[1].text_input("종목명", value=str(cur.get("name") or CTX.get("name") or tkU),
                                     key="ibd_cname")
            cgrp = hc[2].text_input("업종 그룹", value=str(cur.get("group") or ""), key="ibd_cgrp")
            ccomp = hc[3].text_input("Composite", value=str(cur.get("comp") or ""), key="ibd_cc")
            hc2 = st.columns(5)
            ceps = hc2[0].text_input("EPS", value=str(cur.get("eps") or ""), key="ibd_ce")
            crs = hc2[1].text_input("RS", value=str(cur.get("rs") or ""), key="ibd_cr")
            csmr = hc2[2].text_input("SMR", value=str(cur.get("smr") or ""), key="ibd_csmr")
            cad = hc2[3].text_input("A/D", value=str(cur.get("ad") or ""), key="ibd_cad")
            _cols = ["green", "yellow", "red", "none"]
            _cc = str(cur.get("comp_color") or "green")
            ccol = hc2[4].selectbox("Comp 색", _cols,
                                    index=_cols.index(_cc) if _cc in _cols else 0,
                                    key="ibd_ccol")
            cabout = st.text_input("About", value=str(cur.get("about") or ""), key="ibd_cabout")
            cprint = st.text_input("인쇄시각 / 출처",
                                   value=str(cur.get("printed") or cur.get("source") or ""),
                                   key="ibd_cprint")
            seed_items = cur.get("items") or (
                checkup_blank_items() if "checkup_blank_items" in dir() else [
                    {"sec": "General Market", "label": "Stock Market Exposure", "value": "", "color": "yellow"},
                    {"sec": "Current Earnings", "label": "EPS Rating", "value": "", "color": "green"},
                    {"sec": "Price And Volume", "label": "RS Rating", "value": "", "color": "green"},
                    {"sec": "Supply And Demand", "label": "Accumulation/Distribution Rating",
                     "value": "", "color": "green"},
                ])
            st.caption("색점 green=적합 / yellow=주의 / red=미달 / none=없음. 행 추가·삭제 후 저장. "
                       "같은 날짜는 덮어쓰고, 새 날짜는 이력이 됩니다.")
            edited = st.data_editor(
                pd.DataFrame(seed_items),
                num_rows="dynamic",
                use_container_width=True,
                key="ibd_citems",
                column_config={
                    "sec": st.column_config.TextColumn("구분"),
                    "label": st.column_config.TextColumn("항목"),
                    "value": st.column_config.TextColumn("값"),
                    "color": st.column_config.SelectboxColumn(
                        "색점", options=["green", "yellow", "red", "none"]),
                },
            )
            cbody = st.text_area("한 줄 요약", value=str(cur.get("body") or ""),
                                 height=80, key="ibd_cbody")
            b1, b2, b3, b4 = st.columns(4)
            if b1.button("Checkup 저장 (같은 날짜 덮어쓰기)", key="ibd_csave"):
                items = []
                if edited is not None and len(edited):
                    for _, r in edited.fillna("").iterrows():
                        if not str(r.get("label") or "").strip():
                            continue
                        items.append({
                            "sec": str(r.get("sec") or "").strip(),
                            "label": str(r.get("label") or "").strip(),
                            "value": str(r.get("value") or "").strip(),
                            "color": str(r.get("color") or "none").strip().lower(),
                        })
                rec = dict(cur)
                rec.update({
                    "ticker": tkU, "date": cd, "name": cname.strip(),
                    "group": cgrp.strip(), "about": cabout.strip(),
                    "printed": cprint.strip(),
                    "comp": ccomp.strip(), "comp_color": ccol,
                    "eps": ceps.strip(), "rs": crs.strip(),
                    "smr": csmr.strip(), "ad": cad.strip(),
                    "items": items, "body": cbody.strip(),
                    "source": rec.get("source") or "IBD Stock Checkup 수동",
                    "full": True,
                })
                if "upsert_checkup" in dir():
                    upsert_checkup(desk, rec)
                else:
                    rows = desk.setdefault("checkups", {}).setdefault(tkU, [])
                    desk["checkups"][tkU] = [x for x in rows if str(x.get("date")) != str(cd)] + [rec]
                    save_ibd_desk(desk)
                st.success(f"{tkU} Checkup {cd} 저장 · 항목 {len(items)}개")
                st.rerun()
            if b2.button("빈 PDF 뼈대 넣기", key="ibd_cblank"):
                st.info("편집기에 PDF 31항목 뼈대를 준비했습니다. 값·색점을 채운 뒤 저장하세요.")
            if b3.button("WT PDF 다시 넣기", key="ibd_cwt"):
                desk.setdefault("checkups", {}).setdefault("WT", [])
                desk["checkups"]["WT"] = [
                    x for x in desk["checkups"]["WT"] if str(x.get("date")) != "2026-09-02"
                ] + [wt_checkup_full_20260902()]
                save_ibd_desk(desk)
                st.success("WT 2026-09-02 Stock Checkup PDF(파일 20260903)를 다시 넣었습니다.")
                st.rerun()
            del_dt = b4.text_input("삭제할 날짜", value="", key="ibd_cdel")
            if b4.button("해당 날짜 삭제", key="ibd_cdelb") and del_dt.strip():
                desk.setdefault("checkups", {}).setdefault(tkU, [])
                desk["checkups"][tkU] = [
                    x for x in desk["checkups"][tkU] if str(x.get("date")) != del_dt.strip()
                ]
                save_ibd_desk(desk)
                st.success(f"{tkU} {del_dt} 삭제")
                st.rerun()

        with st.expander("이 종목 IBD 분석 수록 (제목·본문)", expanded=False):
            nc = st.columns(5)
            nd = nc[0].text_input("날짜", value=str(datetime.today().date()), key="ibd_nd")
            ne = nc[1].text_input("EPS", value="", key="ibd_ne")
            nr = nc[2].text_input("RS", value="", key="ibd_nr")
            ns = nc[3].text_input("SMR / A-D", value="", key="ibd_ns")
            ncomp = nc[4].text_input("Comp", value="", key="ibd_nc")
            title = st.text_input("제목 (예: IBD Stock of the Day / Industry Theme)", key="ibd_nt")
            body = st.text_area("분석 본문", height=120, key="ibd_nb")
            if st.button("이 종목 일지에 저장", key="ibd_nsave"):
                desk.setdefault("notes", {}).setdefault(tkU, []).append({
                    "date": nd, "eps": ne.strip(), "rs": nr.strip(),
                    "smr": ns.strip(), "comp": ncomp.strip(),
                    "title": title.strip(), "body": body.strip(),
                })
                save_ibd_desk(desk)
                st.success(f"{tkU} IBD 분석 {nd} 저장")
        extra_notes = [n for n in notes if "Stock Checkup" not in str(n.get("title") or "")]
        if extra_notes:
            for n in extra_notes[::-1][:8]:
                st.markdown(
                    f'<div class="ev"><b>{n.get("date","")}</b> · {n.get("title") or "메모"} · '
                    f'EPS {n.get("eps") or "—"} · RS {n.get("rs") or "—"} · '
                    f'{n.get("smr") or "—"} · Comp {n.get("comp") or "—"}<br>'
                    f'<span class="m">{n.get("body") or ""}</span></div>',
                    unsafe_allow_html=True)
        elif not chk:
            st.markdown('<div class="hint">이 종목의 IBD 분석문이 아직 없습니다. '
                        '구독 화면의 Stock Checkup / Big Cap 20 / 산업 스토리를 한 줄이라도 옮기세요. '
                        '자동 크롤은 하지 않습니다.</div>',
                        unsafe_allow_html=True)
