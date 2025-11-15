# -------------------------------------------------
#  app.py   –  ONE-PAGE INVESTMENT HUB
#  Run:   streamlit run app.py
# -------------------------------------------------
import streamlit as st
import math

st.set_page_config(page_title="Investment Hub", page_icon="Chart", layout="wide")

# ────────────────────── GLOBAL STYLE ──────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html,body,[class*="css"]{font-family:'Inter',sans-serif;}
    .main{background:#f5f7fb;}
    .header-grad{
        background:linear-gradient(135deg,#1e3a8a 0%,#3b82f6 100%);
        color:white;padding:2rem 1rem;border-radius:1.5rem;
        text-align:center;margin-bottom:2rem;box-shadow:0 8px 20px rgba(0,0,0,0.1);
    }
    .calc-card{
        background:white;padding:1.8rem;border-radius:1.2rem;
        box-shadow:0 4px 15px rgba(0,0,0,0.07);margin-bottom:2rem;
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

# ────────────────────── HEADER ──────────────────────
st.markdown(
    """
    <div class="header-grad">
        <h1>Investment Hub</h1>
        <p>All calculators • Live charts • Top suggestions (Nov 2025)</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ────────────────────── CHART.JS HELPER ──────────────────────
def chartjs_line(canvas_id, labels, data, title, color="#3b82f6"):
    st.markdown(
        f"""
        <canvas id="{canvas_id}"></canvas>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
        new Chart(document.getElementById('{canvas_id}'), {{
            type:'line',
            data:{{
                labels:{labels},
                datasets:[{{label:'{title}',data:{data},borderColor:'{color}',
                           backgroundColor:'{color}33',fill:true,tension:0.4,pointRadius:4}}]
            }},
            options:{{
                responsive:true,
                plugins:{{title:{{display:true,text:'{title}'}}}},
                scales:{{y:{{ticks:{{callback:v=>'₹'+v.toLocaleString()}}}}}}
            }}
        }});
        </script>
        """,
        unsafe_allow_html=True,
    )

# ────────────────────── 1. SIP CALCULATOR ──────────────────────
st.markdown("<div class='calc-card'><h2>SIP Calculator</h2>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    sip_monthly = st.number_input("Monthly SIP (₹)", min_value=0, value=5000, step=500, key="sip_m")
    sip_years   = st.number_input("Tenure (Years)", min_value=1, value=10, key="sip_y")
with c2:
    sip_rate = st.number_input("Expected Return (%)", min_value=0.1, value=12.0, step=0.5, key="sip_r")

months = sip_years * 12
r = sip_rate / 12 / 100
sip_final = sip_monthly * (((1 + r) ** months - 1) / r) * (1 + r)
sip_invested = sip_monthly * months
sip_gain = sip_final - sip_invested

col_a, col_b, col_c = st.columns(3)
col_a.metric("Invested", f"₹{sip_invested:,.0f}")
col_b.metric("Maturity", f"₹{sip_final:,.0f}")
col_c.metric("Gain", f"₹{sip_gain:,.0f}", delta=f"+{sip_gain/sip_invested*100:.1f}%")

# growth chart
periods = list(range(months + 1))
vals = []
bal = 0
for _ in periods:
    bal = bal * (1 + r) + sip_monthly
    vals.append(round(bal))
chartjs_line("sipChart", [f"M{i}" for i in periods], vals, "SIP Growth")

# suggestions – ALWAYS VISIBLE
st.markdown("### Top SIP Funds (Nov 2025)")
cols = st.columns(3)
for col, (name, cagr) in zip(cols, [
    ("Parag Parikh Flexi Cap", "18.2% 5-yr"),
    ("Kotak Equity Opp.", "17.4% 5-yr"),
    ("SBI Small Cap", "22.1% 5-yr")
]):
    col.markdown(f'<div class="suggestion-card"><h4>{name}</h4><p>{cagr}</p></div>', unsafe_allow_html=True)
st.info("**Debt SIPs** – ICICI Pru All Seasons (~7.5% YTM) | HDFC Corp Bond (~7.2% YTM)")
st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────── 2. SWP CALCULATOR ──────────────────────
st.markdown("<div class='calc-card'><h2>SWP Calculator</h2>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    swp_initial = st.number_input("Initial Corpus (₹)", min_value=0, value=500000, step=10000, key="swp_i")
    swp_monthly = st.number_input("Monthly Withdrawal (₹)", min_value=0, value=5000, step=500, key="swp_w")
with c2:
    swp_rate = st.number_input("Annual Return (%)", min_value=0.1, value=10.0, step=0.5, key="swp_r")
    swp_years = st.number_input("Years", min_value=1, value=10, key="swp_y")

r = swp_rate / 12 / 100
n = swp_years * 12
bal = swp_initial
history = [bal]
for _ in range(n):
    bal = bal * (1 + r) - swp_monthly
    history.append(max(bal, 0))
    if bal <= 0: break

if bal <= 0:
    st.error("Corpus exhausted before period ends.")
else:
    st.success(f"Remaining after {swp_years} yrs: **₹{bal:,.0f}**")

chartjs_line("swpChart", [f"M{i}" for i in range(len(history))], [round(v) for v in history],
             "SWP Corpus Depletion", "#ef4444")

st.markdown("### Top SWP Funds")
cols = st.columns(3)
for col, (name, cagr) in zip(cols, [
    ("HDFC Hybrid Equity", "12.1% 5-yr"),
    ("ICICI Pru Balanced Adv.", "13.0% 5-yr"),
    ("Kotak Debt Hybrid", "9.2% 5-yr")
]):
    col.markdown(f'<div class="suggestion-card"><h4>{name}</h4><p>{cagr}</p></div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────── 3. MUTUAL FUND LUMP-SUM ──────────────────────
st.markdown("<div class='calc-card'><h2>Lump-Sum Mutual Fund Growth</h2>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    mf_lump = st.number_input("Lump-Sum (₹)", min_value=0, value=100000, step=5000, key="mf_l")
with c2:
    mf_rate = st.number_input("Annual Return (%)", min_value=0.1, value=12.0, step=0.5, key="mf_r")
    mf_years = st.number_input("Years", min_value=1, value=10, key="mf_y")

mf_future = mf_lump * (1 + mf_rate/100) ** mf_years
mf_gain = mf_future - mf_lump

col_a, col_b = st.columns(2)
col_a.metric("Future Value", f"₹{mf_future:,.0f}")
col_b.metric("Gain", f"₹{mf_gain:,.0f}", delta=f"+{mf_gain/mf_lump*100:.1f}%")

years_arr = list(range(mf_years + 1))
vals = [round(mf_lump * (1 + mf_rate/100) ** y) for y in years_arr]
chartjs_line("mfChart", [f"Y{y}" for y in years_arr], vals, "Lump-Sum Growth")

st.markdown("### Top Performing Mutual Funds")
cols = st.columns(3)
for col, (name, cagr) in zip(cols, [
    ("Motilal Oswal Large Cap", "16.5% 5-yr"),
    ("HDFC Focused", "28.0% 5-yr"),
    ("SBI PSU", "20.3% 3-yr")
]):
    col.markdown(f'<div class="suggestion-card"><h4>{name}</h4><p>{cagr}</p></div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────── 4. FD CALCULATOR ──────────────────────
st.markdown("<div class='calc-card'><h2>Fixed Deposit Calculator</h2>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    fd_principal = st.number_input("Principal (₹)", min_value=0, value=50000, step=5000, key="fd_p")
    fd_tenure = st.number_input("Tenure (Years)", min_value=1, value=5, key="fd_t")
with c2:
    fd_rate = st.number_input("Interest Rate (%)", min_value=0.1, value=6.5, step=0.1, key="fd_r")
    fd_freq = st.selectbox("Compounding", ["Yearly","Half-Yearly","Quarterly","Monthly"], key="fd_f")

freq_map = {"Yearly":1,"Half-Yearly":2,"Quarterly":4,"Monthly":12}
f = freq_map[fd_freq]
fd_maturity = fd_principal * (1 + fd_rate/100/f) ** (f * fd_tenure)
fd_interest = fd_maturity - fd_principal

col_a, col_b = st.columns(2)
col_a.metric("Maturity", f"₹{fd_maturity:,.0f}")
col_b.metric("Interest", f"₹{fd_interest:,.0f}")

# bar chart of top FD rates
banks = ["Jana SFB","Utkarsh SFB","Bajaj Fin","Canara","Axis"]
rates = [8.00,7.75,7.30,7.45,7.10]
st.markdown(
    f"""
    <canvas id="fdBar"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('fdBar'), {{
        type:'bar',
        data:{{labels:{banks},datasets:[{{label:'Rate (%)',data:{rates},backgroundColor:'#3b82f6'}}]}},
        options:{{plugins:{{title:{{display:true,text:'Highest FD Rates (Nov 2025)'}}}}}}
    }});
    </script>
    """,
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────── 5. RD CALCULATOR ──────────────────────
st.markdown("<div class='calc-card'><h2>Recurring Deposit Calculator</h2>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    rd_monthly = st.number_input("Monthly Deposit (₹)", min_value=0, value=2000, step=500, key="rd_m")
    rd_tenure = st.number_input("Tenure (Years)", min_value=1, value=5, key="rd_t")
with c2:
    rd_rate = st.number_input("Interest Rate (%)", min_value=0.1, value=7.0, step=0.1, key="rd_r")

n = rd_tenure * 12
r_q = rd_rate / 400
rd_maturity = rd_monthly * ((1 + r_q)**(n/3) - 1) / (1 - (1 + r_q)**(-1/3))
rd_interest = rd_maturity - rd_monthly * n

col_a, col_b = st.columns(2)
col_a.metric("Maturity", f"₹{rd_maturity:,.0f}")
col_b.metric("Interest", f"₹{rd_interest:,.0f}")

# bar chart of top RD rates
banks = ["Karur Vysya","Central Bank","Union Bank","Bandhan"]
rates = [7.40,7.25,7.20,7.50]
st.markdown(
    f"""
    <canvas id="rdBar"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('rdBar'), {{
        type:'bar',
        data:{{labels:{banks},datasets:[{{label:'Rate (%)',data:{rates},backgroundColor:'#10b981'}}]}},
        options:{{plugins:{{title:{{display:true,text:'Highest RD Rates (Nov 2025)'}}}}}}
    }});
    </script>
    """,
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

# ────────────────────── FOOTER ──────────────────────
st.markdown(
    """
    <div class="footer">
        <p>Data is illustrative (Nov 2025). Always verify with banks/AMCs.</p>
        <p>Built with <strong>Streamlit</strong> + <strong>Chart.js</strong> (no pip)</p>
    </div>
    """,
    unsafe_allow_html=True,
)
