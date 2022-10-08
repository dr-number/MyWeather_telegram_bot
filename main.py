import json
import re
from constants import TELEGRAM_BOT_TOKEN
from markups import (
    ACTION_NO, ACTION_YES, BTN_CANCEL, BTN_ENTER_COORDS_CITY, BTN_ENTER_NAME_CITY, BTN_SETTINGS, BTN_WEATHER_WEEK, 
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


@bot.message_handler(commands=['start'])
def start(message):
   bot.send_message(message.chat.id, f"<b>Hello {message.from_user.first_name}!</b>", parse_mode="html", reply_markup=get_main_buttons())
   sqlite3db.create_user(message.chat.id)

@bot.message_handler(content_types=['text'])
def events(message):

    event = message.text
    markup = get_main_buttons()

    if event == BTN_WEATHER_WEEK:
        text = weather.get_weather_week()
        markup = get_main_buttons()

    elif event == BTN_SETTINGS:
        text = "Укажите город"
        markup = get_settings_city_buttons()
    
    elif event == BTN_ENTER_NAME_CITY:
        text = "Введите название города"
        markup = get_settings_city_name()
        sub_action.set_action(event)

    elif event == BTN_ENTER_COORDS_CITY:
        text = "Введите координаты города"
        markup = get_settings_city_coords()
        sub_action.set_action(event)

    elif event == BTN_CANCEL:
        text = "Выберите действие"
        sub_action.set_action('')

    else:
        current_sub_action = sub_action.get_action()

        if current_sub_action == BTN_ENTER_NAME_CITY:
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

        else:
            text = "<b>Пока недоступно!</b>"
        

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="html")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    markup = get_main_buttons()
    current_sub_action = sub_action.get_action()

    if current_sub_action == BTN_ENTER_NAME_CITY or current_sub_action == BTN_ENTER_COORDS_CITY:

        if call.data == ACTION_YES:
            data = pre_save_settings.get_data()
            sqlite3db.update_city(call.message.chat.id, data["description"], float(data["lon"]), float(data["lat"]))
            text = "Настройки сохранены"

        elif call.data == ACTION_NO:
            text = "Попробуйте ещё раз"
            markup = get_settings_city_name()
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



