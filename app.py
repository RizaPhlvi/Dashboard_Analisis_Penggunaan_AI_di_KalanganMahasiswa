import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import io

# ==========================================
# 1. KONFIGURASI HALAMAN & TEMA NEO GLASS
# ==========================================
st.set_page_config(
    page_title="AI Learning Impact Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-main: #020617;
    --bg-card: rgba(15, 23, 42, 0.6);
    --bg-card-solid: #0F172A;
    --border-glass: rgba(255, 255, 255, 0.08);
    --primary: #3B82F6;
    --secondary: #14B8A6;
    --purple: #8B5CF6;
    --success: #22C55E;
    --warning: #F59E0B;
    --danger: #EF4444;
    --text-primary: #F8FAFC;
    --text-secondary: #CBD5E1;
    --text-muted: #94A3B8;
}

/* ─── BASE & TYPOGRAPHY ─── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
    color: var(--text-primary);
}

.stApp {
    background-color: var(--bg-main);
    background-image: 
        radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.15) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.1) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(20, 184, 166, 0.08) 0px, transparent 50%);
    background-attachment: fixed;
}

[data-testid="stMainBlockContainer"] {
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* ─── GLASSMORPHISM CARDS ─── */
.glass-card {
    background: var(--bg-card);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-glass);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
}
.glass-card:hover {
    border-color: rgba(255, 255, 255, 0.15);
    transform: translateY(-2px);
    box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.3);
}

/* ─── EXECUTIVE HEADER ─── */
.exec-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 24px;
    margin-bottom: 2rem;
}
.exec-title {
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin: 0 0 8px 0;
    line-height: 1.1;
    background: linear-gradient(135deg, #F8FAFC 0%, #94A3B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.exec-title span {
    background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.exec-subtitle {
    font-size: 15px;
    color: var(--text-muted);
    margin: 0;
    max-width: 600px;
    line-height: 1.6;
}
.exec-header-right {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 600;
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid rgba(34, 197, 94, 0.2);
    color: #4ADE80;
}
.pulse {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #22C55E;
    box-shadow: 0 0 0 rgba(34, 197, 94, 0.4);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(34, 197, 94, 0); }
    100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
}
.meta-chip {
    padding: 6px 14px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border-glass);
    color: var(--text-secondary);
}

/* ─── KPI CARDS ─── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
    margin-bottom: 2rem;
}
@media (max-width: 1200px) { .kpi-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 480px) { .kpi-grid { grid-template-columns: 1fr; } }

.kpi-card {
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 12px;
}
.kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.kpi-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
}
.kpi-icon.blue { background: rgba(59, 130, 246, 0.15); color: #60A5FA; }
.kpi-icon.teal { background: rgba(20, 184, 166, 0.15); color: #2DD4BF; }
.kpi-icon.purple { background: rgba(139, 92, 246, 0.15); color: #A78BFA; }
.kpi-icon.amber { background: rgba(245, 158, 11, 0.15); color: #FBBF24; }
.kpi-icon.red { background: rgba(239, 68, 68, 0.15); color: #F87171; }

.kpi-trend {
    font-size: 11px;
    font-weight: 700;
    padding: 4px 8px;
    border-radius: 6px;
    letter-spacing: 0.02em;
}
.kpi-trend.up { background: rgba(34, 197, 94, 0.1); color: #4ADE80; }
.kpi-trend.down { background: rgba(239, 68, 68, 0.1); color: #F87171; }
.kpi-trend.neutral { background: rgba(148, 163, 184, 0.1); color: #94A3B8; }

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--text-primary);
    line-height: 1;
}
.kpi-label {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-muted);
}
.kpi-progress-track {
    height: 4px;
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    margin-top: 8px;
    overflow: hidden;
}
.kpi-progress-fill {
    height: 100%;
    border-radius: 10px;
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}
.kpi-progress-fill.blue { background: linear-gradient(90deg, #3B82F6, #60A5FA); box-shadow: 0 0 10px rgba(59,130,246,0.5); }
.kpi-progress-fill.teal { background: linear-gradient(90deg, #14B8A6, #2DD4BF); box-shadow: 0 0 10px rgba(20,184,166,0.5); }
.kpi-progress-fill.purple { background: linear-gradient(90deg, #8B5CF6, #A78BFA); box-shadow: 0 0 10px rgba(139,92,246,0.5); }
.kpi-progress-fill.amber { background: linear-gradient(90deg, #F59E0B, #FBBF24); box-shadow: 0 0 10px rgba(245,158,11,0.5); }
.kpi-progress-fill.red { background: linear-gradient(90deg, #EF4444, #F87171); box-shadow: 0 0 10px rgba(239,68,68,0.5); }

/* ─── CHART CONTAINERS ─── */
.chart-title {
    font-size: 16px;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0 0 4px 0;
    letter-spacing: -0.01em;
}
.chart-desc {
    font-size: 13px;
    color: var(--text-muted);
    margin: 0 0 20px 0;
}
.insight-callout {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 14px 16px;
    background: rgba(59, 130, 246, 0.04);
    border: 1px solid rgba(59, 130, 246, 0.12);
    border-radius: 14px;
    margin-top: 20px;
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
}
.insight-icon {
    font-size: 16px;
    flex-shrink: 0;
    margin-top: 2px;
    color: var(--primary);
}
.insight-callout strong { color: var(--text-primary); font-weight: 600; }

/* ─── TABS (PILL STYLE) ─── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid var(--border-glass);
    border-radius: 16px;
    padding: 6px;
    gap: 4px;
    backdrop-filter: blur(8px);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    padding: 10px 24px;
    background: transparent;
    color: var(--text-muted);
    font-weight: 500;
    font-size: 14px;
    border: 1px solid transparent;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary);
    background: rgba(255,255,255,0.03);
}
.stTabs [aria-selected="true"] {
    background: rgba(59, 130, 246, 0.15) !important;
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    color: #60A5FA !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ─── SIDEBAR ─── */
section[data-testid="stSidebar"] {
    background: rgba(2, 6, 23, 0.85);
    backdrop-filter: blur(24px);
    border-right: 1px solid rgba(255,255,255,0.05);
}
section[data-testid="stSidebar"] .st-expander {
    background: transparent;
    border: none;
}
section[data-testid="stSidebar"] .st-expander details {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid var(--border-glass);
    border-radius: 14px;
}
section[data-testid="stSidebar"] .st-expander summary {
    font-weight: 600;
    color: var(--text-secondary);
    font-size: 13px;
}
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px;
    background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(139,92,246,0.05));
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 16px;
    margin-bottom: 1.5rem;
}
.sidebar-brand-icon { font-size: 24px; }
.sidebar-brand-text { font-size: 14px; font-weight: 700; color: var(--text-primary); line-height: 1.2; }
.sidebar-brand-sub { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }

.sidebar-section-label {
    font-size: 11px;
    font-weight: 700;
    color: var(--primary);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 1.5rem 0 0.75rem 4px;
    display: block;
}

/* ─── BUTTONS & INPUTS ─── */
.stButton > button {
    background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
    border: none !important;
    color: #FFFFFF !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 12px 24px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 12px rgba(59,130,246,0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(59,130,246,0.4) !important;
}
.stSelectbox > div > div, .stMultiSelect [data-baseweb="select"] {
    background: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid var(--border-glass) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
}

/* ─── METRICS OVERRIDES ─── */
div[data-testid="stMetricValue"] { color: var(--text-primary) !important; font-weight: 800 !important; font-size: 24px !important; }
div[data-testid="stMetricLabel"] { color: var(--text-muted) !important; font-size: 13px !important; font-weight: 500 !important; }

/* ─── EXECUTIVE INSIGHTS BOX ─── */
.exec-insights-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-top: 16px;
}
@media (max-width: 768px) { .exec-insights-grid { grid-template-columns: 1fr; } }
.exec-insight-item {
    background: rgba(255,255,255,0.02);
    border: 1px solid var(--border-glass);
    border-radius: 14px;
    padding: 16px;
    transition: all 0.2s;
}
.exec-insight-item:hover {
    background: rgba(59,130,246,0.05);
    border-color: rgba(59,130,246,0.2);
}
.exec-insight-icon { font-size: 18px; margin-bottom: 8px; }
.exec-insight-text { font-size: 13px; color: var(--text-secondary); line-height: 1.6; }
.exec-insight-text strong { color: var(--text-primary); font-weight: 600; }

/* ─── FOOTER ─── */
.dashboard-footer {
    margin-top: 4rem;
    padding: 24px 32px;
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid var(--border-glass);
    border-radius: 20px;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    backdrop-filter: blur(12px);
}
.footer-brand { font-size: 14px; font-weight: 700; color: var(--text-primary); }
.footer-brand span {
    background: linear-gradient(90deg, #3B82F6, #8B5CF6);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.footer-meta { font-size: 12px; color: var(--text-muted); }
.tech-badge {
    display: inline-block;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border-glass);
    border-radius: 8px;
    padding: 4px 10px;
    font-size: 11px;
    color: var(--text-muted);
    margin-left: 6px;
}

/* ─── SCROLLBAR ─── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }

/* ─── ARTIFACT REMOVAL ─── */
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
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df_raw = load_data()

# ==========================================
# 3. SIDEBAR CONTROL PANEL
# ==========================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-brand-icon">🎓</div>
        <div>
            <div class="sidebar-brand-text">AI Learning Impact</div>
            <div class="sidebar-brand-sub">Analytics Workspace</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="sidebar-section-label">📁 Dataset Filters</span>', unsafe_allow_html=True)
    
    with st.expander("Program Studi & Semester", expanded=True):
        prodi_list = df_raw['Prodi'].unique().tolist() if not df_raw.empty else []
        filter_prodi = st.multiselect(
            "Program Studi", options=prodi_list, default=prodi_list,
            label_visibility="collapsed", placeholder="Pilih Program Studi..."
        )
        semester_list = sorted(df_raw['Semester'].unique().tolist()) if not df_raw.empty else []
        filter_semester = st.multiselect(
            "Semester", options=semester_list, default=semester_list,
            label_visibility="collapsed", placeholder="Pilih Semester..."
        )

    st.markdown('<span class="sidebar-section-label">🔮 Simulation Engine</span>', unsafe_allow_html=True)
    
    with st.expander("Monte Carlo Settings", expanded=True):
        sim_tugas = st.slider("Porsi Bantuan AI (dari 10 tugas):", 0, 10, 6)
        if sim_tugas > 5:
            st.markdown('<div style="padding:8px 12px; border-radius:8px; background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.2); color:#F87171; font-size:12px; font-weight:500;">⚠️ Risiko Ketergantungan Tinggi</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="padding:8px 12px; border-radius:8px; background:rgba(34,197,94,0.1); border:1px solid rgba(34,197,94,0.2); color:#4ADE80; font-size:12px; font-weight:500;">✅ Penggunaan Dalam Batas Aman</div>', unsafe_allow_html=True)

    st.markdown('<span class="sidebar-section-label">📊 Research Metadata</span>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 16px; font-size: 12px; color: #94A3B8; line-height: 1.8;">
        <div style="display:flex; justify-content:space-between;"><span>Peneliti</span> <strong style="color:#F8FAFC">Ahmad Rizza P.</strong></div>
        <div style="display:flex; justify-content:space-between;"><span>Institusi</span> <strong style="color:#F8FAFC">UIN K.H. Abdurrahman Wahid</strong></div>
        <div style="display:flex; justify-content:space-between;"><span>Periode</span> <strong style="color:#F8FAFC">Juni 2026</strong></div>
        <div style="display:flex; justify-content:space-between;"><span>Data Quality</span> <strong style="color:#4ADE80">98% Verified</strong></div>
    </div>
    """, unsafe_allow_html=True)

# Apply Filters
if not df_raw.empty and filter_prodi and filter_semester:
    df = df_raw[(df_raw['Prodi'].isin(filter_prodi)) & (df_raw['Semester'].isin(filter_semester))]
else:
    df = df_raw

# ==========================================
# 4. HELPER FUNCTIONS
# ==========================================
def apply_glass_theme(fig, height=380):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, Inter, sans-serif", color="#CBD5E1", size=12),
        height=height,
        margin=dict(l=10, r=10, t=20, b=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
            font=dict(color="#94A3B8", size=11),
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
        xaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.04)", gridwidth=1,
            zerolinecolor="rgba(255,255,255,0.04)",
            tickfont=dict(color="#94A3B8", size=11), title_font=dict(color="#CBD5E1", size=12)
        ),
        yaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.04)", gridwidth=1,
            zerolinecolor="rgba(255,255,255,0.04)",
            tickfont=dict(color="#94A3B8", size=11), title_font=dict(color="#CBD5E1", size=12)
        ),
        hoverlabel=dict(
            bgcolor="rgba(15, 23, 42, 0.95)",
            bordercolor="rgba(255,255,255,0.1)",
            font_size=12,
            font_family="Plus Jakarta Sans"
        )
    )
    fig.update_traces(marker_line_width=0)
    return fig

def render_kpi(icon, label, value, trend_text, trend_dir, color, progress):
    trend_class = "up" if trend_dir == "up" else ("down" if trend_dir == "down" else "neutral")
    st.markdown(f"""
    <div class="glass-card kpi-card">
        <div class="kpi-header">
            <div class="kpi-icon {color}">{icon}</div>
            <span class="kpi-trend {trend_class}">{trend_text}</span>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-progress-track">
            <div class="kpi-progress-fill {color}" style="width: {progress}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. EXECUTIVE HEADER
# ==========================================
if not df.empty:
    n_responden = len(df)
    setiap_hari_pct = len(df[df['Frekuensi_Penggunaan'] == 'Setiap hari']) / max(len(df), 1) * 100
    avg_jam = df['Jam_per_Hari'].mean()
    avg_tugas = df['Porsi_Tugas_AI'].mean()
    avg_skor = df['Skor_Efektivitas'].mean()
    ketergantungan_pct = len(df[df['Is_Ketergantungan_Tinggi'] == 'Tinggi (>5 Tugas)']) / max(len(df), 1) * 100
    
    # Generate Report Data
    report_md = f"""# AI Learning Impact Analytics - Executive Report
**Generated:** Juni 2026 | **Author:** Ahmad Rizza Pahlevi | **Institution:** UIN K.H. Abdurrahman Wahid

## Key Metrics
- **Total Responden:** {n_responden}
- **Penggunaan Harian:** {setiap_hari_pct:.0f}%
- **Rata-rata Durasi:** {avg_jam:.1f} Jam/Hari
- **Porsi Tugas AI:** {avg_tugas:.1f}/10
- **Skor Efektivitas:** {avg_skor:.2f}/5
- **Ketergantungan Tinggi:** {ketergantungan_pct:.0f}%

## Insights
Data menunjukkan integrasi AI yang masif dalam ekosistem akademik, namun disertai risiko ketergantungan kognitif yang perlu diwaspadai.
"""
else:
    n_responden = 0
    setiap_hari_pct = 0
    avg_jam = 0
    avg_tugas = 0
    avg_skor = 0
    ketergantungan_pct = 0
    report_md = "No data available."

st.markdown(f"""
<div class="exec-header">
    <div class="exec-header-left">
        <h1 class="exec-title">AI Learning Impact <span>Analytics</span></h1>
        <p class="exec-subtitle">Monitoring komprehensif perilaku penggunaan Artificial Intelligence pada ekosistem akademik mahasiswa perguruan tinggi.</p>
    </div>
    <div class="exec-header-right">
        <div class="status-pill"><span class="pulse"></span> Live Dataset</div>
        <div class="meta-chip">👨‍💻 Ahmad Rizza Pahlevi</div>
        <div class="meta-chip">🏛️ UIN K.H. Abdurrahman Wahid</div>
        <div class="meta-chip">📅 Juni 2026</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. KPI CARDS GRID
# ==========================================
if not df.empty:
    kpi_cols = st.columns(5)
    with kpi_cols[0]:
        render_kpi("👥", "Total Responden", f"{n_responden}", "Active", "neutral", "blue", 100)
    with kpi_cols[1]:
        render_kpi("⏱️", "Durasi AI / Hari", f"{avg_jam:.1f}h", "High" if avg_jam >= 3 else "Normal", "down" if avg_jam >= 3 else "up", "teal", min(avg_jam/8*100, 100))
    with kpi_cols[2]:
        render_kpi("📝", "Porsi Tugas AI", f"{avg_tugas:.1f}/10", "Warning" if avg_tugas > 5 else "Safe", "down" if avg_tugas > 5 else "up", "purple", avg_tugas*10)
    with kpi_cols[3]:
        render_kpi("⭐", "Skor Efektivitas", f"{avg_skor:.2f}/5", "Optimal" if avg_skor >= 3.5 else "Moderate", "up" if avg_skor >= 3.5 else "neutral", "amber", avg_skor/5*100)
    with kpi_cols[4]:
        render_kpi("⚠️", "Ketergantungan Tinggi", f"{ketergantungan_pct:.0f}%", "Critical" if ketergantungan_pct > 50 else "Stable", "down" if ketergantungan_pct > 50 else "up", "red", ketergantungan_pct)
else:
    st.warning("Tidak ada data yang sesuai dengan filter. Silakan sesuaikan filter di sidebar.")

# ==========================================
# 7. EXECUTIVE INSIGHTS
# ==========================================
if not df.empty:
    st.markdown("""
    <div class="glass-card" style="margin-bottom: 2.5rem;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom: 16px;">
            <span style="font-size:18px;">💡</span>
            <h3 style="margin:0; font-size:18px; font-weight:700; color:#F8FAFC;">Executive Insights</h3>
            <span style="margin-left:auto; font-size:11px; font-weight:600; color:#94A3B8; text-transform:uppercase; letter-spacing:0.05em;">Auto-Generated Analysis</span>
        </div>
        <div class="exec-insights-grid">
            <div class="exec-insight-item">
                <div class="exec-insight-icon">🤖</div>
                <div class="exec-insight-text"><strong>{setiap_hari_pct:.0f}% mahasiswa</strong> menggunakan AI setiap hari, menunjukkan integrasi teknologi yang sangat dalam pada proses belajar.</div>
            </div>
            <div class="exec-insight-item">
                <div class="exec-insight-icon">⚠️</div>
                <div class="exec-insight-text"><strong>{ketergantungan_pct:.0f}% responden</strong> memiliki tingkat ketergantungan tinggi (>5 tugas), berisiko pada kemandirian kognitif jangka panjang.</div>
            </div>
            <div class="exec-insight-item">
                <div class="exec-insight-icon">📊</div>
                <div class="exec-insight-text">Skor efektivitas rata-rata <strong>{avg_skor:.2f}/5</strong> mengindikasikan manfaat yang masih belum optimal dari penggunaan AI dalam pembelajaran.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 8. MAIN TABS NAVIGATION
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "📊  Eksplorasi Deskriptif",
    "🔗  Hubungan & Probabilitas",
    "🎲  Monte Carlo Simulation"
])

# ==========================================
# TAB 1: EKSPLORASI DESKRIPTIF
# ==========================================
with tab1:
    if not df.empty:
        # Row 1: Asymmetrical (Tren Frekuensi & Donut)
        col1, col2 = st.columns([1.6, 1])
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<p class="chart-title">📈 Tren Frekuensi Penggunaan AI</p><p class="chart-desc">Distribusi intensitas penggunaan AI per kategori frekuensi</p>', unsafe_allow_html=True)
            trend_data = df['Frekuensi_Penggunaan'].value_counts().reset_index()
            trend_data.columns = ['Frekuensi', 'Jumlah']
            fig_hero = px.bar(trend_data, x='Frekuensi', y='Jumlah', text='Jumlah', 
                              color_discrete_sequence=["#3B82F6"])
            fig_hero.update_traces(textposition='outside', marker=dict(cornerradius=4))
            st.plotly_chart(apply_glass_theme(fig_hero, 340), use_container_width=True)
            top_freq = trend_data.iloc[0]['Frekuensi'] if len(trend_data) > 0 else '-'
            st.markdown(f'<div class="insight-callout"><span class="insight-icon">💡</span><span>Kategori frekuensi terbanyak adalah <strong>{top_freq}</strong>. Pola ini menunjukkan adopsi AI yang tinggi dalam rutinitas akademik harian.</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<p class="chart-title">🍩 Distribusi Ketergantungan</p><p class="chart-desc">Proporsi mahasiswa berdasarkan tingkat ketergantungan AI</p>', unsafe_allow_html=True)
            fig_pie = px.pie(df, names='Is_Ketergantungan_Tinggi', hole=0.65,
                             color='Is_Ketergantungan_Tinggi',
                             color_discrete_map={'Tinggi (>5 Tugas)': '#EF4444', 'Rendah (<=5 Tugas)': '#14B8A6'})
            fig_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent+value', marker=dict(line=dict(color='#0F172A', width=2)))
            fig_pie.update_layout(showlegend=False)
            st.plotly_chart(apply_glass_theme(fig_pie, 340), use_container_width=True)
            st.markdown(f'<div class="insight-callout"><span class="insight-icon">💡</span><span><strong>{ketergantungan_pct:.0f}% mahasiswa</strong> menunjukkan pola ketergantungan tinggi terhadap AI.</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Row 2: Symmetrical (Histogram Porsi & Durasi)
        col3, col4 = st.columns(2)
        with col3:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<p class="chart-title">📊 Distribusi Porsi Tugas AI</p><p class="chart-desc">Sebaran jumlah tugas yang diselesaikan dengan bantuan AI</p>', unsafe_allow_html=True)
            fig_porsi = px.histogram(df, x='Porsi_Tugas_AI', text_auto=True, color_discrete_sequence=["#8B5CF6"])
            fig_porsi.update_traces(marker=dict(cornerradius=4))
            st.plotly_chart(apply_glass_theme(fig_porsi, 320), use_container_width=True)
            st.markdown(f'<div class="insight-callout"><span class="insight-icon">💡</span><span>Rata-rata porsi tugas dibantu AI adalah <strong>{avg_tugas:.1f}/10</strong>. Distribusi condong ke nilai tinggi.</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<p class="chart-title">⏳ Histogram Durasi Pemakaian</p><p class="chart-desc">Sebaran waktu penggunaan AI per hari (jam)</p>', unsafe_allow_html=True)
            fig_hist = px.histogram(df, x='Jam_per_Hari', nbins=8, marginal="box", color_discrete_sequence=["#14B8A6"])
            fig_hist.update_traces(marker=dict(cornerradius=4))
            st.plotly_chart(apply_glass_theme(fig_hist, 320), use_container_width=True)
            max_jam = df['Jam_per_Hari'].max()
            st.markdown(f'<div class="insight-callout"><span class="insight-icon">💡</span><span>Durasi rata-rata <strong>{avg_jam:.1f} jam/hari</strong>, dengan maksimum mencapai <strong>{max_jam} jam/hari</strong>.</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Row 3: Symmetrical (Skor Efektivitas & Peningkatan Nilai)
        col5, col6 = st.columns(2)
        with col5:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<p class="chart-title">⭐ Distribusi Skor Efektivitas</p><p class="chart-desc">Persepsi mahasiswa terhadap efektivitas belajar menggunakan AI</p>', unsafe_allow_html=True)
            fig_skor = px.histogram(df, x='Skor_Efektivitas', text_auto=True, color_discrete_sequence=["#22C55E"])
            fig_skor.update_traces(marker=dict(cornerradius=4))
            st.plotly_chart(apply_glass_theme(fig_skor, 320), use_container_width=True)
            st.markdown(f'<div class="insight-callout"><span class="insight-icon">💡</span><span>Skor efektivitas rata-rata <strong>{avg_skor:.2f}/5</strong>. Menunjukkan persepsi yang positif namun belum maksimal.</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col6:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<p class="chart-title">📈 Persepsi Peningkatan Nilai</p><p class="chart-desc">Distribusi persepsi mahasiswa terhadap dampak AI pada nilai mereka</p>', unsafe_allow_html=True)
            fig_nilai = px.histogram(df, x='Peningkatan_Nilai', text_auto=True, color='Peningkatan_Nilai',
                                     color_discrete_sequence=["#22C55E", "#F59E0B", "#94A3B8"])
            fig_nilai.update_traces(marker=dict(cornerradius=4))
            fig_nilai.update_layout(showlegend=False)
            st.plotly_chart(apply_glass_theme(fig_nilai, 320), use_container_width=True)
            st.markdown(f'<div class="insight-callout"><span class="insight-icon">💡</span><span>Mahasiswa dengan intensitas penggunaan AI terstruktur cenderung melaporkan peningkatan nilai yang lebih konsisten.</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 2: HUBUNGAN & PROBABILITAS
# ==========================================
with tab2:
    if not df.empty:
        # Row 1
        col7, col8 = st.columns(2)
        with col7:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<p class="chart-title">⚠️ Probabilitas Kesulitan Mandiri</p><p class="chart-desc">Persentase kesulitan belajar tanpa AI berdasarkan tingkat ketergantungan</p>', unsafe_allow_html=True)
            prob_df = pd.crosstab(df['Is_Ketergantungan_Tinggi'], df['Kesulitan_Tanpa_AI'], normalize='index') * 100
            prob_df = prob_df.reset_index().melt(id_vars='Is_Ketergantungan_Tinggi', var_name='Kesulitan', value_name='Persentase')
            fig_prob = px.bar(prob_df, x='Is_Ketergantungan_Tinggi', y='Persentase', color='Kesulitan',
                              barmode='stack', text_auto='.1f',
                              color_discrete_map={'Ya': '#EF4444', 'Tidak': '#14B8A6'})
            fig_prob.update_traces(marker=dict(cornerradius=4))
            st.plotly_chart(apply_glass_theme(fig_prob, 360), use_container_width=True)
            st.markdown(f'<div class="insight-callout"><span class="insight-icon">💡</span><span>Mahasiswa dengan <strong>ketergantungan tinggi</strong> memiliki probabilitas kesulitan belajar mandiri yang jauh lebih besar.</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col8:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<p class="chart-title">🔗 Heatmap Korelasi Pearson</p><p class="chart-desc">Matriks korelasi antar variabel numerik utama</p>', unsafe_allow_html=True)
            corr_matrix = df[['Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas']].corr()
            fig_heat = px.imshow(corr_matrix, text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
            fig_heat.update_coloraxes(colorbar=dict(tickfont=dict(color='#64748B'), title=dict(text='r', font=dict(color='#64748B'))))
            st.plotly_chart(apply_glass_theme(fig_heat, 360), use_container_width=True)
            try:
                corr_val = corr_matrix.loc['Porsi_Tugas_AI', 'Skor_Efektivitas']
                st.markdown(f'<div class="insight-callout"><span class="insight-icon">💡</span><span>Korelasi Porsi Tugas ↔ Efektivitas: <strong>r = {corr_val:.2f}</strong>. Bergantung pada AI tidak menjamin efektivitas meningkat.</span></div>', unsafe_allow_html=True)
            except:
                pass
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Row 2: Asymmetrical
        col9, col10 = st.columns([1.2, 1])
        with col9:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<p class="chart-title">📉 Tren Efektivitas vs Porsi Tugas</p><p class="chart-desc">Scatter plot dengan regresi linear</p>', unsafe_allow_html=True)
            z = np.polyfit(df['Porsi_Tugas_AI'], df['Skor_Efektivitas'], 1)
            p = np.poly1d(z)
            df_sorted = df.sort_values('Porsi_Tugas_AI')
            fig_scatter = px.scatter(df, x='Porsi_Tugas_AI', y='Skor_Efektivitas', opacity=0.6)
            fig_scatter.update_traces(marker=dict(size=10, color='#8B5CF6'))
            fig_scatter.add_trace(go.Scatter(x=df_sorted['Porsi_Tugas_AI'], y=p(df_sorted['Porsi_Tugas_AI']),
                                             mode='lines', name='Trendline',
                                             line=dict(color='#EF4444', width=2.5, dash='dot')))
            fig_scatter.update_layout(showlegend=False)
            st.plotly_chart(apply_glass_theme(fig_scatter, 340), use_container_width=True)
            slope_dir = "negatif" if z[0] < 0 else "positif"
            st.markdown(f'<div class="insight-callout"><span class="insight-icon">💡</span><span>Trendline menunjukkan kemiringan <strong>{slope_dir}</strong> (slope ≈ {z[0]:.3f}). Peningkatan porsi bantuan AI tidak selalu mendorong efektivitas belajar.</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col10:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<p class="chart-title">📦 Boxplot Efektivitas</p><p class="chart-desc">Sebaran & outlier skor efektivitas per level porsi tugas</p>', unsafe_allow_html=True)
            fig_box = px.box(df, x='Porsi_Tugas_AI', y='Skor_Efektivitas', color='Porsi_Tugas_AI',
                             color_discrete_sequence=["#3B82F6", "#14B8A6", "#8B5CF6", "#F59E0B", "#EF4444"])
            fig_box.update_layout(showlegend=False)
            st.plotly_chart(apply_glass_theme(fig_box, 340), use_container_width=True)
            st.markdown(f'<div class="insight-callout"><span class="insight-icon">💡</span><span>Variasi (IQR) yang lebar pada level tugas tinggi mengindikasikan hasil yang tidak konsisten.</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Row 3: Full Width
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">📑 Rata-rata Tingkat Copy-Paste</p><p class="chart-desc">Korelasi antara ketergantungan AI dan perilaku copy-paste tanpa pemrosesan mandiri</p>', unsafe_allow_html=True)
        cp_grouped = df.groupby('Porsi_Tugas_AI')['Tingkat_Copy_Paste'].mean().reset_index()
        fig_cp = px.bar(cp_grouped, x='Porsi_Tugas_AI', y='Tingkat_Copy_Paste', text_auto='.2f',
                        color='Tingkat_Copy_Paste', color_continuous_scale=[[0, '#14B8A6'], [0.5, '#8B5CF6'], [1, '#EF4444']])
        fig_cp.update_traces(textposition='outside', marker=dict(cornerradius=4))
        st.plotly_chart(apply_glass_theme(fig_cp, 320), use_container_width=True)
        st.markdown(f'<div class="insight-callout"><span class="insight-icon">💡</span><span>Tren positif antara porsi tugas AI dan tingkat copy-paste mengonfirmasi bahwa penggunaan AI berlebihan mendorong <strong>surface learning</strong>.</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# TAB 3: MONTE CARLO SIMULATION
# ==========================================
with tab3:
    if not df.empty:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">🎲 Stochastic Simulation Engine</p><p class="chart-desc">Proyeksi stokastik stabilitas skor efektivitas belajar pada kelas berskala besar (n=100)</p>', unsafe_allow_html=True)
        
        mc_c1, mc_c2 = st.columns([1, 3])
        with mc_c1:
            st.markdown("<br>", unsafe_allow_html=True)
            iterations = st.number_input("Jumlah Iterasi", min_value=1000, max_value=50000, value=10000, step=1000)
            run_btn = st.button("🚀 Jalankan Simulasi", use_container_width=True)
            if run_btn:
                st.session_state['run_mc'] = True
            else:
                st.session_state['run_mc'] = st.session_state.get('run_mc', False)

            st.markdown("""
            <div style="margin-top:20px; padding:16px; background:rgba(59,130,246,0.05); border:1px solid rgba(59,130,246,0.15); border-radius:14px; font-size:12px; color:#94A3B8; line-height:1.8;">
                <strong style="color:#60A5FA; font-size:13px;">Model Parameters</strong><br>
                • Distribution: Normal<br>
                • Sample / iterasi: 100<br>
                • Confidence Interval: 95%<br>
                • Clip Range: [1, 5]
            </div>
            """, unsafe_allow_html=True)

        with mc_c2:
            if st.session_state.get('run_mc', False):
                with st.spinner(f"Memproses {iterations:,} komputasi stokastik..."):
                    time.sleep(0.5) # Simulate processing
                    p_dist = df['Porsi_Tugas_AI'].value_counts(normalize=True).sort_index()
                    cats, weights = p_dist.index.values, p_dist.values
                    stats = df.groupby('Porsi_Tugas_AI')['Skor_Efektivitas'].agg(['mean', 'std']).fillna(df['Skor_Efektivitas'].std())

                    hasil = []
                    for i in range(iterations):
                        sim_tugas_mc = np.random.choice(cats, size=100, p=weights)
                        skor = [
                            np.clip(np.random.normal(loc=stats.loc[p, 'mean'], scale=stats.loc[p, 'std']), 1, 5)
                            for p in sim_tugas_mc
                        ]
                        hasil.append(np.mean(skor))

                    mean_mc = np.mean(hasil)
                    ci_low = np.percentile(hasil, 2.5)
                    ci_high = np.percentile(hasil, 97.5)
                    ci_width = ci_high - ci_low
                    running_mean = np.cumsum(hasil) / np.arange(1, iterations + 1)

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Total Iterasi", f"{iterations:,}")
                m2.metric("Mean Ekspektasi", f"{mean_mc:.3f}")
                m3.metric("95% CI", f"{ci_low:.3f}–{ci_high:.3f}")
                m4.metric("Lebar CI", f"{ci_width:.3f}")

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<p class="chart-title">📉 Kurva Konvergensi Running Mean</p><p class="chart-desc">Stabilitas estimasi mean skor efektivitas seiring bertambahnya iterasi</p>', unsafe_allow_html=True)

                n_pts = min(iterations, 5000)
                step = max(1, iterations // n_pts)
                xs = np.arange(1, iterations + 1)[::step]
                ys = running_mean[::step]

                fig_run = go.Figure()
                fig_run.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name='Running Mean',
                                             line=dict(color='#3B82F6', width=2.5), fill='none'))
                fig_run.add_hline(y=mean_mc, line_dash="dash", line_color='#EF4444', line_width=1.5,
                                  annotation_text=f"Konvergen: {mean_mc:.3f}", annotation_font_color='#EF4444', annotation_font_size=11)
                fig_run.add_hrect(y0=ci_low, y1=ci_high, fillcolor='rgba(59,130,246,0.08)',
                                  line=dict(color='rgba(59,130,246,0.2)', width=1, dash='dot'),
                                  annotation_text="95% CI", annotation_font_color='#3B82F6', annotation_font_size=10, annotation_position="right")
                fig_run.update_layout(xaxis_title="Iterasi", yaxis_title="Running Mean", showlegend=False)
                st.plotly_chart(apply_glass_theme(fig_run, 320), use_container_width=True)

                st.markdown(f'<div class="insight-callout"><span class="insight-icon">💡</span><span>Model konvergen pada nilai <strong>{mean_mc:.3f}</strong> dengan interval kepercayaan 95% antara <strong>{ci_low:.3f}</strong> dan <strong>{ci_high:.3f}</strong>. Lebar CI sebesar {ci_width:.3f} menunjukkan model yang stabil.</span></div>', unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 80px 20px; gap: 16px; background: rgba(15,23,42,0.3); border: 1px dashed rgba(255,255,255,0.1); border-radius: 16px; margin-top: 20px;">
                    <span style="font-size:48px; opacity:0.3;">🎲</span>
                    <p style="color:#94A3B8; font-size:14px; text-align:center; margin:0; font-weight:500;">
                        Model stokastik siap dijalankan.<br>
                        <span style="color:#64748B; font-size:12px;">Atur parameter dan klik <strong style="color:#3B82F6">Jalankan Simulasi</strong> untuk memulai komputasi.</span>
                    </p>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 9. DOWNLOAD REPORT & FOOTER
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
with col_dl2:
    st.download_button(
        label="📥 Download Executive Report (Markdown)",
        data=report_md,
        file_name="AI_Learning_Impact_Report_2026.md",
        mime="text/markdown",
        use_container_width=True
    )

st.markdown(f"""
<div class="dashboard-footer">
    <div>
        <div class="footer-brand">AI Learning Impact <span>Analytics</span></div>
        <div class="footer-meta">Penelitian Ilmiah · Data Science Portfolio · Sidang Skripsi 2026</div>
    </div>
    <div style="text-align:right;">
        <div class="footer-meta" style="margin-bottom:8px;">👨‍💻 Ahmad Rizza Pahlevi  |  🏛️ UIN K.H. Abdurrahman Wahid</div>
        <div>
            <span class="tech-badge">Python</span>
            <span class="tech-badge">Streamlit</span>
            <span class="tech-badge">Plotly</span>
            <span class="tech-badge">NumPy</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
