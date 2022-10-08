import json
from constants import TELEGRAM_BOT_TOKEN
from markups import (
    BTN_CANCEL, BTN_ENTER_NAME_CITY, BTN_SETTINGS, BTN_WEATHER_WEEK, 
    get_main_buttons, get_settings_city_buttons, get_settings_city_coords,
    get_settings_city_name)
    
from sqlite_db import Sqlite3DB
import telebot
from weather import Weather
import logging

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

class SubAction:
    
    action = ''

    def set_action(self, action):
        self.action = action

    def get_action(self):
        return self.action


@bot.message_handler(commands=['start'])
def start(message):
   bot.send_message(message.chat.id, f"<b>Hello {message.from_user.first_name}!</b>", parse_mode="html", reply_markup=get_main_buttons())

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

    elif event == BTN_ENTER_NAME_CITY:
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
            else:
                text = f"{data['message']}\n<b>Город определен верно?</b>"

        else:
            text = "<b>Пока недоступно!</b>"
        

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="html")

#logger = telebot.logger
#telebot.logger.setLevel(logging. DEBUG)

sqlite3db = Sqlite3DB()
sqlite3db.connect_db()

sub_action = SubAction()
weather = Weather()


print("Bot is work...")
bot.polling(none_stop=True)



