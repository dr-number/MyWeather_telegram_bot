BTN_SETTINGS = "Настройки"
BTN_WEATHER_TODAY = "На сегодня"
BTN_WEATHER_WEEK = "На неделю"

BTN_ENTER_NAME_CITY = "Ввести название"
BTN_ENTER_COORDS_CITY = "Ввести координаты"

BTN_CANCEL = "Отмена"

from telebot import types

def get_main_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    btn_settings = types.KeyboardButton(BTN_SETTINGS)
    btn_weather_today = types.KeyboardButton(BTN_WEATHER_TODAY)
    btn_weather_in_week = types.KeyboardButton(BTN_WEATHER_WEEK)

    markup.add(btn_settings, btn_weather_today, btn_weather_in_week)

    return markup

def get_settings_city_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    btn_name = types.KeyboardButton(BTN_ENTER_NAME_CITY)
    btn_coords = types.KeyboardButton(BTN_ENTER_COORDS_CITY)
    btn_cancel = types.KeyboardButton(BTN_CANCEL)

    markup.add(btn_name, btn_coords, btn_cancel)

    return markup

def get_settings_city_name():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    btn_coords = types.KeyboardButton(BTN_ENTER_COORDS_CITY)
    btn_cancel = types.KeyboardButton(BTN_CANCEL)

    markup.add(btn_coords, btn_cancel)

    return markup

def get_settings_city_coords():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    btn_name = types.KeyboardButton(BTN_ENTER_NAME_CITY)
    btn_cancel = types.KeyboardButton(BTN_CANCEL)

    markup.add(btn_name, btn_cancel)

    return markup