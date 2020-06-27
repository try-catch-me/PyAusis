import json
import requests
from test import VoiceLinux

p1 = VoiceLinux(70)
p1.create()

def main(city=0):
    send_url = (
        "http://api.openweathermap.org/data/2.5/forecast/daily?q={0}&cnt=1"
        "&APPID=ab6ec687d641ced80cc0c935f9dd8ac9&units=metric".format(city)
    )
    r = requests.get(send_url)
    j = json.loads(r.text)
    rain = j['list'][0]['weather'][0]['id']
    if rain >= 300 and rain <= 500:  # In case of drizzle or light rain
        p1.text_to_speech("It appears that you might need an umbrella today.")
    elif rain > 700:
        p1.text_to_speech("Good news! You can leave your umbrella at home for today!")
    else:
        p1.text_to_speech( "Uhh, bad luck! If you go outside, take your umbrella with you.")
#main("haripur")