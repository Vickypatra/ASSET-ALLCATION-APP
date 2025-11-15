import streamlit as st
import math

# -------------------------- APP CONFIG ----------------------------
st.set_page_config(page_title="Asset Allocation | Investment Calculators", page_icon="💼", layout="wide")

st.markdown(
    """
    <style>
        .main { background-color: #F7F9FC; }
        .calculator-box {
            background: white;
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin-bottom: 25px;
        }
        h1, h2, h3 {
            font-family: 'Segoe UI', sans-serif;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------- HEADER ----------------------------
st.title("💼 Asset Allocation & Investment Calculators")
st.write("Professional and visually polished calculators for SIP, SWP, Mutual Funds, FD & RD.")

# -------------------------- SIDEBAR NAVIGATION ----------------------------
calc = st.sidebar.selectbox(
    "Select Calculator",
    ["SIP Calculator", "SWP Calculator", "Mutual Fund Growth", "FD Calculator", "RD Calculator"]
)

# -------------------------- SIP CALCULATOR ----------------------------
if calc == "SIP Calculator":
    st.header("📈 SIP Calculator")
    st.markdown("Estimate wealth creation using monthly SIP investments.")

    col1, col2 = st.columns(2)

    with col1:
        monthly_sip = st.number_input("Monthly SIP Amount (₹)", min_value=0, value=5000)
        years = st.number_input("Investment Duration (Years)", min_value=1, value=10)
    with col2:
        expected_return = st.number_input("Expected Annual Return (%)", min_value=1.0, value=12.0)

    months = years * 12
    r = expected_return / 12 / 100

    final_value = monthly_sip * (((1 + r) ** months - 1) / r) * (1 + r)

    invested = monthly_sip * months
    gain = final_value - invested

    st.subheader("Results")
    st.write(f"**Total Invested:** ₹{invested:,.0f}")
    st.write(f"**Final Maturity Amount:** ₹{final_value:,.0f}")
    st.success(f"**Wealth Gain:** ₹{gain:,.0f}")


# -------------------------- SWP CALCULATOR ----------------------------
if calc == "SWP Calculator":
    st.header("💸 SWP Calculator")
    st.markdown("Calculate monthly withdrawal sustainability.")

    col1, col2 = st.columns(2)
    with col1:
        initial_amount = st.number_input("Initial Investment (₹)", min_value=0, value=500000)
        swp_amount = st.number_input("SWP Monthly Withdrawal (₹)", min_value=0, value=5000)
    with col2:
        return_rate = st.number_input("Expected Annual Return (%)", min_value=1.0, value=10.0)
        duration_years = st.number_input("Withdrawal Duration (Years)", min_value=1, value=10)

    r = return_rate / 12 / 100
    n = duration_years * 12

    try:
        balance = initial_amount
        for _ in range(n):
            balance = balance * (1 + r) - swp_amount
            if balance <= 0:
                break
    except:
        balance = 0

    st.subheader("Results")
    if balance <= 0:
        st.error("Funds will be exhausted before the selected period.")
    else:
        st.success(f"Balance Remaining After {duration_years} Years: ₹{balance:,.0f}")


# -------------------------- MUTUAL FUND CALCULATOR ----------------------------
if calc == "Mutual Fund Growth":
    st.header("📊 Mutual Fund Lump Sum Growth Calculator")

    col1, col2 = st.columns(2)
    with col1:
        lump_sum = st.number_input("Lump Sum Investment (₹)", min_value=0, value=100000)
    with col2:
        return_rate = st.number_input("Expected Annual Return (%)", min_value=1.0, value=12.0)
        years = st.number_input("Investment Duration (Years)", min_value=1, value=10)

    future_value = lump_sum * (1 + return_rate/100) ** years
    gain = future_value - lump_sum

    st.subheader("Results")
    st.write(f"**Investment Value After {years} Years:** ₹{future_value:,.0f}")
    st.success(f"Gain: ₹{gain:,.0f}")


# -------------------------- FD CALCULATOR ----------------------------
if calc == "FD Calculator":
    st.header("🏦 Fixed Deposit Calculator")

    col1, col2 = st.columns(2)
    with col1:
        principal = st.number_input("FD Amount (₹)", min_value=0, value=50000)
        years = st.number_input("FD Tenure (Years)", min_value=1, value=5)
    with col2:
        rate = st.number_input("Interest Rate (%)", min_value=1.0, value=6.5)
        comp = st.selectbox("Compounding Frequency", ["Yearly", "Half-Yearly", "Quarterly", "Monthly"])

    freq = {"Yearly":1, "Half-Yearly":2, "Quarterly":4, "Monthly":12}[comp]

    maturity = principal * (1 + (rate/100)/freq) ** (freq * years)

    st.subheader("Results")
    st.write(f"**Maturity Amount:** ₹{maturity:,.0f}")
    st.success(f"**Interest Earned:** ₹{maturity - principal:,.0f}")


# -------------------------- RD CALCULATOR ----------------------------
if calc == "RD Calculator":
    st.header("📤 Recurring Deposit Calculator")

    col1, col2 = st.columns(2)
    with col1:
        monthly_dep = st.number_input("Monthly Deposit (₹)", min_value=0, value=2000)
        years = st.number_input("Tenure (Years)", min_value=1, value=5)
    with col2:
        rate = st.number_input("Interest Rate (%)", min_value=1.0, value=7.0)
        freq = 4  # Quarterly compounding for RD

    n = years * 12
    r = rate / 400  # Quarterly rate

    maturity = monthly_dep * ((1 + r)**(n/3) - 1) / (1 - (1 + r)**(-1/3))

    st.subheader("Results")
    st.write(f"**Maturity Amount:** ₹{maturity:,.0f}")
    st.success(f"**Interest Earned:** ₹{maturity - (monthly_dep*n):,.0f}")
