from datetime import date, timedelta

import streamlit as st

st.set_page_config(page_title="TrackMySubs Style Demo", page_icon="🫧", layout="wide")

if "subs" not in st.session_state:
    st.session_state.subs = [
        {
            "company": "TrackMySubs",
            "description": "",
            "cost": 0.0,
            "currency": "USD",
            "cycle": "monthly",
            "next_payment": date(2026, 3, 22),
            "folder": "All",
        },
        {
            "company": "Amazon Prime",
            "description": "",
            "cost": 9.99,
            "currency": "USD",
            "cycle": "monthly",
            "next_payment": date(2026, 2, 27),
            "folder": "All",
        },
    ]

if "show_new" not in st.session_state:
    st.session_state.show_new = False
if "wizard_step" not in st.session_state:
    st.session_state.wizard_step = 1

st.markdown(
    """
    <style>
    .stApp {background: #f4f5f7;}
    .top-alert {
      background:#ff8358; color:white; text-align:center; padding:8px; border-radius:6px;
      font-weight:700; margin-bottom:10px;
    }
    .top-nav {background:#fff; border:1px solid #e6e6e6; border-radius:10px; padding:14px 20px; margin-bottom:16px;}
    .brand {font-size:30px; font-weight:800; color:#17c3d6}
    .panel {background:#fff; border:1px solid #e6e6e6; border-radius:14px; padding:16px;}
    .metric-card {background:#fff; border:1px dashed #e6e6e6; border-radius:12px; padding:10px 14px;}
    .row-card {background:#fff; border-bottom:1px solid #efefef; padding:10px 6px;}
    .teal-btn button {background:#25cbd0 !important; color:#fff !important; border-radius:999px !important; border:none !important;}
    .coral-btn button {background:#f26749 !important; color:#fff !important; border-radius:999px !important; border:none !important;}
    .modal {background:#fff; border:1px solid #d9d9d9; border-radius:18px; padding:20px; box-shadow: 0 8px 30px rgba(0,0,0,0.16);}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="top-alert">Alerting is disabled because your email has not been verified, please check your emails.</div>', unsafe_allow_html=True)

st.markdown('<div class="top-nav"><span class="brand">TrackMySubs</span></div>', unsafe_allow_html=True)

nav_col, prog_col = st.columns([5, 2])
with nav_col:
    page = st.radio(
        "Navigation",
        ["Subscriptions", "Calendar", "My Account"],
        horizontal=True,
        label_visibility="collapsed",
    )
with prog_col:
    st.caption("Setup Progress 2/10")
    st.progress(0.2)

if page == "Subscriptions":
    left, right = st.columns([1.2, 2.8])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Folders")
        st.write("📁 Trials")
        st.write("📁 All")
        st.write("📁 Unassigned")
        st.write("➕ New Folder")
        st.divider()
        st.write("Cancelled")
        st.write("Deleted")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        action_cols = st.columns([1, 1, 1, 4])
        with action_cols[0]:
            if st.button("➕ New", width="stretch"):
                st.session_state.show_new = True
                st.session_state.wizard_step = 1
        with action_cols[1]:
            st.button("Advanced", width="stretch")
        with action_cols[2]:
            st.button("🔍", width="stretch")

        m1, m2 = st.columns(2)
        with m1:
            st.markdown('<div class="metric-card"><h4>Subscriptions</h4><p>Monthly Value: -</p></div>', unsafe_allow_html=True)
        with m2:
            st.markdown('<div class="metric-card"><h4>Revenue</h4><p>Total Single Payments: -</p></div>', unsafe_allow_html=True)

        st.markdown("### Showing **All**")
        for idx, sub in enumerate(st.session_state.subs):
            c1, c2, c3, c4, c5 = st.columns([2.4, 1.2, 1, 1, 0.6])
            c1.markdown(f"**{sub['company']}**")
            c2.markdown(f"Renews  \\n{sub['next_payment'].strftime('%b %d, %Y')}")
            c3.write(sub["cycle"])
            c4.write(f"${sub['cost']:.2f}")
            if c5.button("➖", key=f"remove_{idx}"):
                st.session_state.subs.pop(idx)
                st.rerun()

if page == "Calendar":
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Monthly Calendar")
    st.caption("Demo calendar view inspired by your screenshots.")
    month = st.date_input("Month", date(2026, 2, 1))
    st.write(f"Showing renewals for **{month.strftime('%B %Y')}**")
    for sub in st.session_state.subs:
        st.write(f"🟣 {sub['company']} — {sub['next_payment'].strftime('%b %d')} — ${sub['cost']:.2f}")
    st.markdown('</div>', unsafe_allow_html=True)

if page == "My Account":
    left, right = st.columns([1.1, 3.4])
    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        for item in ["My Details", "Billing", "Invoices", "Privacy", "Preferences", "Alert Preferences", "Payment Methods", "Import/Export"]:
            st.button(item, width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.header("Preferences")
        a, b = st.columns(2)
        a.selectbox("Displayed currency", ["USD", "EUR", "GBP"])
        b.selectbox("Timezone", ["(UTC+11:00) Australia/Sydney", "(UTC) London", "(UTC-05:00) New York"])
        st.selectbox("Sort subscriptions by", ["None", "Name", "Value", "Renewal date"])
        st.markdown('<div class="teal-btn">', unsafe_allow_html=True)
        st.button("Save Changes", width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.show_new:
    st.markdown("---")
    st.markdown('<div class="modal">', unsafe_allow_html=True)
    st.subheader("New")
    st.caption(f"Step {st.session_state.wizard_step} of 3")

    if st.session_state.wizard_step == 1:
        col1, col2 = st.columns([1, 1.6])
        col1.markdown("## amazon**Prime**")
        company = col2.text_input("Company", "Amazon Prime")
        description = col2.text_input("Description", "")
        st.selectbox("Type", ["Subscription", "Membership", "Service"])
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="coral-btn">', unsafe_allow_html=True)
            cancel = st.button("Cancel", width="stretch", key="cancel1")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="teal-btn">', unsafe_allow_html=True)
            nxt = st.button("Next", width="stretch", key="next1")
            st.markdown('</div>', unsafe_allow_html=True)
        if cancel:
            st.session_state.show_new = False
            st.rerun()
        if nxt:
            st.session_state.temp_company = company
            st.session_state.temp_desc = description
            st.session_state.wizard_step = 2
            st.rerun()

    elif st.session_state.wizard_step == 2:
        next_payment = st.date_input("Next Payment Date", date(2026, 2, 27), key="np")
        freq = st.selectbox("Every", [1, 2, 3, 6, 12], key="freq")
        cycle = st.selectbox("Billing Cycle", ["Month", "Year"], key="cycle")
        auto = st.selectbox("Does it auto renew?", ["Yes", "No"])
        st.write(f"This subscription auto renews every {freq} {cycle.lower()} from {next_payment.strftime('%d %B %Y')}")
        c1, c2 = st.columns(2)
        if c1.button("Back", width="stretch", key="back2"):
            st.session_state.wizard_step = 1
            st.rerun()
        if c2.button("Next", width="stretch", key="next2"):
            st.session_state.temp_next = next_payment
            st.session_state.temp_cycle = "monthly" if cycle == "Month" else "yearly"
            st.session_state.wizard_step = 3
            st.rerun()

    else:
        cost = st.number_input("Cost", min_value=0.0, value=9.99, step=0.5)
        currency = st.selectbox("Currency", ["USD", "EUR", "GBP"])
        st.write("Do you want to set a reminder alert?")
        st.button("Yes, use my default alert", width="stretch")
        st.button("No thanks", width="stretch")
        c1, c2 = st.columns(2)
        if c1.button("Back", width="stretch", key="back3"):
            st.session_state.wizard_step = 2
            st.rerun()
        if c2.button("Save", width="stretch", key="save3"):
            st.session_state.subs.append(
                {
                    "company": st.session_state.get("temp_company", "New subscription"),
                    "description": st.session_state.get("temp_desc", ""),
                    "cost": float(cost),
                    "currency": currency,
                    "cycle": st.session_state.get("temp_cycle", "monthly"),
                    "next_payment": st.session_state.get("temp_next", date.today() + timedelta(days=30)),
                    "folder": "All",
                }
            )
            st.session_state.show_new = False
            st.success("Subscription saved")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
