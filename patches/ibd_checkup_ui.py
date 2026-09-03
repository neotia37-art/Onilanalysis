        step_header("IBD CHECKUP", "Stock Checkup full sheet", "same date overwrites; later dates manual")
        try:
            ensure_wt_full_checkup(desk)
            chk = checkup_for(TK, desk)
        except Exception:
            chk = checkup_for(TK, desk)
        if chk and (chk.get("items") or chk.get("full")):
            render_checkup_sheet(chk)
        elif chk:
            st.markdown(f'<div class="ev"><b>{chk.get("ticker")} {chk.get("name") or ""}</b> · {chk.get("date")} · Comp {chk.get("comp") or "-"} · EPS {chk.get("eps") or "-"} · RS {chk.get("rs") or "-"}<br><span class="m">{chk.get("body") or ""}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="hint">No Checkup yet. Fill the editor or reload WT PDF.</div>', unsafe_allow_html=True)
        with st.expander("Checkup 항목 입력 · 정정 (색점 포함)", expanded=False):
            tkU = str(TK).upper()
            cur = chk or {}
            hc = st.columns(4)
            cd = hc[0].text_input("date", value=str(cur.get("date") or datetime.today().date()), key="ibd_cd")
            cname = hc[1].text_input("name", value=str(cur.get("name") or CTX.get("name") or tkU), key="ibd_cname")
            cgrp = hc[2].text_input("group", value=str(cur.get("group") or ""), key="ibd_cgrp")
            ccomp = hc[3].text_input("Composite", value=str(cur.get("comp") or ""), key="ibd_cc")
            hc2 = st.columns(5)
            ceps = hc2[0].text_input("EPS", value=str(cur.get("eps") or ""), key="ibd_ce")
            crs = hc2[1].text_input("RS", value=str(cur.get("rs") or ""), key="ibd_cr")
            csmr = hc2[2].text_input("SMR", value=str(cur.get("smr") or ""), key="ibd_csmr")
            cad = hc2[3].text_input("AD", value=str(cur.get("ad") or ""), key="ibd_cad")
            _opts = ["green", "yellow", "red", "none"]
            _cc = str(cur.get("comp_color") or "green")
            ccol = hc2[4].selectbox("Comp color", _opts, index=_opts.index(_cc) if _cc in _opts else 0, key="ibd_ccol")
            cabout = st.text_input("About", value=str(cur.get("about") or ""), key="ibd_cabout")
            seed_items = cur.get("items") or [
                {"sec": "MKT", "label": "Stock Market Exposure", "value": "", "color": "yellow"},
                {"sec": "EPS", "label": "EPS Rating", "value": "", "color": "green"},
                {"sec": "PX", "label": "RS Rating", "value": "", "color": "green"},
                {"sec": "SUP", "label": "Accumulation/Distribution Rating", "value": "", "color": "green"},
            ]
            edited = st.data_editor(pd.DataFrame(seed_items), num_rows="dynamic", use_container_width=True, key="ibd_citems",
                column_config={
                    "sec": st.column_config.TextColumn("sec"),
                    "label": st.column_config.TextColumn("item"),
                    "value": st.column_config.TextColumn("value"),
                    "color": st.column_config.SelectboxColumn("dot", options=["green", "yellow", "red", "none"]),
                })
            cbody = st.text_area("summary", value=str(cur.get("body") or ""), height=80, key="ibd_cbody")
            b1, b2, b3 = st.columns(3)
            if b1.button("save checkup", key="ibd_csave"):
                items = []
                if edited is not None and len(edited):
                    for _, r in edited.fillna("").iterrows():
                        if not str(r.get("label") or "").strip():
                            continue
                        items.append({"sec": str(r.get("sec") or "").strip(), "label": str(r.get("label") or "").strip(), "value": str(r.get("value") or "").strip(), "color": str(r.get("color") or "none").strip().lower()})
                rec = dict(cur)
                rec.update({"ticker": tkU, "date": cd, "name": cname.strip(), "group": cgrp.strip(), "about": cabout.strip(), "comp": ccomp.strip(), "comp_color": ccol, "eps": ceps.strip(), "rs": crs.strip(), "smr": csmr.strip(), "ad": cad.strip(), "items": items, "body": cbody.strip(), "source": rec.get("source") or "manual", "full": True})
                rows = desk.setdefault("checkups", {}).setdefault(tkU, [])
                desk["checkups"][tkU] = [x for x in rows if str(x.get("date")) != str(cd)] + [rec]
                save_ibd_desk(desk)
                st.success(f"{tkU} {cd} saved {len(items)} rows")
                st.rerun()
            if b2.button("WT 2026-09-02 PDF 다시 넣기", key="ibd_cwt"):
                desk.setdefault("checkups", {}).setdefault("WT", [])
                desk["checkups"]["WT"] = [x for x in desk["checkups"]["WT"] if str(x.get("date")) != "2026-09-02"] + [wt_checkup_full_20260902()]
                save_ibd_desk(desk)
                st.success("WT PDF reloaded")
                st.rerun()
            del_dt = b3.text_input("delete date", value="", key="ibd_cdel")
            if b3.button("delete", key="ibd_cdelb") and del_dt.strip():
                desk.setdefault("checkups", {}).setdefault(tkU, [])
                desk["checkups"][tkU] = [x for x in desk["checkups"][tkU] if str(x.get("date")) != del_dt.strip()]
                save_ibd_desk(desk)
                st.success(f"{tkU} {del_dt} deleted")
                st.rerun()
