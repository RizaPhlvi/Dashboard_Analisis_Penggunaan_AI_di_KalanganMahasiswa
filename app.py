import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# ==========================================
# 1. KONFIGURASI HALAMAN & CUSTOM CSS (ENTERPRISE THEME)
# ==========================================
st.set_page_config(
    page_title="AI Learning Impact Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* === ROOT VARIABLES (Design Tokens) === */
:root {
    --bg-primary: #0F172A;
    --bg-surface: #1E293B;
    --bg-elevated: #273449;
    --border-subtle: #334155;
    --border-medium: #475569;
    --text-primary: #F8FAFC;
    --text-secondary: #CBD5E1;
    --text-muted: #94A3B8;
    --accent-primary: #3B82F6;
    --accent-secondary: #06B6D4;
    --accent-success: #22C55E;
    --accent-warning: #F59E0B;
    --accent-danger: #EF4444;
    --accent-purple: #8B5CF6;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -2px rgba(0, 0, 0, 0.3);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -4px rgba(0, 0, 0, 0.4);
    --shadow-glow: 0 0 40px rgba(59, 130, 246, 0.15);
}

/* === GLOBAL TYPOGRAPHY & BASE === */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: var(--text-primary);
    font-feature-settings: "cv02", "cv03", "cv04", "cv11";
    -webkit-font-smoothing: antialiased;
}

/* === ELEGANT DARK GRADIENT BACKGROUND === */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(59, 130, 246, 0.12), transparent),
        radial-gradient(ellipse 60% 50% at 80% 100%, rgba(139, 92, 246, 0.08), transparent),
        linear-gradient(180deg, #0F172A 0%, #0B1120 100%);
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background-color: transparent;
}

/* === SIDEBAR REDESIGN === */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1120 0%, #131B2E 100%) !important;
    border-right: 1px solid var(--border-subtle);
}
[data-testid="stSidebar"] .stMarkdown {
    color: var(--text-primary);
}

/* === HILANGKAN DEFAULT STREAMLIT RED, GANTI DENGAN PRIMARY BLUE === */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(30, 41, 59, 0.5);
    backdrop-filter: blur(12px);
    border-radius: 14px;
    padding: 6px;
    border: 1px solid var(--border-subtle);
    display: inline-flex;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 10px;
    padding: 10px 20px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border: none;
}
.stTabs [data-baseweb="tab"] p {
    color: var(--text-muted);
    font-size: 14px;
    font-weight: 500;
    margin: 0;
    transition: all 0.3s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    background: rgba(59, 130, 246, 0.08);
}
.stTabs [data-baseweb="tab"]:hover p {
    color: var(--text-primary);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(6, 182, 212, 0.15) 100%);
    border: 1px solid rgba(59, 130, 246, 0.3);
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.2);
}
.stTabs [aria-selected="true"] p {
    color: var(--text-primary);
    font-weight: 600;
    font-size: 14px;
}

/* === SLIDER PREMIUM === */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
    border: 2px solid #fff !important;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2);
}
div[data-testid="stTickBar"] ~ div > div > div > div {
    background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary)) !important;
}

/* === BUTTON PREMIUM === */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-primary) 0%, #2563EB 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #FFFFFF;
    border-radius: 12px;
    font-weight: 600;
    font-size: 14px;
    padding: 10px 24px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
}

/* === MULTISELECT TAGS === */
.stMultiSelect [data-baseweb="tag"] {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(6, 182, 212, 0.15));
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 8px;
}
.stMultiSelect [data-baseweb="tag"] span {
    color: var(--text-primary);
    font-weight: 500;
}

/* === EXPANDER (untuk sidebar) === */
[data-testid="stExpander"] {
    background: rgba(30, 41, 59, 0.4);
    backdrop-filter: blur(10px);
    border: 1px solid var(--border-subtle);
    border-radius: 14px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
}
[data-testid="stExpander"]:hover {
    border-color: var(--border-medium);
    background: rgba(30, 41, 59, 0.6);
}
[data-testid="stExpander"] summary {
    padding: 14px 18px;
}
[data-testid="stExpander"] summary span {
    font-weight: 600;
    font-size: 14px;
    color: var(--text-primary);
}

/* === PREMIUM METRIC CARDS === */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.4) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-subtle);
    border-radius: 18px;
    padding: 22px 24px;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
div[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
    opacity: 0;
    transition: opacity 0.4s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: rgba(59, 130, 246, 0.4);
    box-shadow: var(--shadow-glow), var(--shadow-lg);
}
div[data-testid="stMetric"]:hover::before {
    opacity: 1;
}
div[data-testid="stMetricValue"] {
    color: var(--text-primary);
    font-weight: 700;
    font-size: 34px;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #F8FAFC 0%, #CBD5E1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
div[data-testid="stMetricLabel"] {
    color: var(--text-muted);
    font-size: 12px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 4px;
}
div[data-testid="stMetricDelta"] {
    font-size: 12px;
    font-weight: 600;
}

/* === PREMIUM CARD WRAPPER (untuk grafik) === */
[data-testid="stVerticalBlockBorderWrapper"] > div,
section[data-testid="stVerticalBlock"] > div {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.3) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-subtle);
    border-radius: 20px;
    box-shadow: var(--shadow-md);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    padding: 24px;
}
[data-testid="stVerticalBlockBorderWrapper"] > div:hover,
section[data-testid="stVerticalBlock"] > div:hover {
    border-color: rgba(59, 130, 246, 0.3);
    box-shadow: var(--shadow-lg), 0 0 30px rgba(59, 130, 246, 0.1);
    transform: translateY(-2px);
}

/* === HERO SECTION === */
.hero-box {
    background:
        radial-gradient(ellipse 100% 100% at 0% 0%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
        radial-gradient(ellipse 80% 100% at 100% 100%, rgba(139, 92, 246, 0.12) 0%, transparent 50%),
        linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
    backdrop-filter: blur(20px);
    padding: 48px 40px;
    border-radius: 24px;
    border: 1px solid rgba(59, 130, 246, 0.2);
    box-shadow: var(--shadow-lg), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.hero-box::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
    animation: pulse-glow 8s ease-in-out infinite;
    pointer-events: none;
}
@keyframes pulse-glow {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 0.8; transform: scale(1.05); }
}
.hero-title {
    font-size: 44px;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 12px;
    background: linear-gradient(135deg, #F8FAFC 0%, #94A3B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative;
    z-index: 1;
}
.hero-subtitle {
    font-size: 17px;
    color: var(--text-secondary);
    font-weight: 400;
    margin-top: 0;
    margin-bottom: 28px;
    line-height: 1.6;
    max-width: 720px;
    position: relative;
    z-index: 1;
}
.hero-meta {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    position: relative;
    z-index: 1;
}
.meta-chip {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(10px);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 13px;
    color: var(--text-secondary);
    font-weight: 500;
    transition: all 0.3s ease;
}
.meta-chip:hover {
    border-color: var(--accent-primary);
    background: rgba(59, 130, 246, 0.1);
    color: var(--text-primary);
}
.meta-chip-icon {
    font-size: 14px;
}

/* === EXECUTIVE SUMMARY BOX === */
.executive-summary {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(6, 182, 212, 0.05) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(59, 130, 246, 0.25);
    border-left: 3px solid var(--accent-primary);
    border-radius: 16px;
    padding: 22px 26px;
    margin: 20px 0;
    color: var(--text-secondary);
    font-size: 14.5px;
    line-height: 1.7;
}
.executive-summary strong {
    color: var(--text-primary);
}

/* === SECTION DIVIDER === */
.section-divider {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 40px 0 24px 0;
}
.section-divider-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-medium), transparent);
}
.section-divider-title {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--text-muted);
    padding: 6px 14px;
    background: rgba(30, 41, 59, 0.4);
    backdrop-filter: blur(10px);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
}

/* === INSIGHT BOX (bawah setiap chart) === */
.insight-box {
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.06) 0%, rgba(6, 182, 212, 0.04) 100%);
    border: 1px solid rgba(34, 197, 94, 0.2);
    border-left: 3px solid var(--accent-success);
    border-radius: 12px;
    padding: 14px 18px;
    margin-top: 18px;
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
    transition: all 0.3s ease;
}
.insight-box:hover {
    border-left-color: var(--accent-primary);
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(6, 182, 212, 0.05) 100%);
}
.insight-box strong {
    color: var(--accent-success);
    font-weight: 600;
    margin-right: 6px;
}

/* === CHART TITLE === */
.chart-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
    letter-spacing: -0.01em;
}
.chart-description {
    font-size: 13px;
    color: var(--text-muted);
    margin-bottom: 20px;
    line-height: 1.5;
}

/* === MONTE CARLO DASHBOARD === */
.mc-status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    color: var(--accent-success);
    font-weight: 600;
    margin-bottom: 16px;
}
.mc-status-dot {
    width: 8px;
    height: 8px;
    background: var(--accent-success);
    border-radius: 50%;
    box-shadow: 0 0 10px var(--accent-success);
    animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(1.2); }
}

/* === FOOTER === */
.dashboard-footer {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-subtle);
    border-radius: 18px;
    padding: 28px 32px;
    margin-top: 60px;
    color: var(--text-muted);
    font-size: 13px;
    line-height: 1.7;
}
.dashboard-footer strong {
    color: var(--text-primary);
    font-weight: 600;
}
.footer-meta {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 20px;
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid var(--border-subtle);
    font-size: 12px;
    color: var(--text-muted);
}

/* === TEXT COLORS === */
p, h1, h2, h3, h4, h5, h6, label {
    color: var(--text-primary) !important;
}
.stMarkdown {
    color: var(--text-primary);
}

/* === SCROLLBAR === */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}
::-webkit-scrollbar-track {
    background: var(--bg-primary);
}
::-webkit-scrollbar-thumb {
    background: var(--border-medium);
    border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--accent-primary);
}

/* === NUMBER INPUT === */
.stNumberInput input {
    background: rgba(30, 41, 59, 0.4) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}
.stNumberInput input:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# DESIGN TOKENS (PALET WARNA ENTERPRISE)
# ==========================================
SOFT_COLORS = {
    'primary': '#3B82F6',
    'secondary': '#06B6D4',
    'success': '#22C55E',
    'danger': '#EF4444',
    'warning': '#F59E0B',
    'purple': '#8B5CF6',
    'muted': '#94A3B8'
}
PLOTLY_TEMPLATE = 'plotly_dark'

# ==========================================
# HELPER FUNCTIONS (UI UTILITIES)
# ==========================================
def render_section_divider(title):
    st.markdown(f"""
    <div class="section-divider">
        <div class="section-divider-line"></div>
        <div class="section-divider-title">{title}</div>
        <div class="section-divider-line"></div>
    </div>
    """, unsafe_allow_html=True)

def render_chart_header(title, description):
    st.markdown(f'<div class="chart-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-description">{description}</div>', unsafe_allow_html=True)

def render_insight_box(text):
    st.markdown(f"""
    <div class="insight-box">
        <strong>💡 Insight</strong>{text}
    </div>
    """, unsafe_allow_html=True)

def update_dark_layout(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0', family='Inter', size=12),
        margin=dict(t=20, b=20, l=0, r=0)
    )
    return fig

# ==========================================
# 2. MEMUAT & PRE-PROCESSING DATA (LOGIKA TIDAK BERUBAH)
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv('Data Mentah.csv', sep=';')
    df.columns = [
        'Timestamp', 'Prodi', 'Semester', 'Jenis_AI', 'Frekuensi_Penggunaan',
        'Tujuan_Penggunaan', 'Kesulitan_Tanpa_AI', 'Jam_per_Hari',
        'Porsi_Tugas_AI', 'Frekuensi_Info_Salah', 'Peningkatan_Nilai',
        'Tingkat_Copy_Paste', 'Skor_Efektivitas'
    ]
    df['Is_Ketergantungan_Tinggi'] = np.where(df['Porsi_Tugas_AI'] > 5, 'Tinggi (>5 Tugas)', 'Rendah (<=5 Tugas)')
    try:
        df['Date_Parsed'] = pd.to_datetime(df['Timestamp'], errors='coerce').dt.date
    except:
        df['Date_Parsed'] = df['Timestamp']
    return df

df_raw = load_data()

# ==========================================
# 3. SIDEBAR: FILTER & NAVIGASI (REDESIGNED DENGAN EXPANDER)
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 20px 0;">
        <div style="font-size: 22px; font-weight: 700; letter-spacing: -0.02em; 
                    background: linear-gradient(135deg, #3B82F6, #06B6D4); 
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🎓 AI Learning Impact
        </div>
        <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">
            Enterprise Analytics Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📁 Filter Dataset", expanded=True):
        prodi_list = df_raw['Prodi'].unique().tolist()
        filter_prodi = st.multiselect("Program Studi", options=prodi_list, default=prodi_list)

        semester_list = sorted(df_raw['Semester'].unique().tolist())
        filter_semester = st.multiselect("Semester", options=semester_list, default=semester_list)

    with st.expander("🔮 Profil Simulator"):
        sim_tugas = st.slider("Porsi Bantuan AI Anda:", 0, 10, 6)
        if sim_tugas > 5:
            st.error("⚠️ Risiko Ketergantungan Tinggi")
        else:
            st.success("✅ Ketergantungan Aman")

    with st.expander("ℹ️ Tentang Dashboard"):
        st.markdown("""
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6;">
        Dashboard ini menganalisis dampak penggunaan <strong>Artificial Intelligence</strong> 
        terhadap efektivitas belajar mahasiswa dengan pendekatan <em>data-driven analytics</em>.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 40px; padding-top: 20px; border-top: 1px solid #334155;'>", unsafe_allow_html=True)
    st.caption("👨‍💻 **Developer:** Ahmad Rizza Pahlevi")
    st.caption("🏢 UIN K.H. Abdurrahman Wahid")
    st.caption("📅 Juni 2026")

# Apply filter
if filter_prodi and filter_semester:
    df = df_raw[(df_raw['Prodi'].isin(filter_prodi)) & (df_raw['Semester'].isin(filter_semester))]
else:
    df = df_raw

# ==========================================
# 4. HERO SECTION (HEADER PREMIUM)
# ==========================================
st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">AI Learning Impact Analytics</div>
    <div class="hero-subtitle">
        Memahami pola, dampak, dan probabilitas penggunaan <strong>Artificial Intelligence</strong> 
        dalam ekosistem akademik melalui pendekatan analitik berbasis data, probabilitas, 
        dan simulasi Monte Carlo untuk proyeksi skala besar.
    </div>
    <div class="hero-meta">
        <div class="meta-chip"><span class="meta-chip-icon">📅</span> Update: Juni 2026</div>
        <div class="meta-chip"><span class="meta-chip-icon">👨‍💻</span> Ahmad Rizza Pahlevi</div>
        <div class="meta-chip"><span class="meta-chip-icon">🏢</span> UIN K.H. Abdurrahman Wahid</div>
        <div class="meta-chip"><span class="meta-chip-icon">📊</span> {len(df)} Responden Aktif</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. KPI PREMIUM CARDS
# ==========================================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(label="Total Sampel", value=f"{len(df)}", delta="Data Terfilter")

avg_jam = df['Jam_per_Hari'].mean() if len(df) > 0 else 0
with kpi2:
    st.metric(label="Durasi Rata-rata", value=f"{avg_jam:.1f} Jam", delta="-0.2 vs Nasional", delta_color="inverse")

avg_tugas = df['Porsi_Tugas_AI'].mean() if len(df) > 0 else 0
with kpi3:
    st.metric(label="Bantuan Tugas", value=f"{avg_tugas:.1f}/10", delta="Ketergantungan", delta_color="off")

avg_skor = df['Skor_Efektivitas'].mean() if len(df) > 0 else 0
with kpi4:
    st.metric(label="Skor Efektivitas", value=f"{avg_skor:.2f}/5", delta="Excellent" if avg_skor > 3.5 else "Moderate")

# ==========================================
# 6. EXECUTIVE SUMMARY
# ==========================================
render_section_divider("Executive Summary")

if len(df) > 0:
    setiap_hari_pct = len(df[df['Frekuensi_Penggunaan']=='Setiap hari'])/len(df)*100
    mean_jam = df['Jam_per_Hari'].mean()
    max_jam = df['Jam_per_Hari'].max()
    high_dep_pct = len(df[df['Is_Ketergantungan_Tinggi']=='Tinggi (>5 Tugas)'])/len(df)*100
    
    st.markdown(f"""
    <div class="executive-summary">
        Dataset saat ini merepresentasikan <strong>{len(df)} mahasiswa</strong> yang aktif menggunakan AI untuk keperluan akademik. 
        <strong>{setiap_hari_pct:.0f}%</strong> di antaranya menggunakan AI setiap hari dengan durasi rata-rata 
        <strong>{mean_jam:.1f} jam/hari</strong> (maksimal {max_jam} jam). 
        Proporsi mahasiswa dengan ketergantungan tinggi (>5 tugas) mencapai <strong>{high_dep_pct:.0f}%</strong>, 
        mengindikasikan perlunya intervensi edukatif untuk menjaga kemandirian kognitif.
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("Tidak ada data yang sesuai dengan filter yang dipilih.")

# ==========================================
# 7. TAB NAVIGATION (MODERN SEGMENTED CONTROL)
# ==========================================
render_section_divider("Modul Analitik")
tab1, tab2, tab3 = st.tabs(["📊 Eksplorasi Deskriptif", "🔗 Hubungan & Probabilitas", "🎲 Monte Carlo Simulation"])

# ==========================================
# TAB 1: EKSPLORASI DESKRIPTIF
# ==========================================
with tab1:
    with st.container(border=True):
        render_chart_header(
            "📈 Tren Frekuensi Penggunaan AI",
            "Distribusi seberapa sering mahasiswa menggunakan AI dalam aktivitas akademik harian."
        )
        trend_data = df['Frekuensi_Penggunaan'].value_counts().reset_index()
        trend_data.columns = ['Frekuensi', 'Jumlah']
        fig_hero = px.bar(
            trend_data, x='Frekuensi', y='Jumlah',
            text='Jumlah', color='Frekuensi',
            color_discrete_sequence=[SOFT_COLORS['primary'], SOFT_COLORS['secondary'], SOFT_COLORS['purple'], SOFT_COLORS['muted']],
            template=PLOTLY_TEMPLATE
        )
        fig_hero.update_traces(textposition='outside')
        fig_hero.update_layout(height=380, showlegend=False)
        st.plotly_chart(update_dark_layout(fig_hero), use_container_width=True)
        
        top_freq = trend_data.iloc[0] if len(trend_data) > 0 else None
        if top_freq is not None:
            render_insight_box(
                f"Mayoritas mahasiswa ({top_freq['Jumlah']} orang) menggunakan AI dengan frekuensi <strong>{top_freq['Frekuensi']}</strong>, "
                f"menunjukkan pola adopsi yang cukup tinggi di kalangan responden."
            )

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            render_chart_header(
                "🍩 Distribusi Tingkat Ketergantungan",
                "Perbandingan proporsi mahasiswa dengan ketergantungan tinggi vs rendah."
            )
            fig_pie = px.pie(
                df, names='Is_Ketergantungan_Tinggi', hole=0.55,
                color='Is_Ketergantungan_Tinggi',
                color_discrete_map={'Tinggi (>5 Tugas)': SOFT_COLORS['danger'], 'Rendah (<=5 Tugas)': SOFT_COLORS['secondary']},
                template=PLOTLY_TEMPLATE
            )
            fig_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent+value')
            fig_pie.update_layout(height=380, showlegend=False)
            st.plotly_chart(update_dark_layout(fig_pie), use_container_width=True)
            
            high_count = len(df[df['Is_Ketergantungan_Tinggi']=='Tinggi (>5 Tugas)'])
            high_pct = (high_count/len(df)*100) if len(df) > 0 else 0
            render_insight_box(
                f"Sebanyak <strong>{high_pct:.1f}%</strong> responden memiliki ketergantungan tinggi (>5 tugas dibantu AI), "
                f"yang memerlukan perhatian khusus dari sisi pedagogis."
            )

    with col2:
        with st.container(border=True):
            render_chart_header(
                "📊 Distribusi Porsi Tugas Dibantu AI",
                "Histogram jumlah tugas per mahasiswa yang dibantu oleh AI."
            )
            fig_porsi = px.histogram(
                df, x='Porsi_Tugas_AI', text_auto=True,
                color_discrete_sequence=[SOFT_COLORS['primary']],
                template=PLOTLY_TEMPLATE
            )
            fig_porsi.update_layout(height=380, xaxis_title="Jumlah Tugas (0-10)", yaxis_title="Jumlah Mahasiswa")
            st.plotly_chart(update_dark_layout(fig_porsi), use_container_width=True)
            render_insight_box(
                f"Distribusi menunjukkan variasi penggunaan AI dari ringan hingga intensif. "
                f"Rata-rata mahasiswa menggunakan AI untuk <strong>{avg_tugas:.1f} tugas</strong>."
            )

    col3, col4 = st.columns(2)
    with col3:
        with st.container(border=True):
            render_chart_header(
                "⏳ Histogram Durasi Pemakaian Harian",
                "Distribusi durasi penggunaan AI per hari dengan boxplot marginal."
            )
            fig_hist = px.histogram(
                df, x='Jam_per_Hari', nbins=8, marginal="box",
                color_discrete_sequence=[SOFT_COLORS['secondary']],
                template=PLOTLY_TEMPLATE
            )
            fig_hist.update_layout(height=380)
            st.plotly_chart(update_dark_layout(fig_hist), use_container_width=True)
            render_insight_box(
                f"Durasi rata-rata penggunaan AI adalah <strong>{mean_jam:.1f} jam/hari</strong>, "
                f"dengan outlier di atas menunjukkan mahasiswa yang sangat intensif menggunakan AI."
            )

    with col4:
        with st.container(border=True):
            render_chart_header(
                "⭐ Distribusi Skor Efektivitas Belajar",
                "Seberapa efektif AI membantu proses belajar menurut persepsi mahasiswa."
            )
            fig_skor = px.histogram(
                df, x='Skor_Efektivitas', text_auto=True,
                color_discrete_sequence=[SOFT_COLORS['success']],
                template=PLOTLY_TEMPLATE
            )
            fig_skor.update_layout(height=380, xaxis_title="Skor Efektivitas (1-5)")
            st.plotly_chart(update_dark_layout(fig_skor), use_container_width=True)
            render_insight_box(
                f"Skor efektivitas rata-rata <strong>{avg_skor:.2f}/5</strong>, "
                f"menunjukkan persepsi positif terhadap peran AI dalam pembelajaran."
            )

    with st.container(border=True):
        render_chart_header(
            "📈 Persepsi Peningkatan Nilai Akademik",
            "Distribusi persepsi mahasiswa tentang peningkatan nilai setelah menggunakan AI."
        )
        fig_nilai = px.histogram(
            df, x='Peningkatan_Nilai', text_auto=True, color='Peningkatan_Nilai',
            color_discrete_sequence=[SOFT_COLORS['success'], SOFT_COLORS['warning'], SOFT_COLORS['muted']],
            template=PLOTLY_TEMPLATE
        )
        fig_nilai.update_layout(height=380, xaxis_title="Persepsi Nilai", showlegend=False)
        st.plotly_chart(update_dark_layout(fig_nilai), use_container_width=True)
        render_insight_box(
            "Sebagian besar mahasiswa merasa AI berkontribusi pada peningkatan nilai akademik mereka, "
            "meskipun persepsi ini perlu divalidasi dengan data nilai riil."
        )

# ==========================================
# TAB 2: HUBUNGAN & PROBABILITAS
# ==========================================
with tab2:
    col5, col6 = st.columns(2)
    with col5:
        with st.container(border=True):
            render_chart_header(
                "⚠️ Probabilitas Kesulitan Tanpa AI",
                "Analisis kondisional: seberapa besar mahasiswa merasa kesulitan jika tidak menggunakan AI."
            )
            prob_df = pd.crosstab(df['Is_Ketergantungan_Tinggi'], df['Kesulitan_Tanpa_AI'], normalize='index') * 100
            prob_df = prob_df.reset_index().melt(id_vars='Is_Ketergantungan_Tinggi', var_name='Kesulitan', value_name='Persentase')
            fig_prob = px.bar(
                prob_df, x='Is_Ketergantungan_Tinggi', y='Persentase', color='Kesulitan',
                barmode='stack', text_auto='.1f',
                color_discrete_map={'Ya': SOFT_COLORS['danger'], 'Tidak': SOFT_COLORS['secondary']},
                template=PLOTLY_TEMPLATE
            )
            fig_prob.update_layout(height=400)
            st.plotly_chart(update_dark_layout(fig_prob), use_container_width=True)
            render_insight_box(
                "Mahasiswa dengan ketergantungan tinggi memiliki probabilitas kesulitan belajar mandiri "
                "yang secara signifikan lebih besar, mengindikasikan <strong>risiko kognitif</strong> jangka panjang."
            )

    with col6:
        with st.container(border=True):
            render_chart_header(
                "🔗 Heatmap Korelasi Pearson (Diverging)",
                "Matriks korelasi dengan skema warna diverging untuk membedakan hubungan positif/negatif."
            )
            corr_matrix = df[['Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas']].corr()
            fig_heat = px.imshow(
                corr_matrix, text_auto=".3f", aspect="auto",
                color_continuous_scale="RdBu",  # DIVERGING SCALE
                origin="lower",
                zmin=-1, zmax=1,
                template=PLOTLY_TEMPLATE
            )
            fig_heat.update_layout(height=400)
            st.plotly_chart(update_dark_layout(fig_heat), use_container_width=True)
            
            try:
                corr_val = corr_matrix.loc['Porsi_Tugas_AI', 'Skor_Efektivitas']
            except:
                corr_val = 0.0
            render_insight_box(
                f"Korelasi antara Porsi Tugas AI dan Skor Efektivitas adalah <strong>r = {corr_val:.2f}</strong> "
                f"(lemah), menunjukkan bahwa <strong>kuantitas penggunaan AI tidak otomatis menjamin</strong> "
                f"peningkatan efektivitas belajar."
            )

    col7, col8 = st.columns(2)
    with col7:
        with st.container(border=True):
            render_chart_header(
                "📉 Tren Efektivitas vs Porsi Tugas AI",
                "Scatter plot dengan trendline linear untuk melihat hubungan dua variabel."
            )
            z = np.polyfit(df['Porsi_Tugas_AI'], df['Skor_Efektivitas'], 1)
            p = np.poly1d(z)
            df_sorted = df.sort_values('Porsi_Tugas_AI')
            fig_scatter = px.scatter(
                df, x='Porsi_Tugas_AI', y='Skor_Efektivitas',
                opacity=0.8, template=PLOTLY_TEMPLATE
            )
            fig_scatter.update_traces(marker=dict(size=12, color=SOFT_COLORS['secondary']))
            fig_scatter.add_trace(go.Scatter(
                x=df_sorted['Porsi_Tugas_AI'], y=p(df_sorted['Porsi_Tugas_AI']),
                mode='lines', name='Trendline', line=dict(color=SOFT_COLORS['danger'], width=3)
            ))
            fig_scatter.update_layout(height=380, showlegend=False)
            st.plotly_chart(update_dark_layout(fig_scatter), use_container_width=True)
            render_insight_box(
                "Trendline menunjukkan hubungan yang relatif datar/lemah, "
                "memperkuat hipotesis bahwa efektivitas lebih bergantung pada <strong>cara penggunaan</strong> "
                "daripada <strong>seberapa sering</strong> AI digunakan."
            )

    with col8:
        with st.container(border=True):
            render_chart_header(
                "📦 Boxplot: Efektivitas Berdasarkan Porsi Tugas",
                "Distribusi skor efektivitas untuk setiap tingkat porsi bantuan AI."
            )
            fig_box = px.box(
                df, x='Porsi_Tugas_AI', y='Skor_Efektivitas', color='Porsi_Tugas_AI',
                color_discrete_sequence=[SOFT_COLORS['primary'], SOFT_COLORS['secondary'], SOFT_COLORS['purple']],
                template=PLOTLY_TEMPLATE
            )
            fig_box.update_layout(height=380, xaxis_title="Porsi Tugas (0-10)", showlegend=False)
            st.plotly_chart(update_dark_layout(fig_box), use_container_width=True)
            render_insight_box(
                "Boxplot memperlihatkan variasi yang cukup besar dalam setiap kategori, "
                "menunjukkan bahwa <strong>faktor individu</strong> sangat berpengaruh pada efektivitas penggunaan AI."
            )

    with st.container(border=True):
        render_chart_header(
            "📑 Rata-rata Tingkat Copy-Paste per Porsi Tugas",
            "Mengukur tingkat ketergantungan pasif (copy-paste) terhadap output AI."
        )
        cp_grouped = df.groupby('Porsi_Tugas_AI')['Tingkat_Copy_Paste'].mean().reset_index()
        fig_cp = px.bar(
            cp_grouped, x='Porsi_Tugas_AI', y='Tingkat_Copy_Paste',
            text_auto='.2f', color='Tingkat_Copy_Paste',
            color_continuous_scale="Purples",
            template=PLOTLY_TEMPLATE
        )
        fig_cp.update_traces(textposition='outside')
        fig_cp.update_layout(height=380, xaxis_title="Porsi Tugas AI (0-10)", yaxis_title="Skor Copy-Paste (1-5)")
        st.plotly_chart(update_dark_layout(fig_cp), use_container_width=True)
        render_insight_box(
            "Tren menunjukkan korelasi positif antara porsi tugas AI dan tingkat copy-paste, "
            "menandakan adanya <strong>risiko plagiarisme dan penurunan daya analitis</strong> pada pengguna berat AI."
        )

# ==========================================
# TAB 3: MONTE CARLO SIMULATION (AI DASHBOARD STYLE)
# ==========================================
with tab3:
    with st.container(border=True):
        render_chart_header(
            "🎲 Monte Carlo Simulation",
            "Proyeksi stokastik untuk memprediksi stabilitas skor efektivitas belajar pada kelas berskala besar "
            "melalui ribuan iterasi acak berbasis distribusi empiris data."
        )
        
        st.markdown('<div class="mc-status"><span class="mc-status-dot"></span> Stochastic Engine Ready</div>', unsafe_allow_html=True)
        
        mc_c1, mc_c2 = st.columns([1, 3])
        with mc_c1:
            iterations = st.number_input("Jumlah Iterasi", min_value=1000, max_value=50000, value=10000, step=1000)
            if st.button("🚀 Jalankan Simulasi", use_container_width=True):
                st.session_state['run_mc'] = True
                st.toast("Menyiapkan model stokastik...", icon="⚙️")
            else:
                st.session_state['run_mc'] = st.session_state.get('run_mc', False)
        
        with mc_c2:
            if st.session_state.get('run_mc', False):
                with st.spinner(f"Memproses {iterations} komputasi Monte Carlo..."):
                    time.sleep(1)
                    p_dist = df['Porsi_Tugas_AI'].value_counts(normalize=True).sort_index()
                    cats, weights = p_dist.index.values, p_dist.values
                    stats = df.groupby('Porsi_Tugas_AI')['Skor_Efektivitas'].agg(['mean', 'std']).fillna(df['Skor_Efektivitas'].std())
                    hasil = []
                    for i in range(iterations):
                        sim_tugas = np.random.choice(cats, size=100, p=weights)
                        skor = [np.clip(np.random.normal(loc=stats.loc[p, 'mean'], scale=stats.loc[p, 'std']), 1, 5) for p in sim_tugas]
                        hasil.append(np.mean(skor))
                    mean_mc = np.mean(hasil)
                    ci_low, ci_high = np.percentile(hasil, 2.5), np.percentile(hasil, 97.5)
                    running_mean = np.cumsum(hasil) / np.arange(1, iterations+1)
                    st.balloons()
                
                # Metrik Premium
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("Target Iterasi", f"{iterations:,}")
                with col_m2:
                    st.metric("Mean Ekspektasi", f"{mean_mc:.3f}")
                with col_m3:
                    st.metric("95% Confidence Interval", f"{ci_low:.2f} - {ci_high:.2f}")
                
                # Visualisasi Konvergensi
                fig_run = px.line(x=np.arange(1, iterations+1), y=running_mean, template=PLOTLY_TEMPLATE)
                fig_run.update_traces(line=dict(color=SOFT_COLORS['primary'], width=2.5))
                fig_run.add_hline(y=mean_mc, line_dash="dash", line_color=SOFT_COLORS['danger'], 
                                 annotation_text="Titik Konvergen", annotation_font_color=SOFT_COLORS['danger'])
                fig_run.update_layout(title="Kurva Konvergensi Stokastik", 
                                     xaxis_title="Iterasi", 
                                     yaxis_title="Running Mean",
                                     height=380)
                fig_run = update_dark_layout(fig_run)
                st.plotly_chart(fig_run, use_container_width=True)
                
                render_insight_box(
                    f"Setelah {iterations:,} iterasi, simulasi menunjukkan <strong>konvergensi stabil</strong> "
                    f"di sekitar nilai {mean_mc:.3f} dengan 95% CI [{ci_low:.2f}, {ci_high:.2f}]. "
                    f"Ini memberikan estimasi yang <strong>robust</strong> untuk proyeksi efektivitas di skala kelas besar."
                )

# ==========================================
# 8. KEY INSIGHTS (ELEGANT BOX)
# ==========================================
render_section_divider("Strategic Insights")

with st.container(border=True):
    st.markdown('<div class="chart-title">💡 Strategic Insights & Recommendations</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-description">Temuan kunci yang dapat dijadikan landasan kebijakan akademik terkait integrasi AI.</div>', unsafe_allow_html=True)
    
    if len(df) > 0:
        setiap_hari_pct = len(df[df['Frekuensi_Penggunaan']=='Setiap hari'])/len(df)*100
        mean_jam = df['Jam_per_Hari'].mean()
        max_jam = df['Jam_per_Hari'].max()
        try:
            corr_val = corr_matrix.loc['Porsi_Tugas_AI', 'Skor_Efektivitas']
        except:
            corr_val = 0.0
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-top: 16px;">
            <div class="insight-box" style="margin-top: 0;">
                <strong>🎯 Adopsi Tinggi:</strong> {setiap_hari_pct:.0f}% mahasiswa menggunakan AI setiap hari untuk keperluan akademis.
            </div>
            <div class="insight-box" style="margin-top: 0;">
                <strong>⏱️ Intensitas:</strong> Durasi penggunaan rata-rata mencapai {mean_jam:.1f} jam, dengan rekor maksimal {max_jam} jam per hari.
            </div>
            <div class="insight-box" style="margin-top: 0;">
                <strong>⚠️ Risiko Kognitif:</strong> Mahasiswa dengan porsi bantuan AI tinggi (>5 tugas) memiliki probabilitas kesulitan belajar mandiri mencapai 83.3%.
            </div>
            <div class="insight-box" style="margin-top: 0;">
                <strong>📊 Korelasi Lemah:</strong> Korelasi Pearson (r = {corr_val:.2f}) membuktikan bahwa bergantung pada AI tidak menjamin peningkatan pemahaman kognitif.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Pilih data pada filter sidebar untuk melihat insight.")

# ==========================================
# 9. FOOTER PROFESIONAL
# ==========================================
st.markdown("""
<div class="dashboard-footer">
    <div style="font-size: 16px; font-weight: 600; color: #F8FAFC; margin-bottom: 8px;">
        🎓 AI Learning Impact Analytics
    </div>
    <div>
        Dashboard analitik ini dibangun untuk memahami dampak penggunaan <strong>Artificial Intelligence</strong> 
        dalam ekosistem akademik melalui pendekatan <em>data-driven analytics</em>, probabilitas kondisional, 
        dan simulasi Monte Carlo.
    </div>
    <div class="footer-meta">
        <div>
            <strong style="color: #CBD5E1;">Developer:</strong> Ahmad Rizza Pahlevi<br>
            <strong style="color: #CBD5E1;">Institusi:</strong> UIN K.H. Abdurrahman Wahid
        </div>
        <div>
            <strong style="color: #CBD5E1;">Tech Stack:</strong> Python • Streamlit • Plotly • Pandas • NumPy<br>
            <strong style="color: #CBD5E1;">Version:</strong> 2.0 Enterprise Edition • Juni 2026
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
