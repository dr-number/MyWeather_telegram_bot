import json
import requests
import datetime

import redis

from constants import WEATHER_APP_ID
from weather_emoji import get_emoji

CITY_MOSСOW = "Москва"
CITY_SAINT_PETERBURG = "Санкт-Петербург"
CITY_NOVOSIBIRSK = "Новосибирск"

class Weather():

    __TTL = 60 * 1000 * 4
    __URL_ONE_CALL = 'https://api.openweathermap.org/data/2.5/onecall'
    __URL_WEATHER  = 'https://api.openweathermap.org/data/2.5/weather'

    __cache = None
    __sym_degree_celsius = u'\U00002103'

    __days_week = [ "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    __months = ["Янв.", "Фев", "Maрт", "Апр.", "Май", "Июнь", "Июль", "Авг.", "Сен.", "Окт.", "Ноя.", "Дек."]

    def __init__(self):
        self.__cache = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

    def get_link_to_map(self, lat: str, lon: str, city: str = '') -> str:
        return f"<a href=\"https://yandex.ru/maps/?ll={lon},{lat}&z=12&l=map\">{city} на карте</a>\n"
    
    def get_country_info(self, country: str, city: str) -> str:
        info = f"Страна: <b>{country}</b>\n"
        info += f"Город: <b>{city}</b>\n"
        return info

    def get_coordinates(self, city: str) -> set:
        
        if city == CITY_MOSСOW:
            return {"lon": 37.6156, "lat": 55.7522}

        if city == CITY_SAINT_PETERBURG:
            return {"lon": 30.2642, "lat": 59.8944}

        if city == CITY_NOVOSIBIRSK:
            return {"lon": 82.9344, "lat": 55.0411}
        
        return {"lon": 0.0, "lat": 0.0}

    def __prepare_number(self, number: str) -> str:

        number = int(number)

        if number > 0:
            return "+" + str(number) + self.__sym_degree_celsius

        if number < 0:
            return "-" + str(0 - number) + self.__sym_degree_celsius

        return "0" + self.__sym_degree_celsius


    def __get_name_for_cache(self, prefix: str, lat: str, lon: str) -> None:
        return f'weather_{prefix}_lat_{lat}_lon_{lon}'


    def get_coordinates_city(self, city_name: str):

        city_name = city_name.strip().lower().capitalize()
        URL = f'{self.__URL_WEATHER}?q={city_name}&lang=ru&appid={WEATHER_APP_ID}'

        received_data = ''

        try:
            received_data = requests.get(URL)
        except Exception as e:

            return json.dumps({
                "cod": 500,
                "message": "Error get city!"
            })
           
        if(received_data.status_code == 404):
            return json.dumps({
                "cod": "404",
                "message": "Город не найден!"
            })

        if(received_data.status_code != 200):
            return json.dumps({
                "cod": received_data.status_code,
                "message": "Weather server not available!"
            })

        data = json.loads(received_data.text)

        lat = data['coord']['lat']
        lon = data['coord']['lon']
        city = data['name']

        return json.dumps(
            {
                "cod": data['cod'],
                "message": self.get_country_info(data['sys']['country'], city),
                "href": self.get_link_to_map(lat, lon, city),
                "name": city,
                "lat": lat,
                "lon": lon,
            })
        

    def __parse_day(
        self, weather_id: int, time: datetime.date, 
        temperature_morn: str, temperature_day: str, temperature_eve: str, temperature_night: str,
        humidity: str, wind_speed: str, description: str) -> str:

        str_result = '<b>' + str(time.day) + ' ' + str(self.__months[time.month - 1]) + '</b> ' + str(self.__days_week[time.weekday()]) + '\n '
        str_result += 'Утро:  <b>' + self.__prepare_number(temperature_morn) + ' </b> - День:  <b>' + self.__prepare_number(temperature_day) + '</b>\n '
        str_result += 'Вечер: <b>' + self.__prepare_number(temperature_eve) + ' </b> - Ночь:  <b>' + self.__prepare_number(temperature_night) + '</b>\n\n'
        str_result += get_emoji(weather_id) + '<b>' + description.capitalize() + '</b> \n'
        str_result += 'Влажность: <b>' + str(humidity) + '%</b> '
        str_result += 'Скорость ветра: <b>' + str(wind_speed) + 'м/c</b>'
        str_result += '\n\n'

        return str_result

    def get_weather_week(self, lat: float, lon: float):
        return self.__get_weather(lat, lon, "week") 

    def get_weather_day(self, lat: float, lon: float):
        return self.__get_weather(lat, lon, "day") 

    def __get_count_days(self, daily: list, type: str) -> int:

        if type == "week":
            return min(len(daily), 7) # weather for a maximum of 7 days

        return 1

    def __get_weather(self, lat: float, lon: float, type: str) -> str:

        lat = str(lat)
        lon = str(lon)

        URL = f'{self.__URL_ONE_CALL}?units=metric&lang=ru&lat={lat}&lon={lon}&appid={WEATHER_APP_ID}'

        # ============================================ Get from cache ============================================================================

        is_next_day = True
        name_cache = self.__get_name_for_cache(type, lat, lon)
        data_weather = self.__cache.get(name_cache)

        if data_weather:
            data_weather = json.loads(data_weather)
            is_next_day = 'day' in data_weather and int(data_weather['day']) != datetime.datetime.now().day

        if not is_next_day:

            str_result = ''
            daily = data_weather['daily']

            size = self.__get_count_days(daily, type)
            time = datetime.date.today()

            for i in range(size):

                day = daily[i]
                str_result += self.__parse_day(
                    day['id'], time, 
                    day['tm'], day['td'], day['te'], day['tn'], 
                    day['h'], day['ws'], day['w_d'])

                time += datetime.timedelta(days=1)

            return str_result

        # ============================================ Get from server ============================================================================

        received_data = ''

        try:
            received_data = requests.get(URL)
        except Exception as e:
            return 'Error get weather!' + str(e)

        if(received_data.status_code != 200):
            return 'Weather server not available!'

        compress_daily = []

        weather = json.loads(received_data.text)
        daily = weather['daily']

        size = self.__get_count_days(daily, type)
        time = datetime.date.today()

        str_result = ''

        for i in range(size):

            day = daily[i]
            weather = day['weather'][0]

            id = weather['id']
            description = weather['description']

            temperature = day['temp']
            t_morn = temperature['morn']
            t_day = temperature['day']
            t_eve = temperature['eve']
            t_night = temperature['night']

            humidity = day['humidity']
            wind_speed = day['wind_speed']


            str_result += self.__parse_day(
                id, time, t_morn, 
                t_day, t_eve, t_night, 
                humidity, wind_speed, description)

            compress_daily.append({
                'id' : int(id),
                'tm' : int(t_morn),
                'td' : int(t_day),
                'te' : int(t_eve),
                'tn' : int(t_night),
                'h'  : int(humidity),
                'ws' : int(wind_speed),
                'w_d' : description
            })
            
            time += datetime.timedelta(days=1)
        
        
        weatherForCache = {
            'daily' : compress_daily,
            'day' : str(datetime.datetime.now().day)
        }

        self.__cache.set(name_cache, json.dumps(weatherForCache), self.__TTL)
        return str_result
