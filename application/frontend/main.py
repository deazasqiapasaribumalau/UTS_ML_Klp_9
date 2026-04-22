import requests
import streamlit as st

# ============================================================
# Konfigurasi halaman
# ============================================================
st.set_page_config(
    page_title="Plant Growth Classifier",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# Custom CSS - Glassmorphism Theme (Agricultural)
# ============================================================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        background-attachment: fixed;
    }
    
    /* Main container glass effect */
    .main .block-container {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Header Styling - Glassmorphism */
    .main-header {
        background: linear-gradient(135deg, 
            rgba(46, 125, 50, 0.6) 0%, 
            rgba(56, 142, 60, 0.6) 50%, 
            rgba(27, 94, 32, 0.6) 100%);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    .main-header h1 {
        color: #ffffff !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
        letter-spacing: 1px;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.15rem !important;
        font-weight: 300 !important;
    }
    
    /* Section Headers - Glass Effect */
    .section-header {
        color: #a5d6a7 !important;
        font-weight: 600;
        padding: 0.8rem 1rem;
        border-bottom: 2px solid rgba(76, 175, 80, 0.5);
        margin-bottom: 1.2rem;
        background: rgba(76, 175, 80, 0.1);
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }
    
    /* Card Styling - Glassmorphism */
    .css-1r6slb0, div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 16px !important;
        padding: 1.2rem !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Form Container - Glass Effect */
    .stForm {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 1.5rem !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Input Labels */
    .stSelectbox label, .stNumberInput label {
        color: #c8e6c9 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    /* Selectbox & Input - Glass Effect */
    .stSelectbox > div > div, .stNumberInput > div > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    
    .stSelectbox > div > div:hover, .stNumberInput > div > div > div:hover {
        border-color: rgba(76, 175, 80, 0.6) !important;
    }
    
    /* Dropdown menu - Glass Effect */
    div[data-baseweb="select"] > div {
        background: rgba(30, 60, 50, 0.95) !important;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
    }
    
    /* Submit Button - Glass with Glow */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, 
            rgba(46, 125, 50, 0.8) 0%, 
            rgba(76, 175, 80, 0.8) 100%) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
        padding: 0.8rem 2.5rem !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 4px 20px rgba(76, 175, 80, 0.4), 
                    0 0 30px rgba(76, 175, 80, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .stFormSubmitButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(76, 175, 80, 0.6), 
                    0 0 50px rgba(76, 175, 80, 0.3) !important;
        background: linear-gradient(135deg, 
            rgba(56, 142, 60, 0.9) 0%, 
            rgba(102, 187, 106, 0.9) 100%) !important;
    }
    
    /* Success/Error Messages - Glass Effect */
    .stSuccess, div[data-testid="stSuccess"] {
        background: rgba(76, 175, 80, 0.2) !important;
        backdrop-filter: blur(15px);
        border-left: 4px solid #4caf50 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .stError, div[data-testid="stError"] {
        background: rgba(244, 67, 54, 0.2) !important;
        backdrop-filter: blur(15px);
        border-left: 4px solid #f44336 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    /* Metrics */
    [data-testid="stMetricLabel"] {
        color: #a5d6a7 !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
    }
    
    /* Sidebar - Glass Effect */
    section[data-testid="stSidebar"] {
        background: rgba(20, 40, 35, 0.85) !important;
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #c8e6c9 !important;
    }
    
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #a5d6a7 !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(76, 175, 80, 0.5), 
            transparent);
        margin: 1.5rem 0;
    }
    
    /* Expander - Glass Effect */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(10px);
        border-radius: 10px !important;
        color: #a5d6a7 !important;
        font-weight: 500 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, 
            rgba(76, 175, 80, 0.8), 
            rgba(129, 199, 132, 0.9)) !important;
        border-radius: 10px !important;
        box-shadow: 0 0 10px rgba(76, 175, 80, 0.5) !important;
    }
    
    /* Info Box - Glass Effect */
    .stInfo {
        background: rgba(33, 150, 243, 0.15) !important;
        backdrop-filter: blur(10px);
        border-left: 4px solid #2196f3 !important;
        border-radius: 10px !important;
    }
    
    /* Spinner */
    .stSpinner {
        color: #4caf50 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(76, 175, 80, 0.5);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(76, 175, 80, 0.7);
    }
    
    /* Text colors for better visibility on dark glass */
    .stMarkdown p, .stMarkdown li {
        color: rgba(255, 255, 255, 0.85) !important;
    }
    
    /* Input help text */
    .stNumberInput .help, .stSelectbox .help {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Caption */
    .stCaption {
        color: rgba(255, 255, 255, 0.6) !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Sidebar - Informasi Aplikasi (Glassmorphism)
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; 
                background: rgba(255,255,255,0.1); 
                backdrop-filter: blur(15px);
                border-radius: 15px; 
                border: 1px solid rgba(255,255,255,0.15);
                margin-bottom: 1rem;">
        <h2 style="color: #a5d6a7; margin-bottom: 0.5rem; 
                   font-family: 'Playfair Display', serif;">🌱 AgriPredict</h2>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">Plant Growth Classification</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📋 Tentang Aplikasi")
    st.markdown("""
    <div style="background: rgba(255,255,255,0.08); 
                padding: 1rem; border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.1);">
    **Plant Growth Classifier** adalah aplikasi prediksi pertumbuhan tanaman 
    berbasis Machine Learning yang menganalisis kondisi tanah dan lingkungan 
    untuk memprediksi apakah tanaman dapat tumbuh dengan baik atau tidak.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔬 Fitur Utama")
    st.markdown("""
    <div style="background: rgba(255,255,255,0.05); 
                padding: 1rem; border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.1);">
    - 🌿 Analisis 20+ parameter tanah & lingkungan<br>
    - 🤖 Prediksi akurat berbasis model ML<br>
    - 📊 Visualisasi probabilitas hasil<br>
    - 💫 Antarmuka pengguna modern
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Parameter Input")
    st.markdown("""
    <div style="background: rgba(255,255,255,0.05); 
                padding: 1rem; border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.1);">
    - **Tanah**: pH, salinitas, bahan organik, CEC<br>
    - **Nutrisi**: N, P, K (ppm)<br>
    - **Lingkungan**: suhu, kelembapan, cahaya<br>
    - **Tanaman**: kategori tanaman
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.6);">
    <p style="font-size: 0.9rem;">🎓 <strong>UTS Praktikum Machine Learning</strong></p>
    <p style="font-size: 0.8rem;">📅 Semester 6 | Kelompok 9</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# Header Utama (Glassmorphism)
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🌱 Plant Growth Classifier</h1>
    <p>Prediksi Pertumbuhan Tanaman Berdasarkan Kondisi Tanah & Lingkungan</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: rgba(76, 175, 80, 0.15); 
            backdrop-filter: blur(10px);
            padding: 1.2rem; 
            border-radius: 12px; 
            border: 1px solid rgba(76, 175, 80, 0.3);
            margin-bottom: 1.5rem;">
    <strong style="color: #a5d6a7;">📝 Petunjuk:</strong> 
    <span style="color: rgba(255,255,255,0.85);">Isi semua parameter kondisi tanah dan lingkungan di bawah ini, 
    lalu klik tombol </span>
    <strong style="color: #81c784;">"Prediksi Pertumbuhan"</strong> 
    <span style="color: rgba(255,255,255,0.85);">untuk melihat hasil prediksi.</span>
</div>
""", unsafe_allow_html=True)

# ============================================================
# Form Input - Tiga Kolom Profesional
# ============================================================
with st.form(key='plant_prediction_form'):

    # Bagian 1: Informasi Tanah
    st.markdown('<p class="section-header">🪨 INFORMASI TANAH</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**<span style='color: #a5d6a7;'>🌍 Karakteristik Fisik Tanah</span>**", unsafe_allow_html=True)
        soil_type = st.selectbox(
            'Jenis Tanah (Soil Type)',
            options=['Clayey', 'Alluvial', 'Chalky', 'Silty', 'Loamy', 'Sandy', 'Laterite', 'Peaty', 'Saline'],
            help='Tipe/jenis tanah pada lokasi tersebut'
        )
        bulk_density = st.number_input(
            'Bulk Density (g/cm³)',
            min_value=0.70, max_value=1.60, value=1.20, step=0.01,
            help='Kepadatan tanah, rentang 0.70 - 1.60'
        )
        organic_matter_pct = st.number_input(
            'Organic Matter (%)',
            min_value=1.20, max_value=18.00, value=5.00, step=0.1,
            help='Persentase bahan organik dalam tanah'
        )
        cation_exchange_capacity = st.number_input(
            'CEC (cmol/kg)',
            min_value=5, max_value=40, value=20,
            help='Kapasitas tukar kation tanah'
        )

    with col2:
        st.markdown("**<span style='color: #a5d6a7;'>⚗️ Kimia Tanah & pH</span>**", unsafe_allow_html=True)
        soil_ph = st.number_input(
            'Soil pH',
            min_value=4.00, max_value=8.80, value=6.50, step=0.1,
            help='Nilai pH tanah (4.0 = sangat asam, 8.8 = basa)'
        )
        ph_stress_flag = st.selectbox(
            'pH Stress Flag',
            options=[0, 1],
            format_func=lambda x: "Tidak Ada Stres pH (0)" if x == 0 else "Ada Stres pH (1)",
            help='Apakah tanah mengalami stres pH?'
        )
        salinity_ec = st.number_input(
            'Salinity EC (dS/m)',
            min_value=0.20, max_value=4.00, value=1.50, step=0.1,
            help='Tingkat salinitas tanah'
        )
        buffering_capacity = st.number_input(
            'Buffering Capacity',
            min_value=0.30, max_value=0.90, value=0.60, step=0.01,
            help='Kapasitas buffer tanah'
        )

    with col3:
        st.markdown("**<span style='color: #a5d6a7;'>🌿 Nutrisi Tanah (ppm)</span>**", unsafe_allow_html=True)
        nutrient_balance = st.selectbox(
            'Nutrient Balance',
            options=['optimal', 'excessive', 'deficient'],
            help='Keseimbangan nutrisi tanah'
        )
        nitrogen_ppm = st.number_input(
            'Nitrogen (N)',
            min_value=20.0, max_value=220.0, value=120.0, step=1.0,
            help='Kandungan nitrogen dalam tanah'
        )
        phosphorus_ppm = st.number_input(
            'Phosphorus (P)',
            min_value=10.0, max_value=159.0, value=60.0, step=1.0,
            help='Kandungan fosfor dalam tanah'
        )
        potassium_ppm = st.number_input(
            'Potassium (K)',
            min_value=20.0, max_value=220.0, value=100.0, step=1.0,
            help='Kandungan kalium dalam tanah'
        )

    st.markdown("---")
    
    # Bagian 2: Kelembapan & Suhu
    st.markdown('<p class="section-header">💧 KONDISI KELEMBAPAN & SUHU</p>', unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("**<span style='color: #a5d6a7;'>💦 Regime Kelembapan</span>**", unsafe_allow_html=True)
        moisture_regime = st.selectbox(
            'Moisture Regime',
            options=['optimal', 'dry', 'waterlogged'],
            help='Kondisi kelembapan tanah secara umum'
        )
        soil_moisture_pct = st.number_input(
            'Soil Moisture (%)',
            min_value=5.0, max_value=70.0, value=35.0, step=0.5,
            help='Persentase kelembapan tanah'
        )

    with col5:
        st.markdown("**<span style='color: #a5d6a7;'>📊 Batas Kelembapan</span>**", unsafe_allow_html=True)
        moisture_limit_dry = st.number_input(
            'Moisture Limit Dry',
            min_value=8, max_value=30, value=15,
            help='Batas kelembapan minimal (kering)'
        )
        moisture_limit_wet = st.number_input(
            'Moisture Limit Wet',
            min_value=28, max_value=65, value=45,
            help='Batas kelembapan maksimal (basah)'
        )

    with col6:
        st.markdown("**🌡️ Kondisi Termal**")
        thermal_regime = st.selectbox(
            'Thermal Regime',
            options=['optimal', 'heat_stress', 'cold'],
            help='Kondisi termal lingkungan'
        )
        soil_temp_c = st.number_input(
            'Soil Temperature (°C)',
            min_value=10.0, max_value=40.0, value=25.0, step=0.5,
            help='Suhu tanah dalam derajat Celsius'
        )
        air_temp_c = st.number_input(
            'Air Temperature (°C)',
            min_value=7.0, max_value=49.6, value=28.0, step=0.5,
            help='Suhu udara dalam derajat Celsius'
        )

    st.markdown("---")
    
    # Bagian 3: Cahaya & Tanaman
    st.markdown('<p class="section-header">☀️ INFORMASI CAHAYA & TANAMAN</p>', unsafe_allow_html=True)
    col7, col8 = st.columns(2)

    with col7:
        st.markdown("**☀️ Intensitas Cahaya**")
        light_intensity_par = st.number_input(
            'Light Intensity PAR (µmol/m²/s)',
            min_value=200.0, max_value=1200.0, value=700.0, step=10.0,
            help='Intensitas cahaya yang diterima tanaman'
        )

    with col8:
        st.markdown("**🌾 Kategori Tanaman**")
        plant_category = st.selectbox(
            'Plant Category',
            options=['vegetable', 'cereal', 'legume'],
            help='Kategori tanaman yang akan ditanam'
        )

    st.markdown("---")

    # Tombol Submit
    submit_button = st.form_submit_button(
        label='🌱 Prediksi Pertumbuhan Tanaman',
        use_container_width=True
    )

# ============================================================
# Proses Prediksi
# ============================================================
if submit_button:
    # Susun data untuk dikirim ke backend
    user_input = {
        "bulk_density": bulk_density,
        "organic_matter_pct": organic_matter_pct,
        "cation_exchange_capacity": cation_exchange_capacity,
        "salinity_ec": salinity_ec,
        "buffering_capacity": buffering_capacity,
        "soil_moisture_pct": soil_moisture_pct,
        "moisture_limit_dry": moisture_limit_dry,
        "moisture_limit_wet": moisture_limit_wet,
        "soil_temp_c": soil_temp_c,
        "air_temp_c": air_temp_c,
        "light_intensity_par": light_intensity_par,
        "soil_ph": soil_ph,
        "ph_stress_flag": ph_stress_flag,
        "nitrogen_ppm": nitrogen_ppm,
        "phosphorus_ppm": phosphorus_ppm,
        "potassium_ppm": potassium_ppm,
        "soil_type": soil_type,
        "moisture_regime": moisture_regime,
        "thermal_regime": thermal_regime,
        "nutrient_balance": nutrient_balance,
        "plant_category": plant_category,
    }

    # Kirim request ke backend FastAPI
    with st.spinner('🔄 Menganalisis kondisi tanah & lingkungan...'):
        try:
            response = requests.post(
                'http://localhost:8000/predict/',
                json=user_input,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                prediction = result.get('prediction')
                label = result.get('label')
                proba = result.get('probability', {})

                st.markdown("---")
                st.markdown('<p class="section-header">📊 HASIL PREDIKSI</p>', unsafe_allow_html=True)
                
                # Card Hasil Prediksi
                if prediction == 0:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); 
                                padding: 1.5rem; border-radius: 15px; 
                                border-left: 5px solid #2e7d32; margin-bottom: 1rem;">
                        <h2 style="color: #1b5e20; margin: 0;">✅ {label}</h2>
                        <p style="color: #2e7d32; font-size: 1.1rem;">Tanaman <strong>dapat tumbuh</strong> dengan baik pada kondisi tanah ini.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%); 
                                padding: 1.5rem; border-radius: 15px; 
                                border-left: 5px solid #c62828; margin-bottom: 1rem;">
                        <h2 style="color: #b71c1c; margin: 0;">❌ {label}</h2>
                        <p style="color: #c62828; font-size: 1.1rem;">Tanaman <strong>tidak dapat tumbuh</strong> / gagal pada kondisi tanah ini.</p>
                    </div>
                    """, unsafe_allow_html=True)

                # Tampilkan probabilitas dengan visualisasi
                st.markdown("### 🎯 Probabilitas Prediksi")
                col_p1, col_p2 = st.columns(2)
                
                prob_growth = proba.get('dapat_tumbuh', 0) * 100
                prob_fail = proba.get('gagal_tumbuh', 0) * 100
                
                with col_p1:
                    st.metric(
                        label="🌱 Kemungkinan Tumbuh",
                        value=f"{prob_growth:.1f}%"
                    )
                    # Progress bar
                    st.progress(prob_growth / 100)
                    
                with col_p2:
                    st.metric(
                        label="🥀 Kemungkinan Gagal",
                        value=f"{prob_fail:.1f}%"
                    )
                    # Progress bar
                    st.progress(prob_fail / 100)

                # Ringkasan input
                with st.expander("📋 Lihat Detail Data Input"):
                    st.json(user_input)

            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                            padding: 1rem; border-radius: 10px; border-left: 4px solid #f57c00;">
                    <strong>⚠️ Error:</strong> Terjadi kesalahan pada server (Status: """ + str(response.status_code) + """)
                </div>
                """, unsafe_allow_html=True)
                st.code(response.text)

        except requests.exceptions.ConnectionError:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                        padding: 1.5rem; border-radius: 10px; border-left: 4px solid #f57c00;">
                <h3 style="color: #e65100; margin-top: 0;">⚠️ Tidak Dapat Terhubung ke Backend</h3>
                <p style="color: #ef6c00;">Pastikan backend FastAPI sudah berjalan dengan perintah:</p>
                <code style="background: #f5f5f5; padding: 0.5rem; border-radius: 5px; display: block;">
                cd application/backend<br>uvicorn main:app --reload
                </code>
            </div>
            """, unsafe_allow_html=True)
        except requests.exceptions.Timeout:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                        padding: 1rem; border-radius: 10px; border-left: 4px solid #f57c00;">
                <strong>⚠️ Request Timeout</strong> - Coba lagi beberapa saat.
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%); 
                        padding: 1rem; border-radius: 10px; border-left: 4px solid #c62828;">
                <strong>⚠️ Error:</strong> {str(e)}
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# Footer
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #558b2f;">
    <p>🌿 <strong>Plant Growth Classifier</strong> — UTS Praktikum Machine Learning</p>
    <p style="font-size: 0.85rem;">Kelompok 9 | Semester 6</p>
</div>
""", unsafe_allow_html=True)
