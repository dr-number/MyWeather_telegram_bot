from decouple import config

TELEGRAM_BOT_TOKEN = config('telegram_bot_token',default='')
WEATHER_APP_ID = config('weather_app_id',default='')