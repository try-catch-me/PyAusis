from plugin import plugin, require
import requests


@require(network=True)
@plugin('countryinfo')
class country_info:
    """
    Welcome to the Countryinfo plugin documentation! Here you will be able
    to find all the functionalities of the plugin.
    Usage: Type countryinfo and follow the instructions.
    This plugin gives you several important details corresponding to country which is asked as an input
    Please enter country name in smallcase
    Go on and explore your information!!
    """

    def __call__(self, ausis, s):
        ausis.say("Welcome!")
        print()
        country_fetch = self.get_country(ausis)
        if country_fetch is not None:
            self.country_info(ausis, country_fetch)

    def get_country(self, ausis):
        """
        function creates request to api and fetches the corresponding data
        """
        while True:
            country = ausis.input(
                "Enter the name of the country or type exit to leave: ")
            if country == '':
                ausis.say("Please enter valid input.")
            elif country == 'exit':
                return
            else:
                url = "https://restcountries.eu/rest/v2/name/%s?fullText=true" % country
                r = requests.get(url)
                if isinstance(r.json(), dict):
                    ausis.say("Country not found.")
                else:
                    return r.json()

    def country_info(self, ausis, country_fetch):
        capital = country_fetch[0]["capital"]
        calling_code = country_fetch[0]["callingCodes"][0]
        population = country_fetch[0]["population"]
        region = country_fetch[0]["region"]
        currency = country_fetch[0]["currencies"][0]["name"]
        currency_symbol = country_fetch[0]["currencies"][0]["symbol"]
        time_zone = country_fetch[0]["timezones"][0]

        print()
        ausis.say("Capital: " + capital)
        ausis.say("Calling Code: " + calling_code)
        ausis.say("Currency: " + currency)
        ausis.say("Currency Symbol: " + currency_symbol)
        ausis.say("Population: " + str(population))
        ausis.say("Region: " + region)
        ausis.say("Time Zone: " + time_zone)

        return
