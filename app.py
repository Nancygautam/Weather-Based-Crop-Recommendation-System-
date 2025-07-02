import streamlit as st
import numpy as np
import joblib
import requests

model = joblib.load('crop_model.pkl')
scaler = joblib.load('scaler.pkl')

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    rainfall = data.get('rain', {}).get('1h', 0.0)
    return temp, humidity, rainfall

def recommend_crop(N, P, K, ph, temp, humidity, rainfall):
    features = np.array([[N, P, K, temp, humidity, ph, rainfall]])
    scaled = scaler.transform(features)
    return model.predict(scaled)[0]

st.set_page_config(page_title="🌾 Crop Recommender")
st.title("🌱 Weather-Based Crop Recommendation System")

API_KEY = st.text_input("API Key", type="password")
city = st.text_input("City", "Patna")
N = st.number_input("Nitrogen (N)", 0, 200, 90)
P = st.number_input("Phosphorus (P)", 0, 200, 40)
K = st.number_input("Potassium (K)", 0, 200, 40)
ph = st.number_input("Soil pH", 0.0, 14.0, 6.5)

if st.button("Recommend Crop"):
    temp, humidity, rainfall = get_weather(city, API_KEY)
    crop = recommend_crop(N, P, K, ph, temp, humidity, rainfall)
    st.success(f"Recommended Crop: {crop}")