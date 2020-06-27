# !!! This uses the https://newsapi.org/ api. TO comply with the TOU
# !!! we must link back to this site whenever we display results.
import json
import requests
import webbrowser
from colorama import Fore
from plugin import plugin, require


@require(network=True)
@plugin('news')
class News:

    def __init__(self):
        self.sources = [
            'bloomberg',
            'financial-times',
            'cnbc',
            'reuters',
            'al-jazeera-english',
            'the-wall-street-journal',
            'the-huffington-post',
            'business-insider',
            'the-new-york-times',
            'abc-news',
            'fox-news',
            'cnn',
            'google-news',
            'wired']
        self.source_dict = {}

        for source in self.sources:
            self.source_dict[str(self.sources.index(source) + 1)] = source

    def __call__(self, ausis, s):
        if s == "updatekey":
            key = ausis.input(
                "Please enter your NEWS API key (q or Enter go back): ")
            if key.lower() == "q" or key.lower() == "":
                ausis.say("Could not update the NEWS API key! ", Fore.RED)
            else:
                self.update_api_key(ausis, key)
                ausis.say("NEWS API key successfully updated! ", Fore.GREEN)
        elif s == "configure":
            self.configure(ausis)
        elif s == "remove":
            self.remove_source(ausis)
        elif s == "help":
            ausis.say("-------------------------------------")
            ausis.say("Command\t\t | Description")
            ausis.say("-------------------------------------")
            ausis.say("news\t\t : Finds top headlines")
            ausis.say(
                "news updatekey\t : Updates the news API key of the user")
            ausis.say(
                "news configure\t : Configures the news channel of the user")
            ausis.say("news sources\t : List the configured news sources")
            ausis.say(
                "news remove\t : Removes a source from the news channel of the user")
            ausis.say("news [word]\t : Finds articles related to that word")
        elif s == "sources":
            sources = self.get_news_sources(ausis)
            if not sources:
                ausis.say(
                    "No sources configured. Use 'news configure' to add sources.",
                    Fore.RED)
            else:
                dic = {}
                for source in sources:
                    dic[str(sources.index(source) + 1)] = source

                for index in sorted([int(x) for x in dic.keys()]):
                    ausis.say(str(index) + " : " + dic[str(index)])
        elif self.get_api_key(ausis) is None:
            ausis.say("Missing API key", Fore.RED)
            ausis.say("Visit https://newsapi.org/ to get the key", Fore.RED)
            ausis.say(
                "Use \'news updatekey\' command to add a key\n",
                Fore.RED)
        elif s == "" or s == " ":
            self.parse_articles(self.get_headlines(ausis), ausis)
        else:
            searchlist = s.split(" ")
            if "" in searchlist:
                searchlist.remove("")
            if " " in searchlist:
                searchlist.remove(" ")
            self.parse_articles(self.get_news(ausis, searchlist), ausis)

    @staticmethod
    def get_api_key(ausis):
        """
            will return either the news_api key of the user, already stored in the memory.json
            file or None in case the user does not have his own api
        """
        return ausis.get_data("news-settings")

    def update_api_key(self, ausis, api_key):
        """
            the user might have a news api key and they might want to add to memory.json or update an old one
        """
        ausis.update_data("news-settings", api_key)
        return self.get_api_key(ausis)

    def get_news_sources(self, ausis):
        """
            returns a list of all the new sources added to the news channel of the user
        """
        sources = ausis.get_data("news-sources")
        if sources is None:
            sources = []
        return sources

    def add_source(self, ausis, news_source):
        """
            adds a new source (if it does not exist) to the news channel of the user
        """
        sources = self.get_news_sources(ausis)
        if news_source not in sources:
            sources.append(news_source)
            ausis.update_data("news-sources", sources)
            ausis.say(
                news_source
                + " has been successfully been added to your sources!",
                Fore.GREEN)
        else:
            ausis.say(
                news_source
                + " was already included in your sources!",
                Fore.GREEN)
        return self.get_news_sources(ausis)

    def remove_source(self, ausis):
        """
            removes a new source from the news channel of the user
        """
        sources = self.get_news_sources(ausis)

        dic = {}
        for source in sources:
            dic[str(sources.index(source) + 1)] = source

        for index in sorted([int(x) for x in dic.keys()]):
            ausis.say(str(index) + " : " + dic[str(index)])
        index_list = ausis.input(
            "Type the indexes of the sources you would like to remove from your channel separated by "
            "space: ")
        index_list = index_list.split(" ")
        if " " in index_list:
            index_list.remove(" ")
        if "" in index_list:
            index_list.remove("")
        for index in index_list:
            if str(index) in dic:
                source = dic[str(index)]
                sources.remove(source)
                ausis.update_data("news-sources", sources)
                ausis.say(
                    source
                    + " has been successfully removed from your news channel!",
                    Fore.GREEN)
            else:
                ausis.say("Index not found!", Fore.RED)
        return self.get_news_sources(ausis)

    def configure(self, ausis):
        """
            configures the news channel of the user
        """
        for index in sorted([int(x) for x in self.source_dict.keys()]):
            ausis.say(str(index) + ": " + self.source_dict.get(str(index)))
        index_list = ausis.input(
            "Type the indexes of the sources you would like to add to your channel separated by "
            "space: ")
        index_list = index_list.split(" ")
        if " " in index_list:
            index_list.remove(" ")
        if "" in index_list:
            index_list.remove("")
        for index in index_list:
            if index in self.source_dict.keys():
                self.add_source(ausis, self.source_dict.get(index, index))
            else:
                ausis.say(index + " is not a valid index", Fore.RED)

    def get_headlines(self, ausis):
        """
            gets top headlines for a quick lookup of the world news, based on the news channel of the user (if it exists)
        """
        sources = self.get_news_sources(ausis)

        if len(sources) == 0:
            ausis.say(
                "You have not configured any source. Getting top headlines\n",
                Fore.GREEN)
            url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=" + \
                self.get_api_key(ausis)
        else:
            url = "https://newsapi.org/v2/top-headlines?sources="
            for source in sources:
                url += source + ","
            url += "&apiKey=" + self.get_api_key(ausis)
        return self._get(ausis, url)

    def get_news(self, ausis, searchlist):
        """
            gets top news based on a particular search list , based on the news channel of the user (if it exists)
        """
        sources = self.get_news_sources(ausis)

        url = "https://newsapi.org/v2/everything?q="

        for i in searchlist:
            url += i + "%20"
        if len(sources) != 0:
            url += "&sources="
            for source in sources:
                url += source + ","
        url += "&apiKey=" + self.get_api_key(ausis)
        return self._get(ausis, url)

    def _get(self, ausis, url):
        """fetch a webpage"""
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            data = json.loads(response.text)
            return data
        else:
            if response.status_code == 401:
                ausis.say("API key not valid", Fore.RED)
            else:
                ausis.say("An error occured: Error code: "
                           + response.raise_for_status(), Fore.RED)
            return None

    def parse_articles(self, data, ausis):
        article_list = {}
        index = 1
        if data is None:
            ausis.say("No Articles", Fore.RED)
            return
        # ausis.say articles with their index
        if not data['articles']:
            ausis.say("No Articles matching the word(s)", Fore.RED)
            return
        for article in data['articles']:
            ausis.say(str(index) + ": " + article['title'])
            article_list[index] = article
            index += 1

        # Attribution link for News API to comply with TOU
        ausis.say("\nPowered by News API. Type NewsAPI to learn more")
        ausis.say("\nType index to expand news, 0 to return to ausis prompt\n")

        # Check to see if index or NewsAPI was enterd
        idx = ausis.input()
        if idx.lower() == "newsapi":
            webbrowser.open('https://newsapi.org/')
            return

        # check if we have a valid index
        try:
            int(idx)
            if int(idx) > (index - 1):
                ausis.say(str(idx) + " is not a valid index", Fore.RED)
                return
            elif int(idx) == 0:
                return
        except BaseException:
            ausis.say("Not a valid index", Fore.RED)
            return

        # if index valid ausis.say article description
        ausis.say(article_list[int(idx)]['description'])

        ausis.say("Do you want to read more? (yes/no): ")
        i = ausis.input()
        # if user wants to read more open browser to article url
        if i.lower() == "yes" or i.lower() == 'y':
            webbrowser.open(article_list[int(idx)]['url'])
        return
