from constants import TELEGRAM_BOT_TOKEN
from markups import BTN_CANCEL, BTN_ENTER_NAME_CITY, BTN_SETTINGS, BTN_WEATHER_WEEK, get_main_buttons, get_settings_city_buttons, get_settings_city_coords, get_settings_city_name
from sqlite_db import Sqlite3DB
import telebot
from weather import Weather
import logging

sub_action = ''
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


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
        sub_action = event

    elif event == BTN_ENTER_NAME_CITY:
        text = "Введите координаты города"
        markup = get_settings_city_coords()
        sub_action = event

    elif event == BTN_CANCEL:
        text = "Выберите действие"
        sub_action = ''

    else:
        if sub_action == BTN_ENTER_NAME_CITY:
            weather.get_coordinates_city(event)
        else:
            text = "<b>Пока недоступно!</b>"

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="html")

#logger = telebot.logger
#telebot.logger.setLevel(logging. DEBUG)

sqlite3db = Sqlite3DB()
sqlite3db.connect_db()

weather = Weather()


print("Bot is work...")
bot.polling(none_stop=True)



