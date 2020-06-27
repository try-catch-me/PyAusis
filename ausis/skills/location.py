import requests
import json
from colorama import Fore
from plugin import plugin, require


@require(network=True)
@plugin('location')
def location(ausis, s):
    """It gives you your current location"""
    send_url = "http://api.ipstack.com/check?access_key=aafa3f03dc42cd4913a79fd2d9ce514d"
    geo_req = requests.get(send_url)
    geo_json = json.loads(geo_req.text)
    latitude = geo_json['latitude']
    latitude = str(latitude)
    longitude = geo_json['longitude']
    longitude = str(longitude)
    city = geo_json['city']
    continent_name = geo_json['continent_name']
    country_name = geo_json['country_name']
    pin = geo_json['zip']
    pin = str(pin)
    ausis.say(' is your latitude', latitude)
    ausis.say(' is your longitude', longitude)
    ausis.say(' is your city', city)
    ausis.say(' is your country', country_name)
    ausis.say(' is your continent', continent_name)
    ausis.say(' is your pin code', pin)
