COMPANY_TAB_V14_24 = True
COMPANY_TAB_V14_39 = True

to_top()
with TABS[12], guard("회사개요"):
    try:
        from selfdesk.company_panel import render_company
        render_company()
    except Exception as _ce:
        st.error("회사개요: " + str(_ce))
