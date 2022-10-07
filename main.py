from btns_constants import BTN_SETTINGS, BTN_WEATHER_TODAY, BTN_WEATHER_WEEK
from constants import TELEGRAM_BOT_TOKEN
from sqlite_db import Sqlite3DB
import telebot
from telebot import types
from weather import Weather
import logging

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def __get_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    btn_settings = types.KeyboardButton(BTN_SETTINGS)
    btn_weather_today = types.KeyboardButton(BTN_WEATHER_TODAY)
    btn_weather_in_week = types.KeyboardButton(BTN_WEATHER_WEEK)

    markup.add(btn_settings, btn_weather_today, btn_weather_in_week)

    return markup

@bot.message_handler(commands=['start'])
def start(message):
   bot.send_message(message.chat.id, f"<b>Hello {message.from_user.first_name}!</b>", parse_mode="html", reply_markup=__get_buttons())

@bot.message_handler(content_types=['text'])
def events(message):

    event = message.text

    if event == BTN_WEATHER_WEEK:
        text = weather.get_weather_week()
    else:
        text = "<b>Пока недоступно!</b>"

    bot.send_message(message.chat.id, text, reply_markup=__get_buttons(), parse_mode="html")

#logger = telebot.logger
#telebot.logger.setLevel (logging. DEBUG )

sqlite3db = Sqlite3DB()
sqlite3db.connect_db()

weather = Weather()


print("Bot is work...")
bot.polling(none_stop=True)



