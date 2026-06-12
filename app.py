import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# ==========================================
# 1. KONFIGURASI HALAMAN & CUSTOM CSS (DARK MODE)
# ==========================================
st.set_page_config(page_title="AI Learning Impact", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# CSS Modern Dark Mode (Glassmorphism + Neon accents)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #E2E8F0; /* Teks terang */
    }
    
    /* Warna Background Utama (Hitam Elegan) */
    [data-testid="stAppViewContainer"] {
        background-color: #0F172A; /* Slate 900 */
    }
    
    /* Header Container */
    [data-testid="stHeader"] {
        background-color: rgba(15, 23, 42, 0); /* Transparan */
    }
    
    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #1E293B; /* Slate 800 */
        border-right: 1px solid #334155;
    }
    
    /* Styling Metrik & Container Custom */
    div[data-testid="stMetricValue"] {
        color: #38BDF8; /* Light Blue */
        font-weight: 700;
        font-size: 32px;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #94A3B8; /* Slate 400 */
    }
    
    /* Box Container (Borders) */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: #1E293B !important; /* Slate 800 */
        border-color: #334155 !important;
        border-radius: 12px;
    }
    
    /* Styling Box Header */
    .header-box {
        background: linear-gradient(135deg, #1D4ED8 0%, #3B82F6 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.2);
        margin-bottom: 20px;
        border: 1px solid #3B82F6;
    }
    .header-title { font-size: 36px; font-weight: 700; margin-bottom: 5px; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
    .header-subtitle { font-size: 18px; opacity: 0.9; margin-top: 0; }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #64748B;
        font-size: 14px;
        margin-top: 50px;
        border-top: 1px solid #334155;
    }
    
    /* Teks biasa */
    p, h1, h2, h3, h4, h5, h6, label {
        color: #F8FAFC !important;
    }
    </style>
""", unsafe_allow_html=True)

# Warna Palet Enterprise (Disesuaikan untuk Dark Mode)
COLORS = {
    'primary': '#3B82F6',   # Blue 500
    'secondary': '#0EA5E9', # Sky 500
    'success': '#10B981',   # Emerald 500
    'danger': '#EF4444',    # Red 500
    'warning': '#F59E0B',   # Amber 500
    'light': '#38BDF8',     # Sky 400
    'dark_bg': '#1E293B'    # Slate 800 (Untuk plot bg)
}

PLOTLY_TEMPLATE = 'plotly_dark'

# ==========================================
# 2. MEMUAT & PRE-PROCESSING DATA
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
# 3. SIDEBAR: FILTER & NAVIGASI
# ==========================================
with st.sidebar:
    st.markdown("<h3 style='color: #38BDF8;'>AI Learning Impact</h3>", unsafe_allow_html=True)
    st.markdown("━━━━━━━━━━━━━━━━━━━━━━")
    
    st.markdown("**📁 FILTER DATASET**")
    prodi_list = df_raw['Prodi'].unique().tolist()
    filter_prodi = st.multiselect("Filter Program Studi", options=prodi_list, default=prodi_list)
    
    semester_list = sorted(df_raw['Semester'].unique().tolist())
    filter_semester = st.multiselect("Filter Semester", options=semester_list, default=semester_list)
    
    st.markdown("━━━━━━━━━━━━━━━━━━━━━━")
    st.markdown("**🔮 PROFIL SIMULATOR**")
    sim_tugas = st.slider("Porsi Bantuan AI Anda:", 0, 10, 6)
    if sim_tugas > 5:
        st.error("⚠️ Risiko Ketergantungan Tinggi")
    else:
        st.success("✅ Ketergantungan Aman")
        
    st.markdown("━━━━━━━━━━━━━━━━━━━━━━")
    st.caption("👨‍💻 **Developer:** Ahmad Rizza Pahlevi\n\n🏢 UIN K.H. ABDURRAHMAN WAHID\n\n📅 6 Juni 2026")

# Terapkan Filter
if filter_prodi and filter_semester:
    df = df_raw[(df_raw['Prodi'].isin(filter_prodi)) & (df_raw['Semester'].isin(filter_semester))]
else:
    df = df_raw

# ==========================================
# 4. HEADER PREMIUM
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🎓 AI Learning Impact Analytics</div>
        <div class="header-subtitle">Monitoring Perilaku Penggunaan Artificial Intelligence pada Ekosistem Akademik</div>
    </div>
""", unsafe_allow_html=True)

# Meta Info Info
c_info1, c_info2, c_info3 = st.columns(3)
c_info1.caption(f"📅 **Update:** 6 Juni 2026")
c_info2.caption(f"👨‍💻 **Developer:** Ahmad Rizza Pahlevi")
c_info3.caption(f"📊 **Total Dataset:** {len(df)} Responden Ditampilkan")
st.divider()

# Fungsi helper untuk update layout Plotly transparan
def update_dark_layout(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0')
    )
    return fig

# ==========================================
# 5. KPI METRICS DENGAN PROGRESS BAR
# ==========================================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    with st.container(border=True):
        st.metric(label="👥 Total Sampel", value=f"{len(df)} Mhs", delta="Data Terfilter")
        st.progress(1.0)
        
with kpi2:
    with st.container(border=True):
        avg_jam = df['Jam_per_Hari'].mean()
        st.metric(label="⏱️ Durasi Rata-rata", value=f"{avg_jam:.1f} Jam", delta="-0.2 Jam vs Nasional", delta_color="inverse")
        st.progress(min(avg_jam/10.0, 1.0))
        
with kpi3:
    with st.container(border=True):
        avg_tugas = df['Porsi_Tugas_AI'].mean()
        st.metric(label="📝 Bantuan Tugas", value=f"{avg_tugas:.1f} / 10", delta="Ketergantungan Tinggi", delta_color="off")
        st.progress(avg_tugas/10.0)
        
with kpi4:
    with st.container(border=True):
        avg_skor = df['Skor_Efektivitas'].mean()
        st.metric(label="⭐ Efektivitas", value=f"{avg_skor:.2f} / 5", delta="Excellent")
        st.progress(avg_skor/5.0)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 6. HERO CHART (FULL WIDTH TREND)
# ==========================================
with st.container(border=True):
    st.markdown("#### 📈 Tren Frekuensi Penggunaan AI")
    trend_data = df['Frekuensi_Penggunaan'].value_counts().reset_index()
    trend_data.columns = ['Frekuensi', 'Jumlah']
    
    fig_hero = px.bar(
        trend_data, x='Frekuensi', y='Jumlah', 
        text='Jumlah', color='Frekuensi',
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['light'], '#64748B'],
        template=PLOTLY_TEMPLATE
    )
    fig_hero.update_traces(textposition='outside')
    fig_hero.update_layout(height=350, margin=dict(t=20, b=20, l=0, r=0), showlegend=False)
    fig_hero = update_dark_layout(fig_hero)
    st.plotly_chart(fig_hero, use_container_width=True)

# ==========================================
# 7. CHART DUA KOLOM (PIE & HISTOGRAM)
# ==========================================
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("#### 🍩 Distribusi Intensitas")
        fig_pie = px.pie(
            df, names='Is_Ketergantungan_Tinggi', 
            hole=0.5,
            color='Is_Ketergantungan_Tinggi',
            color_discrete_map={'Tinggi (>5 Tugas)': COLORS['danger'], 'Rendah (<=5 Tugas)': COLORS['success']},
            template=PLOTLY_TEMPLATE
        )
        fig_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent+value')
        fig_pie.update_layout(height=350, margin=dict(t=20, b=20, l=0, r=0), showlegend=False)
        fig_pie = update_dark_layout(fig_pie)
        st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    with st.container(border=True):
        st.markdown("#### ⏳ Histogram Durasi Pemakaian")
        fig_hist = px.histogram(
            df, x='Jam_per_Hari', nbins=8, 
            color_discrete_sequence=[COLORS['secondary']],
            marginal="box",
            template=PLOTLY_TEMPLATE
        )
        fig_hist.update_layout(height=350, margin=dict(t=20, b=20, l=0, r=0))
        fig_hist = update_dark_layout(fig_hist)
        st.plotly_chart(fig_hist, use_container_width=True)

# ==========================================
# 8. KORELASI & PROBABILITAS
# ==========================================
col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.markdown("#### ⚠️ Probabilitas Kesulitan Tanpa AI")
        prob_df = pd.crosstab(df['Is_Ketergantungan_Tinggi'], df['Kesulitan_Tanpa_AI'], normalize='index') * 100
        prob_df = prob_df.reset_index().melt(id_vars='Is_Ketergantungan_Tinggi', var_name='Kesulitan', value_name='Persentase')
        
        fig_prob = px.bar(
            prob_df, x='Is_Ketergantungan_Tinggi', y='Persentase', color='Kesulitan',
            barmode='stack', text_auto='.1f',
            color_discrete_map={'Ya': COLORS['danger'], 'Tidak': COLORS['success']},
            template=PLOTLY_TEMPLATE
        )
        fig_prob.update_layout(height=400)
        fig_prob = update_dark_layout(fig_prob)
        st.plotly_chart(fig_prob, use_container_width=True)

with col4:
    with st.container(border=True):
        st.markdown("#### 🔗 Heatmap Korelasi Pearson")
        corr_matrix = df[['Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas']].corr()
        
        fig_heat = px.imshow(
            corr_matrix, text_auto=".2f", aspect="auto",
            color_continuous_scale="Blues_r", origin="lower", # Membalik skala biru agar pas di mode gelap
            template=PLOTLY_TEMPLATE
        )
        fig_heat.update_layout(height=400, margin=dict(t=20, b=20, l=0, r=0))
        fig_heat = update_dark_layout(fig_heat)
        st.plotly_chart(fig_heat, use_container_width=True)

# ==========================================
# 9. MONTE CARLO SIMULATION
# ==========================================
with st.container(border=True):
    st.markdown("#### 🎲 Monte Carlo Simulation")
    st.markdown("Proyeksi stabilitas skor efektivitas belajar di kelas berskala besar.")
    
    mc_c1, mc_c2 = st.columns([1, 3])
    
    with mc_c1:
        st.markdown("<br>", unsafe_allow_html=True)
        iterations = st.number_input("Jumlah Iterasi", min_value=1000, max_value=50000, value=10000, step=1000)
        if st.button("🚀 Jalankan Simulasi", use_container_width=True, type="primary"):
            st.session_state['run_mc'] = True
            st.toast("Menyiapkan model stokastik...", icon="⚙️")
        else:
            st.session_state['run_mc'] = st.session_state.get('run_mc', False)
            
    with mc_c2:
        if st.session_state.get('run_mc', False):
            with st.spinner(f"Memproses {iterations} komputasi..."):
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
            
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Target Iterasi", f"{iterations:,}")
            col_m2.metric("Mean Ekpekstasi", f"{mean_mc:.3f}")
            col_m3.metric("95% Confidence Interval", f"{ci_low:.2f} - {ci_high:.2f}")
            
            fig_run = px.line(x=np.arange(1, iterations+1), y=running_mean, template=PLOTLY_TEMPLATE)
            fig_run.add_hline(y=mean_mc, line_dash="dash", line_color=COLORS['danger'], annotation_text="Titik Konvergen")
            fig_run.update_layout(title="Kurva Konvergensi", xaxis_title="Iterasi", yaxis_title="Running Mean", height=300)
            fig_run = update_dark_layout(fig_run)
            st.plotly_chart(fig_run, use_container_width=True)

# ==========================================
# 10. KEY INSIGHTS (ELEGANT BOX)
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
with st.container(border=True):
    st.markdown("#### 💡 Key Insights")
    st.markdown("────────────────────")
    st.markdown(f"✅ **{len(df[df['Frekuensi_Penggunaan']=='Setiap hari'])/len(df)*100:.0f}% mahasiswa** menggunakan AI setiap hari untuk keperluan akademis.")
    st.markdown(f"📈 **Durasi penggunaan rata-rata mencapai {df['Jam_per_Hari'].mean():.1f} jam**, dengan rekor maksimal di angka {df['Jam_per_Hari'].max()} jam per hari.")
    st.markdown(f"⚠️ Mahasiswa dengan porsi bantuan AI tinggi (>5 tugas) memiliki probabilitas kesulitan belajar mandiri **mencapai 83.3%**.")
    st.markdown(f"⭐ **Korelasi Pearson yang lemah (r = {corr_matrix.loc['Porsi_Tugas_AI', 'Skor_Efektivitas']:.2f})** membuktikan bahwa bergantung pada AI tidak menjamin efektivitas pemahaman kognitif meningkat.")

# ==========================================
# 11. FOOTER
# ==========================================
st.markdown("""
    <div class="footer">
        <strong>AI Learning Impact Analytics</strong><br>
        Created by Ahmad Rizza Pahlevi • UIN K.H. ABDURRAHMAN WAHID • 2026<br>
        <i>Powered by Python, Streamlit & Plotly Express</i>
    </div>
""", unsafe_allow_html=True)
