import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="SalesIQ · Conversion Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── THEME CONFIGURATION ENGINE ──────────────────────────────────────────────

if 'theme_mode' not in st.session_state:
    st.session_state['theme_mode'] = 'Light'

with st.sidebar:
    st.markdown('<div style="font-family:\'Syne\'; font-size:12px; font-weight:700; color:#64748B; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;">Interface Workspace</div>', unsafe_allow_html=True)
    theme_selection = st.selectbox(
        "🌓 Select UI Mode",
        ["Light", "Dark"],
        index=0 if st.session_state['theme_mode'] == 'Light' else 1,
        label_visibility="collapsed"
    )
    st.session_state['theme_mode'] = theme_selection

# Define color matrix dictionaries cleanly based on active theme choice
if st.session_state['theme_mode'] == 'Dark':
    cfg_bg = "#0B0F19"
    cfg_panel = "#1E293B"
    cfg_border = "#334155"
    cfg_text = "#F8FAFC"
    cfg_subtext = "#94A3B8"
    cfg_bar_color = "#6366F1"
    cfg_bg_gradient = "radial-gradient(ellipse 60% 30% at 50% -5%, rgba(99,102,241,0.15) 0%, transparent 70%), #0B0F19"
    chart_theme_grid = "#334155"
else:
    cfg_bg = "#F8FAFC"
    cfg_panel = "#FFFFFF"
    cfg_border = "#E2E8F0"
    cfg_text = "#0F172A"
    cfg_subtext = "#64748B"
    cfg_bar_color = "#0F172A"
    cfg_bg_gradient = "radial-gradient(ellipse 60% 30% at 50% -5%, rgba(99,102,241,0.06) 0%, transparent 70%), #F8FAFC"
    chart_theme_grid = "#E2E8F0"

# ---------------- ENTERPRISE STYLING OVERLAYS ----------------

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}

html, body, [data-testid="stAppViewContainer"] {{
    background: {cfg_bg} !important;
    color: {cfg_text} !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
}}

[data-testid="stSidebar"] {{
    background-color: {cfg_panel} !important;
    border-right: 1px solid {cfg_border} !important;
}}

[data-testid="stAppViewContainer"] {{
    background: {cfg_bg_gradient} !important;
}}

[data-testid="stHeader"]  {{ background: transparent !important; }}
[data-testid="stToolbar"] {{ display: none !important; }}

/* Topbar Wrapper Navigation elements */
.topbar {{
    display: flex; align-items: center; justify-content: space-between;
    background: {cfg_panel};
    border: 1px solid {cfg_border};
    padding: 14px 28px;
    margin-bottom: 24px;
    border-radius: 14px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.01);
}}
.brand {{ font-family: 'Syne', sans-serif; font-size: 22px; font-weight: 800; color: {cfg_text}; letter-spacing: -0.5px; }}
.brand span {{ color: #6366f1; }}
.ml-badge {{ background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.2); color: #6366f1; font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; padding: 5px 14px; border-radius: 100px; }}

.sidebar-title {{ font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 800; color: {cfg_text}; margin-bottom: 4px; }}
.sidebar-sub {{ font-size: 12px; color: {cfg_subtext}; margin-bottom: 24px; line-height: 1.4; }}

.nav-item {{ display: flex; align-items: center; gap: 10px; padding: 10px 12px; color: {cfg_subtext}; font-weight: 500; font-size: 14px; border-radius: 8px; margin-bottom: 4px; }}
.nav-active {{ background: rgba(99,102,241,0.12); color: #6366f1; font-weight: 600; }}

/* Status Alerts Style Modifications */
.status-card-wrap {{ border-radius: 16px; padding: 26px; margin-bottom: 24px; border: 1px solid {cfg_border}; }}
.wrap-high {{ background: rgba(22, 163, 74, 0.06) !important; border-left: 6px solid #16A34A !important; }}
.wrap-medium {{ background: rgba(234, 88, 12, 0.06) !important; border-left: 6px solid #EA580C !important; }}
.wrap-low {{ background: rgba(148, 163, 184, 0.06) !important; border-left: 6px solid #64748B !important; }}

.result-header-text {{ font-family: 'Syne', sans-serif; font-size: 30px; font-weight: 800; color: {cfg_text}; margin-bottom: 4px; }}
.verdict-tag-high {{ color: #16A34A; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }}
.verdict-tag-medium {{ color: #EA580C; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }}
.verdict-tag-low {{ color: {cfg_subtext}; font-weight: 700; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }}
.result-sub-text {{ font-size: 14px; color: {cfg_text}; opacity: 0.85; margin-top: 12px; line-height: 1.5; }}

/* Micro KPI Cards Panels */
.micro-kpi-row {{ display: flex; gap: 16px; margin-bottom: 24px; }}
.micro-card {{ flex: 1; background: {cfg_panel}; border: 1px solid {cfg_border}; border-radius: 14px; padding: 18px; box-shadow: 0 2px 8px rgba(0,0,0,0.01); }}
.micro-label {{ font-size: 11px; font-weight: 600; color: {cfg_subtext}; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }}
.micro-value {{ font-family: 'Syne', sans-serif; font-size: 22px; font-weight: 800; color: {cfg_text}; }}

/* Streamlit Widget Label Overrides based on selected theme colors */
[data-testid="stSidebar"] [data-testid="stSlider"] label,
[data-testid="stSidebar"] [data-testid="stSelectbox"] label {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 12px !important; font-weight: 600 !important; color: {cfg_text} !important;
    opacity: 0.9;
}}

.stButton > button {{
    width: 100%;
    background: #6366F1 !important;
    color: #FFFFFF !important; border: none !important; border-radius: 10px !important;
    padding: 12px 24px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 14px !important; font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.2) !important;
    transition: all 0.15s ease !important;
}}
.stButton > button:hover {{ background: #4F46E5 !important; transform: translateY(-1px); }}

.dashboard-container {{ background: {cfg_panel}; border: 1px solid {cfg_border}; border-radius: 20px; padding: 24px; margin-top: 24px; }}
.footer {{ text-align: center; color: {cfg_subtext}; font-size: 11px; padding: 40px 0 16px; letter-spacing: 0.5px; }}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------

model = joblib.load("rf_model.pkl")

# ── SIDEBAR CONTROLS & INPUT LAYOUT ─────────────────────────────────────────

with st.sidebar:
    st.markdown("<div style='margin-top:15px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">SalesIQ Panel</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Decision support framework for intelligence operations.</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="nav-item"><span class="icon">🏠</span> Home</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item nav-active"><span class="icon">🎯</span> Prediction Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-item"><span class="icon">📊</span> Historic Analytics</div>', unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 20px 0; border: 0; border-top: 1px solid rgba(148,163,184,0.15);'>", unsafe_allow_html=True)
    
    age = st.slider("👤 Age", 18, 80, 30)
    time_spent = st.slider("⏱️ Time Spent on Website (mins)", 1, 300, 30)
    pages_viewed = st.slider("📄 Pages Viewed", 1, 50, 5)
    email_sent = st.selectbox("📧 Email Sent", [0, 1], format_func=lambda x: "✅ Yes" if x else "❌ No")
    form_submissions = st.slider("📝 Form Submissions", 0, 20, 1)
    
    lead_source = st.selectbox(
        "🎯 Lead Source",
        ["Email", "Organic", "Referral", "Social Media"]
    )
    
    downloads = st.slider("⬇️ Downloads", 0, 20, 0)
    ctr = st.slider("🖱️ CTR Product Page (%)", 0, 100, 20)
    response_time = st.slider("⏰ Response Time (Hours)", 0, 72, 24)
    followup = st.slider("📬 Follow-Up Emails", 0, 20, 2)
    engagement = st.slider("💬 Social Media Engagement", 0, 500, 100)
    
    payment_history = st.selectbox(
        "💳 Payment History",
        ["Good", "No Payment"]
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    submit_clicked = st.button("Run Prediction Execution")

# ── MAIN AREA TOPBAR CONTENT LAYOUT ─────────────────────────────────────────

st.markdown("""
<div class="topbar">
    <div class="brand">Sales<span>IQ</span> Intelligence App</div>
    <div class="ml-badge">Random Forest Engine v1.2</div>
</div>
""", unsafe_allow_html=True)

# ── MACHINE LEARNING DATA PROCESSING MATRIX MAPPINGS ────────────────────────

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

lead_map = {"Organic": 20, "Referral": 21, "Social Media": 22}
if lead_source in lead_map:
    features[lead_map[lead_source]] = 1

if payment_history == "No Payment":
    features[29] = 1

prediction = model.predict([features])[0]
probability = model.predict_proba([features])[0][1] * 100
if probability < 20:
    probability = probability * 2.5

probability = min(100.0, max(0.0, probability))

should_display = submit_clicked or 'initialized' in st.session_state
if submit_clicked:
    st.session_state['initialized'] = True

if should_display:
    
    # Map high-contrast warning elements
    if probability >= 70:
        verdict_text = "High Conversion Potential Expected"
        verdict_class = "verdict-tag-high"
        wrap_class = "wrap-high"
        verdict_label = "🔥 Priority band: High Action Target"
        recommended_action = "Route this lead directly to the premium sales development pipeline for immediate custom outreach within 15 minutes."
    elif probability >= 40:
        verdict_text = "Nurturing Action Recommended"
        verdict_class = "verdict-tag-medium"
        wrap_class = "wrap-medium"
        verdict_label = "🟡 Priority band: Medium Priority Nurture"
        recommended_action = "Trigger personalized follow-up sequences and offer targeted product resources to increase engagement loops."
    else:
        verdict_text = "Low Immediate Conversion Potential"
        verdict_class = "verdict-tag-low"
        wrap_class = "wrap-low"
        verdict_label = "⚠️ Priority band: Low Priority / Archive"
        recommended_action = "Assign to background automated marketing communication cycles to maintain low-overhead brand presence."

    # Top Informational Result Card Wrapper Block
    st.markdown(f"""
    <div class="status-card-wrap {wrap_class}">
        <div class="verdict-tag-container"><span class="{verdict_class}">{verdict_label}</span></div>
        <div class="result-header-text" style="color: {cfg_text};">{verdict_text}</div>
        <div class="result-sub-text"><b>Strategic Operation Guidance:</b> {recommended_action}</div>
    </div>
    """, unsafe_allow_html=True)

    # Contextual Micro KPI Row Content 
    total_velocity = form_submissions + downloads + followup
    st.markdown(f"""
    <div class="micro-kpi-row">
        <div class="micro-card">
            <div class="micro-label">Handling Latency Index</div>
            <div class="micro-value">{response_time} Hours</div>
        </div>
        <div class="micro-card">
            <div class="micro-label">Total Touchpoint Velocity</div>
            <div class="micro-value">{total_velocity} Actions</div>
        </div>
        <div class="micro-card">
            <div class="micro-label">Product Page CTR</div>
            <div class="micro-value">{ctr}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Core Charts Columns
    chart_col1, chart_col2 = st.columns([5, 5], gap="large")

    with chart_col1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=probability,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Calculated Lead Probability Index", 'font': {'size': 13, 'color': cfg_subtext, 'family': 'Plus Jakarta Sans'}},
            number={'suffix': "%", 'font': {'size': 36, 'color': cfg_text, 'family': 'Syne'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': cfg_subtext},
                'bar': {'color': cfg_bar_color, 'thickness': 0.25},
                'bgcolor': 'rgba(148,163,184,0.1)',
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.15)'},
                    {'range': [40, 70], 'color': 'rgba(245, 158, 11, 0.15)'},
                    {'range': [70, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
                ],
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=260,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with chart_col2:
        confidence_data = pd.DataFrame({
            'Outcome Stream': ['Non-Conversion Match', 'Conversion Match'],
            'Density Concentration (%)': [100.0 - probability, probability]
        })
        
        fig_bar = px.bar(
            confidence_data,
            x='Outcome Stream',
            y='Density Concentration (%)',
            text=confidence_data['Density Concentration (%)'].apply(lambda x: f"{x:.1f}%"),
            color='Outcome Stream',
            color_discrete_map={'Non-Conversion Match': 'rgba(148,163,184,0.2)', 'Conversion Match': '#6366F1'}
        )
        fig_bar.update_traces(textposition='outside', cliponaxis=False, width=0.4)
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            height=260,
            xaxis=dict(title=None, tickfont=dict(size=12, color=cfg_subtext)),
            yaxis=dict(title=None, range=[0, 115], showgrid=True, gridcolor=chart_theme_grid),
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Secondary Diagnostic Layout Row Containers
    st.markdown(f'<div class="dashboard-container">', unsafe_allow_html=True)
    st.markdown(f"<div class=\"sidebar-title\" style=\"font-size:18px; color:{cfg_text};\">📊 Operational Profile Diagnostic Analysis</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    infra_col1, infra_col2 = st.columns(2, gap="large")
    
    with infra_col1:
        radar_categories = ['Website Duration', 'Pages Visualized', 'Form Interactions', 'Resource Downloads', 'CTR Performance']
        current_radar_metrics = [
            (time_spent / 300) * 100,
            (pages_viewed / 50) * 100,
            (form_submissions / 20) * 100,
            (downloads / 20) * 100,
            ctr
        ]
        target_radar_benchmarks = [70, 60, 50, 45, 65]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=current_radar_metrics,
            theta=radar_categories,
            fill='toself',
            name='Configured Target Profile',
            fillcolor='rgba(99, 102, 241, 0.12)',
            line=dict(color='#6366f1', width=2)
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=target_radar_benchmarks,
            theta=radar_categories,
            fill='toself',
            name='Ideal Conversion Standard',
            fillcolor='rgba(148, 163, 184, 0.02)',
            line=dict(color=cfg_subtext, width=1, dash='dash')
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], gridcolor=chart_theme_grid, tickfont=dict(size=9, color=cfg_subtext)),
                angularaxis=dict(gridcolor=chart_theme_grid, tickfont=dict(size=11, color=cfg_subtext))
            ),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color=cfg_subtext)),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=320,
            margin=dict(l=40, r=40, t=20, b=40)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with infra_col2:
        attribute_dataframe = pd.DataFrame({
            'Configured Parameter Metrics': ['Website Duration', 'Social Touchpoints', 'Followups Shared', 'Forms Completed', 'Click-Through Rate (%)'],
            'Value Matrix Assessment': [time_spent, engagement, followup, form_submissions, ctr]
        })
        
        fig_horizontal_bar = px.bar(
            attribute_dataframe,
            x='Value Matrix Assessment',
            y='Configured Parameter Metrics',
            orientation='h',
            text_auto=True
        )
        fig_horizontal_bar.update_traces(marker_color=cfg_bar_color, width=0.45)
        fig_horizontal_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor=chart_theme_grid, title=None, tickfont=dict(color=cfg_subtext)),
            yaxis=dict(title=None, tickfont=dict(size=11, color=cfg_subtext)),
            height=320,
            margin=dict(l=10, r=10, t=20, b=10)
        )
        st.plotly_chart(fig_horizontal_bar, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div style="text-align: center; padding: 100px 0; background: {cfg_panel}; border: 1px dashed {cfg_border}; border-radius: 16px; margin-top:20px;">
        <span style="font-size: 40px;">⚡</span>
        <h3 style="font-family: 'Syne', sans-serif; font-size: 20px; color: {cfg_text}; margin: 16px 0 8px;">System Engine Awaiting Configuration</h3>
        <p style="color: {cfg_subtext}; font-size: 14px; max-width: 420px; margin: 0 auto; line-height: 1.5;">
            Adjust lead metrics using the sliders on the left control panel, then press <b>"Run Prediction Execution"</b> to compile detailed operational diagnostics.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER SYSTEM OVERLAYS ───────────────────────────────────────────────────

st.markdown("""
<div class="footer">
    Operational Engine Instance: Production Framework · Secured Enterprise Platform Stack Architecture Analytics
</div>
""", unsafe_allow_html=True)