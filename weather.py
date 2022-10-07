import json
from urllib import response
import requests
import datetime

import traceback
import logging

from constants import WEATHER_APP_ID

__params = {
    "ttl_cache" : 4
}

__days_week = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Satardy", "Sunday"]
__months = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]

__response = {
    'result' : '',
    'error' : '',
    'code' : 200
}

def __prepare_number(number):

    number = int(number)

    if number > 0:
        return "+ " + str(number)

    if number < 0:
        return "- " + str(0 - number)

    return "0"


def __prepare_weather(data_weather):
    for item in data_weather:
        item["tmp"] = __prepare_number(item["tmp"])

    return data_weather



def __get_name_for_cache(lat, lon):
    return 'weather_lat_' + lat + 'lon_' + lon

def __return_result(response, is_ajax):

    if is_ajax:
        return JsonResponse(response)

    return response



def get_weather(lat=55.0415, lon=82.9346, is_ajax=True):

    lat = str(lat)
    lon = str(lon)

    '''
    name_cache = __get_name_for_cache(lat, lon)

    data_weather = cache.get(name_cache)

    if data_weather:
        data_weather = json.loads(data_weather)
        is_next_day = 'day' in data_weather and data_weather['day'] != datetime.datetime.now().day

        if not is_next_day:
            data_weather = __prepare_weather(data_weather['daily'])

    
    if data_weather:
        __response['result'] = data_weather
        return __return_result(__response, is_ajax)
    '''

        
    url = 'https://api.openweathermap.org/data/2.5/onecall?units=metric&lat=' + lat + '&lon=' + lon + '&appid=' + WEATHER_APP_ID
    received_data = ''

    try:
        received_data = requests.get(url)
    except Exception as e:
        return 'Error get weather!' + str(e)

    if(received_data.status_code != 200):
        return 'Weather server not available!'

    compress_daily = []

    weather = json.loads(received_data.text)
    daily = weather['daily']

    size = min(len(daily), 7) # weather for a maximum of 7 days
    time = datetime.date.today()

    str_result = ''

    for i in range(size):

        day = daily[i]

        str_result += '<b>' + str(time.day) + ' ' + str(__months[time.month - 1]) + '</b>\n' + str(__days_week[time.weekday()]) + '\n '
        str_result += day['weather'][0]['icon'] + ' ' + str(day['temp']['day']) + '\n '

        '''
        ico = day['weather'][0]['icon']
        temperature = day['temp']['day']

        compress_daily.append({
            'ico' : ico,
            'tmp' : int(temperature)
        })
        '''
        
        time += datetime.timedelta(days=1)
    
    '''
    weatherForCache = {
        'daily' : compress_daily,
        'day' : datetime.datetime.now().day
    }

    cache.set(name_cache, json.dumps(weatherForCache), 60 * __params['ttl_cache'])
    __response['result'] = __prepare_weather(compress_daily)

    return __return_result(__response, is_ajax)
    '''

    return str_result
