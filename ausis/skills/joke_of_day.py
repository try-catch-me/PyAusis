from plugin import plugin, require
import requests
from colorama import Fore


@require(network=True)
@plugin('joke daily')
class joke_of_day:
    """
    Provides you with a joke of day to help you laugh amidst the
    daily boring schedule

    Enter 'joke daily' to use

    """

    def __call__(self, ausis, s):
        ausis.say("Welcome To The Plugin Joke Of Day!", Fore.CYAN)
        ausis.say("Jokes provided by jokes.one API", Fore.CYAN, False)
        print()
        joke_fetch = self.get_joke(ausis)
        if joke_fetch is not None:
            self.joke(ausis, joke_fetch)

    def get_joke(self, ausis):
        while True:
            url = "https://api.jokes.one/jod"
            ausis.spinner_start('Fetching')
            r = requests.get(url)
            if r is None:
                spinner.stop()
                ausis.say(
                    "Error in fetching joke - try again! later", Fore.RED)
            ausis.spinner_stop()
            return r.json()

    def joke(self, ausis, joke_fetch):
        title = joke_fetch["contents"]["jokes"][0]["joke"]["title"]
        joke = joke_fetch["contents"]["jokes"][0]["joke"]["text"]
        print()
        ausis.say("Title: " + title, Fore.BLUE)
        print()
        ausis.say(joke, Fore.YELLOW)
