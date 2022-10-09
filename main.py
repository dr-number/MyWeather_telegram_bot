import json
from constants import TELEGRAM_BOT_TOKEN
from weather import CITY_MOSСOW, CITY_SAINT_PETERBURG, CITY_NOVOSIBIRSK

from markups import (
    ACTION_NO, ACTION_YES, BTN_CANCEL, BTN_ENTER_COORDS_CITY, 
    BTN_ENTER_NAME_CITY, BTN_SETTINGS, BTN_SHOW_COORDINATES, 
    BTN_WEATHER_TODAY, BTN_WEATHER_WEEK, 
    get_main_buttons, get_settings_city_buttons, get_settings_city_coords,
    get_settings_city_name, get_settings_yes_no)
    
from sqlite_db import Sqlite3DB
import telebot
from weather import Weather
import logging

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

class SubAction:
    __action = ''

    def set_action(self, action: str):
        self.__action = action

    def get_action(self) -> str:
        return self.__action

class PreSaveSettings:
    __data = {}

    def get_data(self) -> set:
        return self.__data

    def set_data(self, data: set):
        self.__data = data

    def is_float(self, s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False


@bot.message_handler(commands=['start'])
def start(message):
   sqlite3db.create_user(message.chat.id)

   text = f"<b>Hello {message.from_user.first_name}!</b>"
   markup = get_main_buttons(sqlite3db.is_correct_coord(message.chat.id))

   bot.send_message(message.chat.id, text, parse_mode="html", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def events(message):

    event = message.text

    markup = get_main_buttons(sqlite3db.is_correct_coord(message.chat.id))

    if event == BTN_WEATHER_WEEK:
        data_user = sqlite3db.get_user(message.chat.id)
        text = sqlite3db.get_title(data_user) + "\n"
        text += weather.get_weather_week(float(data_user["lat"]), float(data_user["lon"]))

    elif event == BTN_WEATHER_TODAY:
        data_user = sqlite3db.get_user(message.chat.id)
        text = sqlite3db.get_title(data_user) + "\n"
        text += weather.get_weather_day(float(data_user["lat"]), float(data_user["lon"]))

    elif event == BTN_SETTINGS:
        text = "Укажите город"
        markup = get_settings_city_buttons()
    
    elif event == BTN_ENTER_NAME_CITY:
        text = "Введите название города"
        markup = get_settings_city_name()
        sub_action.set_action(event)

    elif event == BTN_ENTER_COORDS_CITY:
        text = "Введите координаты города (в формате <b>широта-долгота</b>)"
        markup = get_settings_city_coords()
        sub_action.set_action(event)

    elif event == BTN_SHOW_COORDINATES:
        data = sqlite3db.get_user(message.chat.id)

        if not data:
            text = "<b>Нет данных!</b>"
        else:
            text = weather.get_link_to_map(data["lat"], data["lon"], data.get("description", ""))

    elif event == BTN_CANCEL:
        text = "Выберите действие"
        sub_action.set_action('')
        

    else:
        current_sub_action = sub_action.get_action()

        if current_sub_action == BTN_ENTER_NAME_CITY:

            if event == CITY_MOSСOW or event == CITY_SAINT_PETERBURG or event == CITY_NOVOSIBIRSK:

                description = weather.get_country_info("Россия", event)
                data = weather.get_coordinates(event)
               
                sqlite3db.update_city(message.chat.id, data["lon"], data["lat"], description)
                markup = get_main_buttons(True)

                bot.send_message(message.chat.id, "Настройки сохранены", reply_markup=markup, parse_mode="html")
                return

            data = json.loads(weather.get_coordinates_city(event))

            if data['cod'] != 200:
                text = f"<b>{data['message']}</b>\nПопробуйте ещё раз"
                markup = get_settings_city_buttons()
                sub_action.set_action('')
            else:
                text = f"{data['message'] + data['href']}\n<b>Город определен верно?</b>"
                pre_save_settings.set_data({
                    "description" : data['message'],
                    "lon" : data['lon'],
                    "lat" : data['lat'],
                })
                markup = get_settings_yes_no()

        elif current_sub_action == BTN_ENTER_COORDS_CITY:
            
            try:
                data = event.replace(".", ",").split("-")

                if not pre_save_settings.is_float(data[0]) or not pre_save_settings.is_float(data[1]):
                    text = "<b>Можно вводить только целые или дробные числа!</b>"
                    markup = get_settings_city_coords()
                else:
                    text = f"Широта: <b>{data[0]}</b>\nДолгота: <b>{data[1]}</b>\n<b>Верно?</b>"
                    pre_save_settings.set_data({
                        "lat" : data[0].replace(",", "."),
                        "lon" : data[1].replace(",", "."),
                    })
                    markup = get_settings_yes_no()

            except Exception as e:
                text = "<b>Некорректные данные!</b>"
                markup = get_settings_city_coords()

        else:
            text = "<b>Не понял команду...</b>"
        

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="html")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    markup = get_main_buttons(sqlite3db.is_correct_coord(call.message.chat.id))
    current_sub_action = sub_action.get_action()

    if current_sub_action == BTN_ENTER_NAME_CITY or current_sub_action == BTN_ENTER_COORDS_CITY:

        if call.data == ACTION_YES:
            data = pre_save_settings.get_data()
            sqlite3db.update_city(call.message.chat.id, float(data["lon"]), float(data["lat"]), data.get("description", ""))
            
            is_correct_coordinates = data["lon"] != "0.0" and data["lat"] != "0.0"
            markup = get_main_buttons(is_correct_coordinates)
            text = "Настройки сохранены"

        elif call.data == ACTION_NO:
            text = "Попробуйте ещё раз"

            if current_sub_action == BTN_ENTER_NAME_CITY:
                markup = get_settings_city_name()
            else:
                markup = get_settings_city_coords()

            sub_action.set_action(current_sub_action)

    bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode="html")


#logger = telebot.logger
#telebot.logger.setLevel(logging. DEBUG)

sqlite3db = Sqlite3DB()
sqlite3db.connect_db()

sub_action = SubAction()
weather = Weather()
pre_save_settings = PreSaveSettings()


print("Bot is work...")
bot.polling(none_stop=True)



