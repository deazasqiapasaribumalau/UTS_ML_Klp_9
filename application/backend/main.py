import joblib
import uvicorn
import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ============================================================
# Inisialisasi FastAPI
# ============================================================
app = FastAPI(
    title="Plant Growth Classification API",
    description="API untuk mengklasifikasikan apakah tanaman dapat tumbuh pada kondisi tanah tertentu.",
    version="1.0.0"
)

# Izinkan akses dari frontend (Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Load model dan preprocessor yang sudah dilatih
# ============================================================
model = joblib.load('../../model/model.pkl')
preprocessor = joblib.load('../../model/preprocessor.pkl')

# ============================================================
# Definisi kolom fitur (HARUS SAMA dengan notebook)
# ============================================================
NUMERIC_FEATURES = [
    'bulk_density', 'organic_matter_pct', 'cation_exchange_capacity',
    'salinity_ec', 'buffering_capacity', 'soil_moisture_pct',
    'moisture_limit_dry', 'moisture_limit_wet', 'soil_temp_c',
    'air_temp_c', 'light_intensity_par', 'soil_ph',
    'ph_stress_flag', 'nitrogen_ppm', 'phosphorus_ppm', 'potassium_ppm'
]

CATEGORICAL_FEATURES = [
    'soil_type', 'moisture_regime', 'thermal_regime',
    'nutrient_balance', 'plant_category'
]

ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

# ============================================================
# Schema input dari pengguna (Pydantic BaseModel)
# ============================================================
class UserInput(BaseModel):
    # Fitur Numerik
    bulk_density: float
    organic_matter_pct: float
    cation_exchange_capacity: int
    salinity_ec: float
    buffering_capacity: float
    soil_moisture_pct: float
    moisture_limit_dry: int
    moisture_limit_wet: int
    soil_temp_c: float
    air_temp_c: float
    light_intensity_par: float
    soil_ph: float
    ph_stress_flag: int
    nitrogen_ppm: float
    phosphorus_ppm: float
    potassium_ppm: float

    # Fitur Kategorikal
    soil_type: str           # Clayey, Alluvial, Chalky, Silty, Loamy, Sandy, Laterite, Peaty, Saline
    moisture_regime: str     # dry, optimal, waterlogged
    thermal_regime: str      # optimal, heat_stress, cold
    nutrient_balance: str    # excessive, optimal, deficient
    plant_category: str      # vegetable, cereal, legume

    class Config:
        json_schema_extra = {
            "example": {
                "bulk_density": 1.2,
                "organic_matter_pct": 5.0,
                "cation_exchange_capacity": 20,
                "salinity_ec": 1.5,
                "buffering_capacity": 0.6,
                "soil_moisture_pct": 35.0,
                "moisture_limit_dry": 15,
                "moisture_limit_wet": 45,
                "soil_temp_c": 25.0,
                "air_temp_c": 28.0,
                "light_intensity_par": 700.0,
                "soil_ph": 6.5,
                "ph_stress_flag": 0,
                "nitrogen_ppm": 120.0,
                "phosphorus_ppm": 60.0,
                "potassium_ppm": 100.0,
                "soil_type": "Loamy",
                "moisture_regime": "optimal",
                "thermal_regime": "optimal",
                "nutrient_balance": "optimal",
                "plant_category": "vegetable"
            }
        }

# ============================================================
# Endpoints
# ============================================================

@app.get("/", summary="Root endpoint")
def root():
    return {"message": "Plant Growth Classification API is running!"}


@app.get("/health", summary="Health check")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}


@app.post(
    "/predict/",
    summary="Prediksi apakah tanaman dapat tumbuh pada kondisi tanah tertentu"
)
async def predict(user_input: UserInput):
    """
    Menerima data kondisi tanah dari frontend dan mengembalikan prediksi:
    - **0** = Tanaman dapat tumbuh (tidak gagal)
    - **1** = Tanaman gagal tumbuh
    """
    # Ubah input menjadi DataFrame dengan urutan kolom yang sama seperti training
    data = pd.DataFrame([{
        'bulk_density': user_input.bulk_density,
        'organic_matter_pct': user_input.organic_matter_pct,
        'cation_exchange_capacity': user_input.cation_exchange_capacity,
        'salinity_ec': user_input.salinity_ec,
        'buffering_capacity': user_input.buffering_capacity,
        'soil_moisture_pct': user_input.soil_moisture_pct,
        'moisture_limit_dry': user_input.moisture_limit_dry,
        'moisture_limit_wet': user_input.moisture_limit_wet,
        'soil_temp_c': user_input.soil_temp_c,
        'air_temp_c': user_input.air_temp_c,
        'light_intensity_par': user_input.light_intensity_par,
        'soil_ph': user_input.soil_ph,
        'ph_stress_flag': user_input.ph_stress_flag,
        'nitrogen_ppm': user_input.nitrogen_ppm,
        'phosphorus_ppm': user_input.phosphorus_ppm,
        'potassium_ppm': user_input.potassium_ppm,
        'soil_type': user_input.soil_type,
        'moisture_regime': user_input.moisture_regime,
        'thermal_regime': user_input.thermal_regime,
        'nutrient_balance': user_input.nutrient_balance,
        'plant_category': user_input.plant_category,
    }])

    # Langsung prediksi - model berupa Pipeline yang sudah包含 preprocessing
    prediction = model.predict(data)
    prediction_proba = model.predict_proba(data)[0]

    label = "Gagal Tumbuh" if prediction[0] == 1 else "Dapat Tumbuh"

    return {
        "prediction": int(prediction[0]),
        "label": label,
        "probability": {
            "dapat_tumbuh": round(float(prediction_proba[0]), 4),
            "gagal_tumbuh": round(float(prediction_proba[1]), 4),
        }
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
