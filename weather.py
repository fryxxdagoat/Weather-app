import requests
from dotenv import load_dotenv
import os
from dataclasses import dataclass

load_dotenv()
API_KEY = os.getenv('API_KEY')

@dataclass
class WeatherData:
    main: str
    desc: str
    icon: str
    temp: int

def get_lat_lon(city_name, state_code, country_code, api_key):
    try:
        resp = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit=1&appid={api_key}"
        ).json()

        if resp:  # Check if response has data
            data = resp[0]
            return data['lat'], data['lon']
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching latitude and longitude: {e}")
        return None, None

def get_current_weather(lat, lon, api_key):
    try:
        resp = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        ).json()

        if resp.get('weather') and resp.get('main'):
            data = WeatherData(
                main=resp['weather'][0]['main'],
                desc=resp['weather'][0]['description'],
                icon=resp['weather'][0]['icon'],
                temp=resp['main']['temp']
            )
            return data
        else:
            print("Error: Unexpected response from weather API.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching current weather: {e}")
        return None

def main(city_name, state_code, country_code):
    lat, lon = get_lat_lon(city_name, state_code, country_code, API_KEY)
    
    if lat is None or lon is None:
        print("Could not retrieve coordinates.")
        return

    weather_data = get_current_weather(lat, lon, API_KEY)
    
    if weather_data:
        return {
            "temp": weather_data.temp,
            "desc": weather_data.desc,
            "icon": weather_data.icon
        }
    else:
        print("Could not retrieve weather data.")
        return

if __name__ == '__main__':
    # Example call
    city_name = "London"
    state_code = "ON"
    country_code = "CA"
    
    weather_info = main(city_name, state_code, country_code)
    
    if weather_info:
        print(weather_info)
