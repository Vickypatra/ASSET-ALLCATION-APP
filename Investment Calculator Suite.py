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
        .stMetric {
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 10px;
        }
        .suggestion-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 15px;
            margin: 10px 0;
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
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Total Invested", f"₹{invested:,.0f}")
    with col_b:
        st.metric("Final Maturity Amount", f"₹{final_value:,.0f}")
    with col_c:
        st.success(f"Wealth Gain: ₹{gain:,.0f}")
    
    # Suggestions Section
    with st.expander("🔍 Micro Level Analysis: Top SIP Suggestions (Based on Past Performance)"):
        st.markdown("### Top Mutual Funds for SIP")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.markdown("""
            <div class="suggestion-card">
                <h4>Parag Parikh Flexi Cap Fund</h4>
                <p>Consistent returns ~18% CAGR (5Y)</p>
            </div>
            """, unsafe_allow_html=True)
        with col_s2:
            st.markdown("""
            <div class="suggestion-card">
                <h4>Kotak Equity Opportunities Fund</h4>
                <p>Strong growth ~17% CAGR (5Y)</p>
            </div>
            """, unsafe_allow_html=True)
        with col_s3:
            st.markdown("""
            <div class="suggestion-card">
                <h4>SBI Small Cap Fund</h4>
                <p>High potential ~22% CAGR (5Y)</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Top Bonds/Debt Funds for Conservative SIP")
        st.info("• ICICI Prudential All Seasons Bond Fund (~7.5% YTM)\n• HDFC Corporate Bond Fund (~7.2% YTM)\n• Axis Dynamic Bond Fund (~7.0% YTM)")

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
    col_d, col_e = st.columns(2)
    with col_d:
        if balance <= 0:
            st.error("Funds will be exhausted before the selected period.")
        else:
            st.success(f"Balance Remaining After {duration_years} Years: ₹{balance:,.0f}")
    
    # Suggestions Section
    with st.expander("🔍 Micro Level Analysis: Top SWP Suggestions (Based on Past Performance)"):
        st.markdown("### Top Mutual Funds for SWP")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.markdown("""
            <div class="suggestion-card">
                <h4>HDFC Hybrid Equity Fund</h4>
                <p>Balanced ~12% CAGR (5Y)</p>
            </div>
            """, unsafe_allow_html=True)
        with col_s2:
            st.markdown("""
            <div class="suggestion-card">
                <h4>ICICI Prudential Balanced Advantage</h4>
                <p>Dynamic allocation ~13% CAGR (5Y)</p>
            </div>
            """, unsafe_allow_html=True)
        with col_s3:
            st.markdown("""
            <div class="suggestion-card">
                <h4>Kotak Debt Hybrid Fund</h4>
                <p>Conservative ~9% CAGR (5Y)</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### Top Bonds/Debt Funds for Safe SWP")
        st.info("• SBI Magnum Medium Duration Fund (~7.3% YTM)\n• Kotak Debt Hybrid Fund (~7.5% YTM)\n• Axis Equity Saver (~7.0% YTM)")

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
    col_f, col_g = st.columns(2)
    with col_f:
        st.metric("Investment Value After Years", f"₹{future_value:,.0f}")
    with col_g:
        st.success(f"Gain: ₹{gain:,.0f}")
    
    # Suggestions Section
    with st.expander("🔍 Micro Level Analysis: Top Mutual Funds in Indian Market (Based on Past Performance)"):
        st.markdown("### Best Performing Mutual Funds")
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.markdown("""
            <div class="suggestion-card">
                <h4>Motilal Oswal Large Cap Fund</h4>
                <p>~16% CAGR (5Y)</p>
            </div>
            """, unsafe_allow_html=True)
        with col_m2:
            st.markdown("""
            <div class="suggestion-card">
                <h4>HDFC Focused Fund</h4>
                <p>~28% CAGR (5Y)</p>
            </div>
            """, unsafe_allow_html=True)
        with col_m3:
            st.markdown("""
            <div class="suggestion-card">
                <h4>SBI PSU Fund</h4>
                <p>High growth ~20% CAGR (3Y)</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.info("• Parag Parikh Flexi Cap (~18% CAGR)\n• ICICI Prudential Infrastructure (~19% CAGR)")

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
    col_h, col_i = st.columns(2)
    with col_h:
        st.metric("Maturity Amount", f"₹{maturity:,.0f}")
    with col_i:
        st.success(f"Interest Earned: ₹{maturity - principal:,.0f}")
    
    # Suggestions Section
    with st.expander("🔍 Micro Level Analysis: Best Banks for FD Rates (November 2025)"):
        st.markdown("### Top Banks Offering Highest FD Rates")
        st.info("""
        • **Jana Small Finance Bank**: Up to 8.00% p.a. (for 1-2 years)
        • **Utkarsh Small Finance Bank**: Up to 7.75% p.a. (for 1 year)
        • **Bajaj Finance**: Up to 7.30% p.a. (for 12-60 months)
        • **Canara Bank**: Up to 7.45% p.a. (for 444 days)
        """)

# -------------------------- RD CALCULATOR ----------------------------
if calc == "RD Calculator":
    st.header("📤 Recurring Deposit Calculator")
    col1, col2 = st.columns(2)
    with col1:
        monthly_dep = st.number_input("Monthly Deposit (₹)", min_value=0, value=2000)
        years = st.number_input("Tenure (Years)", min_value=1, value=5)
    with col2:
        rate = st.number_input("Interest Rate (%)", min_value=1.0, value=7.0)
        freq = 4 # Quarterly compounding for RD
    n = years * 12
    r = rate / 400 # Quarterly rate
    maturity = monthly_dep * ((1 + r)**(n/3) - 1) / (1 - (1 + r)**(-1/3))
    st.subheader("Results")
    col_j, col_k = st.columns(2)
    with col_j:
        st.metric("Maturity Amount", f"₹{maturity:,.0f}")
    with col_k:
        st.success(f"Interest Earned: ₹{maturity - (monthly_dep*n):,.0f}")
    
    # Suggestions Section
    with st.expander("🔍 Micro Level Analysis: Best Banks for RD Rates (November 2025)"):
        st.markdown("### Top Banks Offering Highest RD Rates")
        st.info("""
        • **Karur Vysya Bank**: Up to 7.40% p.a. (for general)
        • **Central Bank of India**: Up to 7.25% p.a. (for seniors)
        • **Union Bank of India**: Up to 7.20% p.a. (for 2-3 years)
        • **Bandhan Bank**: Up to 7.50% p.a. (for small finance options)
        """)
