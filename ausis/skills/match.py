from os import system
from colorama import Fore
from plugin import plugin, require


@require(native='grep')
@plugin('match')
def match(ausis, string):
    """
    Matches a string pattern in a file using regex.
    Type "match" and you'll be prompted.
    """
    file_name = ausis.input("Enter file name?:\n", Fore.RED)
    pattern = ausis.input("Enter string:\n", Fore.GREEN)
    file_name = file_name.strip()
    if file_name == "":
        ausis.say("Invalid Filename")
    else:
        system("grep '" + pattern + "' " + file_name)
