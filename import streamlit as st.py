import streamlit as st
import requests

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    # Debug: print full API response to console
    print(data)

    if 'main' in data:
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        rainfall = data.get('rain', {}).get('1h', 0)  # safely get rainfall in last 1 hour
        return temp, humidity, rainfall
    else:
        # If there's an error, print it and return None values
        print("Error fetching weather data:", data)
        return None, None, None

def main():
    st.title("Simple Weather App")

    # Your OpenWeatherMap API key here (replace with your actual key)
    API_KEY = "YOUR_API_KEY_HERE"

    city = st.text_input("Enter city name:")

    if st.button("Get Weather"):
        if city.strip() == "":
            st.error("Please enter a city name.")
        else:
            temp, humidity, rainfall = get_weather(city, API_KEY)

            if temp is None:
                st.error("Could not fetch weather data. Please check city name or API key.")
            else:
                st.write(f"Temperature: {temp} °C")
                st.write(f"Humidity: {humidity} %")
                st.write(f"Rainfall (last 1 hour): {rainfall} mm")

if __name__ == "__main__":
    main()
