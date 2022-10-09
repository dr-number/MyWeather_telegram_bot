# Telegram bot on Python "MyWeather" (with redis, sqlite3)

## How to use

- Rename file in root project **test.env** to **.env** and paste:

    telegram_bot_token = 'Your telegram bot token'

    weather_app_id = 'Your token from https://openweathermap.org/'

Then build

    docker-compose build

And run composition

    docker-compose up -d

## Screenshots

**Weather forecast for the week or day**
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/MyWeather_telegram_bot/blob/master/z_for_read_me/weather.png">
   </p>
</figure>

**Setting location**

- Choice of cities: Moscow, St. Petersburg, Novosibirsk.
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/MyWeather_telegram_bot/blob/master/z_for_read_me/settings.png">
   </p>
</figure>

<figure>
   <p align="center">
      <img src="https://github.com/dr-number/MyWeather_telegram_bot/blob/master/z_for_read_me/set-sity-name.png">
   </p>
</figure>

- Manual city entry
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/MyWeather_telegram_bot/blob/master/z_for_read_me/set-sity-name-2.png">
   </p>
</figure>

- Weather in the specified coordinates
<figure>
   <p align="center">
      <img src="https://github.com/dr-number/MyWeather_telegram_bot/blob/master/z_for_read_me/set-sity-coord.png">
   </p>
</figure>