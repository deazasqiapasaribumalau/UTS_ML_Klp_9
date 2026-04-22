import requests
import json

# Test data
data = {
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

# Test prediction endpoint
try:
    response = requests.post('http://localhost:8000/predict/', json=data, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")