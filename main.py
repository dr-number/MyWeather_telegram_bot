from btns_constants import BTN_SETTINGS, BTN_WEATHER_TODAY, BTN_WEATHER_WEEK
import telebot
from telebot import types
from weather import get_weather

TELEGRAM_BOT_TOKEN = '5655777778:AAE8eOLQ_9cMVOlfWaAlVjYI52GFFRvFY5Q'

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
        text = get_weather()
    else:
        text = "<b>Пока недоступно!</b>"

    bot.send_message(message.chat.id, text, reply_markup=__get_buttons(), parse_mode="html")

#logger = telebot.logger
#telebot.logger.setLevel (logging. DEBUG )
bot.polling(none_stop=True)



