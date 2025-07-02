def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if 'main' not in data:
            st.error(f"❌ API Error: {data.get('message', 'Unknown error')}")
            return None, None, None

        temp = data['main']['temp']
        humidity = data['main']['humidity']
        rainfall = data.get('rain', {}).get('1h', 0.0)
        return temp, humidity, rainfall
    except Exception as e:
        st.error(f"❌ Weather fetch failed: {e}")
        return None, None, None
