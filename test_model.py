import joblib
import pandas as pd
import numpy as np

# Load model
model = joblib.load('model/model.pkl')
preprocessor = joblib.load('model/preprocessor.pkl')

# Test data yang sama dengan frontend
data = pd.DataFrame([{
    'bulk_density': 1.2,
    'organic_matter_pct': 5.0,
    'cation_exchange_capacity': 20,
    'salinity_ec': 1.5,
    'buffering_capacity': 0.6,
    'soil_moisture_pct': 35.0,
    'moisture_limit_dry': 15,
    'moisture_limit_wet': 45,
    'soil_temp_c': 25.0,
    'air_temp_c': 28.0,
    'light_intensity_par': 700.0,
    'soil_ph': 6.5,
    'ph_stress_flag': 0,
    'nitrogen_ppm': 120.0,
    'phosphorus_ppm': 60.0,
    'potassium_ppm': 100.0,
    'soil_type': 'Loamy',
    'moisture_regime': 'optimal',
    'thermal_regime': 'optimal',
    'nutrient_balance': 'optimal',
    'plant_category': 'vegetable'
}])

print("Input columns:", list(data.columns))
print("\nInput data:")
print(data)

# Langsung ke model (pipeline sudah包含 preprocessing)
try:
    # Predict langsung - model pipeline akan melakukan preprocessing sendiri
    pred = model.predict(data)
    proba = model.predict_proba(data)[0]
    print("\nPrediction:", pred)
    print("Probability:", proba)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()