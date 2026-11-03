# TAB 10 — 기관동향. 사이드바 종목과 연동. IBD Mutual·Checkup 입력은 이 탭에서 빼 둔다.
to_top()
with TABS[10], guard("기관동향"):
    try:
        from selfdesk.inst_panel import render_self_inst
        render_self_inst()
    except Exception as _sie:
        st.warning("기관동향: " + str(_sie))
