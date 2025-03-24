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
    resp = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit=1&appid={api_key}"
    ).json()

    if resp:  # check if response has data
        data = resp[0]
        return data['lat'], data['lon']
    else:
        return None, None

def get_current_weather(lat, lon, api_key):
    resp = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    ).json()

    data = WeatherData(
        main=resp.get('weather')[0].get('main'),
        desc=resp.get('weather')[0].get('description'),
        icon=resp.get('weather')[0].get('icon'),
        temp=resp.get('main').get('temp')
    )
    return data

def main(city_name, state_code, country_code):
    lat, lon = get_lat_lon(city_name, state_code, country_code, API_KEY)
    weather_data = get_current_weather(lat, lon, API_KEY)
    return {
        "temp": weather_data.temp,
        "desc": weather_data.desc,
        "icon": weather_data.icon
    }


if __name__ == '__main__':
    pass

