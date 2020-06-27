from plugin import plugin
from colorama import Fore


@plugin("binary")
def binary(ausis, s):
    """
    Converts an integer into a binary number
    """

    if s == "":
        s = ausis.input("What's your number? ")

    try:
        n = int(s)
    except ValueError:
        ausis.say("This is no number, right?", Fore.RED)
        return
    else:
        if n < 0:
            ausis.say("-" + bin(n)[3:], Fore.YELLOW)
        else:
            ausis.say(bin(n)[2:], Fore.YELLOW)
