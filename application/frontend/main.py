import requests
import streamlit as st

# ============================================================
# Konfigurasi halaman
# ============================================================
st.set_page_config(
    page_title="Plant Growth Classifier",
    page_icon="🌱",
    layout="wide"
)

# ============================================================
# Header
# ============================================================
st.title("🌱 Plant Growth Classifier")
st.markdown("""
Aplikasi ini memprediksi apakah suatu tanaman **dapat tumbuh** atau **gagal tumbuh**
berdasarkan kondisi tanah dan lingkungan yang diberikan.

Masukkan parameter kondisi tanah di bawah ini, lalu klik **Prediksi**.
""")
st.divider()

# ============================================================
# Form Input
# ============================================================
with st.form(key='plant_prediction_form'):

    st.subheader("🪨 Informasi Tanah")
    col1, col2, col3 = st.columns(3)

    with col1:
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
            'Cation Exchange Capacity (cmol/kg)',
            min_value=5, max_value=40, value=20,
            help='Kapasitas tukar kation tanah'
        )

    with col2:
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

    with col3:
        nutrient_balance = st.selectbox(
            'Nutrient Balance',
            options=['optimal', 'excessive', 'deficient'],
            help='Keseimbangan nutrisi tanah'
        )
        nitrogen_ppm = st.number_input(
            'Nitrogen (ppm)',
            min_value=20.0, max_value=220.0, value=120.0, step=1.0,
            help='Kandungan nitrogen dalam tanah'
        )
        phosphorus_ppm = st.number_input(
            'Phosphorus (ppm)',
            min_value=10.0, max_value=159.0, value=60.0, step=1.0,
            help='Kandungan fosfor dalam tanah'
        )
        potassium_ppm = st.number_input(
            'Potassium (ppm)',
            min_value=20.0, max_value=220.0, value=100.0, step=1.0,
            help='Kandungan kalium dalam tanah'
        )

    st.divider()
    st.subheader("💧 Kondisi Kelembapan & Temperatur")
    col4, col5, col6 = st.columns(3)

    with col4:
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

    st.divider()
    st.subheader("☀️ Informasi Cahaya & Tanaman")
    col7, col8 = st.columns(2)

    with col7:
        light_intensity_par = st.number_input(
            'Light Intensity PAR (µmol/m²/s)',
            min_value=200.0, max_value=1200.0, value=700.0, step=10.0,
            help='Intensitas cahaya yang diterima tanaman'
        )

    with col8:
        plant_category = st.selectbox(
            'Plant Category',
            options=['vegetable', 'cereal', 'legume'],
            help='Kategori tanaman yang akan ditanam'
        )

    st.divider()

    # Tombol Submit
    submit_button = st.form_submit_button(
        label='🔍 Prediksi Pertumbuhan Tanaman',
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
    with st.spinner('Memproses prediksi...'):
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

                st.divider()
                st.subheader("📊 Hasil Prediksi")

                if prediction == 0:
                    st.success(f"✅ **{label}**\n\nTanaman **dapat tumbuh** pada kondisi tanah ini.")
                else:
                    st.error(f"❌ **{label}**\n\nTanaman **tidak dapat tumbuh** / gagal pada kondisi tanah ini.")

                # Tampilkan probabilitas
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    st.metric(
                        label="🌱 Probabilitas Dapat Tumbuh",
                        value=f"{proba.get('dapat_tumbuh', 0) * 100:.2f}%"
                    )
                with col_p2:
                    st.metric(
                        label="🥀 Probabilitas Gagal Tumbuh",
                        value=f"{proba.get('gagal_tumbuh', 0) * 100:.2f}%"
                    )

                # Ringkasan input
                with st.expander("📋 Lihat Detail Input yang Dikirim"):
                    st.json(user_input)

            else:
                st.error(f"❌ Terjadi kesalahan pada server. Status code: {response.status_code}")
                st.code(response.text)

        except requests.exceptions.ConnectionError:
            st.error(
                "⚠️ **Tidak dapat terhubung ke backend.**\n\n"
                "Pastikan backend FastAPI sudah berjalan dengan perintah:\n"
                "```\ncd application/backend\nuvicorn main:app --reload\n```"
            )
        except requests.exceptions.Timeout:
            st.error("⚠️ Request timeout. Coba lagi beberapa saat.")
        except Exception as e:
            st.error(f"⚠️ Terjadi error: {str(e)}")

# ============================================================
# Footer
# ============================================================
st.divider()
st.caption("🌿 Plant Growth Classifier — UTS Praktikum Machine Learning")
