import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

st.set_page_config(
    page_title="Condé Nast — Paid Media Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #F0F4F8; }

[data-testid="stSidebar"] {
    background-color: #1B3A5C;
    border-right: none;
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
    font-family: 'Inter', sans-serif !important;
}

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: #F0F4F8; }
::-webkit-scrollbar-thumb { background: #1B3A5C; }

.brand-header {
    background: linear-gradient(135deg, #1B3A5C 0%, #2E5F8A 100%);
    padding: 56px 48px 44px 48px;
    margin: -1rem -1rem 52px -1rem;
    animation: fadeInDown 0.8s ease forwards;
}
.brand-eyebrow {
    font-family: 'Inter', sans-serif;
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 0.35em;
    color: #A8C8E8;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.brand-name {
    font-family: 'Playfair Display', serif;
    font-size: 64px;
    font-weight: 300;
    font-style: italic;
    color: #FFFFFF;
    margin: 0;
    line-height: 1;
    letter-spacing: -0.01em;
}
.brand-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 10px;
    font-weight: 400;
    letter-spacing: 0.25em;
    color: rgba(255,255,255,0.5);
    margin-top: 14px;
    text-transform: uppercase;
}
.brand-rule {
    width: 40px;
    height: 1px;
    background: #A8C8E8;
    margin-top: 22px;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 400;
    color: #1B3A5C;
    letter-spacing: -0.01em;
    margin-bottom: 2px;
}
.section-sub {
    font-size: 9px;
    color: #2E5F8A;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-bottom: 24px;
    font-weight: 500;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #D8E8F4;
    border-top: 2px solid #1B3A5C;
    padding: 24px 20px;
    transition: all 0.3s ease;
    overflow: visible !important;
}
[data-testid="stMetric"]:hover {
    box-shadow: 0 4px 24px rgba(27,58,92,0.1);
    transform: translateY(-2px);
}
[data-testid="stMetricLabel"] {
    font-size: 9px !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #6B8FAA !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: unset !important;
    line-height: 1.4 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 28px !important;
    font-weight: 400 !important;
    color: #1B3A5C !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: unset !important;
    line-height: 1.2 !important;
}
[data-testid="stMetricDelta"] {
    overflow: visible !important;
}

.narrative-block {
    background: #FFFFFF;
    border: 1px solid #D8E8F4;
    border-left: 3px solid #1B3A5C;
    padding: 20px 24px;
    margin: 12px 0 28px 0;
    font-size: 13px;
    line-height: 1.9;
    color: #4A6A85;
}
.narrative-block strong { color: #1B3A5C; font-weight: 600; }

.insight-tag {
    display: inline-block;
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 3px 10px;
    margin-bottom: 10px;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    border: 1px solid currentColor;
}
.tag-navy { color: #1B3A5C; }
.tag-blue { color: #2E5F8A; }
.tag-grey { color: #7A98B2; }

.platform-card {
    background: #FFFFFF;
    border: 1px solid #D8E8F4;
    border-top: 2px solid #1B3A5C;
    padding: 24px 20px;
    text-align: center;
    transition: all 0.3s ease;
}
.platform-card:hover {
    box-shadow: 0 8px 32px rgba(27,58,92,0.1);
    transform: translateY(-2px);
}
.platform-name {
    font-size: 9px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #2E5F8A;
    margin-bottom: 14px;
    font-weight: 600;
}
.platform-roi {
    font-family: 'Playfair Display', serif;
    font-size: 44px;
    font-weight: 300;
    color: #1B3A5C;
    line-height: 1;
    margin-bottom: 4px;
}
.platform-roi-label {
    font-size: 9px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #A8C8E8;
    margin-bottom: 16px;
}
.platform-stats {
    font-size: 11px;
    color: #6B8FAA;
    line-height: 2;
    text-align: left;
    border-top: 1px solid #EEF4FA;
    padding-top: 12px;
    margin-top: 4px;
}
.platform-stats span {
    color: #1B3A5C;
    font-weight: 600;
    float: right;
}

.rec-card {
    background: #FFFFFF;
    border: 1px solid #D8E8F4;
    padding: 28px 24px;
    height: 100%;
    transition: all 0.3s ease;
}
.rec-card:hover {
    box-shadow: 0 8px 32px rgba(27,58,92,0.1);
    transform: translateY(-2px);
}
.rec-number {
    font-family: 'Playfair Display', serif;
    font-size: 52px;
    font-weight: 300;
    color: #1B3A5C;
    line-height: 1;
    margin-bottom: 8px;
}
.rec-card-title {
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-weight: 400;
    color: #1B3A5C;
    margin-bottom: 20px;
}
.rec-card ul {
    margin: 0;
    padding: 0;
    list-style: none;
    color: #4A6A85;
    font-size: 12px;
}
.rec-card li {
    padding: 10px 0;
    border-bottom: 1px solid #EEF4FA;
    letter-spacing: 0.01em;
    line-height: 1.5;
    transition: color 0.2s ease;
}
.rec-card li:hover { color: #1B3A5C; }
.rec-card li:last-child { border-bottom: none; }

.thin-divider {
    border: none;
    border-top: 1px solid #D8E8F4;
    margin: 44px 0;
}

@keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.stDataFrame { border: 1px solid #D8E8F4 !important; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

CN_NAVY  = "#1B3A5C"
CN_BLUE  = "#2E5F8A"
CN_LIGHT = "#A8C8E8"
CN_WHITE = "#FFFFFF"
CN_BG    = "#F0F4F8"

CHART_COLORS = [CN_NAVY, CN_BLUE, "#4A8AB5", "#7AAED0", "#A8C8E8"]

LEGEND_STYLE = dict(
    font=dict(size=11, color="#4A6A85"),
    bgcolor="rgba(255,255,255,0.95)",
    bordercolor="#D8E8F4",
    borderwidth=1
)

base = "data/processed" if os.path.exists("data/processed/kpis.json") else "."

@st.cache_data
def load_kpis():
    with open(f"{base}/kpis.json") as f: return json.load(f)

@st.cache_data
def load_platform():    return pd.read_csv(f"{base}/platform_summary.csv")

@st.cache_data
def load_monthly():     return pd.read_csv(f"{base}/monthly_trend.csv")

@st.cache_data
def load_goals():       return pd.read_csv(f"{base}/campaign_goals.csv")

@st.cache_data
def load_audience():    return pd.read_csv(f"{base}/audience_summary.csv")

@st.cache_data
def load_location():    return pd.read_csv(f"{base}/location_summary.csv")

@st.cache_data
def load_platform_trend(): return pd.read_csv(f"{base}/platform_trend.csv")

kpis           = load_kpis()
platform_df    = load_platform()
monthly_df     = load_monthly()
goals_df       = load_goals()
audience_df    = load_audience()
location_df    = load_location()
platform_trend = load_platform_trend()

platform_df["CTR"] = (platform_df["Clicks"] / platform_df["Impressions"] * 100).round(2)
audience_df["CTR"] = (audience_df["Clicks"] / audience_df["Impressions"] * 100).round(2)

# ── SIDEBAR ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='padding:28px 0 6px;font-family:Playfair Display,serif;font-size:24px;font-weight:300;font-style:italic;color:#FFFFFF;'>Condé Nast</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:rgba(168,200,232,0.7);padding-bottom:20px;font-weight:500;'>Paid Media Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(255,255,255,0.1);margin-bottom:20px;'>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:#A8C8E8;margin-bottom:4px;font-weight:600;'>Platform</p>", unsafe_allow_html=True)
    platforms = ["All"] + sorted(platform_df["Channel_Used"].unique().tolist())
    selected_platform = st.selectbox("platform", platforms, label_visibility="collapsed")

    st.markdown("<p style='font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:#A8C8E8;margin:16px 0 4px;font-weight:600;'>Campaign Goal</p>", unsafe_allow_html=True)
    goals = ["All"] + sorted(goals_df["Campaign_Goal"].unique().tolist())
    selected_goal = st.selectbox("goal", goals, label_visibility="collapsed")

    st.markdown("<p style='font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:#A8C8E8;margin:16px 0 4px;font-weight:600;'>Audience</p>", unsafe_allow_html=True)
    audiences = ["All"] + sorted(audience_df["Target_Audience"].unique().tolist())
    selected_audience = st.selectbox("audience", audiences, label_visibility="collapsed")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.1);margin:20px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <p style='font-size:9px;color:rgba(255,255,255,0.25);letter-spacing:.08em;margin-bottom:16px;'>Paid Media Analytics Portfolio<br>Built with Python and Streamlit</p>
    <div style='border-top:1px solid rgba(255,255,255,0.1);padding-top:16px;'>
        <p style='font-size:9px;color:rgba(168,200,232,0.7);letter-spacing:0.1em;margin-bottom:4px;text-transform:uppercase;font-weight:600;'>Made with love by</p>
        <p style='font-family:Playfair Display,serif;font-size:16px;font-style:italic;color:#FFFFFF;letter-spacing:0.02em;margin-bottom:8px;'>Shreeya Aggarwal</p>
        <a href='mailto:sa9172@nyu.edu' style='display:block;font-size:10px;color:rgba(255,255,255,0.35);letter-spacing:0.04em;margin-bottom:4px;text-decoration:none;'>sa9172@nyu.edu</a>
        <a href='https://aesthetic-canvas-sparkle.lovable.app' target='_blank' style='display:block;font-size:10px;color:#A8C8E8;letter-spacing:0.04em;text-decoration:none;'>Portfolio</a>
    </div>
    """, unsafe_allow_html=True)

# ── FILTERS ────────────────────────────────────────────────
plat_f = platform_df.copy()
if selected_platform != "All":
    plat_f = plat_f[plat_f["Channel_Used"] == selected_platform]

goal_f = goals_df.copy()
if selected_goal != "All":
    goal_f = goal_f[goal_f["Campaign_Goal"] == selected_goal]

aud_f = audience_df.copy()
if selected_audience != "All":
    aud_f = aud_f[aud_f["Target_Audience"] == selected_audience]

# ── HEADER ─────────────────────────────────────────────────
st.markdown("""
<div class='brand-header'>
    <div class='brand-eyebrow'>Paid Media Intelligence Dashboard</div>
    <div class='brand-name'>Condé Nast</div>
    <div class='brand-subtitle'>Multi-Platform Campaign Analytics — All Brands & Markets</div>
    <div class='brand-rule'></div>
</div>
""", unsafe_allow_html=True)

# ── EXECUTIVE SUMMARY ──────────────────────────────────────
best_platform = platform_df.loc[platform_df["Avg_ROI"].idxmax(), "Channel_Used"]
best_roi      = round(platform_df["Avg_ROI"].max(), 2)
best_goal     = goals_df.loc[goals_df["Avg_ROI"].idxmax(), "Campaign_Goal"]
total_camps   = kpis["total_campaigns"]
avg_ctr       = round(kpis["avg_ctr"], 1)

st.markdown("<div class='section-title'>Executive Summary</div><div class='section-sub'>Full portfolio — all platforms, brands and markets</div>", unsafe_allow_html=True)
st.markdown(f"""
<div class='narrative-block'>
    Across <strong>{total_camps:,} campaigns</strong>, the portfolio delivers an average ROI of <strong>{kpis['avg_roi']}x</strong>
    with a click-through rate of <strong>{avg_ctr}%</strong> and an average conversion rate of <strong>{round(kpis['avg_conversion']*100,1)}%</strong>.
    <strong>{best_platform}</strong> is the highest-performing platform at <strong>{best_roi}x ROI</strong>.
    <strong>{best_goal}</strong> campaigns deliver the strongest returns by objective.
    Pinterest significantly underperforms the portfolio average — immediate review of spend allocation is recommended.
</div>
""", unsafe_allow_html=True)

# ── KPIs ───────────────────────────────────────────────────
st.markdown("<div class='section-title'>Key Performance Indicators</div><div class='section-sub'>Full portfolio metrics</div>", unsafe_allow_html=True)
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Campaigns",   f"{kpis['total_campaigns']:,}")
k2.metric("Total Impressions", f"{int(kpis['total_impressions']):,}")
k3.metric("Total Clicks",      f"{int(kpis['total_clicks']):,}")
k4.metric("Average ROI",       f"{kpis['avg_roi']}x")
k5.metric("Average CTR",       f"{avg_ctr}%")
k6.metric("Avg Conversion",    f"{round(kpis['avg_conversion']*100,1)}%")

st.markdown("<hr class='thin-divider'>", unsafe_allow_html=True)

# ── PLATFORM CARDS ─────────────────────────────────────────
st.markdown("<div class='section-title'>Platform Performance</div><div class='section-sub'>ROI, CTR and conversion rate by channel</div>", unsafe_allow_html=True)

p_cols = st.columns(len(platform_df))
for col, (_, row) in zip(p_cols, platform_df.sort_values("Avg_ROI", ascending=False).iterrows()):
    ctr = round(row["Clicks"] / row["Impressions"] * 100, 1)
    col.markdown(f"""
    <div class='platform-card'>
        <div class='platform-name'>{row['Channel_Used']}</div>
        <div class='platform-roi'>{round(row['Avg_ROI'], 2)}x</div>
        <div class='platform-roi-label'>Average ROI</div>
        <div class='platform-stats'>
            CTR <span>{ctr}%</span><br>
            Conv Rate <span>{round(row['Avg_Conv']*100,1)}%</span><br>
            Engagement <span>{round(row['Avg_Engagement'],1)}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div class='narrative-block'>
    <span class='insight-tag tag-navy'>Platform Insight</span><br>
    <strong>{best_platform}</strong> leads the portfolio at <strong>{best_roi}x ROI</strong>.
    Pinterest at <strong>0.72x ROI</strong> significantly underperforms all other channels — budget reallocation toward Instagram, Twitter and Facebook is the immediate priority.
    All three top platforms deliver near-identical conversion rates (~8%), indicating the creative performs consistently — platform reach and engagement are the key differentiators.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='thin-divider'>", unsafe_allow_html=True)

# ── PLATFORM TREND ─────────────────────────────────────────
st.markdown("<div class='section-title'>ROI Trend by Platform</div><div class='section-sub'>Monthly performance across all channels</div>", unsafe_allow_html=True)

fig_trend = px.line(platform_trend, x="Month", y="Avg_ROI",
                    color="Channel_Used",
                    markers=True,
                    color_discrete_sequence=CHART_COLORS,
                    labels={"Avg_ROI": "Average ROI (x)", "Month": "", "Channel_Used": "Platform"})
fig_trend.update_traces(line=dict(width=2), marker=dict(size=5))
fig_trend.update_layout(
    paper_bgcolor=CN_WHITE,
    plot_bgcolor=CN_WHITE,
    font=dict(family="Inter", color="#4A6A85", size=11),
    title=dict(text="Average ROI by Platform — Monthly",
               font=dict(family="Playfair Display", size=17, color=CN_NAVY)),
    legend=dict(**LEGEND_STYLE, title="Platform"),
    xaxis=dict(tickangle=-45, gridcolor="#EEF4FA", color="#6B8FAA", title=""),
    yaxis=dict(gridcolor="#EEF4FA", color="#6B8FAA", title="Average ROI (x)"),
    margin=dict(t=50, b=60, l=20, r=20)
)
st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("<hr class='thin-divider'>", unsafe_allow_html=True)

# ── CAMPAIGN GOALS ─────────────────────────────────────────
st.markdown("<div class='section-title'>Campaign Goal Analysis</div><div class='section-sub'>Performance breakdown by campaign objective</div>", unsafe_allow_html=True)

ga, gb = st.columns(2)
with ga:
    fig_g1 = px.bar(goal_f.sort_values("Avg_ROI", ascending=True),
                    x="Avg_ROI", y="Campaign_Goal", orientation="h",
                    title="Average ROI by Campaign Goal",
                    color="Campaign_Goal",
                    color_discrete_sequence=CHART_COLORS,
                    labels={"Avg_ROI": "Average ROI (x)", "Campaign_Goal": ""})
    fig_g1.update_layout(
        paper_bgcolor=CN_WHITE, plot_bgcolor=CN_WHITE,
        font=dict(family="Inter", color="#4A6A85", size=11),
        title=dict(font=dict(family="Playfair Display", size=17, color=CN_NAVY)),
        showlegend=False,
        xaxis=dict(title="Average ROI (x)", gridcolor="#EEF4FA", color="#6B8FAA"),
        yaxis=dict(title="", color="#6B8FAA"),
        margin=dict(t=50, b=30, l=20, r=20)
    )
    st.plotly_chart(fig_g1, use_container_width=True)

with gb:
    fig_g2 = px.bar(goal_f.sort_values("Avg_Engagement", ascending=True),
                    x="Avg_Engagement", y="Campaign_Goal", orientation="h",
                    title="Average Engagement Score by Goal",
                    color="Campaign_Goal",
                    color_discrete_sequence=CHART_COLORS,
                    labels={"Avg_Engagement": "Avg Engagement Score", "Campaign_Goal": ""})
    fig_g2.update_layout(
        paper_bgcolor=CN_WHITE, plot_bgcolor=CN_WHITE,
        font=dict(family="Inter", color="#4A6A85", size=11),
        title=dict(font=dict(family="Playfair Display", size=17, color=CN_NAVY)),
        showlegend=False,
        xaxis=dict(title="Average Engagement Score", gridcolor="#EEF4FA", color="#6B8FAA"),
        yaxis=dict(title="", color="#6B8FAA"),
        margin=dict(t=50, b=30, l=20, r=20)
    )
    st.plotly_chart(fig_g2, use_container_width=True)

st.markdown("<hr class='thin-divider'>", unsafe_allow_html=True)

# ── AUDIENCE PERFORMANCE ───────────────────────────────────
st.markdown("<div class='section-title'>Audience Segment Performance</div><div class='section-sub'>ROI and conversion rate by target demographic</div>", unsafe_allow_html=True)

aa, ab = st.columns(2)
with aa:
    fig_a1 = px.bar(aud_f.sort_values("Avg_ROI", ascending=True),
                    x="Avg_ROI", y="Target_Audience", orientation="h",
                    title="ROI by Audience Segment",
                    color="Avg_ROI",
                    color_continuous_scale=["#D8E8F4", "#2E5F8A", CN_NAVY],
                    labels={"Avg_ROI": "Average ROI (x)", "Target_Audience": ""})
    fig_a1.update_layout(
        paper_bgcolor=CN_WHITE, plot_bgcolor=CN_WHITE,
        font=dict(family="Inter", color="#4A6A85", size=11),
        title=dict(font=dict(family="Playfair Display", size=17, color=CN_NAVY)),
        coloraxis_showscale=False,
        xaxis=dict(title="Average ROI (x)", gridcolor="#EEF4FA", color="#6B8FAA"),
        yaxis=dict(title="", color="#6B8FAA"),
        margin=dict(t=50, b=30, l=20, r=20)
    )
    st.plotly_chart(fig_a1, use_container_width=True)

with ab:
    fig_a2 = px.bar(aud_f.sort_values("Avg_Conv", ascending=True),
                    x="Avg_Conv", y="Target_Audience", orientation="h",
                    title="Conversion Rate by Audience Segment",
                    color="Avg_Conv",
                    color_continuous_scale=["#D8E8F4", "#2E5F8A", CN_NAVY],
                    labels={"Avg_Conv": "Conversion Rate", "Target_Audience": ""})
    fig_a2.update_layout(
        paper_bgcolor=CN_WHITE, plot_bgcolor=CN_WHITE,
        font=dict(family="Inter", color="#4A6A85", size=11),
        title=dict(font=dict(family="Playfair Display", size=17, color=CN_NAVY)),
        coloraxis_showscale=False,
        xaxis=dict(title="Conversion Rate", gridcolor="#EEF4FA", color="#6B8FAA"),
        yaxis=dict(title="", color="#6B8FAA"),
        margin=dict(t=50, b=30, l=20, r=20)
    )
    st.plotly_chart(fig_a2, use_container_width=True)

st.markdown(f"""
<div class='narrative-block'>
    <span class='insight-tag tag-blue'>Audience Insight</span><br>
    Conversion rates are remarkably consistent across all demographic segments at approximately <strong>8%</strong> — indicating the creative and offer resonate broadly.
    ROI variation across segments is the primary lever for optimisation. Focus incremental budget on the highest-ROI segments while maintaining baseline spend across others.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='thin-divider'>", unsafe_allow_html=True)

# ── MONTHLY TREND ──────────────────────────────────────────
st.markdown("<div class='section-title'>Monthly Performance Trend</div><div class='section-sub'>ROI and conversion rate over time — full portfolio</div>", unsafe_allow_html=True)

ma, mb = st.columns(2)
with ma:
    fig_m1 = px.line(monthly_df, x="Month", y="Avg_ROI",
                     title="Average ROI — Monthly Trend",
                     markers=True,
                     color_discrete_sequence=[CN_NAVY],
                     labels={"Avg_ROI": "Average ROI (x)", "Month": ""})
    fig_m1.update_traces(line=dict(width=2.5), marker=dict(size=6, color=CN_BLUE))
    fig_m1.update_layout(
        paper_bgcolor=CN_WHITE, plot_bgcolor=CN_WHITE,
        font=dict(family="Inter", color="#4A6A85", size=11),
        title=dict(font=dict(family="Playfair Display", size=17, color=CN_NAVY)),
        xaxis=dict(tickangle=-45, gridcolor="#EEF4FA", color="#6B8FAA", title=""),
        yaxis=dict(gridcolor="#EEF4FA", color="#6B8FAA", title="Average ROI (x)"),
        margin=dict(t=50, b=60, l=20, r=20)
    )
    st.plotly_chart(fig_m1, use_container_width=True)

with mb:
    fig_m2 = px.line(monthly_df, x="Month", y="Avg_Conv",
                     title="Average Conversion Rate — Monthly Trend",
                     markers=True,
                     color_discrete_sequence=[CN_BLUE],
                     labels={"Avg_Conv": "Conversion Rate", "Month": ""})
    fig_m2.update_traces(line=dict(width=2.5), marker=dict(size=6, color=CN_LIGHT))
    fig_m2.update_layout(
        paper_bgcolor=CN_WHITE, plot_bgcolor=CN_WHITE,
        font=dict(family="Inter", color="#4A6A85", size=11),
        title=dict(font=dict(family="Playfair Display", size=17, color=CN_NAVY)),
        xaxis=dict(tickangle=-45, gridcolor="#EEF4FA", color="#6B8FAA", title=""),
        yaxis=dict(gridcolor="#EEF4FA", color="#6B8FAA", title="Conversion Rate"),
        margin=dict(t=50, b=60, l=20, r=20)
    )
    st.plotly_chart(fig_m2, use_container_width=True)

st.markdown("<hr class='thin-divider'>", unsafe_allow_html=True)

# ── REGIONAL PERFORMANCE ───────────────────────────────────
st.markdown("<div class='section-title'>Regional Performance</div><div class='section-sub'>ROI and reach by market location</div>", unsafe_allow_html=True)

ra, rb = st.columns(2)
with ra:
    top_loc = location_df.sort_values("Avg_ROI", ascending=False).head(15)
    fig_r1 = px.bar(top_loc.sort_values("Avg_ROI", ascending=True),
                    x="Avg_ROI", y="Location", orientation="h",
                    title="Top 15 Markets by ROI",
                    color="Avg_ROI",
                    color_continuous_scale=["#D8E8F4", "#2E5F8A", CN_NAVY],
                    labels={"Avg_ROI": "Average ROI (x)", "Location": ""})
    fig_r1.update_layout(
        paper_bgcolor=CN_WHITE, plot_bgcolor=CN_WHITE,
        font=dict(family="Inter", color="#4A6A85", size=11),
        title=dict(font=dict(family="Playfair Display", size=17, color=CN_NAVY)),
        coloraxis_showscale=False,
        xaxis=dict(title="Average ROI (x)", gridcolor="#EEF4FA", color="#6B8FAA"),
        yaxis=dict(title="", color="#6B8FAA"),
        margin=dict(t=50, b=30, l=20, r=20)
    )
    st.plotly_chart(fig_r1, use_container_width=True)

with rb:
    fig_r2 = px.scatter(location_df,
                        x="Avg_Conv", y="Avg_ROI",
                        size="Impressions",
                        text="Location",
                        title="Conversion Rate vs ROI by Market",
                        color="Avg_ROI",
                        color_continuous_scale=["#D8E8F4", "#2E5F8A", CN_NAVY],
                        labels={"Avg_Conv": "Conversion Rate",
                                "Avg_ROI": "Average ROI (x)",
                                "Location": ""})
    fig_r2.update_traces(textposition="top center",
                         textfont=dict(size=8, color="#4A6A85"))
    fig_r2.update_layout(
        paper_bgcolor=CN_WHITE, plot_bgcolor=CN_WHITE,
        font=dict(family="Inter", color="#4A6A85", size=11),
        title=dict(font=dict(family="Playfair Display", size=17, color=CN_NAVY)),
        coloraxis_showscale=False,
        xaxis=dict(title="Conversion Rate", gridcolor="#EEF4FA", color="#6B8FAA"),
        yaxis=dict(title="Average ROI (x)", gridcolor="#EEF4FA", color="#6B8FAA"),
        margin=dict(t=50, b=30, l=20, r=20)
    )
    st.plotly_chart(fig_r2, use_container_width=True)

st.markdown("<hr class='thin-divider'>", unsafe_allow_html=True)

# ── RECOMMENDATIONS ────────────────────────────────────────
st.markdown("<div class='section-title'>Strategic Recommendations</div><div class='section-sub'>Three priority actions for the paid media team</div>", unsafe_allow_html=True)

r1, r2, r3 = st.columns(3)
with r1:
    st.markdown(f"""
    <div class='rec-card'>
        <div class='rec-number'>01</div>
        <div class='insight-tag tag-navy'>Spend Optimisation</div>
        <div class='rec-card-title'>Reallocate Away from Pinterest</div>
        <ul>
            <li>Pinterest ROI of 0.72x vs portfolio average of {kpis['avg_roi']}x — immediate review required</li>
            <li>Shift Pinterest budget toward Instagram and Twitter which deliver 4x+ ROI</li>
            <li>Set platform ROAS floor thresholds — pause campaigns below minimum</li>
            <li>Run weekly spend vs performance reviews across all channels</li>
            <li>Build automated reallocation triggers based on 7-day rolling ROI</li>
        </ul>
    </div>""", unsafe_allow_html=True)

with r2:
    st.markdown(f"""
    <div class='rec-card'>
        <div class='rec-number'>02</div>
        <div class='insight-tag tag-blue'>Audience Strategy</div>
        <div class='rec-card-title'>Double Down on Top Segments</div>
        <ul>
            <li>Scale budget toward the 3 highest ROI audience segments immediately</li>
            <li>Conversion rates are consistent at ~8% — ROI variance is the key differentiator</li>
            <li>Build lookalike audiences from top-converting demographic profiles</li>
            <li>Implement frequency caps on lower-ROI segments to reduce waste</li>
            <li>A/B test creative formats across highest-performing demographics</li>
        </ul>
    </div>""", unsafe_allow_html=True)

with r3:
    st.markdown(f"""
    <div class='rec-card'>
        <div class='rec-number'>03</div>
        <div class='insight-tag tag-grey'>Reporting Excellence</div>
        <div class='rec-card-title'>Standardise Measurement</div>
        <ul>
            <li>Define unified KPI benchmarks across all platforms and brand partners</li>
            <li>Build automated weekly performance reports for internal stakeholders</li>
            <li>Establish data discrepancy detection protocol across platform sources</li>
            <li>Produce monthly trend analysis to support repeat revenue planning</li>
            <li>Create executive summary template for quarterly business reviews</li>
        </ul>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;font-size:10px;color:#A8C8E8;letter-spacing:0.15em;padding:24px 0;border-top:1px solid #D8E8F4;text-transform:uppercase;font-family:Inter,sans-serif;'>Condé Nast &nbsp;·&nbsp; Paid Media Intelligence &nbsp;·&nbsp; Python · Streamlit · Plotly</p>", unsafe_allow_html=True)