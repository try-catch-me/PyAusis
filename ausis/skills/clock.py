from os import system
from time import ctime
from colorama import Fore
from plugin import plugin, require


@plugin('clock')
def clock(ausis, s):
    """Gives information about time"""
    ausis.say(ctime(), Fore.BLUE)


@plugin('stopwatch')
def stopwatch(ausis, s):
    """
    Start stopwatch

    L       Lap
    R       Reset
    SPACE   Pause
    Q       Quit
    """
    system("python -m termdown")


@plugin('timer')
def timer(ausis, s):
    """
    Set a timer

    R       Reset
    SPACE   Pause
    Q       Quit

    Usages:

    timer 10
    timer 1h5m30s
    """
    k = s.split(' ', 1)
    if k[0] == '':
        ausis.say("Please specify duration")
        return
    timer_cmd = "python -m termdown " + k[0]
    system(timer_cmd)
