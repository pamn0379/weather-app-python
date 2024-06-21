#weather.py
import argparse
import requests
from configparser import ConfigParser
from urllib import parse
import style

BASE_WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
THUNDERSTORM = range(200, 300)
DRIZZLE = range(300, 400)
RAIN = range(500, 600)
SNOW = range(600, 700)
ATMOSPHERE = range(700, 800)
CLEAR = range(800, 801)
CLOUDY = range(801, 900)

def _get_API_key():
    config = ConfigParser()
    config.read('secret.ini')
    return config['openweather']['api_key']

def read_user_cli_args():
    parser = argparse.ArgumentParser(description='gets weather and temperature information for a city')
    parser.add_argument('city', nargs='+', type=str, help='enter the city name')
    parser.add_argument(
        '-i', '--imperial', action='store_true', help='display the temperature in imperial units'
    )
    return parser.parse_args()

def build_weather_query(city_input, imperial=False):
    api_key = _get_API_key()
    city_name = ' '.join(city_input)
    city_name_encoded = parse.quote_plus(city_name)
    units = 'imperial' if imperial else 'metric'
    url = (
        f'{BASE_WEATHER_API_URL}?q={city_name_encoded}&units={units}&appid={api_key}'
    )
    return url

def get_weather_data(query_url):
    response = requests.get(query_url)
    response.raise_for_status()
    return response.json()

def display_weather_info(weather_data, imperial=False):
    city = weather_data['name']
    description = weather_data['weather'][0]['description']
    temp = weather_data['main']['temp']
    weather_id = weather_data['weather'][0]['id']

    emoji, color = _select_weather_display_params(weather_id)

    style.change_color(style.REVERSE)
    print(f'{city:^{style.PADDING}}', end='')
    style.change_color(style.RESET)

    style.change_color(color)
    print(f'{emoji}')
    print(f'\t{description:^{style.PADDING}}', end=' ')
    style.change_color(style.RESET)

    print(f'({temp}°{'F' if imperial else 'C'})')

def _select_weather_display_params(weather_id):
    if weather_id in THUNDERSTORM:
        display_params = ("💥", style.RED)
    elif weather_id in DRIZZLE:
        display_params = ("💧", style.CYAN)
    elif weather_id in RAIN:
        display_params = ("💦", style.BLUE)
    elif weather_id in SNOW:
        display_params = ("⛄️", style.WHITE)
    elif weather_id in ATMOSPHERE:
        display_params = ("🌀", style.BLUE)
    elif weather_id in CLEAR:
        display_params = ("🔆", style.YELLOW)
    elif weather_id in CLOUDY:
        display_params = ("💨", style.WHITE)
    else:  # In case the API adds new weather codes
        display_params = ("🌈", style.RESET)
    return display_params

if __name__ == '__main__':
    user_args = read_user_cli_args()
    query_url = build_weather_query(user_args.city, user_args.imperial)
    weather_data = get_weather_data(query_url)
    display_weather_info(weather_data)
