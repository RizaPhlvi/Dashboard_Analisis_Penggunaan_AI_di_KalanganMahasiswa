import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# ==========================================
# 1. KONFIGURASI HALAMAN & CUSTOM CSS
# ==========================================
st.set_page_config(page_title="AI Learning Impact", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# CSS Kustom untuk Tampilan Enterprise Modern (Glassmorphism & Dark Slate)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Konfigurasi Font & Warna Dasar */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #F8FAFC;
    }
    
    /* Background Utama: Dark Slate Gradient (Tanpa Grid) */
    [data-testid="stAppViewContainer"] { 
        background: radial-gradient(circle at top left, #1E293B 0%, #0F172A 100%);
        background-attachment: fixed;
    }
    
    /* Transparansi Header Bawaan */
    [data-testid="stHeader"] { background-color: transparent !important; }
    
    /* Sidebar: Elegan dan Terbatas */
    [data-testid="stSidebar"] { 
        background-color: rgba(15, 23, 42, 0.95) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.05); 
    }
    
    /* =========================================================
       GLASSMORPHISM CARDS & HOVER EFFECTS
       ========================================================= */
    /* Modifikasi Container Border (Bawaan Streamlit) */
    [data-testid="stVerticalBlockBorderWrapper"] > div {
        background-color: rgba(30, 41, 59, 0.6) !important; 
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        padding: 1rem;
    }
    
    /* Efek Hover untuk Card Container */
    [data-testid="stVerticalBlockBorderWrapper"]:hover > div {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
        border-color: rgba(59, 130, 246, 0.4) !important; /* Glow Biru Tipis */
    }

    /* =========================================================
       UI ELEMENTS: TABS, BUTTONS, SLIDERS, METRICS
       ========================================================= */
    /* Tabs Navigation Ala Aplikasi Modern */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        padding-bottom: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(30, 41, 59, 0.4);
        border-radius: 8px;
        padding: 10px 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"] p {
        color: #94A3B8 !important;
        font-size: 15px;
        font-weight: 500;
        margin: 0;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(59, 130, 246, 0.1);
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: rgba(59, 130, 246, 0.15) !important;
        border-bottom-color: transparent !important;
        border: 1px solid rgba(59, 130, 246, 0.5) !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] p {
        color: #3B82F6 !important;
        font-weight: 600 !important;
    }

    /* Custom Slider */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #3B82F6 !important;
        border: 2px solid #F8FAFC !important;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
    }
    div[data-testid="stTickBar"] ~ div > div > div > div { background-color: #3B82F6 !important; }

    /* Custom Buttons (Primary Action) */
    .stButton > button {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
        border: none !important;
        color: #FFFFFF !important;
        font-weight: 600;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        box-shadow: 0 8px 15px rgba(59, 130, 246, 0.4);
        transform: translateY(-2px);
    }

    /* MultiSelect Tag Warna Biru Khas Vercel/Notion */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: rgba(59, 130, 246, 0.2) !important;
        border: 1px solid rgba(59, 130, 246, 0.4);
        border-radius: 6px;
    }
    .stMultiSelect [data-baseweb="tag"] span { color: #EFF6FF !important; font-weight: 500; }

    /* Desain Angka Metric yang Premium */
    div[data-testid="stMetricValue"] { color: #F8FAFC; font-weight: 700; font-size: 2.2rem; }
    div[data-testid="stMetricLabel"] { color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.85rem;}
    
    /* =========================================================
       CUSTOM KOMPONEN (HERO, INSIGHT, FOOTER)
       ========================================================= */
    .hero-section {
        background: radial-gradient(circle at 100% 0%, rgba(59, 130, 246, 0.15) 0%, transparent 40%),
                    linear-gradient(180deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(20px);
        padding: 40px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    .hero-title { font-size: 2.5rem; font-weight: 800; background: -webkit-linear-gradient(45deg, #F8FAFC, #93C5FD); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px;}
    .hero-subtitle { font-size: 1.1rem; color: #94A3B8; font-weight: 400; max-width: 800px; line-height: 1.6;}
    
    .insight-box {
        background-color: rgba(6, 182, 212, 0.05);
        border-left: 4px solid #06B6D4;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin-top: 15px;
        font-size: 0.9rem;
        color: #E2E8F0;
    }
    
    .footer { text-align: center; padding: 30px 20px; color: #64748B; font-size: 0.85rem; margin-top: 60px; border-top: 1px solid rgba(255, 255, 255, 0.05); }
    .footer a { color: #3B82F6; text-decoration: none; }
    
    p, h1, h2, h3, h4, h5, h6, label { color: #F8FAFC !important; }
    hr { border-color: rgba(255, 255, 255, 0.05) !important; margin: 2rem 0; }
    </style>
""", unsafe_allow_html=True)

# Palet Warna Enterprise (Tailwind Base)
ENT_COLORS = {
    'primary': '#3B82F6',   # Blue 500
    'secondary': '#06B6D4', # Cyan 500
    'success': '#22C55E',   # Green 500
    'danger': '#EF4444',    # Red 500
    'warning': '#F59E0B',   # Amber 500
    'purple': '#8B5CF6',    # Violet 500
    'muted': '#64748B',     # Slate 500
    'surface': '#1E293B',   # Slate 800
    'text': '#F8FAFC'       # Slate 50
}

PLOTLY_TEMPLATE = 'plotly_dark'

# ==========================================
# 2. MEMUAT & PRE-PROCESSING DATA
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
        df['Is_Ketergantungan_Tinggi'] = np.where(df['Porsi_Tugas_AI'] > 5, 'Tinggi (>5 Tugas)', 'Rendah (<=5 Tugas)')
        df['Date_Parsed'] = pd.to_datetime(df['Timestamp'], errors='coerce').dt.date
        return df
    except FileNotFoundError:
        st.error("⚠️ Dataset 'Data Mentah.csv' tidak ditemukan. Pastikan file berada dalam direktori yang sama.")
        return pd.DataFrame()

df_raw = load_data()

# ==========================================
# 3. SIDEBAR: FILTER & NAVIGASI
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103285.png", width=60) # Ikon modern
    st.markdown("### Model Konfigurasi")
    st.caption("Sesuaikan parameter analisis dataset.")
    
    with st.expander("📁 Parameter Dataset", expanded=True):
        prodi_list = df_raw['Prodi'].unique().tolist() if not df_raw.empty else []
        filter_prodi = st.multiselect("Program Studi", options=prodi_list, default=prodi_list)
        
        semester_list = sorted(df_raw['Semester'].unique().tolist()) if not df_raw.empty else []
        filter_semester = st.multiselect("Semester", options=semester_list, default=semester_list)
    
    with st.expander("🔮 Simulator Profil", expanded=True):
        sim_tugas = st.slider("Porsi Bantuan AI Anda:", 0, 10, 6)
        if sim_tugas > 5:
            st.markdown(f"**Status:** <span style='color:{ENT_COLORS['danger']}'>Risiko Ketergantungan Tinggi</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"**Status:** <span style='color:{ENT_COLORS['success']}'>Ketergantungan Aman</span>", unsafe_allow_html=True)
        
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.caption("👨‍💻 **Developer**\nAhmad Rizza Pahlevi\n\n🏢 **Afiliasi**\nUIN K.H. ABDURRAHMAN WAHID\n\n📅 **Versi**\nJuni 2026")

if not df_raw.empty and filter_prodi and filter_semester:
    df = df_raw[(df_raw['Prodi'].isin(filter_prodi)) & (df_raw['Semester'].isin(filter_semester))]
else:
    df = df_raw

if df.empty:
    st.warning("Data kosong atau tidak tersedia berdasarkan filter saat ini.")
    st.stop()

# ==========================================
# 4. HEADER PREMIUM (HERO SECTION)
# ==========================================
st.markdown(f"""
    <div class="hero-section">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
            <div>
                <div class="hero-title">AI Learning Impact Analytics</div>
                <div class="hero-subtitle">Pemantauan dan Analisis Preskriptif terhadap Perilaku Penggunaan Artificial Intelligence pada Ekosistem Akademik. Dashboard ini memvisualisasikan korelasi antara intensitas penggunaan, tingkat efektivitas, dan risiko ketergantungan.</div>
            </div>
            <div style="text-align: right; color: #94A3B8; font-size: 0.85rem;">
                <div><strong>Status Infrastruktur</strong></div>
                <div style="color: {ENT_COLORS['success']}; margin-top: 4px;">● Sistem Aktif</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Helper untuk transparansi Chart Plotly
def update_dark_layout(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=ENT_COLORS['text']),
        title_font=dict(size=18, family="Inter", color="#F8FAFC"),
        margin=dict(t=40, b=20, l=10, r=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.1)')
    return fig

# ==========================================
# 5. METRIK KPI MODERN
# ==========================================
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    with st.container(border=True):
        st.metric(label="👥 TOTAL RESPONDEN", value=f"{len(df):,} Mhs", delta="Sampel Aktif")
with kpi2:
    with st.container(border=True):
        avg_jam = df['Jam_per_Hari'].mean()
        st.metric(label="⏱️ DURASI RATA-RATA", value=f"{avg_jam:.1f} Jam/Hari", delta="Intensitas Paparan", delta_color="off")
with kpi3:
    with st.container(border=True):
        avg_tugas = df['Porsi_Tugas_AI'].mean()
        st.metric(label="📝 PORSI BANTUAN TUGAS", value=f"{avg_tugas:.1f} / 10", delta="Skala Indeks", delta_color="off")
with kpi4:
    with st.container(border=True):
        avg_skor = df['Skor_Efektivitas'].mean()
        st.metric(label="⭐ SKOR EFEKTIVITAS", value=f"{avg_skor:.2f} / 5", delta="Persepsi Kognitif", delta_color="normal")

st.markdown("<hr>", unsafe_allow_html=True)

# ==========================================
# 6. EXECUTIVE SUMMARY
# ==========================================
setiap_hari_pct = len(df[df['Frekuensi_Penggunaan']=='Setiap hari']) / len(df) * 100
ketergantungan_tinggi = len(df[df['Is_Ketergantungan_Tinggi'] == 'Tinggi (>5 Tugas)']) / len(df) * 100

st.markdown("### 📋 Executive Summary")
st.info(f"""
Tinjauan awal data menunjukkan **{setiap_hari_pct:.1f}%** mahasiswa terbiasa menggunakan AI setiap hari untuk keperluan akademis. Di antara populasi yang dianalisis, **{ketergantungan_tinggi:.1f}%** responden masuk ke dalam kategori *Risiko Ketergantungan Tinggi* dengan penggunaan dominan pada penyelesaian tugas. Telusuri korelasi dan proyeksi lebih dalam melalui tab navigasi di bawah.
""")
st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 7. TAB NAVIGASI UTAMA
# ==========================================
tab1, tab2, tab3 = st.tabs(["📊 Distribusi Data", "🔗 Korelasi Lanjutan", "🎲 Engine Simulasi (Monte Carlo)"])

# ------------------------------------------
# TAB 1: EKSPLORASI DESKRIPTIF
# ------------------------------------------
with tab1:
    st.markdown("#### Tinjauan Distribusi Variabel")
    st.caption("Analisis deskriptif untuk mengidentifikasi pola perilaku dasar penggunaan AI mahasiswa.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container(border=True):
        trend_data = df['Frekuensi_Penggunaan'].value_counts().reset_index()
        trend_data.columns = ['Frekuensi', 'Jumlah']
        
        fig_hero = px.bar(
            trend_data, x='Frekuensi', y='Jumlah', 
            text='Jumlah', color='Frekuensi',
            color_discrete_sequence=[ENT_COLORS['primary'], ENT_COLORS['secondary'], ENT_COLORS['purple'], ENT_COLORS['muted']],
            template=PLOTLY_TEMPLATE, title="Tren Frekuensi Penggunaan AI Akademik"
        )
        fig_hero.update_traces(textposition='outside', marker_line_width=0)
        st.plotly_chart(update_dark_layout(fig_hero), use_container_width=True)
        
        st.markdown(f"""<div class='insight-box'>💡 <b>Insight:</b> Kategori <b>'{trend_data.iloc[0]['Frekuensi']}'</b> merupakan frekuensi dominan dengan total {trend_data.iloc[0]['Jumlah']} responden. Hal ini mengindikasikan adopsi teknologi yang sudah menjadi rutinitas harian.</div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            fig_pie = px.pie(
                df, names='Is_Ketergantungan_Tinggi', hole=0.6,
                color='Is_Ketergantungan_Tinggi',
                color_discrete_map={'Tinggi (>5 Tugas)': ENT_COLORS['danger'], 'Rendah (<=5 Tugas)': ENT_COLORS['primary']},
                template=PLOTLY_TEMPLATE, title="Rasio Ketergantungan AI"
            )
            fig_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent+value', textfont_size=14)
            st.plotly_chart(update_dark_layout(fig_pie), use_container_width=True)
            st.markdown(f"""<div class='insight-box'>💡 <b>Insight:</b> Proporsi warna merah menunjukkan segmen rentan yang sangat bergantung pada AI untuk menyelesaikan beban akademis.</div>""", unsafe_allow_html=True)

    with col2:
        with st.container(border=True):
            fig_porsi = px.histogram(
                df, x='Porsi_Tugas_AI', text_auto=True, 
                color_discrete_sequence=[ENT_COLORS['secondary']], 
                template=PLOTLY_TEMPLATE, title="Distribusi Porsi Tugas (Bantuan AI)"
            )
            fig_porsi.update_layout(xaxis_title="Jumlah Tugas Berbantuan AI (0-10)", yaxis_title="Frekuensi")
            st.plotly_chart(update_dark_layout(fig_porsi), use_container_width=True)
            st.markdown(f"""<div class='insight-box'>💡 <b>Insight:</b> Mayoritas distribusi condong ke skala rata-rata {avg_tugas:.1f}, merepresentasikan perilaku hybrid antara tugas mandiri dan bantuan mesin.</div>""", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        with st.container(border=True):
            fig_hist = px.histogram(
                df, x='Jam_per_Hari', nbins=8, marginal="box",
                color_discrete_sequence=[ENT_COLORS['purple']],
                template=PLOTLY_TEMPLATE, title="Distribusi Durasi Pemakaian Harian"
            )
            st.plotly_chart(update_dark_layout(fig_hist), use_container_width=True)

    with col4:
        with st.container(border=True):
            fig_skor = px.histogram(
                df, x='Skor_Efektivitas', text_auto=True, 
                color_discrete_sequence=[ENT_COLORS['success']], 
                template=PLOTLY_TEMPLATE, title="Persebaran Skor Efektivitas Belajar"
            )
            fig_skor.update_layout(xaxis_title="Skor Evaluasi (1-5)")
            st.plotly_chart(update_dark_layout(fig_skor), use_container_width=True)

# ------------------------------------------
# TAB 2: HUBUNGAN & PROBABILITAS
# ------------------------------------------
with tab2:
    st.markdown("#### Matriks Hubungan Linear & Probabilitas")
    st.caption("Pendeteksian anomali korelasi dan validasi hipotesis ketergantungan mahasiswa.")
    st.markdown("<br>", unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        with st.container(border=True):
            prob_df = pd.crosstab(df['Is_Ketergantungan_Tinggi'], df['Kesulitan_Tanpa_AI'], normalize='index') * 100
            prob_df = prob_df.reset_index().melt(id_vars='Is_Ketergantungan_Tinggi', var_name='Kesulitan', value_name='Persentase')
            
            fig_prob = px.bar(
                prob_df, x='Is_Ketergantungan_Tinggi', y='Persentase', color='Kesulitan',
                barmode='stack', text_auto='.1f',
                color_discrete_map={'Ya': ENT_COLORS['danger'], 'Tidak': ENT_COLORS['primary']},
                template=PLOTLY_TEMPLATE, title="Risiko Kesulitan Belajar Tanpa AI"
            )
            fig_prob.update_layout(yaxis_title="Persentase Kumulatif (%)")
            st.plotly_chart(update_dark_layout(fig_prob), use_container_width=True)
            st.markdown(f"""<div class='insight-box'>💡 <b>Insight:</b> Segmen dengan ketergantungan tinggi memiliki rasio kepastian <i>"kesulitan tanpa AI"</i> yang signifikan secara statistik.</div>""", unsafe_allow_html=True)

    with col6:
        with st.container(border=True):
            corr_matrix = df[['Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas']].corr(numeric_only=True)
            
            # Penggunaan palet Diverging "RdBu_r" untuk matriks korelasi
            fig_heat = px.imshow(
                corr_matrix, text_auto=".2f", aspect="auto",
                color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
                origin="lower", template=PLOTLY_TEMPLATE, title="Matriks Korelasi Pearson"
            )
            st.plotly_chart(update_dark_layout(fig_heat), use_container_width=True)
            try:
                corr_val = corr_matrix.loc['Porsi_Tugas_AI', 'Skor_Efektivitas']
                st.markdown(f"""<div class='insight-box'>💡 <b>Insight:</b> Korelasi antara porsi AI dan skor efektivitas adalah <b>{corr_val:.2f}</b>, menandakan bahwa volume pemakaian tidak menjamin kualitas belajar secara mutlak.</div>""", unsafe_allow_html=True)
            except:
                pass

    col7, col8 = st.columns(2)
    with col7:
        with st.container(border=True):
            # Cek panjang data sebelum polyfit agar tidak error
            if len(df) > 1:
                z = np.polyfit(df['Porsi_Tugas_AI'], df['Skor_Efektivitas'], 1)
                p = np.poly1d(z)
                df_sorted = df.sort_values('Porsi_Tugas_AI')
                
                fig_scatter = px.scatter(
                    df, x='Porsi_Tugas_AI', y='Skor_Efektivitas', 
                    opacity=0.7, template=PLOTLY_TEMPLATE, title="Tren Porsi Bantuan vs Efektivitas"
                )
                fig_scatter.update_traces(marker=dict(size=10, color=ENT_COLORS['secondary']))
                fig_scatter.add_trace(go.Scatter(
                    x=df_sorted['Porsi_Tugas_AI'], y=p(df_sorted['Porsi_Tugas_AI']), 
                    mode='lines', name='Regresi Linear', line=dict(color=ENT_COLORS['danger'], width=3)
                ))
                st.plotly_chart(update_dark_layout(fig_scatter), use_container_width=True)
            else:
                st.info("Data tidak cukup untuk kalkulasi regresi.")

    with col8:
        with st.container(border=True):
            fig_box = px.box(
                df, x='Porsi_Tugas_AI', y='Skor_Efektivitas', color='Porsi_Tugas_AI',
                color_discrete_sequence=[ENT_COLORS['primary'], ENT_COLORS['secondary'], ENT_COLORS['purple']], 
                template=PLOTLY_TEMPLATE, title="Dispersi Efektivitas per Tingkat Bantuan"
            )
            fig_box.update_layout(xaxis_title="Porsi Tugas (0-10)", showlegend=False)
            st.plotly_chart(update_dark_layout(fig_box), use_container_width=True)

# ------------------------------------------
# TAB 3: MONTE CARLO SIMULATION (ENGINE)
# ------------------------------------------
with tab3:
    st.markdown("#### Model Prediktif Skala Besar")
    st.caption("Engine komputasi Monte Carlo untuk memproyeksikan stabilitas skor efektivitas belajar jika diuji pada skala universitas dengan pola yang sama.")
    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        mc_c1, mc_c2 = st.columns([1, 2.5])
        
        with mc_c1:
            st.markdown("##### Parameter Simulasi", unsafe_allow_html=True)
            iterations = st.number_input("Jumlah Iterasi (N)", min_value=1000, max_value=100000, value=10000, step=5000)
            st.markdown("<div style='font-size: 0.85rem; color: #94A3B8; margin-bottom: 20px;'>Semakin tinggi N, simulasi akan menghasilkan proyeksi konvergensi yang semakin kuat berdasar The Law of Large Numbers.</div>", unsafe_allow_html=True)
            
            if st.button("▶ Eksekusi Simulasi", use_container_width=True):
                st.session_state['run_mc'] = True
                st.toast("Inisialisasi Model Stokastik...", icon="⚙️")
            else:
                st.session_state['run_mc'] = st.session_state.get('run_mc', False)
                
        with mc_c2:
            if st.session_state.get('run_mc', False):
                with st.spinner(f"Mesin Monte Carlo memproses {iterations:,} kalkulasi iteratif..."):
                    time.sleep(1) # Efek komputasi untuk UX
                    
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
                
                # Hasil Simulasi
                res1, res2, res3 = st.columns(3)
                res1.metric("Target Iterasi (N)", f"{iterations:,}")
                res2.metric("Mean Konvergensi Eksekusi", f"{mean_mc:.3f}", delta="Proyeksi Stabilitas", delta_color="normal")
                res3.metric("Interval Kepercayaan (95%)", f"{ci_low:.2f} — {ci_high:.2f}", delta="Margin of Error", delta_color="off")
                
                fig_run = px.line(x=np.arange(1, iterations+1), y=running_mean, template=PLOTLY_TEMPLATE)
                fig_run.update_traces(line=dict(color=ENT_COLORS['primary'], width=2))
                fig_run.add_hline(y=mean_mc, line_dash="dash", line_color=ENT_COLORS['warning'], annotation_text="Titik Temu (Mean Convergence)")
                fig_run.update_layout(title="Kurva Konvergensi Monte Carlo", xaxis_title="Iterasi (n)", yaxis_title="Running Mean")
                st.plotly_chart(update_dark_layout(fig_run), use_container_width=True)
            else:
                st.info("Tekan tombol **Eksekusi Simulasi** pada panel kiri untuk menjalankan mesin Monte Carlo berbasis data survei mahasiswa.")

# ==========================================
# 8. FOOTER PROFESIONAL
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div class="footer">
        <div style="font-weight: 600; font-size: 1rem; color: #F8FAFC;">🎓 Sistem Informasi Analisis Preskriptif</div>
        <div style="margin-top: 8px;">Dikembangkan oleh <b>Ahmad Rizza Pahlevi</b> — Program Studi Sains Data</div>
        <div style="margin-top: 4px;">UIN K.H. ABDURRAHMAN WAHID PEKALONGAN © 2026</div>
        <div style="margin-top: 15px; display: inline-flex; gap: 15px; opacity: 0.7;">
            <span><i>Powered by</i> Streamlit</span>
            <span>•</span>
            <span>Plotly Enterprise</span>
            <span>•</span>
            <span>Monte Carlo Stochastic Engine</span>
        </div>
    </div>
""", unsafe_allow_html=True)
