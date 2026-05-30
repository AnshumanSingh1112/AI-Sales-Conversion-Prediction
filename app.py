import streamlit as st
import joblib

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="SalesIQ · Conversion Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CSS ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #F0F4FF !important;
    color: #1e293b;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 70% 35% at 50% -5%, rgba(99,102,241,0.10) 0%, transparent 65%),
        radial-gradient(ellipse 40% 25% at 95% 85%, rgba(20,184,166,0.09) 0%, transparent 60%),
        #F0F4FF !important;
}
[data-testid="stHeader"]  { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }

/* Topbar */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    background: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    padding: 14px 28px;
    border-radius: 0 0 0 0;
    margin-bottom: 0;
}
.brand { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; }
.brand span { color: #6366f1; }
.ml-badge { background: #eef2ff; border: 1px solid #c7d2fe; color: #4f46e5; font-size: 11px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; padding: 5px 14px; border-radius: 100px; }

/* Hero */
.hero-wrap { text-align: center; padding: 48px 0 28px; }
.hero-title { font-family: 'Syne', sans-serif; font-size: clamp(32px, 4vw, 54px); font-weight: 800; line-height: 1.1; color: #0f172a; margin: 0 0 16px; letter-spacing: -1.5px; }
.hero-title span { background: linear-gradient(135deg, #6366f1 0%, #14b8a6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-sub { font-size: 15px; color: #64748b; font-weight: 400; max-width: 480px; margin: 0 auto; line-height: 1.75; }

/* Stat cards */
.stats-row { display: flex; gap: 14px; margin: 32px 0 28px; }
.stat-card { flex: 1; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px 16px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(99,102,241,0.05); transition: box-shadow 0.2s, transform 0.2s, border-color 0.2s; }
.stat-card:hover { box-shadow: 0 4px 24px rgba(99,102,241,0.14); border-color: #c7d2fe; transform: translateY(-2px); }
.stat-icon { width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 17px; margin: 0 auto 10px; }
.icon-indigo { background: #eef2ff; }
.icon-teal   { background: #f0fdfa; }
.icon-amber  { background: #fffbeb; }
.stat-value  { font-family: 'Syne', sans-serif; font-size: 28px; font-weight: 800; color: #0f172a; line-height: 1; margin-bottom: 4px; }
.stat-label  { font-size: 12px; color: #94a3b8; font-weight: 500; }
.c-indigo { color: #6366f1; } .c-teal { color: #0d9488; } .c-amber { color: #d97706; }

/* Section */
.section-heading { font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 800; color: #0f172a; margin-bottom: 2px; }
.section-sub { font-size: 12px; color: #94a3b8; margin-bottom: 16px; }

/* Input panel */
.input-panel { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; padding: 28px 28px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.03), 0 8px 32px rgba(99,102,241,0.04); }

/* Slider / select labels */
[data-testid="stSlider"] label,
[data-testid="stSelectbox"] label {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 12px !important; font-weight: 600 !important; color: #475569 !important;
}
[data-testid="stSlider"] > div > div > div > div { background: #6366f1 !important; }

/* Button */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: #fff !important; border: none !important; border-radius: 14px !important;
    padding: 16px 40px !important;
    font-family: 'Syne', sans-serif !important; font-size: 15px !important; font-weight: 700 !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.28) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 28px rgba(99,102,241,0.40) !important; }

/* Result card */
.result-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 20px; padding: 36px 28px; text-align: center; margin-top: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.03), 0 8px 32px rgba(99,102,241,0.05); }
.result-percent { font-family: 'Syne', sans-serif; font-size: 68px; font-weight: 800; line-height: 1; margin-bottom: 6px; background: linear-gradient(135deg, #6366f1 0%, #14b8a6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.result-label { font-size: 12px; color: #94a3b8; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 600; margin-bottom: 22px; }
.verdict-high { display: inline-flex; align-items: center; gap: 8px; background: #f0fdf4; border: 1px solid #bbf7d0; color: #15803d; font-weight: 700; font-size: 14px; padding: 10px 26px; border-radius: 100px; }
.verdict-low  { display: inline-flex; align-items: center; gap: 8px; background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; font-weight: 700; font-size: 14px; padding: 10px 26px; border-radius: 100px; }

/* Progress bar */
[data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg, #6366f1, #14b8a6) !important; border-radius: 100px; }
[data-testid="stProgressBar"] > div { background: #e2e8f0 !important; border-radius: 100px; height: 8px !important; }

/* Footer */
.footer { text-align: center; color: #cbd5e1; font-size: 11px; padding: 28px 0 16px; letter-spacing: 0.5px; }
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------

model = joblib.load("rf_model.pkl")

# ── TOPBAR ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="topbar">
    <div class="brand">Sales<span>IQ</span></div>
    <div class="ml-badge">ML Powered</div>
</div>
""", unsafe_allow_html=True)

# ── HERO ────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-wrap">
    <h1 class="hero-title">Predict Sales Conversions<br>with <span>AI Precision</span></h1>
    <p class="hero-sub">Enter your lead's data and let our Random Forest model instantly score their conversion likelihood.</p>
</div>
""", unsafe_allow_html=True)

# ── STAT CARDS ──────────────────────────────────────────────────────────────

st.markdown("""
<div class="stats-row">
    <div class="stat-card">
        <div class="stat-icon icon-indigo">📊</div>
        <div class="stat-value c-indigo">100K</div>
        <div class="stat-label">Training Records</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon icon-teal">🎯</div>
        <div class="stat-value c-teal">99%</div>
        <div class="stat-label">Model Accuracy</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon icon-amber">🌲</div>
        <div class="stat-value c-amber">RF</div>
        <div class="stat-label">Random Forest</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── INPUTS ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="section-heading">Lead Parameters</div>
<div class="section-sub">Fill in the details about your lead to generate a conversion score.</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-panel">', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    age            = st.slider("👤  Age", 18, 80, 30)
    time_spent     = st.slider("⏱️  Time Spent on Website (mins)", 1, 300, 30)
    pages_viewed   = st.slider("📄  Pages Viewed", 1, 50, 5)
    email_sent     = st.selectbox("📧  Email Sent", [0, 1], format_func=lambda x: "✅ Yes" if x else "❌ No")
    form_submissions = st.slider("📝  Form Submissions", 0, 20, 1)

with col2:
    downloads      = st.slider("⬇️  Downloads", 0, 20, 0)
    ctr            = st.slider("🖱️  CTR Product Page (%)", 0, 100, 20)
    response_time  = st.slider("⏰  Response Time (Hours)", 0, 72, 24)
    followup       = st.slider("📬  Follow-Up Emails", 0, 20, 2)
    engagement     = st.slider("💬  Social Media Engagement", 0, 500, 100)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ── PREDICT ─────────────────────────────────────────────────────────────────

if st.button("⚡  Predict Conversion Probability"):

    features = [0] * 30
    features[0] = age
    features[1] = time_spent
    features[2] = pages_viewed
    features[3] = email_sent
    features[4] = form_submissions
    features[5] = downloads
    features[6] = ctr
    features[7] = response_time
    features[8] = followup
    features[9] = engagement

    prediction  = model.predict([features])[0]
    probability = model.predict_proba([features])[0][1] * 100

    verdict_html = (
        '<div class="verdict-high">✅ High-Priority Lead — Engage Now</div>'
        if prediction == 1
        else '<div class="verdict-low">⚠️ Low Priority — Needs Nurturing</div>'
    )

    st.markdown(f"""
    <div class="result-card">
        <div class="result-percent">{probability:.1f}%</div>
        <div class="result-label">Conversion Probability Score</div>
        {verdict_html}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(int(probability))

# ── FOOTER ───────────────────────────────────────────────────────────────────

st.markdown("""
<div class="footer">
    Built with Python &nbsp;·&nbsp; Scikit-Learn &nbsp;·&nbsp; Random Forest &nbsp;·&nbsp; Streamlit
</div>
""", unsafe_allow_html=True)
