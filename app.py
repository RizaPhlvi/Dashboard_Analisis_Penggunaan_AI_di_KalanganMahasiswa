
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. KONFIGURASI HALAMAN & THEME PREMIUM
# ==========================================
st.set_page_config(
    page_title="AI Learning Impact Analytics", 
    page_icon="🎓", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeksi CSS Khusus untuk mempercantik UI (Menghilangkan kesan polos)
st.markdown("""
    <style>
    /* Mengubah font dan background utama */
    .main { background-color: #f4f6f9; }
    
    /* Desain Kotak Premium untuk KPI Metrics */
    .kpi-box {
        background-color: #ffffff;
        padding: 22px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-top: 4px solid #660099;
        text-align: center;
        transition: transform 0.2s;
    }
    .kpi-box:hover {
        transform: translateY(-5px);
    }
    .kpi-label { font-size: 14px; color: #6c757d; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-val { font-size: 32px; color: #660099; font-weight: bold; margin-top: 5px; }
    
    /* Desain Kotak untuk Wawasan/Insight */
    .insight-box {
        background-color: #eef2f7;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2a9d8f;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. MEMUAT DATASET
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
    df['Is_Ketergantungan_Tinggi'] = np.where(df['Porsi_Tugas_AI'] > 5, 'Ketergantungan Tinggi (>5)', 'Ketergantungan Rendah (<=5)')
    return df

df = load_data()

# ==========================================
# 3. SIDEBAR INTERAKTIF: SIMULASI PROFIL
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #660099;'>⚙️ Panel Kontrol</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("🔮 Simulasi Profil Anda")
    st.caption("Masukkan data Anda untuk melihat klasifikasi sistem secara otomatis:")
    
    # Input interaktif
    input_jam = st.slider("Durasi Penggunaan AI (Jam/Hari):", 0, 10, 3)
    input_tugas = st.slider("Porsi Tugas Berbantu AI (0-10):", 0, 10, 6)
    
    st.markdown("---")
    st.markdown("### 📊 Status Hasil Simulasi:")
    if input_tugas > 5:
        st.error("🔴 Ketergantungan Tinggi\n\nRisiko kesulitan belajar mandiri tanpa AI mencapai **83.33%**.")
    else:
        st.success("🟢 Ketergantungan Rendah\n\nKemandirian kognitif terjaga dengan baik.")

# ==========================================
# 4. KONTEN UTAMA: HEADER BREADCRUMB
# ==========================================
st.markdown("<h1 style='color: #660099; margin-bottom: 0;'>🎓 AI Academic Impact Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #555; font-style: italic; margin-top:0;'>Analisis Tingkat Ketergantungan Komputasi, Integritas Akademik, dan Efektivitas Kognitif Mahasiswa</p>", unsafe_allow_html=True)

# Membuat Grid KPI Menggunakan Custom HTML Card
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown(f"<div class='kpi-box'><div class='kpi-label'>👥 Sampel Data</div><div class='kpi-val'>{len(df)} Mhs</div></div>", unsafe_allow_html=True)
with kpi2:
    st.markdown(f"<div class='kpi-box'><div class='kpi-label'>⏱️ Rerata Durasi AI</div><div class='kpi-val'>{df['Jam_per_Hari'].mean():.2f} Jam</div></div>", unsafe_allow_html=True)
with kpi3:
    st.markdown(f"<div class='kpi-box'><div class='kpi-label'>📝 Rerata Bantuan Tugas</div><div class='kpi-val'>{df['Porsi_Tugas_AI'].mean():.1f} / 10</div></div>", unsafe_allow_html=True)
with kpi4:
    st.markdown(f"<div class='kpi-box'><div class='kpi-label'>⭐ Skor Efektivitas</div><div class='kpi-val'>{df['Skor_Efektivitas'].mean():.2f} / 5</div></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 5. STRUKTUR TABS NAVIGASI
# ==========================================
tab1, tab2, tab3 = st.tabs(["📊 Eksplorasi Deskriptif", "🔗 Hubungan & Probabilitas Bersyarat", "🎲 Proyeksi Monte Carlo"])

# Pengaturan Tema Global Grafik Matplotlib/Seaborn
plt.rcParams['figure.facecolor'] = '#ffffff'
plt.rcParams['axes.facecolor'] = '#ffffff'

# --- TAB 1: EKSPLORASI DESKRIPTIF ---
with tab1:
    st.markdown("<h3 style='color: #660099;'>Pola Distribusi Penggunaan AI</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    with c1:
        fig1, ax1 = plt.subplots(figsize=(7, 4.5))
        freq_order = ['Setiap hari', '3-5 kali seminggu', '1-2 kali seminggu', 'Kurang dari 1 kali seminggu']
        counts = df['Frekuensi_Penggunaan'].value_counts().reindex(freq_order)
        ax1.pie(counts.values, labels=counts.index, autopct='%1.1f%%', colors=['#660099', '#9954b8', '#cc99cc', '#e1cae6'], startangle=140, pctdistance=0.75)
        ax1.set_title("Proporsi Frekuensi Pemakaian AI", fontweight='bold', color='#333333')
        st.pyplot(fig1)
        plt.close(fig1)
        
    with c2:
        fig2, ax2 = plt.subplots(figsize=(7, 4.5))
        sns.histplot(data=df, x='Jam_per_Hari', bins=8, kde=True, color='#457B9D', ax=ax2)
        ax2.set_title("Sebaran Durasi Belajar Bersama AI (Jam/Hari)", fontweight='bold', color='#333333')
        ax2.set_ylabel("Jumlah Mahasiswa")
        st.pyplot(fig2)
        plt.close(fig2)

# --- TAB 2: HUBUNGAN & PROBABILITAS ---
with tab2:
    st.markdown("<h3 style='color: #660099;'>Analisis Inferensial & Risiko Ketergantungan</h3>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    
    with c3:
        fig3, ax3 = plt.subplots(figsize=(7, 4.5))
        prob_data = pd.crosstab(df['Is_Ketergantungan_Tinggi'], df['Kesulitan_Tanpa_AI'], normalize='index') * 100
        prob_data.plot(kind='bar', stacked=True, color=['#e63946', '#457b9d'], ax=ax3)
        ax3.set_title("Probabilitas Bersyarat: Kesulitan Belajar Tanpa AI", fontweight='bold')
        ax3.set_ylabel("Persentase (%)")
        ax3.tick_params(axis='x', rotation=0)
        for p in ax3.patches:
            if p.get_height() > 0:
                ax3.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width()/2, p.get_y() + p.get_height()/2), ha='center', va='center', color='white', fontweight='bold')
        st.pyplot(fig3)
        plt.close(fig3)
        
    with c4:
        fig5, ax5 = plt.subplots(figsize=(6, 4))
        matrix_corr = df[['Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas']].corr()
        sns.heatmap(matrix_corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".3f", ax=ax5, cbar=False)
        ax5.set_title("Matriks Korelasi Linier Pearson", fontweight='bold')
        st.pyplot(fig5)
        plt.close(fig5)
        
    st.markdown("""
        <div class='insight-box'>
        <strong>💡 Rangkuman Insight:</strong> Terdapat selisih probabilitas yang masif (~40%). Mahasiswa yang menyerahkan mayoritas tugasnya ke AI (>5 tugas) 
        mengalami lonjakan risiko ketidakmampuan belajar mandiri hingga <strong>83.33%</strong>. Korelasi Pearson yang lemah (r = 0.257) membuktikan bahwa menambah kuantitas penggunaan AI tidak serta-merta meningkatkan pemahaman kognitif.
        </div>
    """, unsafe_allow_html=True)

# --- TAB 3: PROYEKSI MONTE CARLO ---
with tab3:
    st.markdown("<h3 style='color: #660099;'>Pemodelan Stokastik Masa Depan</h3>", unsafe_allow_html=True)
    
    iterasi = st.select_slider(
        "Pilih Kekuatan Akurasi Iterasi Simulasi:",
        options=[1000, 5000, 10000, 15000, 20000],
        value=10000
    )
    
    if st.button("⚡ Jalankan Komputasi Monte Carlo", type="primary"):
        with st.spinner("Menghitung model stokastik populasi kelas..."):
            p_dist = df['Porsi_Tugas_AI'].value_counts(normalize=True).sort_index()
            cats = p_dist.index.values
            weights = p_dist.values
            
            stats = df.groupby('Porsi_Tugas_AI')['Skor_Efektivitas'].agg(['mean', 'std'])
            stats['std'] = stats['std'].fillna(df['Skor_Efektivitas'].std())
            
            hasil = []
            for i in range(iterasi):
                sim_tugas = np.random.choice(cats, size=100, p=weights)
                skor = [np.clip(np.random.normal(loc=stats.loc[p, 'mean'], scale=stats.loc[p, 'std']), 1, 5) for p in sim_tugas]
                hasil.append(np.mean(skor))
            
            mean_mc = np.mean(hasil)
            ci_low, ci_high = np.percentile(hasil, 2.5), np.percentile(hasil, 97.5)
            
            c5, c6 = st.columns(2)
            with c5:
                fig7, ax7 = plt.subplots(figsize=(7, 4.5))
                ax7.hist(hasil, bins=50, color='#2a9d8f', edgecolor='black', alpha=0.75, density=True)
                ax7.axvline(mean_mc, color='orange', ls='--', lw=2.5, label=f'Mean: {mean_mc:.3f}')
                ax7.axvline(ci_low, color='red', ls=':', lw=2, label=f'CI Bawah: {ci_low:.3f}')
                ax7.axvline(ci_high, color='red', ls=':', lw=2, label=f'CI Atas: {ci_high:.3f}')
                ax7.set_title("Histogram Distribusi Probabilitas Skor Kelas", fontweight='bold')
                ax7.legend()
                st.pyplot(fig7)
                plt.close(fig7)
                
            with c6:
                running_mean = np.cumsum(hasil) / np.arange(1, iterasi+1)
                fig8, ax8 = plt.subplots(figsize=(7, 4.5))
                ax8.plot(np.arange(1, iterasi+1), running_mean, color='#e76f51', lw=2)
                ax8.axhline(mean_mc, color='black', ls='--', lw=1.5)
                ax8.set_title("Kurva Konvergensi Running Mean", fontweight='bold')
                ax8.set_xlabel("Jumlah Iterasi Eksperimen")
                st.pyplot(fig8)
                plt.close(fig8)
                
            st.success(f"🎉 **Hasil Proyeksi:** Pada pengujian tingkat stabilitas tinggi menggunakan {iterasi} iterasi, nilai ekspektasi efektivitas kelas mengunci secara presisi pada angka **{mean_mc:.3f}** dengan Interval Kepercayaan 95% berada pada rentang [{ci_low:.3f} – {ci_high:.3f}].")

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

# CSS Modern ala Microsoft Power BI / Glassmorphism
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Warna Background Utama */
    [data-testid="stAppViewContainer"] {
        background-color: #F8FAFC;
    }
    
    /* Styling Metrik & Container Custom */
    div[data-testid="stMetricValue"] {
        color: #2563EB;
        font-weight: 700;
        font-size: 32px;
    }
    
    /* Styling Box Header */
    .header-box {
        background: linear-gradient(135deg, #2563EB 0%, #0EA5E9 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.2);
        margin-bottom: 20px;
    }
    .header-title { font-size: 36px; font-weight: 700; margin-bottom: 5px; }
    .header-subtitle { font-size: 18px; opacity: 0.9; margin-top: 0; }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #64748B;
        font-size: 14px;
        margin-top: 50px;
        border-top: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# Warna Palet Enterprise
COLORS = {
    'primary': '#2563EB',
    'secondary': '#0EA5E9',
    'success': '#22C55E',
    'danger': '#EF4444',
    'warning': '#F59E0B',
    'light': '#E0F2FE'
}

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
    # Membersihkan dan merekayasa data
    df['Is_Ketergantungan_Tinggi'] = np.where(df['Porsi_Tugas_AI'] > 5, 'Tinggi (>5 Tugas)', 'Rendah (<=5 Tugas)')
    # Mencoba parse tanggal untuk Trend (Abaikan jam, ambil harinya saja jika format string)
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
    st.image("https://cdn-icons-png.flaticon.com/512/8616/8616075.png", width=60) # Placeholder Logo
    st.markdown("<h3 style='color: #2563EB;'>AI Learning Impact</h3>", unsafe_allow_html=True)
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
    st.caption("👨‍💻 **Developer:** Ahmad Rizza Pahlevi\n\n🏢 Universitas ...\n\n📅 Juni 2026")

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
c_info1.caption(f"📅 **Update:** Juni 2026")
c_info2.caption(f"👨‍💻 **Developer:** Ahmad Rizza Pahlevi")
c_info3.caption(f"📊 **Total Dataset:** {len(df)} Responden Ditampilkan")
st.divider()

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
        st.progress(min(avg_jam/10.0, 1.0)) # Asumsi max 10 jam
        
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
    # Karena data Timestamp hanya beberapa hari, kita gunakan persebaran kategori
    trend_data = df['Frekuensi_Penggunaan'].value_counts().reset_index()
    trend_data.columns = ['Frekuensi', 'Jumlah']
    
    fig_hero = px.bar(
        trend_data, x='Frekuensi', y='Jumlah', 
        text='Jumlah', color='Frekuensi',
        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['light'], '#94A3B8'],
        template='plotly_white'
    )
    # HANYA MENGGUNAKAN textposition, TANPA marker_border_radius
    fig_hero.update_traces(textposition='outside')
    fig_hero.update_layout(height=350, margin=dict(t=20, b=20, l=0, r=0), showlegend=False)
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
            hole=0.5, # Membuatnya Donut Chart yang elegan
            color='Is_Ketergantungan_Tinggi',
            color_discrete_map={'Tinggi (>5 Tugas)': COLORS['danger'], 'Rendah (<=5 Tugas)': COLORS['success']}
        )
        fig_pie.update_traces(textinfo='percent+label', hoverinfo='label+percent+value')
        fig_pie.update_layout(height=350, margin=dict(t=20, b=20, l=0, r=0), showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    with st.container(border=True):
        st.markdown("#### ⏳ Histogram Durasi Pemakaian")
        fig_hist = px.histogram(
            df, x='Jam_per_Hari', nbins=8, 
            color_discrete_sequence=[COLORS['secondary']],
            marginal="box", # Menambahkan boxplot di atasnya
            template='plotly_white'
        )
        fig_hist.update_layout(height=350, margin=dict(t=20, b=20, l=0, r=0))
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
            template='plotly_white'
        )
        fig_prob.update_layout(height=400)
        st.plotly_chart(fig_prob, use_container_width=True)

with col4:
    with st.container(border=True):
        st.markdown("#### 🔗 Heatmap Korelasi Pearson")
        corr_matrix = df[['Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas']].corr()
        
        fig_heat = px.imshow(
            corr_matrix, text_auto=".2f", aspect="auto",
            color_continuous_scale="Blues", origin="lower"
        )
        fig_heat.update_layout(height=400, margin=dict(t=20, b=20, l=0, r=0))
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
                time.sleep(1) # Efek dramatis untuk dashboard enterprise
                
                # Logic Monte Carlo
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
            
            # Sub-metrik Monte Carlo
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Target Iterasi", f"{iterations:,}")
            col_m2.metric("Mean Ekpekstasi", f"{mean_mc:.3f}")
            col_m3.metric("95% Confidence Interval", f"{ci_low:.2f} - {ci_high:.2f}")
            
            # Plotly Line Chart Running Mean
            fig_run = px.line(x=np.arange(1, iterations+1), y=running_mean, template='plotly_white')
            fig_run.add_hline(y=mean_mc, line_dash="dash", line_color=COLORS['danger'], annotation_text="Titik Konvergen")
            fig_run.update_layout(title="Kurva Konvergensi", xaxis_title="Iterasi", yaxis_title="Running Mean", height=300)
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
        Created by Ahmad Rizza Pahlevi • Universitas ... • 2026<br>
        <i>Powered by Python, Streamlit & Plotly Express</i>
    </div>
""", unsafe_allow_html=True)
