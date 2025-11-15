import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# -------------------------------------------------
# 1. PAGE CONFIG & GLOBAL STYLE
# -------------------------------------------------
st.set_page_config(
    page_title="Asset Allocation • Investment Hub",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS – modern, gradient cards, dark-mode toggle, fonts
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] {font-family: 'Inter', sans-serif;}
    .main {background: #f5f7fb;}
    .header-grad {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 2rem 1rem;
        border-radius: 1.5rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    .calc-card {
        background: white;
        padding: 1.8rem;
        border-radius: 1.2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.07);
        margin-bottom: 1.5rem;
    }
    .suggestion-card {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        transition: transform .2s;
    }
    .suggestion-card:hover {transform: translateY(-4px);}
    .stMetric {background:#eef2ff; padding:0.8rem; border-radius:0.8rem;}
    .footer {text-align:center; margin-top:3rem; color:#64748b;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Dark-mode toggle (optional)
dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=False)
if dark_mode:
    st.markdown(
        """
        <style>
        .main {background:#0f172a;}
        .calc-card {background:#1e293b; color:#e2e8f0;}
        .stMetric {background:#334155;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------------------------
# 2. HEADER
# -------------------------------------------------
st.markdown(
    """
    <div class="header-grad">
        <h1>💼 Asset Allocation & Investment Hub</h1>
        <p>Professional calculators • Real-time suggestions • Interactive charts</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# 3. SIDEBAR NAVIGATION
# -------------------------------------------------
calc = st.sidebar.selectbox(
    "📊 Choose Calculator",
    [
        "SIP Calculator",
        "SWP Calculator",
        "Mutual Fund Growth",
        "FD Calculator",
        "RD Calculator",
    ],
)

# -------------------------------------------------
# 4. HELPER: Plotly growth chart (used in SIP, SWP, MF)
# -------------------------------------------------
def plot_growth(df, title, y_col, color="#3b82f6"):
    fig = px.line(
        df,
        x="Period",
        y=y_col,
        title=title,
        markers=True,
        line_shape="spline",
        color_discrete_sequence=[color],
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter"),
        hovermode="x unified",
    )
    fig.update_yaxes(title="₹ Amount", tickprefix="₹", separatethousands=True)
    return fig

# -------------------------------------------------
# 5. CALCULATORS (unchanged logic + UI + Charts)
# -------------------------------------------------
if calc == "SIP Calculator":
    st.markdown("<div class='calc-card'><h2>📈 SIP Calculator</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        monthly_sip = st.number_input("Monthly SIP (₹)", min_value=0, value=5000, step=500)
        years = st.number_input("Tenure (Years)", min_value=1, value=10)
    with col2:
        expected_return = st.number_input("Expected Annual Return (%)", min_value=0.1, value=12.0, step=0.5)

    months = years * 12
    r = expected_return / 12 / 100
    final_value = monthly_sip * (((1 + r) ** months - 1) / r) * (1 + r)
    invested = monthly_sip * months
    gain = final_value - invested

    # ---- Results ----
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Invested", f"₹{invested:,.0f}")
    c2.metric("Maturity Value", f"₹{final_value:,.0f}")
    c3.metric("Wealth Gain", f"₹{gain:,.0f}", delta=f"+{gain/invested*100:.1f}%")

    # ---- Growth Chart ----
    periods = np.arange(0, months + 1)
    values = [monthly_sip * i for i in periods]
    for m in periods[1:]:
        values[m] = values[m - 1] * (1 + r) + monthly_sip
    df = pd.DataFrame({"Period": periods, "Amount": values})
    st.plotly_chart(plot_growth(df, "SIP Growth Over Time", "Amount"), use_container_width=True)

    # ---- Suggestions (expandable) ----
    with st.expander("🔍 Top SIP Recommendations (Nov 2025)"):
        cols = st.columns(3)
        funds = [
            ("Parag Parikh Flexi Cap", "18.2% 5-yr CAGR"),
            ("Kotak Equity Opportunities", "17.4% 5-yr CAGR"),
            ("SBI Small Cap", "22.1% 5-yr CAGR"),
        ]
        for col, (name, cagr) in zip(cols, funds):
            col.markdown(
                f"""
                <div class="suggestion-card">
                    <h4>{name}</h4>
                    <p>{cagr}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.info(
            """
            **Debt SIPs** – ICICI Pru All Seasons Bond (~7.5% YTM) | HDFC Corporate Bond (~7.2% YTM)
            """
        )
    st.markdown("</div>", unsafe_allow_html=True)


elif calc == "SWP Calculator":
    st.markdown("<div class='calc-card'><h2>💸 SWP Calculator</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        initial = st.number_input("Initial Corpus (₹)", min_value=0, value=500_000, step=10_000)
        swp_monthly = st.number_input("Monthly Withdrawal (₹)", min_value=0, value=5_000, step=500)
    with col2:
        ret_rate = st.number_input("Annual Return (%)", min_value=0.1, value=10.0, step=0.5)
        duration = st.number_input("Withdrawal Years", min_value=1, value=10)

    r = ret_rate / 12 / 100
    n = duration * 12
    balance = initial
    history = [balance]
    for _ in range(n):
        balance = balance * (1 + r) - swp_monthly
        history.append(max(balance, 0))
        if balance <= 0:
            break

    # ---- Results ----
    if balance <= 0:
        st.error("⚠️ Corpus will be exhausted before the selected period.")
    else:
        st.success(f"Remaining Balance after {duration} yrs: **₹{balance:,.0f}**")

    # ---- Chart ----
    df = pd.DataFrame({"Month": range(len(history)), "Corpus": history})
    fig = plot_growth(df, "SWP Corpus Depletion", "Corpus", color="#ef4444")
    st.plotly_chart(fig, use_container_width=True)

    # ---- Suggestions ----
    with st.expander("🔍 Top SWP Funds (Balanced & Debt)"):
        cols = st.columns(3)
        funds = [
            ("HDFC Hybrid Equity", "12.1% 5-yr CAGR"),
            ("ICICI Pru Balanced Advantage", "13.0% 5-yr CAGR"),
            ("Kotak Debt Hybrid", "9.2% 5-yr CAGR"),
        ]
        for col, (name, cagr) in zip(cols, funds):
            col.markdown(
                f"""
                <div class="suggestion-card">
                    <h4>{name}</h4>
                    <p>{cagr}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)


elif calc == "Mutual Fund Growth":
    st.markdown("<div class='calc-card'><h2>📊 Lump-Sum Mutual Fund Growth</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        lump = st.number_input("Lump-Sum (₹)", min_value=0, value=100_000, step=5_000)
    with col2:
        ret = st.number_input("Annual Return (%)", min_value=0.1, value=12.0, step=0.5)
        yrs = st.number_input("Years", min_value=1, value=10)

    future = lump * (1 + ret / 100) ** yrs
    gain = future - lump

    c1, c2 = st.columns(2)
    c1.metric("Future Value", f"₹{future:,.0f}")
    c2.metric("Gain", f"₹{gain:,.0f}", delta=f"+{gain/lump*100:.1f}%")

    # ---- Year-by-year chart ----
    years_arr = np.arange(0, yrs + 1)
    vals = lump * (1 + ret / 100) ** years_arr
    df = pd.DataFrame({"Year": years_arr, "Value": vals})
    st.plotly_chart(plot_growth(df, "Lump-Sum Growth", "Value"), use_container_width=True)

    # ---- Top MF ----
    with st.expander("🔍 Top Performing Mutual Funds (Nov 2025)"):
        cols = st.columns(3)
        top = [
            ("Motilal Oswal Large Cap", "16.5% 5-yr"),
            ("HDFC Focused", "28.0% 5-yr"),
            ("SBI PSU", "20.3% 3-yr"),
        ]
        for col, (name, cagr) in zip(cols, top):
            col.markdown(
                f"""
                <div class="suggestion-card">
                    <h4>{name}</h4>
                    <p>{cagr}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)


elif calc == "FD Calculator":
    st.markdown("<div class='calc-card'><h2>🏦 Fixed Deposit Calculator</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        principal = st.number_input("Principal (₹)", min_value=0, value=50_000, step=5_000)
        tenure = st.number_input("Tenure (Years)", min_value=1, value=5)
    with col2:
        rate = st.number_input("Interest Rate (%)", min_value=0.1, value=6.5, step=0.1)
        freq = st.selectbox("Compounding", ["Yearly", "Half-Yearly", "Quarterly", "Monthly"])

    freq_map = {"Yearly": 1, "Half-Yearly": 2, "Quarterly": 4, "Monthly": 12}
    f = freq_map[freq]
    maturity = principal * (1 + rate / 100 / f) ** (f * tenure)
    interest = maturity - principal

    c1, c2 = st.columns(2)
    c1.metric("Maturity Amount", f"₹{maturity:,.0f}")
    c2.metric("Interest Earned", f"₹{interest:,.0f}")

    # ---- Bar chart of top FD rates (Nov 2025) ----
    fd_data = {
        "Bank": [
            "Jana Small Finance",
            "Utkarsh SFB",
            "Bajaj Finance",
            "Canara Bank",
            "Axis Bank",
        ],
        "Rate (%)": [8.00, 7.75, 7.30, 7.45, 7.10],
    }
    df_fd = pd.DataFrame(fd_data)
    fig = px.bar(
        df_fd,
        x="Bank",
        y="Rate (%)",
        text="Rate (%)",
        color="Rate (%)",
        color_continuous_scale="Blues",
        title="🏦 Highest FD Rates (Nov 2025)",
    )
    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_layout(showlegend=False, yaxis=dict(range=[0, 9]))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


elif calc == "RD Calculator":
    st.markdown("<div class='calc-card'><h2>📤 Recurring Deposit Calculator</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        monthly = st.number_input("Monthly Deposit (₹)", min_value=0, value=2_000, step=500)
        tenure_y = st.number_input("Tenure (Years)", min_value=1, value=5)
    with col2:
        rate = st.number_input("Interest Rate (%)", min_value=0.1, value=7.0, step=0.1)

    n = tenure_y * 12
    r_q = rate / 400  # quarterly rate
    maturity = monthly * ((1 + r_q) ** (n / 3) - 1) / (1 - (1 + r_q) ** (-1 / 3))
    interest = maturity - monthly * n

    c1, c2 = st.columns(2)
    c1.metric("Maturity Amount", f"₹{maturity:,.0f}")
    c2.metric("Interest Earned", f"₹{interest:,.0f}")

    # ---- Bar chart of top RD rates ----
    rd_data = {
        "Bank": ["Karur Vysya", "Central Bank", "Union Bank", "Bandhan Bank"],
        "Rate (%)": [7.40, 7.25, 7.20, 7.50],
    }
    df_rd = pd.DataFrame(rd_data)
    fig = px.bar(
        df_rd,
        x="Bank",
        y="Rate (%)",
        text="Rate (%)",
        color="Rate (%)",
        color_continuous_scale="Greens",
        title="📤 Highest RD Rates (Nov 2025)",
    )
    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    fig.update_layout(showlegend=False, yaxis=dict(range=[0, 8]))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------
# 6. FOOTER
# -------------------------------------------------
st.markdown(
    """
    <div class="footer">
        <p>💡 <em>Data shown is illustrative & based on publicly available information as of Nov 2025. 
        Always verify with the official bank / AMC before investing.</em></p>
        <p>Built with ❤️ using <strong>Streamlit</strong> • <strong>Plotly</strong></p>
    </div>
    """,
    unsafe_allow_html=True,
)
