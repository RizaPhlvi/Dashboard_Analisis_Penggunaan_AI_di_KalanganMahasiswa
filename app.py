%%writefile app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. KONFIGURASI HALAMAN (BIAR TIDAK POLOS)
# ==========================================
st.set_page_config(page_title="AI Education Analytics", page_icon="🚀", layout="wide")

# Custom CSS untuk mempercantik tampilan background metrik
st.markdown("""
    <style>
    div[data-testid="stMetricValue"] {font-size: 28px; color: #660099;}
    div[data-testid="stMetricLabel"] {font-size: 14px; color: #457b9d; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Dashboard Analisis Penggunaan AI Akademik")
st.markdown("*Platform analisis data interaktif untuk mengeksplorasi hubungan intensitas penggunaan AI, perilaku belajar, dan integritas akademik mahasiswa.*")
st.divider()

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
    # Rekayasa fitur
    df['Is_Ketergantungan_Tinggi'] = np.where(df['Porsi_Tugas_AI'] > 5, 'Ketergantungan Tinggi (>5)', 'Ketergantungan Rendah (<=5)')
    return df

df = load_data()

# ==========================================
# 3. KOTAK METRIK UTAMA (KPI)
# ==========================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Total Responden", f"{len(df)} Mhs")
col2.metric("⏱️ Rata-rata Durasi AI", f"{df['Jam_per_Hari'].mean():.1f} Jam/Hari")
col3.metric("📝 Rata-rata Tugas via AI", f"{df['Porsi_Tugas_AI'].mean():.1f} dari 10")
col4.metric("⭐ Efektivitas Kognitif", f"{df['Skor_Efektivitas'].mean():.2f} / 5.0")
st.divider()

# ==========================================
# 4. TAB NAVIGASI MULTIPANEL
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Profil Pengguna", "⚠️ Ketergantungan & Dampak", "🔗 Analisis Korelasi", "🎲 Simulasi Monte Carlo"])

sns.set_theme(style="whitegrid")

# --- TAB 1: PROFIL PENGGUNA ---
with tab1:
    st.header("Profil Penggunaan AI Harian")
    c1, c2 = st.columns(2)
    
    with c1:
        # Pie Chart Frekuensi
        fig1, ax1 = plt.subplots(figsize=(6, 5))
        freq_order = ['Setiap hari', '3-5 kali seminggu', '1-2 kali seminggu', 'Kurang dari 1 kali seminggu']
        counts = df['Frekuensi_Penggunaan'].value_counts().reindex(freq_order)
        ax1.pie(counts.values, labels=counts.index, autopct='%1.1f%%', colors=['#660099', '#9954b8', '#cc99cc', '#e1cae6'], startangle=140)
        ax1.set_title("Distribusi Frekuensi Penggunaan AI", fontweight='bold')
        st.pyplot(fig1)
        plt.close(fig1)
        
    with c2:
        # Histogram Jam per Hari
        fig2, ax2 = plt.subplots(figsize=(7, 5))
        sns.histplot(data=df, x='Jam_per_Hari', bins=8, kde=True, color='#457B9D', ax=ax2)
        ax2.set_title("Distribusi Durasi Penggunaan (Jam/Hari)", fontweight='bold')
        ax2.set_ylabel("Jumlah Mahasiswa")
        st.pyplot(fig2)
        plt.close(fig2)

# --- TAB 2: KETERGANTUNGAN & DAMPAK ---
with tab2:
    st.header("Analisis Ketergantungan dan Integritas")
    c3, c4 = st.columns(2)
    
    with c3:
        # Probabilitas Bersyarat
        fig3, ax3 = plt.subplots(figsize=(7, 5))
        prob_data = pd.crosstab(df['Is_Ketergantungan_Tinggi'], df['Kesulitan_Tanpa_AI'], normalize='index') * 100
        prob_data.plot(kind='bar', stacked=True, color=['#e63946', '#457b9d'], ax=ax3)
        ax3.set_title("Peluang Merasa Kesulitan Tanpa AI", fontweight='bold')
        ax3.set_ylabel("Persentase (%)")
        ax3.tick_params(axis='x', rotation=0)
        for p in ax3.patches:
            if p.get_height() > 0:
                ax3.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width()/2, p.get_y() + p.get_height()/2), ha='center', va='center', color='white', fontweight='bold')
        st.pyplot(fig3)
        plt.close(fig3)
        
    with c4:
        # Peningkatan Nilai
        fig4, ax4 = plt.subplots(figsize=(7, 5))
        sns.countplot(data=df, x='Peningkatan_Nilai', palette='Set2', ax=ax4, order=['Ya, meningkat drastis', 'Ya, meningkat sedikit', 'Tidak ada perubahan'])
        ax4.set_title("Persepsi Peningkatan Nilai", fontweight='bold')
        ax4.set_ylabel("Jumlah Responden")
        st.pyplot(fig4)
        plt.close(fig4)
        
    with st.expander("💡 Insight Analisis (Klik untuk membuka)"):
        st.write("**Temuan Krusial:** Mahasiswa dengan ketergantungan tinggi (>5 tugas diserahkan ke AI) memiliki probabilitas **83.3%** merasa kesulitan belajar tanpa AI, jauh lebih rentan dibanding mahasiswa berketergantungan rendah (43.7%). Hal ini mengonfirmasi adanya sindrom ketergantungan teknologi.")

# --- TAB 3: ANALISIS KORELASI ---
with tab3:
    st.header("Matriks Korelasi Pearson")
    st.markdown("Menganalisis hubungan linier antara Intensitas Bantuan AI, Tingkat Copy-Paste, dan Efektivitas Belajar.")
    
    c5, c6 = st.columns(2)
    with c5:
        # Heatmap
        matrix_corr = df[['Jam_per_Hari', 'Porsi_Tugas_AI', 'Tingkat_Copy_Paste', 'Skor_Efektivitas']].corr()
        fig5, ax5 = plt.subplots(figsize=(6, 5))
        sns.heatmap(matrix_corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".3f", ax=ax5)
        st.pyplot(fig5)
        plt.close(fig5)
        
    with c6:
        # Regplot
        fig6, ax6 = plt.subplots(figsize=(7, 5))
        sns.regplot(data=df, x='Porsi_Tugas_AI', y='Skor_Efektivitas', color='#8338ec', scatter_kws={'s':60, 'alpha':0.6}, line_kws={'color':'red'})
        ax6.set_title("Tren Efektivitas vs Porsi Bantuan AI", fontweight='bold')
        st.pyplot(fig6)
        plt.close(fig6)

# --- TAB 4: SIMULASI MONTE CARLO ---
with tab4:
    st.header("Simulasi Monte Carlo (Proyeksi Populasi)")
    
    # Interaktivitas
    iterasi = st.slider("Atur Jumlah Iterasi Simulasi (Semakin besar semakin stabil kurvanya):", min_value=1000, max_value=20000, value=10000, step=1000)
    
    if st.button("🚀 Eksekusi Simulasi Komputasi", type="primary"):
        with st.spinner("Menghitung probabilitas stokastik..."):
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
            
            # Plot
            c7, c8 = st.columns(2)
            with c7:
                fig7, ax7 = plt.subplots(figsize=(7, 5))
                ax7.hist(hasil, bins=50, color='#2a9d8f', edgecolor='black', alpha=0.75, density=True)
                ax7.axvline(mean_mc, color='orange', ls='--', lw=2.5, label=f'Mean: {mean_mc:.3f}')
                ax7.axvline(ci_low, color='red', ls=':', lw=2, label=f'CI Bawah: {ci_low:.3f}')
                ax7.axvline(ci_high, color='red', ls=':', lw=2, label=f'CI Atas: {ci_high:.3f}')
                ax7.set_title("Histogram Distribusi Probabilitas")
                ax7.legend()
                st.pyplot(fig7)
                plt.close(fig7)
                
            with c8:
                running_mean = np.cumsum(hasil) / np.arange(1, iterasi+1)
                fig8, ax8 = plt.subplots(figsize=(7, 5))
                ax8.plot(np.arange(1, iterasi+1), running_mean, color='#e76f51', lw=2)
                ax8.axhline(mean_mc, color='black', ls='--', lw=1.5)
                ax8.set_title("Grafik Konvergensi Simulasi")
                ax8.set_xlabel("Iterasi")
                st.pyplot(fig8)
                plt.close(fig8)
                
            st.success(f"**Kesimpulan Simulasi:** Berdasarkan {iterasi} simulasi pada kelas 100 mahasiswa, diproyeksikan nilai efektivitas kelas stabil di angka **{mean_mc:.3f}** (Rentang Kepercayaan 95%: {ci_low:.3f} - {ci_high:.3f}).")
