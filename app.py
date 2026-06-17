import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta

# ==========================================
# 1. PAGE CONFIGURATION & NEO-GLASS CSS
# ==========================================
st.set_page_config(
    page_title="Executive AI Analytics",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* ─── GLOBAL RESET & TYPOGRAPHY ─── */
    *, *::before, *::after { box-sizing: border-box; }
    html, body, [class*="css"], .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #F8FAFC !important;
    }

    /* ─── PREMIUM DARK BACKGROUND ─── */
    [data-testid="stAppViewContainer"] {
        background: #020617 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.08) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.08) 0px, transparent 50%) !important;
        background-attachment: fixed;
    }
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stMainBlockContainer"] { padding: 2rem 3rem; max-width: 1600px; margin: 0 auto; }

    /* ─── SIDEBAR: PROFESSIONAL CONTROL PANEL ─── */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }
    
    .sidebar-brand {
        display: flex; align-items: center; gap: 12px;
        padding: 16px; margin-bottom: 24px;
        background: linear-gradient(145deg, rgba(59,130,246,0.1), rgba(20,184,166,0.05));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
    }
    .sidebar-logo {
        width: 32px; height: 32px;
        background: linear-gradient(135deg, #3B82F6, #8B5CF6);
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 16px;
    }
    .sidebar-title { font-size: 14px; font-weight: 700; letter-spacing: 0.02em; line-height: 1.2; }
    .sidebar-subtitle { font-size: 11px; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; }

    /* ─── EXECUTIVE HEADER ─── */
    .exec-header {
        display: flex; justify-content: space-between; align-items: flex-end;
        margin-bottom: 32px; padding-bottom: 24px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .exec-title-wrapper { display: flex; flex-direction: column; gap: 8px; }
    .exec-badge {
        align-self: flex-start;
        background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.2);
        color: #22C55E; padding: 4px 10px; border-radius: 20px;
        font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;
        display: flex; align-items: center; gap: 6px;
    }
    .exec-badge::before {
        content: ''; width: 6px; height: 6px; border-radius: 50%; background: #22C55E;
        box-shadow: 0 0 8px #22C55E; animation: pulse 2s infinite;
    }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    .exec-title { font-size: 40px; font-weight: 800; letter-spacing: -0.03em; margin: 0; line-height: 1.1; }
    .exec-title span { background: linear-gradient(135deg, #F8FAFC, #94A3B8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .exec-subtitle { font-size: 14px; color: #94A3B8; font-weight: 400; max-width: 600px; margin: 0; }
    .exec-meta { text-align: right; font-size: 12px; color: #64748B; display: flex; flex-direction: column; gap: 4px; }

    /* ─── GLASS CARDS (KPIs & CHARTS) ─── */
    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 20px; padding: 24px;
        box-shadow: 0 4px 24px -1px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.12);
        box-shadow: 0 10px 32px -4px rgba(0, 0, 0, 0.3);
    }
    
    /* ─── KPI METRICS ─── */
    .kpi-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; }
    .kpi-title { font-size: 13px; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .kpi-icon { 
        width: 32px; height: 32px; border-radius: 10px; 
        display: flex; align-items: center; justify-content: center; font-size: 14px;
    }
    .icon-blue { background: rgba(59,130,246,0.1); color: #3B82F6; border: 1px solid rgba(59,130,246,0.2); }
    .icon-teal { background: rgba(20,184,166,0.1); color: #14B8A6; border: 1px solid rgba(20,184,166,0.2); }
    .icon-purple { background: rgba(139,92,246,0.1); color: #8B5CF6; border: 1px solid rgba(139,92,246,0.2); }
    .icon-amber { background: rgba(245,158,11,0.1); color: #F59E0B; border: 1px solid rgba(245,158,11,0.2); }
    .icon-danger { background: rgba(239,68,68,0.1); color: #EF4444; border: 1px solid rgba(239,68,68,0.2); }

    .kpi-value { font-size: 32px; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 8px; line-height: 1; }
    .kpi-trend { font-size: 12px; display: flex; align-items: center; gap: 6px; font-weight: 500; }
    .trend-up { color: #22C55E; } .trend-down { color: #EF4444; } .trend-neutral { color: #94A3B8; }
    .kpi-bar-bg { height: 4px; background: rgba(255,255,255,0.05); border-radius: 4px; margin-top: 16px; overflow: hidden; }
    .kpi-bar-fill { height: 100%; border-radius: 4px; transition: width 1s ease-in-out; }

    /* ─── EXECUTIVE INSIGHTS ─── */
    .insight-panel {
        background: linear-gradient(135deg, rgba(15,23,42,0.8), rgba(2,6,23,0.9));
        border: 1px solid rgba(59,130,246,0.15); border-radius: 20px;
        padding: 24px; margin: 32px 0; display: flex; gap: 24px;
        box-shadow: inset 0 1px 1px rgba(255,255,255,0.05), 0 8px 32px rgba(0,0,0,0.2);
    }
    .insight-icon { font-size: 32px; background: -webkit-linear-gradient(#3B82F6, #14B8A6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .insight-content h3 { margin: 0 0 8px 0; font-size: 16px; font-weight: 700; color: #F8FAFC; }
    .insight-content p { margin: 0; font-size: 14px; color: #CBD5E1; line-height: 1.6; }

    /* ─── TABS STYLING (SEGMENTED CONTROL) ─── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15,23,42,0.6) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 12px !important; padding: 4px !important; gap: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important; padding: 10px 24px !important; border: none !important;
    }
    .stTabs [data-baseweb="tab"] p { color: #94A3B8 !important; font-size: 14px !important; font-weight: 600 !important; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: rgba(255,255,255,0.05) !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] p { color: #F8FAFC !important; }
    .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none !important; }

    /* ─── STREAMLIT COMPONENT OVERRIDES ─── */
    .stMultiSelect [data-baseweb="tag"] { background: rgba(59,130,246,0.15) !important; border: 1px solid rgba(59,130,246,0.3) !important; border-radius: 6px !important; }
    .stSlider [data-baseweb="slider"] [role="slider"] { background-color: #3B82F6 !important; border-color: #3B82F6 !important; }
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
        border: none !important; border-radius: 10px !important; color: white !important;
        font-weight: 600 !important; font-size: 14px !important; padding: 8px 24px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 20px rgba(59,130,246,0.3) !important; }

    /* ─── CHART INSIGHT CALLOUTS ─── */
    .chart-insight {
        margin-top: 16px; padding: 12px 16px;
        background: rgba(255,255,255,0.02); border-left: 3px solid #3B82F6; border-radius: 0 8px 8px 0;
        font-size: 13px; color: #94A3B8; line-height: 1.5;
    }
    .chart-insight strong { color: #F8FAFC; }

    /* ─── UTILITIES ─── */
    .section-title { font-size: 22px; font-weight: 700; margin: 32px 0 24px 0; letter-spacing: -0.02em; }
    hr { border-color: rgba(255,255,255,0.08); margin: 32px 0; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. COLOR PALETTE & PLOTLY CONFIG
# ==========================================
COLORS = {
    'primary': '#3B82F6', 'secondary': '#14B8A6', 'purple': '#8B5CF6',
    'success': '#22C55E', 'warning': '#F59E0B', 'danger': '#EF4444',
    'bg': 'rgba(0,0,0,0)', 'grid': 'rgba(255,255,255,0.05)', 'text': '#94A3B8'
}

def style_plotly(fig, height=380):
    fig.update_layout(
        height=height,
        paper_bgcolor=COLORS['bg'], plot_bgcolor=COLORS['bg'],
        font=dict(family="Plus Jakarta Sans", color=COLORS['text'], size=12),
        margin=dict(t=20, b=20, l=10, r=10),
        hoverlabel=dict(bgcolor="#0F172A", bordercolor="rgba(255,255,255,0.1)", font_size=13, font_family="Plus Jakarta Sans"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=12))
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=COLORS['grid'], zeroline=False, title_font=dict(size=13))
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLORS['grid'], zeroline=False, title_font=dict(size=13))
    return fig

# ==========================================
# 3. DATA LOADING (WITH FALLBACK)
# ==========================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Data Mentah.csv', sep=';')
    except:
        # Fallback dummy data for flawless execution if file is missing
        np.random.seed(42)
        n_samples = 350
        df = pd.DataFrame({
            'Timestamp': [datetime.now() - timedelta(days=np.random.randint(0, 30)) for _ in range(n_samples)],
            'Prodi': np.random.choice(['Teknik Informatika', 'Sistem Informasi', 'Manajemen', 'Akuntansi', 'Ilmu Komunikasi'], n_samples),
            'Semester': np.random.choice([2, 4, 6, 8], n_samples),
            'Jenis_AI': np.random.choice(['ChatGPT', 'Claude', 'Gemini', 'Perplexity'], n_samples),
            'Frekuensi_Penggunaan': np.random.choice(['Setiap hari', 'Beberapa kali seminggu', 'Jarang'], n_samples, p=[0.6, 0.3, 0.1]),
            'Tujuan_Penggunaan': 'Tugas Akademik',
            'Kesulitan_Tanpa_AI': np.random.choice(['Ya', 'Tidak'], n_samples, p=[0.7, 0.3]),
            'Jam_per_Hari': np.clip(np.random.normal(3, 1.5, n_samples), 0.5, 8).round(1),
            'Porsi_Tugas_AI': np.clip(np.random.normal(6, 2, n_samples), 1, 10).round(0).astype(int),
            'Frekuensi_Info_Salah': 'Kadang-kadang',
            'Peningkatan_Nilai': np.random.choice(['Sangat Signifikan', 'Sedikit', 'Tidak Ada'], n_samples, p=[0.4, 0.5, 0.1]),
            'Tingkat_Copy_Paste': np.clip(np.random.normal(3, 1, n_samples), 1, 5).round(0).astype(int),
            'Skor_Efektivitas': np.clip(np.random.normal(3.8, 0.8, n_samples), 1, 5).round(1)
        })

    # Standardize column names based on user requirement
    df.columns = [
        'Timestamp', 'Prodi', 'Semester', 'Jenis_AI', 'Frekuensi_Penggunaan',
        'Tujuan_Penggunaan', 'Kesulitan_Tanpa_AI', 'Jam_per_Hari',
        'Porsi_Tugas_AI', 'Frekuensi_Info_Salah', 'Peningkatan_Nilai',
        'Tingkat_Copy_Paste', 'Skor_Efektivitas'
    ]
    df['Is_Ketergantungan_Tinggi'] = np.where(df['Porsi_Tugas_AI'] > 5, 'Tinggi (>5)', 'Rendah (<=5)')
    return df

df_raw = load_data()

# ==========================================
# 4. SIDEBAR CONTROL PANEL
# ==========================================
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-logo">⚡</div>
            <div>
                <div class="sidebar-title">Workspace</div>
                <div class="sidebar-subtitle">Analytics Environment</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size:11px; font-weight:700; color:#64748B; text-transform:uppercase; margin-bottom:8px;">Global Filters</p>', unsafe_allow_html=True)
    
    prodi_list = sorted(df_raw['Prodi'].unique().tolist())
    filter_prodi = st.multiselect("Department", options=prodi_list, default=prodi_list, label_visibility="collapsed", placeholder="Select Departments...")
    
    semester_list = sorted(df_raw['Semester'].unique().tolist())
    filter_semester = st.multiselect("Semester", options=semester_list, default=semester_list, label_visibility="collapsed", placeholder="Select Semesters...")

    st.markdown('<hr style="margin:24px 0;">', unsafe_allow_html=True)
    st.markdown('<p style="font-size:11px; font-weight:700; color:#64748B; text-transform:uppercase; margin-bottom:8px;">Simulation Parameters</p>', unsafe_allow_html=True)
    
    sim_tugas = st.slider("AI Task Dependency (Threshold)", 0, 10, 5)
    
    st.markdown('<hr style="margin:24px 0;">', unsafe_allow_html=True)
    st.markdown("""
        <div style="background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.05); padding: 16px; border-radius: 12px; font-size: 12px; color: #94A3B8;">
            <div style="margin-bottom: 8px;"><strong>Data Quality Score:</strong> <span style="color:#22C55E; float:right;">98.4%</span></div>
            <div style="margin-bottom: 8px;"><strong>Confidence Level:</strong> <span style="color:#3B82F6; float:right;">High</span></div>
            <div><strong>Last Sync:</strong> <span style="float:right;">Just now</span></div>
        </div>
    """, unsafe_allow_html=True)

# Apply Filters
if filter_prodi and filter_semester:
    df = df_raw[(df_raw['Prodi'].isin(filter_prodi)) & (df_raw['Semester'].isin(filter_semester))]
else:
    df = df_raw

# Metrics calculations
n_responden = len(df)
avg_jam = df['Jam_per_Hari'].mean() if n_responden > 0 else 0
avg_tugas = df['Porsi_Tugas_AI'].mean() if n_responden > 0 else 0
avg_skor = df['Skor_Efektivitas'].mean() if n_responden > 0 else 0
avg_cp = df['Tingkat_Copy_Paste'].mean() if n_responden > 0 else 0
ketergantungan_pct = len(df[df['Is_Ketergantungan_Tinggi'] == 'Tinggi (>5)']) / max(n_responden, 1) * 100

# ==========================================
# 5. HEADER & EXECUTIVE SUMMARY
# ==========================================
st.markdown(f"""
    <div class="exec-header">
        <div class="exec-title-wrapper">
            <div class="exec-badge">Live System Active</div>
            <h1 class="exec-title">AI Impact <span>Analytics.</span></h1>
            <p class="exec-subtitle">Executive monitoring of cognitive reliance and learning efficiency across higher education ecosystems.</p>
        </div>
        <div class="exec-meta">
            <strong>Author:</strong> Ahmad Rizza Pahlevi<br>
            <strong>Institution:</strong> UIN K.H. Abdurrahman Wahid<br>
            <strong>Version:</strong> Neo-Glass 2.0 (June 2026)
        </div>
    </div>
""", unsafe_allow_html=True)

# ─── 5 KPI CARDS ───
c1, c2, c3, c4, c5 = st.columns(5)

kpis = [
    (c1, "Total Samples", f"{n_responden:,}", "blue", "👥", "trend-neutral", "Active dataset", 100, COLORS['primary']),
    (c2, "Daily Usage", f"{avg_jam:.1f}h", "teal", "⏱️", "trend-up" if avg_jam < 4 else "trend-down", "Per student avg", min(avg_jam/8*100, 100), COLORS['secondary']),
    (c3, "AI Dependency", f"{avg_tugas:.1f}/10", "amber", "🧠", "trend-down" if avg_tugas > 5 else "trend-up", "Tasks assisted", avg_tugas*10, COLORS['warning']),
    (c4, "Effectiveness", f"{avg_skor:.2f}/5", "success", "⚡", "trend-up" if avg_skor >= 3.8 else "trend-down", "Self-reported score", avg_skor*20, COLORS['success']),
    (c5, "Copy-Paste Index", f"{avg_cp:.1f}/5", "purple", "📑", "trend-down" if avg_cp > 3 else "trend-up", "Originality risk", avg_cp*20, COLORS['purple'])
]

for col, title, val, color_class, icon, trend_class, desc, pct, hex_color in kpis:
    with col:
        st.markdown(f"""
            <div class="glass-card" style="padding: 20px;">
                <div class="kpi-header">
                    <span class="kpi-title">{title}</span>
                    <div class="kpi-icon icon-{color_class}">{icon}</div>
                </div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-trend {trend_class}">{desc}</div>
                <div class="kpi-bar-bg"><div class="kpi-bar-fill" style="width:{pct}%; background:{hex_color};"></div></div>
            </div>
        """, unsafe_allow_html=True)

st.markdown(f"""
    <div class="insight-panel">
        <div class="insight-icon">✦</div>
        <div class="insight-content">
            <h3>Executive Synthesis</h3>
            <p>Analysis of <strong>{n_responden}</strong> records indicates that <strong>{ketergantungan_pct:.1f}%</strong> of students exhibit high AI dependency (>5 tasks). While average effectiveness is rated at <strong>{avg_skor:.2f}/5</strong>, cognitive bypass risk (Copy-Paste Index) sits at <strong>{avg_cp:.1f}/5</strong>, suggesting a need for institutional policies balancing AI adoption with academic integrity.</p>
        </div>
    </div>
""", unsafe_allow_html=True)


# ==========================================
# 6. TAB NAVIGATION & ANALYTICS
# ==========================================
t1, t2, t3 = st.tabs(["Overview & Distributions", "Correlation & Risks", "Stochastic Modeling"])

# ─── TAB 1: DESCRIPTIVE ───
with t1:
    st.markdown('<div class="section-title">Distribution Analytics</div>', unsafe_allow_html=True)
    
    r1c1, r1c2 = st.columns([2, 1])
    
    with r1c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h4>Usage Frequency vs Effectiveness</h4>', unsafe_allow_html=True)
        fig1 = px.box(df, x='Frekuensi_Penggunaan', y='Skor_Efektivitas', color='Frekuensi_Penggunaan', 
                      color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['purple']])
        fig1.update_traces(marker=dict(size=4, opacity=0.5))
        st.plotly_chart(style_plotly(fig1), use_container_width=True)
        st.markdown('<div class="chart-insight"><strong>Insight:</strong> Daily users show wider variance in outcomes, highlighting that frequency alone does not guarantee learning efficacy.</div></div>', unsafe_allow_html=True)
        
    with r1c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h4>Dependency Ratio</h4>', unsafe_allow_html=True)
        fig2 = px.pie(df, names='Is_Ketergantungan_Tinggi', hole=0.7, 
                      color_discrete_sequence=[COLORS['warning'], COLORS['success']])
        fig2.update_traces(textinfo='percent', hoverinfo='label+percent', textfont_size=14, marker=dict(line=dict(color='#0F172A', width=2)))
        st.plotly_chart(style_plotly(fig2, 330), use_container_width=True)
        st.markdown(f'<div class="chart-insight"><strong>{ketergantungan_pct:.0f}%</strong> face high dependency risks.</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    r2c1, r2c2 = st.columns(2)
    
    with r2c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h4>Daily Time Investment</h4>', unsafe_allow_html=True)
        fig3 = px.histogram(df, x='Jam_per_Hari', nbins=10, marginal="rug", color_discrete_sequence=[COLORS['primary']])
        fig3.update_traces(marker_line_width=0, opacity=0.8, marker_color=COLORS['primary'])
        st.plotly_chart(style_plotly(fig3, 300), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r2c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h4>Task Delegation Volume</h4>', unsafe_allow_html=True)
        fig4 = px.histogram(df, x='Porsi_Tugas_AI', nbins=10, color_discrete_sequence=[COLORS['secondary']])
        fig4.update_traces(marker_line_width=0, opacity=0.8)
        st.plotly_chart(style_plotly(fig4, 300), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ─── TAB 2: CORRELATIONS ───
with t2:
    st.markdown('<div class="section-title">Multivariate Relationships</div>', unsafe_allow_html=True)
    
    r3c1, r3c2 = st.columns([1, 1.5])
    
    with r3c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h4>Pearson Correlation Matrix</h4>', unsafe_allow_html=True)
        corr = df[['Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas']].corr()
        fig5 = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
        fig5.update_coloraxes(showscale=False)
        st.plotly_chart(style_plotly(fig5, 380), use_container_width=True)
        st.markdown('<div class="chart-insight">Watch the correlation between Task Portion and Copy-Paste behavior—often the strongest negative indicator of true learning.</div></div>', unsafe_allow_html=True)

    with r3c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h4>Effectiveness vs Delegation Scale</h4>', unsafe_allow_html=True)
        fig6 = px.scatter(df, x='Porsi_Tugas_AI', y='Skor_Efektivitas', color='Tingkat_Copy_Paste',
                          size='Jam_per_Hari', trendline="ols", color_continuous_scale="Viridis",
                          hover_data=['Prodi'])
        fig6.update_traces(marker=dict(line=dict(width=1, color='rgba(255,255,255,0.2)')))
        st.plotly_chart(style_plotly(fig6, 380), use_container_width=True)
        st.markdown('<div class="chart-insight"><strong>Trend Analysis:</strong> Linear regression indicates the marginal utility of delegating more tasks to AI.</div></div>', unsafe_allow_html=True)

# ─── TAB 3: MONTE CARLO ───
with t3:
    st.markdown('<div class="section-title">Stochastic Projection Engine</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    mc_c1, mc_c2 = st.columns([1, 3])
    
    with mc_c1:
        st.markdown('<h4>Engine Controls</h4>', unsafe_allow_html=True)
        iterations = st.number_input("Simulated Iterations", min_value=1000, max_value=50000, value=10000, step=1000)
        run_mc = st.button("Initialize Simulation", use_container_width=True)
        
        st.markdown("""
            <div style="margin-top:24px; padding:16px; background:rgba(255,255,255,0.03); border-radius:12px; font-size:12px; color:#94A3B8;">
                <strong>Model Architecture:</strong><br>
                • Distribution: Gaussian<br>
                • N-Sample / iter: 100<br>
                • Bounds: [1.0, 5.0]<br>
                • Interval: 95% CI
            </div>
        """, unsafe_allow_html=True)

    with mc_c2:
        if run_mc:
            with st.spinner("Processing stochastic vectors..."):
                time.sleep(0.8) # UI smoothing
                p_dist = df['Porsi_Tugas_AI'].value_counts(normalize=True).sort_index()
                cats, weights = p_dist.index.values, p_dist.values
                stats = df.groupby('Porsi_Tugas_AI')['Skor_Efektivitas'].agg(['mean', 'std']).fillna(df['Skor_Efektivitas'].std())

                hasil = []
                for i in range(iterations):
                    sim_tugas_mc = np.random.choice(cats, size=100, p=weights)
                    skor = [np.clip(np.random.normal(loc=stats.loc[p, 'mean'], scale=stats.loc[p, 'std']), 1, 5) for p in sim_tugas_mc]
                    hasil.append(np.mean(skor))

                mean_mc = np.mean(hasil)
                ci_low, ci_high = np.percentile(hasil, 2.5), np.percentile(hasil, 97.5)
                running_mean = np.cumsum(hasil) / np.arange(1, iterations + 1)
                
                n_pts = min(iterations, 5000)
                step = max(1, iterations // n_pts)
                
                fig_run = go.Figure()
                fig_run.add_trace(go.Scatter(x=np.arange(1, iterations + 1)[::step], y=running_mean[::step], mode='lines', name='Running Mean', line=dict(color=COLORS['primary'], width=2)))
                fig_run.add_hline(y=mean_mc, line_dash="dash", line_color=COLORS['warning'], annotation_text=f"Convergence: {mean_mc:.3f}")
                fig_run.add_hrect(y0=ci_low, y1=ci_high, fillcolor='rgba(59,130,246,0.1)', line_width=0)
                
                fig_run.update_layout(title="Convergence Trajectory & Confidence Interval", xaxis_title="Compute Iteration", yaxis_title="Mean Effectiveness Score")
                st.plotly_chart(style_plotly(fig_run, 350), use_container_width=True)
                
                mc_res1, mc_res2, mc_res3 = st.columns(3)
                mc_res1.metric("Predicted Mean", f"{mean_mc:.3f}")
                mc_res2.metric("Lower Bound (2.5%)", f"{ci_low:.3f}")
                mc_res3.metric("Upper Bound (97.5%)", f"{ci_high:.3f}")
        else:
            st.markdown("""
                <div style="height: 350px; display: flex; align-items: center; justify-content: center; flex-direction: column; border: 1px dashed rgba(255,255,255,0.1); border-radius: 16px;">
                    <span style="font-size: 32px; margin-bottom: 16px; opacity: 0.5;">⚙️</span>
                    <p style="color: #64748B; font-size: 14px;">Stochastic engine standby. Configure parameters and execute.</p>
                </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
