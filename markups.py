BTN_WEATHER_TODAY = "На сегодня"
BTN_WEATHER_WEEK = "На неделю"

BTN_SETTINGS = "Настройки"
BTN_SHOW_COORDINATES = "Где смотрим погоду"

BTN_ENTER_NAME_CITY = "Ввести название"
BTN_ENTER_COORDS_CITY = "Ввести координаты"

BTN_CANCEL = "Отмена"
BTN_YES = "Да"
BTN_NO = "Нет"

ACTION_NO = "no"
ACTION_YES = "yes"

from telebot import types
from weather import CITY_MOSСOW, CITY_SAINT_PETERBURG, CITY_NOVOSIBIRSK

def get_main_buttons(is_correct_coordinates: bool):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    btn_weather_today = types.KeyboardButton(BTN_WEATHER_TODAY)
    btn_weather_in_week = types.KeyboardButton(BTN_WEATHER_WEEK)
    btn_settings = types.KeyboardButton(BTN_SETTINGS)
    btn_show_coordinates = types.KeyboardButton(BTN_SHOW_COORDINATES)

    if is_correct_coordinates:
        markup.add(
            btn_weather_today, btn_weather_in_week,
            btn_settings, btn_show_coordinates)
    else:
        markup.add(btn_settings)

    return markup

def __install_city_buttons(markup):
    markup.add(
        types.KeyboardButton(CITY_MOSСOW),
        types.KeyboardButton(CITY_SAINT_PETERBURG),
        types.KeyboardButton(CITY_NOVOSIBIRSK)
    )

    return markup

def get_settings_city_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    btn_name = types.KeyboardButton(BTN_ENTER_NAME_CITY)
    btn_coords = types.KeyboardButton(BTN_ENTER_COORDS_CITY)
    btn_cancel = types.KeyboardButton(BTN_CANCEL)

    markup.add(btn_name, btn_coords, btn_cancel)

    return markup

def get_settings_city_name():

    btn_coords = types.KeyboardButton(BTN_ENTER_COORDS_CITY)
    btn_cancel = types.KeyboardButton(BTN_CANCEL)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup =__install_city_buttons(markup)
    markup.add(btn_coords, btn_cancel)

    return markup

def get_settings_city_coords():
    
    btn_name = types.KeyboardButton(BTN_ENTER_NAME_CITY)
    btn_cancel = types.KeyboardButton(BTN_CANCEL)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(btn_name, btn_cancel)

    return markup

def get_settings_yes_no():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2

    btn_yes = types.InlineKeyboardButton(BTN_YES, callback_data=ACTION_YES)
    btn_no = types.InlineKeyboardButton(BTN_NO, callback_data=ACTION_NO)

    markup.add(btn_yes, btn_no)
    return markup