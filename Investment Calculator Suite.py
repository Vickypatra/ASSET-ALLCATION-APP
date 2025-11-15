import streamlit as st
import math
from datetime import datetime

# -------------------------------------------------
# 1. PAGE CONFIG & GLOBAL STYLE (no external CSS files)
# -------------------------------------------------
st.set_page_config(
    page_title="Investment Hub",
    page_icon="Chart",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] {font-family:'Inter',sans-serif;}
    .main {background:#f5f7fb;}
    .header-grad{
        background:linear-gradient(135deg,#1e3a8a 0%,#3b82f6 100%);
        color:white;padding:2rem 1rem;border-radius:1.5rem;
        text-align:center;margin-bottom:2rem;box-shadow:0 8px 20px rgba(0,0,0,0.1);
    }
    .calc-card{
        background:white;padding:1.8rem;border-radius:1.2rem;
        box-shadow:0 4px 15px rgba(0,0,0,0.07);margin-bottom:1.5rem;
    }
    .suggestion-card{
        background:linear-gradient(135deg,#6366f1 0%,#8b5cf6 100%);
        color:white;padding:1rem;border-radius:1rem;margin:0.5rem 0;
        transition:transform .2s;
    }
    .suggestion-card:hover{transform:translateY(-4px);}
    .footer{text-align:center;margin-top:3rem;color:#64748b;}
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
        <h1>Investment Hub</h1>
        <p>Professional calculators • Live suggestions • Interactive charts</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# 3. SIDEBAR NAVIGATION
# -------------------------------------------------
calc = st.sidebar.selectbox(
    "Choose Calculator",
    [
        "SIP Calculator",
        "SWP Calculator",
        "Mutual Fund Growth",
        "FD Calculator",
        "RD Calculator",
    ],
)

# -------------------------------------------------
# 4. CHART.JS HELPER (no pip, pure HTML/JS)
# -------------------------------------------------
def chartjs_line(labels, data, title, color="#3b82f6"):
    return st.markdown(
        f"""
        <canvas id="chart{hash(title)}"></canvas>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
        const ctx = document.getElementById('chart{hash(title)}').getContext('2d');
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: {labels},
                datasets: [{{
                    label: '{title}',
                    data: {data},
                    borderColor: '{color}',
                    backgroundColor: '{color}33',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{title:{{display:true,text:'{title}'}}}},
                scales: {{y:{{ticks:{{callback:v=> '₹'+v.toLocaleString()}}}}}}
            }}
        }});
        </script>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------------------------
# 5. CALCULATORS (unchanged logic + UI + Chart.js)
# -------------------------------------------------
if calc == "SIP Calculator":
    st.markdown("<div class='calc-card'><h2>SIP Calculator</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        monthly_sip = st.number_input("Monthly SIP (₹)", min_value=0, value=5000, step=500)
        years = st.number_input("Tenure (Years)", min_value=1, value=10)
    with col2:
        expected_return = st.number_input("Expected Return (%)", min_value=0.1, value=12.0, step=0.5)

    months = years * 12
    r = expected_return / 12 / 100
    final_value = monthly_sip * (((1 + r) ** months - 1) / r) * (1 + r)
    invested = monthly_sip * months
    gain = final_value - invested

    # ---- Results ----
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Invested", f"₹{invested:,.0f}")
    c2.metric("Maturity", f"₹{final_value:,.0f}")
    c3.metric("Gain", f"₹{gain:,.0f}", delta=f"+{gain/invested*100:.1f}%")

    # ---- Chart ----
    periods = list(range(0, months + 1))
    values = []
    bal = 0
    for m in periods:
        bal = bal * (1 + r) + monthly_sip
        values.append(round(bal))
    chartjs_line([f"M{m}" for m in periods], values, "SIP Growth Over Time")

    # ---- Suggestions ----
    with st.expander("Top SIP Recommendations (Nov 2025)"):
        cols = st.columns(3)
        funds = [
            ("Parag Parikh Flexi Cap", "18.2% 5-yr CAGR"),
            ("Kotak Equity Opp.", "17.4% 5-yr CAGR"),
            ("SBI Small Cap", "22.1% 5-yr CAGR"),
        ]
        for col, (name, cagr) in zip(cols, funds):
            col.markdown(
                f'<div class="suggestion-card"><h4>{name}</h4><p>{cagr}</p></div>',
                unsafe_allow_html=True,
            )
        st.info("**Debt SIPs** – ICICI Pru All Seasons (~7.5% YTM) | HDFC Corp Bond (~7.2% YTM)")
    st.markdown("</div>", unsafe_allow_html=True)


elif calc == "SWP Calculator":
    st.markdown("<div class='calc-card'><h2>SWP Calculator</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        initial = st.number_input("Initial Corpus (₹)", min_value=0, value=500_000, step=10_000)
        swp_monthly = st.number_input("Monthly Withdrawal (₹)", min_value=0, value=5_000, step=500)
    with col2:
        ret_rate = st.number_input("Annual Return (%)", min_value=0.1, value=10.0, step=0.5)
        duration = st.number_input("Years", min_value=1, value=10)

    r = ret_rate / 12 / 100
    n = duration * 12
    balance = initial
    history = [balance]
    for _ in range(n):
        balance = balance * (1 + r) - swp_monthly
        history.append(max(balance, 0))
        if balance <= 0: break

    if balance <= 0:
        st.error("Corpus will be exhausted before the selected period.")
    else:
        st.success(f"Remaining after {duration} yrs: **₹{balance:,.0f}**")

    months = list(range(len(history)))
    chartjs_line([f"M{m}" for m in months], [round(v) for v in history], "SWP Corpus Depletion", "#ef4444")

    with st.expander("Top SWP Funds"):
        cols = st.columns(3)
        funds = [
            ("HDFF Hybrid Equity", "12.1% 5-yr"),
            ("ICICI Pru Balanced Adv.", "13.0% 5-yr"),
            ("Kotak Debt Hybrid", "9.2% 5-yr"),
        ]
        for col, (name, cagr) in zip(cols, funds):
            col.markdown(
                f'<div class="suggestion-card"><h4>{name}</h4><p>{cagr}</p></div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)


elif calc == "Mutual Fund Growth":
    st.markdown("<div class='calc-card'><h2>Lump-Sum Growth</h2>", unsafe_allow_html=True)
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

    years_arr = list(range(yrs + 1))
    vals = [round(lump * (1 + ret / 100) ** y) for y in years_arr]
    chartjs_line([f"Y{y}" for y in years_arr], vals, "Lump-Sum Growth")

    with st.expander("Top Mutual Funds (Nov 2025)"):
        cols = st.columns(3)
        top = [
            ("Motilal Oswal Large Cap", "16.5% 5-yr"),
            ("HDFC Focused", "28.0% 5-yr"),
            ("SBI PSU", "20.3% 3-yr"),
        ]
        for col, (name, cagr) in zip(cols, top):
            col.markdown(
                f'<div class="suggestion-card"><h4>{name}</h4><p>{cagr}</p></div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)


elif calc == "FD Calculator":
    st.markdown("<div class='calc-card'><h2>Fixed Deposit</h2>", unsafe_allow_html=True)
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
    c1.metric("Maturity", f"₹{maturity:,.0f}")
    c2.metric("Interest", f"₹{interest:,.0f}")

    # ---- Bar chart (Chart.js) ----
    banks = ["Jana SFB", "Utkarsh SFB", "Bajaj Fin", "Canara", "Axis"]
    rates = [8.00, 7.75, 7.30, 7.45, 7.10]
    st.markdown(
        f"""
        <canvas id="fdBar"></canvas>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
        new Chart(document.getElementById('fdBar'), {{
            type: 'bar',
            data: {{
                labels: {banks},
                datasets: [{{
                    label: 'FD Rate (%)',
                    data: {rates},
                    backgroundColor: '#3b82f6'
                }}]
            }},
            options: {{plugins:{{title:{{display:true,text:'Highest FD Rates (Nov 2025)'}}}}}}
        }});
        </script>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


elif calc == "RD Calculator":
    st.markdown("<div class='calc-card'><h2>Recurring Deposit</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        monthly = st.number_input("Monthly Deposit (₹)", min_value=0, value=2_000, step=500)
        tenure_y = st.number_input("Tenure (Years)", min_value=1, value=5)
    with col2:
        rate = st.number_input("Interest Rate (%)", min_value=0.1, value=7.0, step=0.1)

    n = tenure_y * 12
    r_q = rate / 400
    maturity = monthly * ((1 + r_q) ** (n / 3) - 1) / (1 - (1 + r_q) ** (-1 / 3))
    interest = maturity - monthly * n

    c1, c2 = st.columns(2)
    c1.metric("Maturity", f"₹{maturity:,.0f}")
    c2.metric("Interest", f"₹{interest:,.0f}")

    # ---- Bar chart ----
    banks = ["Karur Vysya", "Central Bank", "Union Bank", "Bandhan"]
    rates = [7.40, 7.25, 7.20, 7.50]
    st.markdown(
        f"""
        <canvas id="rdBar"></canvas>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
        new Chart(document.getElementById('rdBar'), {{
            type: 'bar',
            data: {{
                labels: {banks},
                datasets: [{{
                    label: 'RD Rate (%)',
                    data: {rates},
                    backgroundColor: '#10b981'
                }}]
            }},
            options: {{plugins:{{title:{{display:true,text:'Highest RD Rates (Nov 2025)'}}}}}}
        }});
        </script>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------------------------
# 6. FOOTER
# -------------------------------------------------
st.markdown(
    """
    <div class="footer">
        <p>Data is illustrative (Nov 2025). Verify with banks/AMCs before investing.</p>
        <p>Built with <strong>Streamlit</strong> + <strong>Chart.js</strong> (no pip)</p>
    </div>
    """,
    unsafe_allow_html=True,
)
