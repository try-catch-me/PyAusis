import tempfile

from Ausis import HISTORY_FILENAME
from colorama import Fore
from plugin import plugin


@plugin('cat his')
def cat_history(ausis, s):
    """Prints the history of commands"""
    HISTORY_FILENAME.seek(0)
    history = str(HISTORY_FILENAME.read())
    ausis.say(history, Fore.BLUE)
