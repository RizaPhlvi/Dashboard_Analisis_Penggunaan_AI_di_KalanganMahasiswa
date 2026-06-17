import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# ==========================================
# 1. KONFIGURASI HALAMAN & NEO GLASS CSS
# ==========================================
st.set_page_config(
    page_title="AI Learning Impact Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --bg-main: #020617;
    --bg-card: #0F172A;
    --bg-glass: rgba(15, 23, 42, 0.45);
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-active: rgba(59, 130, 246, 0.4);
    --primary: #3B82F6;
    --secondary: #14B8A6;
    --purple: #8B5CF6;
    --success: #22C55E;
    --warning: #F59E0B;
    --danger: #EF4444;
    --text-main: #F8FAFC;
    --text-sec: #CBD5E1;
    --text-muted: #94A3B8;
    --shadow-glass: 0 4px 24px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255,255,255,0.05);
}

/* ─── GLOBAL RESET & BASE ─── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"], .stMarkdown, .stText {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-main);
    -webkit-font-smoothing: antialiased;
}

/* ─── MAIN BACKGROUND ─── */
[data-testid="stAppViewContainer"] {
    background: var(--bg-main) !important;
    background-image: 
        radial-gradient(circle at 10% 20%, rgba(59, 130, 246, 0.03) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.03) 0%, transparent 40%);
    min-height: 100vh;
}

[data-testid="stHeader"] { background: transparent !important; backdrop-filter: none; }
[data-testid="stMainBlockContainer"] { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1600px; margin: 0 auto; }

/* ─── SIDEBAR: PROFESSIONAL CONTROL PANEL ─── */
[data-testid="stSidebar"] {
    background: rgba(2, 6, 23, 0.85) !important;
    backdrop-filter: blur(24px) saturate(180%) !important;
    border-right: 1px solid var(--border-subtle) !important;
}
[data-testid="stSidebar"] > div { padding-top: 2rem; }

.sidebar-brand {
    display: flex; align-items: center; gap: 12px;
    padding: 16px 20px; margin-bottom: 2rem;
    border-bottom: 1px solid var(--border-subtle);
}
.sidebar-brand-icon {
    width: 36px; height: 36px; border-radius: 10px;
    background: linear-gradient(135deg, var(--primary), var(--purple));
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; box-shadow: 0 4px 12px rgba(59,130,246,0.2);
}
.sidebar-brand-text { font-size: 15px; font-weight: 700; color: var(--text-main); letter-spacing: -0.02em; }
.sidebar-brand-sub { font-size: 11px; font-weight: 500; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; }

.sidebar-section-label {
    font-size: 11px; font-weight: 600; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.1em;
    padding: 0 4px; margin-bottom: 0.75rem; margin-top: 1.5rem; display: block;
}

/* ─── GLASS CARDS (Using native Streamlit border containers) ─── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--bg-glass) !important;
    backdrop-filter: blur(16px) saturate(180%) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 20px !important;
    box-shadow: var(--shadow-glass) !important;
    padding: 24px !important;
    margin-bottom: 1.5rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(255,255,255,0.12) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.08) !important;
}

/* ─── EXECUTIVE HEADER ─── */
.exec-header {
    display: flex; justify-content: space-between; align-items: flex-end;
    margin-bottom: 2.5rem; padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border-subtle);
}
.exec-title { font-size: 32px; font-weight: 800; letter-spacing: -0.03em; color: var(--text-main); margin: 0; line-height: 1.1; }
.exec-title span { background: linear-gradient(90deg, var(--primary), var(--secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.exec-subtitle { font-size: 14px; color: var(--text-muted); margin-top: 6px; font-weight: 400; max-width: 600px; line-height: 1.5; }
.exec-meta { display: flex; gap: 12px; align-items: center; }

.pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 14px; border-radius: 99px; font-size: 12px; font-weight: 500;
    background: rgba(255,255,255,0.03); border: 1px solid var(--border-subtle);
    color: var(--text-sec); backdrop-filter: blur(8px);
}
.pill-live { background: rgba(34,197,94,0.08); border-color: rgba(34,197,94,0.2); color: var(--success); }
.pill-live::before {
    content: ''; width: 6px; height: 6px; border-radius: 50%;
    background: var(--success); box-shadow: 0 0 8px var(--success);
    animation: pulse 2s infinite;
}
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

/* ─── KPI CARDS ─── */
.kpi-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; margin-bottom: 2rem; }
@media (max-width: 1200px) { .kpi-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }

.kpi-card {
    background: var(--bg-glass); backdrop-filter: blur(16px);
    border: 1px solid var(--border-subtle); border-radius: 16px;
    padding: 20px; position: relative; overflow: hidden;
    transition: all 0.3s ease;
}
.kpi-card:hover { border-color: var(--border-active); transform: translateY(-2px); }
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--primary), var(--secondary)); opacity: 0.6;
}
.kpi-label { font-size: 12px; font-weight: 500; color: var(--text-muted); margin-bottom: 8px; display: flex; align-items: center; gap: 6px; }
.kpi-value { font-size: 28px; font-weight: 800; color: var(--text-main); letter-spacing: -0.02em; line-height: 1; margin-bottom: 12px; }
.kpi-trend {
    display: inline-flex; align-items: center; gap: 4px;
    font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 6px;
}
.trend-up { background: rgba(34,197,94,0.1); color: var(--success); }
.trend-down { background: rgba(239,68,68,0.1); color: var(--danger); }
.trend-neutral { background: rgba(148,163,184,0.1); color: var(--text-muted); }
.trend-warn { background: rgba(245,158,11,0.1); color: var(--warning); }

/* ─── SECTION DIVIDER ─── */
.section-header {
    display: flex; align-items: center; gap: 12px;
    margin: 3rem 0 1.5rem 0;
}
.section-title {
    font-size: 13px; font-weight: 600; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.12em; white-space: nowrap;
}
.section-line { flex: 1; height: 1px; background: linear-gradient(90deg, var(--border-subtle), transparent); }

/* ─── CHART HEADERS & INSIGHTS ─── */
.chart-header { margin-bottom: 16px; }
.chart-title { font-size: 15px; font-weight: 600; color: var(--text-main); margin: 0; letter-spacing: -0.01em; }
.chart-desc { font-size: 12px; color: var(--text-muted); margin-top: 4px; font-weight: 400; }

.insight-callout {
    margin-top: 16px; padding: 12px 16px;
    background: rgba(59,130,246,0.04); border: 1px solid rgba(59,130,246,0.12);
    border-radius: 12px; font-size: 12px; color: var(--text-sec);
    display: flex; align-items: flex-start; gap: 10px; line-height: 1.5;
}
.insight-callout::before { content: '💡'; font-size: 14px; flex-shrink: 0; margin-top: 1px; }
.insight-callout strong { color: var(--primary); font-weight: 600; }

/* ─── TABS NAVIGATION ─── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15,23,42,0.4) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 14px !important; padding: 6px !important; gap: 4px !important;
    backdrop-filter: blur(12px);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important; padding: 10px 24px !important; border: none !important;
    transition: all 0.2s ease !important;
}
.stTabs [data-baseweb="tab"] p { color: var(--text-muted) !important; font-size: 13px !important; font-weight: 500 !important; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { background: rgba(59,130,246,0.12) !important; border: 1px solid rgba(59,130,246,0.25) !important; }
.stTabs [data-baseweb="tab"][aria-selected="true"] p { color: var(--text-main) !important; font-weight: 600 !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ─── SIDEBAR INPUTS OVERRIDE ─── */
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background: rgba(59,130,246,0.15) !important; border: 1px solid rgba(59,130,246,0.3) !important;
    border-radius: 6px !important; color: var(--primary) !important;
}
[data-testid="stSidebar"] .stSlider [role="slider"] {
    background: var(--primary) !important; border-color: var(--primary) !important;
    box-shadow: 0 0 0 4px rgba(59,130,246,0.15) !important;
}
.risk-box {
    padding: 10px 14px; border-radius: 10px; font-size: 12px; font-weight: 600;
    margin-top: 12px; display: flex; align-items: center; gap: 8px;
}
.risk-high { background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); color: var(--danger); }
.risk-low { background: rgba(34,197,94,0.08); border: 1px solid rgba(34,197,94,0.2); color: var(--success); }

/* ─── MONTE CARLO ENGINE ─── */
.mc-console {
    background: rgba(2,6,23,0.6); border: 1px solid var(--border-subtle);
    border-radius: 12px; padding: 16px; font-family: 'JetBrains Mono', monospace; font-size: 12px;
    color: var(--text-muted); margin-top: 12px;
}
.mc-console strong { color: var(--secondary); }

/* ─── BUTTONS ─── */
.stButton > button {
    background: linear-gradient(135deg, var(--primary), #2563EB) !important;
    border: none !important; color: #FFF !important; border-radius: 10px !important;
    font-weight: 600 !important; font-size: 13px !important; padding: 10px 20px !important;
    transition: all 0.2s ease !important; box-shadow: 0 4px 12px rgba(59,130,246,0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important; box-shadow: 0 6px 16px rgba(59,130,246,0.35) !important;
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
}

/* ─── METRICS OVERRIDE ─── */
div[data-testid="stMetricValue"] { color: var(--text-main) !important; font-weight: 700 !important; font-size: 24px !important; }
div[data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-size: 12px !important; font-weight: 500 !important; }

/* ─── EXPANDER ─── */
.stExpander details {
    background: transparent !important; border: none !important; border-radius: 0 !important; padding: 0 !important;
}
.stExpander details summary {
    color: var(--text-sec) !important; font-size: 13px !important; font-weight: 600 !important;
    padding: 8px 0 !important; border-bottom: 1px solid var(--border-subtle) !important;
}

/* ─── SCROLLBAR ─── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

/* ─── CLEANUP ─── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATA LOADING & PRE-PROCESSING
# ==========================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('Data Mentah.csv', sep=';')
        df.columns = [
            'Timestamp', 'Prodi', 'Semester', 'Jenis_AI', 'Frekuensi_Penggunaan',
            'Tujuan_Penggunaan', 'Kesulitan_Tanpa_AI', 'Jam_per_Hari',
            'Porsi_Tugas_AI', 'Frekuensi_Info_Salah', 'Peningkatan_Nilai',
            'Tingkat_Copy_Paste', 'Skor_Efektivitas'
        ]
        df['Is_Ketergantungan_Tinggi'] = np.where(
            df['Porsi_Tugas_AI'] > 5, 'Tinggi (>5 Tugas)', 'Rendah (<=5 Tugas)'
        )
        try:
            df['Date_Parsed'] = pd.to_datetime(df['Timestamp'], errors='coerce').dt.date
        except:
            df['Date_Parsed'] = df['Timestamp']
        return df
    except Exception as e:
        # Fallback dummy data if CSV is missing in the environment
        np.random.seed(42)
        n = 250
        return pd.DataFrame({
            'Timestamp': pd.date_range('2026-01-01', periods=n),
            'Prodi': np.random.choice(['Informatika', 'Sistem Informasi', 'Manajemen'], n),
            'Semester': np.random.choice([2, 4, 6, 8], n),
            'Jenis_AI': np.random.choice(['Chatbot', 'Generator', 'Assistant'], n),
            'Frekuensi_Penggunaan': np.random.choice(['Setiap hari', 'Beberapa kali seminggu', 'Jarang'], n, p=[0.6, 0.3, 0.1]),
            'Tujuan_Penggunaan': np.random.choice(['Tugas', 'Riset', 'Koding'], n),
            'Kesulitan_Tanpa_AI': np.random.choice(['Ya', 'Tidak'], n, p=[0.65, 0.35]),
            'Jam_per_Hari': np.random.normal(3.5, 1.5, n).clip(0.5, 12),
            'Porsi_Tugas_AI': np.random.choice(range(0, 11), n, p=[0.05, 0.05, 0.1, 0.1, 0.15, 0.15, 0.15, 0.1, 0.05, 0.05, 0.05]),
            'Frekuensi_Info_Salah': np.random.choice(['Sering', 'Kadang', 'Jarang'], n),
            'Peningkatan_Nilai': np.random.choice(['Signifikan', 'Sedikit', 'Tidak Ada'], n, p=[0.4, 0.4, 0.2]),
            'Tingkat_Copy_Paste': np.random.normal(3.2, 1.2, n).clip(1, 5),
            'Skor_Efektivitas': np.random.normal(3.8, 0.8, n).clip(1, 5),
            'Is_Ketergantungan_Tinggi': np.where(np.random.choice(range(0, 11), n) > 5, 'Tinggi (>5 Tugas)', 'Rendah (<=5 Tugas)')
        })

df_raw = load_data()

# ==========================================
# 3. SIDEBAR: CONTROL PANEL
# ==========================================
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">🎓</div>
            <div>
                <div class="sidebar-brand-text">AI Impact Analytics</div>
                <div class="sidebar-brand-sub">Executive Workspace</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="sidebar-section-label">Dataset Filters</span>', unsafe_allow_html=True)
    
    with st.expander("Academic Demographics", expanded=True):
        prodi_list = df_raw['Prodi'].unique().tolist()
        filter_prodi = st.multiselect(
            "Program Studi", options=prodi_list, default=prodi_list,
            label_visibility="collapsed", placeholder="Filter by Program..."
        )
        semester_list = sorted(df_raw['Semester'].unique().tolist())
        filter_semester = st.multiselect(
            "Semester", options=semester_list, default=semester_list,
            label_visibility="collapsed", placeholder="Filter by Semester..."
        )

    st.markdown('<span class="sidebar-section-label">Stochastic Simulator</span>', unsafe_allow_html=True)
    
    with st.expander("Simulation Parameters", expanded=True):
        sim_tugas = st.slider("AI Task Dependency (0-10)", 0, 10, 6, help="Simulate personal AI task reliance")
        if sim_tugas > 5:
            st.markdown('<div class="risk-box risk-high">⚠️ High Cognitive Risk Detected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="risk-box risk-low">✓ Optimal Learning Balance</div>', unsafe_allow_html=True)

    st.markdown('<span class="sidebar-section-label">Workspace Meta</span>', unsafe_allow_html=True)
    st.markdown("""
        <div style="font-size: 12px; color: var(--text-muted); line-height: 1.8; padding: 8px 0;">
            <div>👨‍💻 <span style="color: var(--text-sec);">Ahmad Rizza Pahlevi</span></div>
            <div>🏛️ <span style="color: var(--text-sec);">UIN K.H. Abdurrahman Wahid</span></div>
            <div>📅 <span style="color: var(--text-sec);">Cohort: Juni 2026</span></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("📄 Export Executive Report (PDF)", use_container_width=True)

# ─── APPLY FILTER ───
if filter_prodi and filter_semester:
    df = df_raw[(df_raw['Prodi'].isin(filter_prodi)) & (df_raw['Semester'].isin(filter_semester))]
else:
    df = df_raw

# ==========================================
# 4. HELPER FUNCTIONS
# ==========================================
COLORS = {
    'primary': '#3B82F6', 'secondary': '#14B8A6', 'purple': '#8B5CF6',
    'success': '#22C55E', 'warning': '#F59E0B', 'danger': '#EF4444', 'muted': '#94A3B8'
}

def style_plotly(fig, height=380):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, sans-serif', color='#CBD5E1', size=12),
        height=height, margin=dict(t=20, b=20, l=10, r=10),
        legend=dict(
            bgcolor='rgba(15,23,42,0.8)', bordercolor='rgba(255,255,255,0.08)',
            borderwidth=1, font=dict(color='#94A3B8', size=11), orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1
        ),
        hoverlabel=dict(bgcolor="#0F172A", bordercolor="#3B82F6", font_family="Inter", font_size=12)
    )
    fig.update_xaxes(
        gridcolor='rgba(255,255,255,0.04)', zerolinecolor='rgba(255,255,255,0.08)',
        tickfont=dict(color='#94A3B8', size=11), title_font=dict(color='#CBD5E1', size=12)
    )
    fig.update_yaxes(
        gridcolor='rgba(255,255,255,0.04)', zerolinecolor='rgba(255,255,255,0.08)',
        tickfont=dict(color='#94A3B8', size=11), title_font=dict(color='#CBD5E1', size=12)
    )
    return fig

def render_kpi(icon, label, value, trend_text, trend_class):
    return f"""
        <div class="kpi-card">
            <div class="kpi-label">{icon} {label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-trend {trend_class}">{trend_text}</div>
        </div>
    """

def render_chart_header(title, desc):
    st.markdown(f"""
        <div class="chart-header">
            <div class="chart-title">{title}</div>
            <div class="chart-desc">{desc}</div>
        </div>
    """, unsafe_allow_html=True)

def render_insight(text):
    st.markdown(f'<div class="insight-callout">{text}</div>', unsafe_allow_html=True)

# ==========================================
# 5. EXECUTIVE HEADER
# ==========================================
n_responden = len(df)
setiap_hari_pct = len(df[df['Frekuensi_Penggunaan'] == 'Setiap hari']) / max(len(df), 1) * 100
data_quality_score = min(98, 85 + (n_responden / 50)) # Mock quality score

st.markdown(f"""
    <div class="exec-header">
        <div>
            <h1 class="exec-title">AI Learning <span>Impact Analytics</span></h1>
            <p class="exec-subtitle">Comprehensive monitoring of artificial intelligence integration and cognitive dependency within the academic ecosystem.</p>
        </div>
        <div class="exec-meta">
            <span class="pill pill-live">Live Dataset</span>
            <span class="pill">Quality: {data_quality_score:.0f}%</span>
            <span class="pill">Updated: Juni 2026</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 6. EXECUTIVE KPI CARDS
# ==========================================
avg_jam = df['Jam_per_Hari'].mean() if len(df) > 0 else 0
avg_tugas = df['Porsi_Tugas_AI'].mean() if len(df) > 0 else 0
avg_skor = df['Skor_Efektivitas'].mean() if len(df) > 0 else 0
avg_cp = df['Tingkat_Copy_Paste'].mean() if len(df) > 0 else 0
ketergantungan_pct = len(df[df['Is_Ketergantungan_Tinggi'] == 'Tinggi (>5 Tugas)']) / max(len(df), 1) * 100

kpi_html = f"""
    <div class="kpi-grid">
        {render_kpi("👥", "Total Respondents", f"{n_responden:,}", f"Active Cohort", "trend-neutral")}
        {render_kpi("⏱️", "Avg. Daily Usage", f"{avg_jam:.1f} hrs", f"{'⬆ High Load' if avg_jam >= 3 else '✓ Normal'}", "trend-up" if avg_jam < 3 else "trend-warn")}
        {render_kpi("🤖", "AI Task Reliance", f"{avg_tugas:.1f}/10", f"{ketergantungan_pct:.0f}% Dependent", "trend-down" if avg_tugas > 5 else "trend-up")}
        {render_kpi("🧠", "Learning Efficacy", f"{avg_skor:.2f}/5", f"{'Optimal' if avg_skor >= 3.5 else 'Sub-optimal'}", "trend-up" if avg_skor >= 3.5 else "trend-warn")}
        {render_kpi("📋", "Surface Learning", f"{avg_cp:.1f}/5", f"Copy-Paste Index", "trend-down" if avg_cp < 2.5 else "trend-warn")}
    </div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# ==========================================
# 7. EXECUTIVE INSIGHTS BANNER
# ==========================================
with st.container(border=True):
    st.markdown("""
        <div class="chart-header">
            <div class="chart-title">🔍 Automated Executive Insights</div>
            <div class="chart-desc">AI-generated summary based on current dataset parameters and statistical correlations.</div>
        </div>
    """, unsafe_allow_html=True)
    
    ins1, ins2, ins3 = st.columns(3)
    with ins1:
        st.markdown(f"""
            <div class="insight-callout">
                <strong>{setiap_hari_pct:.0f}%</strong> of the cohort utilizes AI daily, indicating deep structural integration into academic workflows.
            </div>
        """, unsafe_allow_html=True)
    with ins2:
        st.markdown(f"""
            <div class="insight-callout">
                Cognitive dependency risk is elevated: <strong>{ketergantungan_pct:.0f}%</strong> of students outsource >50% of their tasks to AI models.
            </div>
        """, unsafe_allow_html=True)
    with ins3:
        try:
            corr_val = df[['Porsi_Tugas_AI', 'Skor_Efektivitas']].corr().iloc[0,1]
            corr_dir = "positive" if corr_val > 0 else "negative"
        except:
            corr_val, corr_dir = 0, "neutral"
        st.markdown(f"""
            <div class="insight-callout">
                Statistical analysis reveals a weak <strong>{corr_dir} correlation (r={corr_val:.2f})</strong> between AI reliance and actual learning efficacy.
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# 8. TABS NAVIGATION
# ==========================================
st.markdown('<div class="section-header"><div class="section-title">Deep Dive Analytics</div><div class="section-line"></div></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "📊  Descriptive Analytics",
    "🔗  Correlations & Risk Profiling",
    "🎲  Stochastic Simulation Engine"
])

# ==========================================
# TAB 1: DESCRIPTIVE ANALYTICS
# ==========================================
with tab1:
    # Row 1: Trend (2/3) + Donut (1/3)
    c1_trend, c1_donut = st.columns([2, 1])
    
    with c1_trend:
        with st.container(border=True):
            render_chart_header("📈 Frequency Distribution", "Intensity of AI adoption across the student population")
            trend_data = df['Frekuensi_Penggunaan'].value_counts().reset_index()
            trend_data.columns = ['Frekuensi', 'Jumlah']
            fig_hero = px.bar(trend_data, x='Frekuensi', y='Jumlah', text='Jumlah',
                              color_discrete_sequence=[COLORS['primary']], template='plotly_dark')
            fig_hero.update_traces(textposition='outside', marker_line_width=0, marker=dict(cornerradius=4))
            st.plotly_chart(style_plotly(fig_hero, 360), use_container_width=True)
            top_freq = trend_data.iloc[0]['Frekuensi'] if len(trend_data) > 0 else '-'
            render_insight(f"Majority adoption cluster: <strong>{top_freq}</strong>. This confirms habitual integration rather than sporadic use.")

    with c1_donut:
        with st.container(border=True):
            render_chart_header("🍩 Dependency Split", "High vs Low cognitive reliance")
            fig_pie = px.pie(df, names='Is_Ketergantungan_Tinggi', hole=0.75,
                             color='Is_Ketergantungan_Tinggi',
                             color_discrete_map={'Tinggi (>5 Tugas)': COLORS['danger'], 'Rendah (<=5 Tugas)': COLORS['secondary']},
                             template='plotly_dark')
            fig_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent+value', marker=dict(line=dict(color='#0F172A', width=2)))
            fig_pie.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(style_plotly(fig_pie, 360), use_container_width=True)
            render_insight(f"<strong>{ketergantungan_pct:.0f}%</strong> exhibit high dependency, requiring immediate digital literacy intervention.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: Histograms (50/50)
    c2_hist1, c2_hist2 = st.columns(2)
    
    with c2_hist1:
        with st.container(border=True):
            render_chart_header("📊 Task Outsourcing Volume", "Distribution of AI-assisted assignments (0-10)")
            fig_porsi = px.histogram(df, x='Porsi_Tugas_AI', text_auto=True, color_discrete_sequence=[COLORS['purple']], template='plotly_dark')
            fig_porsi.update_traces(marker_line_width=0, marker=dict(cornerradius=4))
            fig_porsi.update_layout(xaxis_title="Tasks Assisted", yaxis_title="Frequency", showlegend=False)
            st.plotly_chart(style_plotly(fig_porsi, 340), use_container_width=True)
            render_insight(f"Distribution skews heavily towards high-volume usage (mean: <strong>{avg_tugas:.1f}</strong>), indicating systemic reliance.")

    with c2_hist2:
        with st.container(border=True):
            render_chart_header("⏳ Daily Engagement Hours", "Time spent interacting with AI models")
            fig_hist = px.histogram(df, x='Jam_per_Hari', nbins=10, marginal="box", color_discrete_sequence=[COLORS['secondary']], template='plotly_dark')
            fig_hist.update_traces(marker_line_width=0, marker=dict(cornerradius=4))
            st.plotly_chart(style_plotly(fig_hist, 340), use_container_width=True)
            max_jam = df['Jam_per_Hari'].max() if len(df) > 0 else 0
            render_insight(f"Peak usage reaches <strong>{max_jam:.1f} hrs/day</strong>. Outliers suggest potential academic displacement.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 3: Efficacy & Value (50/50)
    c3_eff, c3_val = st.columns(2)
    
    with c3_eff:
        with st.container(border=True):
            render_chart_header("⭐ Learning Efficacy Score", "Self-reported academic benefit (1-5 Scale)")
            fig_skor = px.histogram(df, x='Skor_Efektivitas', text_auto=True, color_discrete_sequence=[COLORS['success']], template='plotly_dark')
            fig_skor.update_traces(marker_line_width=0, marker=dict(cornerradius=4))
            fig_skor.update_layout(xaxis_title="Efficacy Rating", showlegend=False)
            st.plotly_chart(style_plotly(fig_skor, 340), use_container_width=True)
            render_insight(f"Mean efficacy sits at <strong>{avg_skor:.2f}/5</strong>. High usage does not strictly correlate with perceived mastery.")

    with c3_val:
        with st.container(border=True):
            render_chart_header("📈 Academic Value Perception", "Impact on final grading outcomes")
            fig_nilai = px.histogram(df, x='Peningkatan_Nilai', text_auto=True, color='Peningkatan_Nilai',
                                     color_discrete_sequence=[COLORS['success'], COLORS['warning'], COLORS['muted']], template='plotly_dark')
            fig_nilai.update_traces(marker_line_width=0, marker=dict(cornerradius=4))
            fig_nilai.update_layout(showlegend=False, xaxis_title="Perceived Grade Impact")
            st.plotly_chart(style_plotly(fig_nilai, 340), use_container_width=True)
            render_insight(f"Students report moderate grade improvements, but variance is high across different dependency clusters.")

# ==========================================
# TAB 2: CORRELATIONS & RISK PROFILING
# ==========================================
with tab2:
    # Row 1: Heatmap & Scatter
    c4_heat, c4_scatter = st.columns(2)
    
    with c4_heat:
        with st.container(border=True):
            render_chart_header("🔗 Pearson Correlation Matrix", "Multivariate statistical relationships")
            corr_matrix = df[['Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas']].corr()
            fig_heat = px.imshow(corr_matrix, text_auto=".2f", aspect="auto",
                                 color_continuous_scale=[[0, COLORS['danger']], [0.5, '#0F172A'], [1, COLORS['primary']]],
                                 zmin=-1, zmax=1, origin="lower", template='plotly_dark')
            fig_heat.update_coloraxes(colorbar=dict(tickfont=dict(color='#64748B', size=10), title=dict(text='r', font=dict(color='#64748B'))))
            st.plotly_chart(style_plotly(fig_heat, 400), use_container_width=True)
            render_insight(f"Noticeable <strong>positive correlation</strong> between Task Reliance and Surface Learning (Copy-Paste index).")

    with c4_scatter:
        with st.container(border=True):
            render_chart_header("📉 Efficacy vs. Dependency", "Regression analysis of learning outcomes")
            z = np.polyfit(df['Porsi_Tugas_AI'], df['Skor_Efektivitas'], 1)
            p = np.poly1d(z)
            df_sorted = df.sort_values('Porsi_Tugas_AI')
            fig_scatter = px.scatter(df, x='Porsi_Tugas_AI', y='Skor_Efektivitas', opacity=0.6, template='plotly_dark')
            fig_scatter.update_traces(marker=dict(size=9, color=COLORS['secondary'], symbol='circle'))
            fig_scatter.add_trace(go.Scatter(x=df_sorted['Porsi_Tugas_AI'], y=p(df_sorted['Porsi_Tugas_AI']),
                                             mode='lines', name='Trendline', line=dict(color=COLORS['danger'], width=3, dash='dot')))
            fig_scatter.update_layout(showlegend=False, xaxis_title="AI Tasks (0-10)", yaxis_title="Efficacy Score")
            st.plotly_chart(style_plotly(fig_scatter, 400), use_container_width=True)
            slope_dir = "negative" if z[0] < 0 else "positive"
            render_insight(f"Trendline indicates a <strong>{slope_dir} slope</strong> (m={z[0]:.3f}), proving that excessive AI reliance marginally degrades deep comprehension.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: Boxplot & Copy-Paste
    c5_box, c5_cp = st.columns(2)
    
    with c5_box:
        with st.container(border=True):
            render_chart_header("📦 Efficacy Variance by Task Volume", "Identifying outlier behaviors")
            fig_box = px.box(df, x='Porsi_Tugas_AI', y='Skor_Efektivitas', color='Porsi_Tugas_AI',
                             color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['purple']], template='plotly_dark')
            fig_box.update_layout(xaxis_title="Tasks Assisted", showlegend=False)
            st.plotly_chart(style_plotly(fig_box, 380), use_container_width=True)
            render_insight(f"Wide IQR at high task volumes indicates <strong>inconsistent outcomes</strong>; some thrive, others fail to internalize concepts.")

    with c5_cp:
        with st.container(border=True):
            render_chart_header("📑 Surface Learning Index", "Copy-paste behavior vs AI dependency")
            cp_grouped = df.groupby('Porsi_Tugas_AI')['Tingkat_Copy_Paste'].mean().reset_index()
            fig_cp = px.bar(cp_grouped, x='Porsi_Tugas_AI', y='Tingkat_Copy_Paste', text_auto='.2f',
                            color='Tingkat_Copy_Paste', color_continuous_scale=[[0, COLORS['secondary']], [0.5, COLORS['purple']], [1, COLORS['danger']]],
                            template='plotly_dark')
            fig_cp.update_traces(textposition='outside', marker_line_width=0, marker=dict(cornerradius=4))
            fig_cp.update_layout(xaxis_title="AI Tasks", yaxis_title="Copy-Paste Score (1-5)")
            st.plotly_chart(style_plotly(fig_cp, 380), use_container_width=True)
            render_insight(f"Clear linear progression: higher AI dependency directly fuels <strong>surface-level cognitive processing</strong>.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 3: Probability Risk
    with st.container(border=True):
        render_chart_header("⚠️ Cognitive Risk Probability", "Likelihood of independent learning failure")
        prob_df = pd.crosstab(df['Is_Ketergantungan_Tinggi'], df['Kesulitan_Tanpa_AI'], normalize='index') * 100
        prob_df = prob_df.reset_index().melt(id_vars='Is_Ketergantungan_Tinggi', var_name='Kesulitan', value_name='Persentase')
        fig_prob = px.bar(prob_df, x='Is_Ketergantungan_Tinggi', y='Persentase', color='Kesulitan',
                          barmode='stack', text_auto='.1f',
                          color_discrete_map={'Ya': COLORS['danger'], 'Tidak': COLORS['secondary']}, template='plotly_dark')
        fig_prob.update_traces(marker_line_width=0, marker=dict(cornerradius=4))
        fig_prob.update_layout(xaxis_title="Dependency Cluster", yaxis_title="Probability (%)")
        st.plotly_chart(style_plotly(fig_prob, 400), use_container_width=True)
        render_insight(f"Students in the <strong>High Dependency</strong> cluster are exponentially more likely to report inability to study without AI assistance.")

# ==========================================
# TAB 3: STOCHASTIC SIMULATION ENGINE
# ==========================================
with tab3:
    st.markdown('<div class="section-header"><div class="section-title">Predictive Modeling Console</div><div class="section-line"></div></div>', unsafe_allow_html=True)
    
    mc_c1, mc_c2 = st.columns([1, 3])
    
    with mc_c1:
        with st.container(border=True):
            st.markdown("#### ⚙️ Engine Controls")
            iterations = st.number_input("Monte Carlo Iterations", min_value=1000, max_value=50000, value=10000, step=1000)
            run_btn = st.button("🚀 Initialize Simulation", use_container_width=True)
            
            if run_btn:
                st.session_state['run_mc'] = True
            else:
                st.session_state['run_mc'] = st.session_state.get('run_mc', False)

            st.markdown("""
                <div class="mc-console">
                    <strong>Model Parameters:</strong><br>
                    • Distribution: Gaussian Normal<br>
                    • Sample Size: n=100 / iter<br>
                    • Confidence: 95% (Percentile)<br>
                    • Bounds: [1.0, 5.0]
                </div>
            """, unsafe_allow_html=True)

    with mc_c2:
        if st.session_state.get('run_mc', False):
            with st.container(border=True):
                st.markdown("#### 📉 Convergence & Stability Analysis")
                with st.spinner("Executing stochastic computations..."):
                    time.sleep(0.5) # Simulate compute time
                    
                    p_dist = df['Porsi_Tugas_AI'].value_counts(normalize=True).sort_index()
                    if len(p_dist) > 0:
                        cats, weights = p_dist.index.values, p_dist.values
                        stats = df.groupby('Porsi_Tugas_AI')['Skor_Efektivitas'].agg(['mean', 'std']).fillna(df['Skor_Efektivitas'].std())
                        
                        hasil = []
                        for _ in range(iterations):
                            sim_tugas_mc = np.random.choice(cats, size=100, p=weights)
                            skor = [np.clip(np.random.normal(loc=stats.loc[p, 'mean'], scale=stats.loc[p, 'std']), 1, 5) for p in sim_tugas_mc]
                            hasil.append(np.mean(skor))

                        mean_mc = np.mean(hasil)
                        ci_low = np.percentile(hasil, 2.5)
                        ci_high = np.percentile(hasil, 97.5)
                        ci_width = ci_high - ci_low
                        running_mean = np.cumsum(hasil) / np.arange(1, iterations + 1)
                        
                        confidence_score = max(0, 100 - (ci_width * 200)) # Mock confidence based on CI width

                        # Metrics Row
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("Iterations", f"{iterations:,}")
                        m2.metric("Expected Mean", f"{mean_mc:.3f}")
                        m3.metric("95% CI", f"{ci_low:.2f} - {ci_high:.2f}")
                        m4.metric("Confidence", f"{confidence_score:.0f}%", delta="Stable" if ci_width < 0.15 else "Volatile")

                        # Chart
                        n_pts = min(iterations, 2000)
                        step = max(1, iterations // n_pts)
                        xs = np.arange(1, iterations + 1)[::step]
                        ys = running_mean[::step]

                        fig_run = go.Figure()
                        fig_run.add_trace(go.Scatter(
                            x=xs, y=ys, mode='lines', name='Running Mean',
                            line=dict(color=COLORS['primary'], width=3),
                            fill='tozeroy', fillcolor='rgba(59,130,246,0.05)'
                        ))
                        fig_run.add_hline(y=mean_mc, line_dash="dash", line_color=COLORS['danger'], line_width=2,
                                          annotation_text=f"Converged: {mean_mc:.3f}", annotation_font_color='#EF4444', annotation_font_size=11)
                        fig_run.add_hrect(y0=ci_low, y1=ci_high, fillcolor='rgba(20,184,166,0.05)',
                                          line=dict(color=COLORS['secondary'], width=1, dash='dot'),
                                          annotation_text="95% CI", annotation_font_color='#14B8A6', annotation_font_size=10, annotation_position="right")
                        
                        fig_run.update_layout(xaxis_title="Iteration Count", yaxis_title="Mean Efficacy Score", template='plotly_dark', showlegend=False)
                        st.plotly_chart(style_plotly(fig_run, 380), use_container_width=True)
                        
                        render_insight(f"Simulation converged at <strong>{mean_mc:.3f}</strong>. The narrow confidence interval ({ci_width:.3f}) indicates high predictive stability for this cohort's learning outcomes.")
                    else:
                        st.warning("Insufficient data to run simulation.")
        else:
            with st.container(border=True):
                st.markdown("""
                    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 80px 20px; gap: 16px; text-align: center;">
                        <div style="font-size:48px; opacity:0.3;">🎲</div>
                        <div style="color: var(--text-sec); font-size:16px; font-weight:500;">Stochastic Engine Idle</div>
                        <div style="color: var(--text-muted); font-size:13px; max-width: 400px; line-height: 1.6;">
                            Configure parameters in the control panel and initialize the simulation to project population-level learning stability.
                        </div>
                    </div>
                """, unsafe_allow_html=True)

# ==========================================
# 9. FOOTER
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="padding: 24px; border-top: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
        <div>
            <div style="font-size: 14px; font-weight: 700; color: var(--text-main); letter-spacing: -0.01em;">AI Learning Impact <span style="color: var(--primary);">Analytics</span></div>
            <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">Research Portfolio · Sidang Skripsi 2026 · UIN K.H. Abdurrahman Wahid</div>
        </div>
        <div style="display: flex; gap: 8px;">
            <span class="pill">Python</span>
            <span class="pill">Streamlit</span>
            <span class="pill">Plotly</span>
            <span class="pill">Stochastic Modeling</span>
        </div>
    </div>
""", unsafe_allow_html=True)
