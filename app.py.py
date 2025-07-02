import streamlit as st
import numpy as np
import joblib
import requests
import os

# ---------- Load Model & Scaler ----------
MODEL_PATH = "crop_model.pkl"
SCALER_PATH = "scaler.pkl"

if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
    st.error("❌ Model or scaler file not found. Make sure 'crop_model.pkl' and 'scaler.pkl' are in the same folder.")
    st.stop()

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ---------- Weather API ----------
def get_weather(city, api_key):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=10)
        data = response.json()

        # Check for city not found
        if data.get("cod") != 200:
            return None, None, None

        temp = data['main']['temp']
        humidity = data['main']['humidity']
        rainfall = data.get('rain', {}).get('1h', 0.0)
        return temp, humidity, rainfall
    except Exception as e:
        return None, None, None

# ---------- Crop Prediction ----------
def recommend_crop(N, P, K, ph, temp, humidity, rainfall):
    features = np.array([[N, P, K, temp, humidity, ph, rainfall]])
    scaled = scaler.transform(features)
    prediction = model.predict(scaled)[0]
    return prediction

# ---------- Streamlit UI ----------
st.set_page_config(page_title="🌾 Crop Recommender", layout="centered")
st.title("🌱 Weather-Based Crop Recommendation System")

st.markdown("This app predicts the best crop to grow based on soil nutrients and **real-time weather data** 🌦️.")

# ---------- Input Fields ----------
API_KEY = st.text_input("🔑 Enter your OpenWeatherMap API Key", type="password")
city = st.text_input("🏙️ Enter City Name (e.g., Patna)", value="Patna")

N = st.number_input("🌿 Nitrogen (N)", min_value=0, max_value=200, value=90)
P = st.number_input("🪴 Phosphorus (P)", min_value=0, max_value=200, value=40)
K = st.number_input("🌱 Potassium (K)", min_value=0, max_value=200, value=40)
ph = st.number_input("⚗️ Soil pH", min_value=0.0, max_value=14.0, value=6.5)

# ---------- Predict Button ----------
if st.button("🚀 Recommend Crop"):
    if not API_KEY:
        st.error("❗ Please enter your OpenWeatherMap API Key.")
    else:
        temp, humidity, rainfall = get_weather(city.strip(), API_KEY.strip())

        if temp is None:
            st.error("❌ Failed to fetch weather data. Check your city name or API key.")
        else:
            crop = recommend_crop(N, P, K, ph, temp, humidity, rainfall)
            st.success(f"✅ Recommended Crop for {city.title()}: **{crop.upper()}**")
            st.info(f"🌡️ Temperature: {temp}°C\n💧 Humidity: {humidity}%\n🌧️ Rainfall: {rainfall} mm")
