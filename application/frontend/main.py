import os
import requests
import streamlit as st
import pandas as pd


def resolve_backend_url() -> str:
    env_url = os.getenv("BACKEND_URL")
    if env_url:
        return env_url

    try:
        secret_url = st.secrets.get("BACKEND_URL")
        if secret_url:
            return secret_url
    except Exception:
        pass

    return "http://localhost:8000"


BACKEND_URL = resolve_backend_url()
PREDICT_ENDPOINT = f"{BACKEND_URL.rstrip('/')}/predict/"


def request_prediction(payload: dict, timeout: int = 10):
    """Send prediction payload to backend and return HTTP response."""
    return requests.post(PREDICT_ENDPOINT, json=payload, timeout=timeout)


# ============================================================
# Preset Values dan Penjelasan Jenis Tanah
# ============================================================
SOIL_PRESETS = {
    'Loamy': {
        'bulk_density': 1.20, 'organic_matter_pct': 5.0,
        'cation_exchange_capacity': 20, 'salinity_ec': 1.5,
        'buffering_capacity': 0.60, 'moisture_limit_dry': 15,
        'moisture_limit_wet': 45, 'nitrogen_ppm': 120.0,
        'phosphorus_ppm': 60.0, 'potassium_ppm': 100.0,
        'light_intensity_par': 700.0
    },
    'Sandy': {
        'bulk_density': 1.40, 'organic_matter_pct': 2.5,
        'cation_exchange_capacity': 8, 'salinity_ec': 1.2,
        'buffering_capacity': 0.35, 'moisture_limit_dry': 8,
        'moisture_limit_wet': 28, 'nitrogen_ppm': 100.0,
        'phosphorus_ppm': 40.0, 'potassium_ppm': 80.0,
        'light_intensity_par': 750.0
    },
    'Clayey': {
        'bulk_density': 1.35, 'organic_matter_pct': 6.0,
        'cation_exchange_capacity': 30, 'salinity_ec': 1.8,
        'buffering_capacity': 0.75, 'moisture_limit_dry': 20,
        'moisture_limit_wet': 55, 'nitrogen_ppm': 140.0,
        'phosphorus_ppm': 70.0, 'potassium_ppm': 120.0,
        'light_intensity_par': 650.0
    },
    'Silty': {
        'bulk_density': 1.25, 'organic_matter_pct': 5.5,
        'cation_exchange_capacity': 18, 'salinity_ec': 1.4,
        'buffering_capacity': 0.55, 'moisture_limit_dry': 14,
        'moisture_limit_wet': 42, 'nitrogen_ppm': 115.0,
        'phosphorus_ppm': 55.0, 'potassium_ppm': 95.0,
        'light_intensity_par': 700.0
    },
    'Peaty': {
        'bulk_density': 0.80, 'organic_matter_pct': 15.0,
        'cation_exchange_capacity': 25, 'salinity_ec': 0.8,
        'buffering_capacity': 0.70, 'moisture_limit_dry': 25,
        'moisture_limit_wet': 65, 'nitrogen_ppm': 160.0,
        'phosphorus_ppm': 50.0, 'potassium_ppm': 110.0,
        'light_intensity_par': 600.0
    },
    'Chalky': {
        'bulk_density': 1.30, 'organic_matter_pct': 3.0,
        'cation_exchange_capacity': 12, 'salinity_ec': 1.3,
        'buffering_capacity': 0.45, 'moisture_limit_dry': 12,
        'moisture_limit_wet': 35, 'nitrogen_ppm': 90.0,
        'phosphorus_ppm': 45.0, 'potassium_ppm': 85.0,
        'light_intensity_par': 720.0
    },
    'Alluvial': {
        'bulk_density': 1.22, 'organic_matter_pct': 5.8,
        'cation_exchange_capacity': 22, 'salinity_ec': 1.4,
        'buffering_capacity': 0.62, 'moisture_limit_dry': 16,
        'moisture_limit_wet': 48, 'nitrogen_ppm': 125.0,
        'phosphorus_ppm': 62.0, 'potassium_ppm': 105.0,
        'light_intensity_par': 690.0
    },
    'Laterite': {
        'bulk_density': 1.33, 'organic_matter_pct': 3.5,
        'cation_exchange_capacity': 14, 'salinity_ec': 1.6,
        'buffering_capacity': 0.50, 'moisture_limit_dry': 14,
        'moisture_limit_wet': 40, 'nitrogen_ppm': 95.0,
        'phosphorus_ppm': 42.0, 'potassium_ppm': 88.0,
        'light_intensity_par': 730.0
    },
    'Saline': {
        'bulk_density': 1.28, 'organic_matter_pct': 2.8,
        'cation_exchange_capacity': 11, 'salinity_ec': 3.2,
        'buffering_capacity': 0.42, 'moisture_limit_dry': 11,
        'moisture_limit_wet': 33, 'nitrogen_ppm': 80.0,
        'phosphorus_ppm': 38.0, 'potassium_ppm': 76.0,
        'light_intensity_par': 740.0
    },
}

SOIL_INFO = {
    'Loamy': {
        'emoji': '🟫',
        'deskripsi': 'Tanah ideal! Campuran pasir, lempung & silt. Subur, mudah dikerjakan.',
        'cocok_untuk': 'Hampir semua tanaman',
        'ciri': 'Warna coklat, remah, drainase baik'
    },
    'Sandy': {
        'emoji': '🟡',
        'deskripsi': 'Tanah ringan & porus. Drainase cepat, perlu nutrisi lebih sering.',
        'cocok_untuk': 'Tanaman tahan kering (wortel, kacang)',
        'ciri': 'Warna kuning, terasa kasar, cepat kering'
    },
    'Clayey': {
        'emoji': '🟩',
        'deskripsi': 'Tanah berat & lengket. Drainase lambat, kaya nutrisi, keras saat kering.',
        'cocok_untuk': 'Padi, sayuran air',
        'ciri': 'Warna gelap, lengket, sulit dikerjakan saat basah'
    },
    'Silty': {
        'emoji': '⚪',
        'deskripsi': 'Tanah halus, mudah erosi. Subur tapi perlu perbaikan drainase.',
        'cocok_untuk': 'Gandum, sayuran umum',
        'ciri': 'Warna abu-abu, terasa halus seperti bubuk'
    },
    'Peaty': {
        'emoji': '🟤',
        'deskripsi': 'Tanah gambut. Sangat organik, asam, perlu amandemen.',
        'cocok_untuk': 'Tanaman toleran asam (blueberry)',
        'ciri': 'Warna coklat gelap, banyak sisa organik, asam'
    },
    'Chalky': {
        'emoji': '⚫',
        'deskripsi': 'Tanah berkapur. Basa, kurang air, kurang nutrisi.',
        'cocok_untuk': 'Tanaman tahan kapur',
        'ciri': 'Warna terang, berbatu, alkalin'
    },
    'Alluvial': {
        'emoji': '🟠',
        'deskripsi': 'Tanah sungai. Subur dari endapan aluvial, mudah banjir.',
        'cocok_untuk': 'Padi, sayuran',
        'ciri': 'Berlapis, warna bervariasi, fertile'
    },
    'Laterite': {
        'emoji': '🔴',
        'deskripsi': 'Tanah merah tropis. Tinggi besi, asam, perlu kapur.',
        'cocok_untuk': 'Tanaman tropis',
        'ciri': 'Warna merah/orange, keras, kurang subur'
    },
    'Saline': {
        'emoji': '⚪️',
        'deskripsi': 'Tanah asin. Tinggi garam, tidak cocok untuk tanaman biasa.',
        'cocok_untuk': 'Tanaman halophyte',
        'ciri': 'Putih, rasa asin, sulit berproduktif'
    },
}


# ============================================================
# Konfigurasi halaman
# ============================================================
st.set_page_config(
    page_title="Plant Growth Classifier",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# ============================================================
# Custom CSS - Glassmorphism dengan Color Fix
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

    .stApp {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(180deg, #f4f7fb 0%, #eef3f8 100%);
        color: #1f2937;
    }

    .main .block-container {
        background: #ffffff;
        border-radius: 18px;
        border: 1px solid #d9e2ec;
        padding: 2rem;
        box-shadow: 0 10px 26px rgba(31, 41, 55, 0.08);
    }

    .main-header {
        background: linear-gradient(135deg, #d8f3dc 0%, #b7e4c7 55%, #95d5b2 100%);
        padding: 2.2rem;
        border-radius: 16px;
        margin-bottom: 1.25rem;
        text-align: center;
        border: 1px solid #74c69d;
        box-shadow: 0 6px 18px rgba(116, 198, 157, 0.22);
    }

    .main-header h1 {
        color: #114b2e !important;
        font-family: 'Playfair Display', serif !important;
        font-size: 2.6rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.35rem !important;
    }

    .main-header p {
        color: #1b4332 !important;
        font-weight: 500;
    }

    .section-header {
        color: #0f5132 !important;
        background: #e9f7ef !important;
        font-weight: 700;
        padding: 0.8rem 1rem;
        border: 1px solid #b7e4c7;
        margin-bottom: 1rem;
        border-radius: 10px;
    }

    .step-indicator {
        background: #ecfdf3;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1.2rem;
        border: 1px solid #b7e4c7;
    }

    .step-indicator strong {
        color: #166534 !important;
    }

    .step-indicator p {
        color: #14532d !important;
    }

    .stForm {
        background: #f8fafc !important;
        padding: 1.25rem !important;
        border-radius: 16px !important;
        border: 1px solid #dbe7f3 !important;
    }

    .stSelectbox label, .stNumberInput label, .stSlider label, label {
        color: #1f2937 !important;
        font-weight: 600 !important;
    }

    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #2d6a4f 0%, #40916c 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border-radius: 10px !important;
        border: 1px solid #2d6a4f !important;
        box-shadow: 0 6px 16px rgba(45, 106, 79, 0.2) !important;
    }

    .stFormSubmitButton > button:hover {
        transform: translateY(-1px) !important;
        filter: brightness(1.04);
    }

    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
    }

    div[data-baseweb="select"] * {
        color: #1f2937 !important;
    }

    .stNumberInput input,
    .stTextInput input,
    .stTextArea textarea {
        color: #1f2937 !important;
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
    }

    .stTabs [data-baseweb="tab-list"] button {
        color: #334155 !important;
        background: #f1f5f9 !important;
        border-radius: 10px 10px 0 0 !important;
        border: 1px solid #d9e2ec !important;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #14532d !important;
        background: #dcfce7 !important;
        border-bottom: 2px solid #22c55e !important;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] * {
        color: #334155 !important;
    }

    [data-testid="stMetricValue"] {
        color: #0f172a !important;
    }

    table, .dataframe {
        color: #1f2937 !important;
        background: #ffffff !important;
    }

    thead {
        background: #dcfce7 !important;
    }

    .stMarkdown,
    .stMarkdown p,
    .stMarkdown li,
    .stMarkdown span {
        color: #1f2937 !important;
    }

    div[data-testid="stAlert"] {
        background: #eff6ff !important;
        border: 1px solid #93c5fd !important;
    }

    div[data-testid="stAlert"] * {
        color: #1e3a8a !important;
    }

    .tip-box {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        border-radius: 12px;
        padding: 0.85rem 1rem;
        color: #1e3a8a;
        font-weight: 600;
    }

    section[data-testid="stSidebar"] {
        background: #f8fafc !important;
        border-right: 1px solid #dbe7f3 !important;
    }

    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1f2937 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Sidebar - Informasi Aplikasi & Jenis Tanah
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: #ffffff; 
                border-radius: 15px; border: 1px solid #dbe7f3; margin-bottom: 1rem; box-shadow: 0 6px 14px rgba(15, 23, 42, 0.06);">
        <h2 style="color: #1b4332; margin-bottom: 0.5rem; font-family: 'Playfair Display', serif;">🌱 AgriPredict</h2>
        <p style="color: #475569; font-size: 0.85rem;">Plant Growth Classifier</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📚 Jenis-Jenis Tanah")
    
    # Soil type selector di sidebar
    selected_soil = st.selectbox("Pilih untuk info lengkap:", list(SOIL_INFO.keys()))
    soil = SOIL_INFO[selected_soil]
    
    st.markdown(f"""
    <div style="background: #ecfdf3; padding: 1rem; border-radius: 10px; border-left: 4px solid #22c55e; border: 1px solid #bbf7d0;">
        <h3 style="color: #0d3b2a; margin-top: 0;">{soil['emoji']} {selected_soil}</h3>
        <p style="color: #0f3f2d;"><strong>Deskripsi:</strong> {soil['deskripsi']}</p>
        <p style="color: #155239;"><strong>Cocok untuk:</strong> {soil['cocok_untuk']}</p>
        <p style="color: #155239;"><strong>Ciri-ciri:</strong> {soil['ciri']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### ✨ Tentang Aplikasi")
    st.markdown("""
    <div style="background: #eff6ff; padding: 1rem; border-radius: 10px; border-left: 4px solid #3b82f6; border: 1px solid #bfdbfe;">
        <p style="color: #1e3a8a; margin: 0; font-size: 0.9rem;">
        Aplikasi prediksi pertumbuhan tanaman berbasis Machine Learning. Cukup input kondisi tanah sederhana, sistem akan otomatis menganalisis dan memberikan prediksi akurat.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔌 Backend API")
    st.code(BACKEND_URL)
    if "localhost" in BACKEND_URL or "127.0.0.1" in BACKEND_URL:
        st.warning("Untuk deploy publik, ganti BACKEND_URL ke endpoint backend online.")
    else:
        st.success("Backend URL sudah siap untuk akses publik.")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #334155; font-size: 0.9rem;">
    🎓 UTS Praktikum ML | Kelompok 9
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# Header Utama
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>🌱 Plant Growth Classifier</h1>
    <p>Prediksi Pertumbuhan Tanaman dengan Mudah & Akurat</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# STEP 1: FORM SEDERHANA
# ============================================================
if st.session_state.step == 1:
    st.markdown("""
    <div class="step-indicator">
        <strong>📝 Langkah 1 / 2: Informasi Dasar Tanah</strong>
        <p>Isi informasi dasar tanah dan tanaman yang mudah diukur. Parameter lanjutan akan diatur otomatis berdasarkan jenis tanah kamu.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form(key='step1_form'):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<p class="section-header">🌾 TANAMAN & TANAH</p>', unsafe_allow_html=True)
            
            plant_category = st.selectbox(
                '🌿 Kategori Tanaman',
                options=['vegetable', 'cereal', 'legume'],
                format_func=lambda x: {'vegetable': '🥬 Sayuran', 'cereal': '🌾 Serealia', 'legume': '🫘 Kacang-kacangan'}.get(x),
            )
            
            soil_type = st.selectbox(
                '🪨 Jenis Tanah',
                options=['Loamy', 'Sandy', 'Clayey', 'Silty', 'Peaty', 'Chalky', 'Alluvial', 'Laterite', 'Saline'],
            )
            
            st.markdown(
                '<div class="tip-box">💡 Tips: Lihat deskripsi jenis tanah di sidebar untuk membantu kamu memilih.</div>',
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown('<p class="section-header">💧 KONDISI LINGKUNGAN</p>', unsafe_allow_html=True)
            
            moisture_regime = st.selectbox(
                '💦 Kondisi Kelembapan Tanah',
                options=['optimal', 'dry', 'waterlogged'],
                format_func=lambda x: {'optimal': '✅ Normal (basah tapi tidak licin)', 'dry': '🏜️ Kering', 'waterlogged': '🌊 Sangat Basah (berair)'}.get(x),
            )
            
            thermal_regime = st.selectbox(
                '🌡️ Kondisi Suhu Udara',
                options=['optimal', 'heat_stress', 'cold'],
                format_func=lambda x: {'optimal': '✅ Normal (20-30°C)', 'heat_stress': '🔥 Panas', 'cold': '❄️ Dingin'}.get(x),
            )
            
            soil_ph = st.slider(
                '🧪 pH Tanah (perkiraan)',
                min_value=4.0, max_value=8.8, value=6.5, step=0.5,
            )
        
        st.markdown("---")
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            next_btn = st.form_submit_button("➡️ Lanjut", use_container_width=True)
        with col_btn2:
            quick_predict = st.form_submit_button("🚀 Prediksi Sekarang (Cepat)", use_container_width=True)
        
        if quick_predict:
            preset = SOIL_PRESETS.get(soil_type, SOIL_PRESETS['Loamy'])
            st.session_state.form_data = {
                'plant_category': plant_category,
                'soil_type': soil_type,
                'moisture_regime': moisture_regime,
                'thermal_regime': thermal_regime,
                'soil_ph': soil_ph,
                'ph_stress_flag': 0,
                'soil_moisture_pct': 35.0 if moisture_regime == 'optimal' else (20.0 if moisture_regime == 'dry' else 50.0),
                'soil_temp_c': 25.0,
                'air_temp_c': 28.0 if thermal_regime == 'optimal' else (35.0 if thermal_regime == 'heat_stress' else 15.0),
                'nutrient_balance': 'optimal',
                **preset
            }
            st.session_state.step = 3
            st.rerun()
        
        if next_btn:
            st.session_state.form_data = {
                'plant_category': plant_category,
                'soil_type': soil_type,
                'moisture_regime': moisture_regime,
                'thermal_regime': thermal_regime,
                'soil_ph': soil_ph,
            }
            st.session_state.step = 2
            st.rerun()

# ============================================================
# STEP 2: FORM LANJUTAN
# ============================================================
elif st.session_state.step == 2:
    st.markdown("""
    <div class="step-indicator">
        <strong>⚙️ Langkah 2 / 2: Pengaturan Lanjutan (Opsional)</strong>
        <p>Jika punya data dari lab tanah, isi di sini. Jika tidak, biarkan nilai default.</p>
    </div>
    """, unsafe_allow_html=True)
    
    soil_type = st.session_state.form_data.get('soil_type', 'Loamy')
    preset = SOIL_PRESETS.get(soil_type, SOIL_PRESETS['Loamy'])
    
    with st.form(key='step2_form'):
        with st.expander("📋 Ringkasan Data Step 1", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Tanaman**: {st.session_state.form_data.get('plant_category')}")
                st.write(f"**Jenis Tanah**: {st.session_state.form_data.get('soil_type')}")
            with col2:
                st.write(f"**Kelembapan**: {st.session_state.form_data.get('moisture_regime')}")
                st.write(f"**Suhu**: {st.session_state.form_data.get('thermal_regime')}")
        
        st.markdown("---")
        st.markdown('<p class="section-header">🔬 PARAMETER FISIK TANAH</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            bulk_density = st.number_input(
                'Bulk Density (g/cm³)',
                min_value=0.70, max_value=1.60, 
                value=preset.get('bulk_density', 1.20), step=0.01,
            )
        with col2:
            organic_matter_pct = st.number_input(
                'Bahan Organik (%)',
                min_value=1.20, max_value=18.00,
                value=preset.get('organic_matter_pct', 5.0), step=0.1,
            )
        with col3:
            cation_exchange_capacity = st.number_input(
                'CEC (cmol/kg)',
                min_value=5, max_value=40,
                value=int(preset.get('cation_exchange_capacity', 20)),
            )
        
        st.markdown("---")
        st.markdown('<p class="section-header">⚗️ PARAMETER KIMIA TANAH</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ph_stress_flag = st.selectbox(
                'Stres pH',
                options=[0, 1],
                format_func=lambda x: "Tidak Ada (0)" if x == 0 else "Ada (1)",
            )
        with col2:
            salinity_ec = st.number_input(
                'Salinitas EC (dS/m)',
                min_value=0.20, max_value=4.00,
                value=preset.get('salinity_ec', 1.50), step=0.1,
            )
        with col3:
            buffering_capacity = st.number_input(
                'Kapasitas Buffer',
                min_value=0.30, max_value=0.90,
                value=preset.get('buffering_capacity', 0.60), step=0.01,
            )
        
        st.markdown("---")
        st.markdown('<p class="section-header">🌾 NUTRISI TANAH (ppm)</p>', unsafe_allow_html=True)
        
        nutrient_balance = st.selectbox(
            'Keseimbangan Nutrisi',
            options=['optimal', 'excessive', 'deficient'],
            format_func=lambda x: {'optimal': '✅ Optimal', 'excessive': '⚠️ Berlebihan', 'deficient': '⚠️ Kekurangan'}.get(x),
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            nitrogen_ppm = st.number_input(
                'Nitrogen (N)',
                min_value=20.0, max_value=220.0,
                value=preset.get('nitrogen_ppm', 120.0), step=1.0,
            )
        with col2:
            phosphorus_ppm = st.number_input(
                'Phosphorus (P)',
                min_value=10.0, max_value=159.0,
                value=preset.get('phosphorus_ppm', 60.0), step=1.0,
            )
        with col3:
            potassium_ppm = st.number_input(
                'Potassium (K)',
                min_value=20.0, max_value=220.0,
                value=preset.get('potassium_ppm', 100.0), step=1.0,
            )
        
        st.markdown("---")
        st.markdown('<p class="section-header">💧 PARAMETER KELEMBAPAN & CAHAYA</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            soil_moisture_pct = st.slider(
                'Kelembapan Tanah (%)',
                min_value=5.0, max_value=70.0,
                value=35.0, step=0.5,
            )
        with col2:
            moisture_limit_dry = st.number_input(
                'Batas Kering',
                min_value=8, max_value=30,
                value=int(preset.get('moisture_limit_dry', 15)),
            )
        with col3:
            moisture_limit_wet = st.number_input(
                'Batas Basah',
                min_value=28, max_value=65,
                value=int(preset.get('moisture_limit_wet', 45)),
            )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            soil_temp_c = st.slider(
                'Suhu Tanah (°C)',
                min_value=10.0, max_value=40.0, value=25.0, step=0.5,
            )
        with col2:
            air_temp_c = st.slider(
                'Suhu Udara (°C)',
                min_value=7.0, max_value=49.6, value=28.0, step=0.5,
            )
        with col3:
            light_intensity_par = st.slider(
                'Intensitas Cahaya (µmol/m²/s)',
                min_value=200.0, max_value=1200.0,
                value=preset.get('light_intensity_par', 700.0), step=10.0,
            )
        
        st.markdown("---")
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            back_btn = st.form_submit_button("⬅️ Kembali", use_container_width=True)
        with col_btn2:
            predict_btn = st.form_submit_button("🌱 Prediksi", use_container_width=True)
        
        if back_btn:
            st.session_state.step = 1
            st.rerun()
        
        if predict_btn:
            full_data = {
                **st.session_state.form_data,
                'bulk_density': bulk_density,
                'organic_matter_pct': organic_matter_pct,
                'cation_exchange_capacity': cation_exchange_capacity,
                'salinity_ec': salinity_ec,
                'buffering_capacity': buffering_capacity,
                'soil_moisture_pct': soil_moisture_pct,
                'moisture_limit_dry': moisture_limit_dry,
                'moisture_limit_wet': moisture_limit_wet,
                'soil_temp_c': soil_temp_c,
                'air_temp_c': air_temp_c,
                'light_intensity_par': light_intensity_par,
                'ph_stress_flag': ph_stress_flag,
                'nitrogen_ppm': nitrogen_ppm,
                'phosphorus_ppm': phosphorus_ppm,
                'potassium_ppm': potassium_ppm,
                'nutrient_balance': nutrient_balance,
            }
            st.session_state.form_data = full_data
            st.session_state.step = 3
            st.rerun()

# ============================================================
# STEP 3: HASIL PREDIKSI (DENGAN TABEL CANTIK)
# ============================================================
elif st.session_state.step == 3:
    st.markdown('<p class="section-header">📊 HASIL PREDIKSI</p>', unsafe_allow_html=True)
    
    with st.spinner('🔄 Menganalisis kondisi tanah & lingkungan...'):
        try:
            response = request_prediction(st.session_state.form_data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                prediction = result.get('prediction')
                label = result.get('label')
                proba = result.get('probability', {})
                
                # Hasil Prediksi - Big Card
                if prediction == 0:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%); 
                                padding: 2rem; border-radius: 15px; border-left: 5px solid #22c55e; border: 1px solid #86efac;
                                margin-bottom: 1.5rem; text-align: center;">
                        <h2 style="color: #14532d; margin: 0;">✅ {label}</h2>
                        <p style="color: #166534; font-size: 1.1rem; margin-top: 0.8rem;">
                        Tanaman <strong>dapat tumbuh dengan baik</strong> pada kondisi tanah ini! 🎉
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); 
                                padding: 2rem; border-radius: 15px; border-left: 5px solid #ef4444; border: 1px solid #fecaca;
                                margin-bottom: 1.5rem; text-align: center;">
                        <h2 style="color: #991b1b; margin: 0;">⚠️ {label}</h2>
                        <p style="color: #b91c1c; font-size: 1.1rem; margin-top: 0.8rem;">
                        Tanaman <strong>tidak dapat tumbuh</strong> / gagal pada kondisi tanah ini.
                        </p>
                        <p style="color: #7f1d1d; font-size: 0.95rem; margin-top: 0.5rem;">
                        💡 Saran: Perbaiki kondisi tanah (kelembapan, pH, nutrisi) sebelum menanam.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Probabilitas dengan Progress Bar
                st.markdown("### 🎯 Tingkat Kepercayaan Prediksi")
                col_p1, col_p2 = st.columns(2)
                
                prob_growth = proba.get('dapat_tumbuh', 0) * 100
                prob_fail = proba.get('gagal_tumbuh', 0) * 100
                
                with col_p1:
                    st.metric(label="🌱 Kemungkinan Tumbuh", value=f"{prob_growth:.1f}%")
                    st.progress(prob_growth / 100)
                
                with col_p2:
                    st.metric(label="🥀 Kemungkinan Gagal", value=f"{prob_fail:.1f}%")
                    st.progress(prob_fail / 100)
                
                # Tabel Detail Input - Cantik & Rapi
                st.markdown("### 📋 Detail Parameter yang Dianalisis")
                
                # Kategorisasi data untuk tabel
                data_tables = {
                    'Informasi Tanaman & Tanah': {
                        'Kategori Tanaman': st.session_state.form_data.get('plant_category', '-'),
                        'Jenis Tanah': st.session_state.form_data.get('soil_type', '-'),
                        'Kelembapan Regime': st.session_state.form_data.get('moisture_regime', '-'),
                        'Termal Regime': st.session_state.form_data.get('thermal_regime', '-'),
                    },
                    'Parameter Fisik Tanah': {
                        'Bulk Density (g/cm³)': f"{st.session_state.form_data.get('bulk_density', '-'):.2f}",
                        'Bahan Organik (%)': f"{st.session_state.form_data.get('organic_matter_pct', '-'):.2f}",
                        'CEC (cmol/kg)': str(st.session_state.form_data.get('cation_exchange_capacity', '-')),
                        'Buffering Capacity': f"{st.session_state.form_data.get('buffering_capacity', '-'):.2f}",
                    },
                    'Parameter Kimia Tanah': {
                        'pH Tanah': f"{st.session_state.form_data.get('soil_ph', '-'):.2f}",
                        'Salinitas EC (dS/m)': f"{st.session_state.form_data.get('salinity_ec', '-'):.2f}",
                        'Stres pH': 'Ya' if st.session_state.form_data.get('ph_stress_flag', 0) == 1 else 'Tidak',
                        'Keseimbangan Nutrisi': st.session_state.form_data.get('nutrient_balance', '-'),
                    },
                    'Nutrisi Tanah (ppm)': {
                        'Nitrogen (N)': f"{st.session_state.form_data.get('nitrogen_ppm', '-'):.1f}",
                        'Phosphorus (P)': f"{st.session_state.form_data.get('phosphorus_ppm', '-'):.1f}",
                        'Potassium (K)': f"{st.session_state.form_data.get('potassium_ppm', '-'):.1f}",
                    },
                    'Kondisi Kelembapan & Cahaya': {
                        'Kelembapan Tanah (%)': f"{st.session_state.form_data.get('soil_moisture_pct', '-'):.1f}",
                        'Batas Kering (%)': str(st.session_state.form_data.get('moisture_limit_dry', '-')),
                        'Batas Basah (%)': str(st.session_state.form_data.get('moisture_limit_wet', '-')),
                        'Intensitas Cahaya (µmol/m²/s)': f"{st.session_state.form_data.get('light_intensity_par', '-'):.1f}",
                    },
                    'Kondisi Suhu': {
                        'Suhu Tanah (°C)': f"{st.session_state.form_data.get('soil_temp_c', '-'):.1f}",
                        'Suhu Udara (°C)': f"{st.session_state.form_data.get('air_temp_c', '-'):.1f}",
                    },
                }
                
                tabs = st.tabs([f"📑 {key}" for key in data_tables.keys()])
                
                for tab, (section_name, data_dict) in zip(tabs, data_tables.items()):
                    with tab:
                        df = pd.DataFrame(list(data_dict.items()), columns=['Parameter', 'Nilai'])
                        st.dataframe(df, hide_index=True, use_container_width=True)
                
                st.markdown("---")
                
                # Tombol Aksi
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("🔄 Prediksi Lagi", use_container_width=True):
                        st.session_state.step = 1
                        st.session_state.form_data = {}
                        st.rerun()
                with col_btn2:
                    if st.button("⚙️ Edit Parameter Lanjutan", use_container_width=True):
                        st.session_state.step = 2
                        st.rerun()
                
                # Info tentang parameter
                with st.expander("ℹ️ Apakah 21 Parameter ini Sudah Cukup untuk Prediksi Akurat?"):
                    st.markdown("""
                    ✅ **YA, parameter ini sudah cukup!** Model machine learning kamu dilatih dengan 21 parameter ini dan memberikan akurasi 98.67%.
                    
                    **Penjelasan Parameter:**
                    - **11 Parameter Numerik** (bulk density, pH, NPK, suhu, dll) - mengukur karakteristik fisik & kimia tanah
                    - **5 Parameter Kategorikal** (jenis tanah, kelembapan regime, suhu regime, dll) - mendeskripsikan kondisi umum
                    - **5 Parameter Lanjutan** (CEC, salinity, buffering, dll) - detail khusus untuk presisi tinggi
                    
                    **Validasi Akurasi:**
                    - Accuracy: 98.67%
                    - F1-Score: 95.81% (keseimbangan precision & recall)
                    - ROC-AUC: 99.77% (sangat baik)
                    - Cross-Validation: ~98.63% (stabil, tidak overfitting)
                    
                    **Cukupkah untuk petani?** Untuk prediksi cepat di lapangan, cukup pakai **5 parameter dari Step 1 saja** (kategori tanaman, jenis tanah, kelembapan, suhu, pH). Nilai lainnya akan otomatis diisi berdasarkan preset yang sudah terbukti.
                    """)
            
            else:
                st.error(f"❌ Error dari backend: {response.status_code}")
                st.code(response.text)
        
        except requests.exceptions.ConnectionError:
            st.error("""
            ⚠️ **Tidak Dapat Terhubung ke Backend**
            
            Pastikan backend sudah berjalan:
            ```bash
            cd application/backend
            uvicorn main:app --reload
            ```
            """)
        except requests.exceptions.Timeout:
            st.error("⚠️ **Request Timeout** - Coba lagi beberapa saat.")
        except Exception as e:
            st.error(f"⚠️ **Error**: {str(e)}")

# ============================================================
# Footer
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #475569;">
    <p>🌿 <strong>Plant Growth Classifier</strong> — UTS Praktikum Machine Learning</p>
    <p style="font-size: 0.85rem;">Kelompok 9 | Semester 6</p>
</div>
""", unsafe_allow_html=True)
