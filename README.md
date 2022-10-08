# Telegram bot on Python "MyWeather" (with redis, sqlite3)

## How to use

- Rename file in root project **test.env** to **.env** and paste:
    telegram_bot_token = 'Your telegram bot token'
    weather_app_id = 'Your token from https://openweathermap.org/'

Then build

    docker-compose build

And run composition

    docker-compose up -d
