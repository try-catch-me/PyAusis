import os
from plugin import plugin


@plugin('clear')
def clear(ausis, s):
    """Clears terminal"""
    os.system("clear")
