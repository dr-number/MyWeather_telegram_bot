thunderstorm = u'\U0001F4A8'    # Code: 200's, 900, 901, 902, 905
drizzle = u'\U0001F4A7'         # Code: 300's
rain = u'\U00002614'            # Code: 500's
snowflake = u'\U00002744'       # Code: 600's snowflake
snowman = u'\U000026C4'         # Code: 600's snowman, 903, 906
atmosphere = u'\U0001F301'      # Code: 700's foogy
clearSky = u'\U00002600'        # Code: 800 clear sky
fewClouds = u'\U000026C5'       # Code: 801 sun behind clouds
clouds = u'\U00002601'          # Code: 802-803-804 clouds general
hot = u'\U0001F525'             # Code: 904
default_enmoji = u'\U0001F300'  

def get_emoji(weather_id: int):
    if weather_id:
        if str(weather_id)[0] == '2' or weather_id == 900 or weather_id==901 or weather_id==902 or weather_id==905:
            return thunderstorm
        elif str(weather_id)[0] == '3':
            return drizzle
        elif str(weather_id)[0] == '5':
            return rain
        elif str(weather_id)[0] == '6' or weather_id==903 or weather_id== 906:
            return snowflake + ' ' + snowman
        elif str(weather_id)[0] == '7':
            return atmosphere
        elif weather_id == 800:
            return clearSky
        elif weather_id == 801:
            return fewClouds
        elif weather_id==802 or weather_id==803 or weather_id==803:
            return clouds
        elif weather_id == 904:
            return hot
        else:
            return default_enmoji    # Default emoji

    else:
        return default_enmoji   # Default emoji