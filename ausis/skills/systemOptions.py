import os
from platform import architecture, release, mac_ver
from platform import system as sys
import distro
from colorama import Fore, Style
from plugin import LINUX, UNIX, MACOS, WINDOWS, plugin, require


@require(platform=MACOS, native="pmset")
@plugin('screen off')
def screen_off__MAC(ausis, s):
    """Turn of screen instantly"""
    os.system('pmset displaysleepnow')


@require(platform=LINUX, native="xset")
@plugin('screen off')
def screen_off__LINUX(ausis, s):
    """Turn of screen instantly"""
    os.system('xset dpms force off')


@require(platform=MACOS)
@plugin('os')
def Os__MAC(ausis, s):
    """Displays information about your operating system"""
    ausis.say(
        Style.BRIGHT
        + '[!] Operating System Information'
        + Style.RESET_ALL,
        Fore.BLUE)
    ausis.say('[*] Kernel: ' + sys(), Fore.GREEN)
    ausis.say('[*] Kernel Release Version: ' + release(), Fore.GREEN)
    ausis.say('[*] macOS System version: ' + mac_ver()[0], Fore.GREEN)
    for _ in architecture():
        if _ != '':
            ausis.say('[*] ' + _, Fore.GREEN)


@require(platform=[LINUX, WINDOWS])
@plugin('os')
def Os__LINUX(ausis, s):
    """Displays information about your operating system"""
    ausis.say('[!] Operating System Information', Fore.BLUE)
    ausis.say('[*] ' + sys(), Fore.GREEN)
    ausis.say('[*] ' + release(), Fore.GREEN)
    ausis.say('[*] ' + distro.name(), Fore.GREEN)
    for _ in architecture():
        ausis.say('[*] ' + _, Fore.GREEN)


@require(platform=LINUX)
@plugin('systeminfo')
def systeminfo__LINUX(ausis, s):
    """Display system information with distribution logo"""
    from archey import archey
    archey.main()


@require(platform=MACOS, native="screenfetch")
@plugin('systeminfo')
def systeminfo__MAC(ausis, s):
    """Display system information with distribution logo"""
    os.system("screenfetch")


@require(platform=WINDOWS)
@plugin('systeminfo')
def systeminfo_win(ausis, s):
    """Display system infomation"""
    os.system("systeminfo")


@require(native="free", platform=UNIX)
@plugin("check ram")
def check_ram__UNIX(ausis, s):
    """
    checks your system's RAM stats.
    -- Examples:
        check ram
    """
    os.system("free -lm")


@require(platform=WINDOWS)
@plugin("check ram")
def check_ram__WINDOWS(ausis, s):
    """
    checks your system's RAM stats.
    -- Examples:
        check ram
    """
    import psutil
    mem = psutil.virtual_memory()

    def format(size):
        mb, _ = divmod(size, 1024 * 1024)
        gb, mb = divmod(mb, 1024)
        return "%s GB %s MB" % (gb, mb)
    ausis.say("Total RAM: %s" % (format(mem.total)), Fore.BLUE)
    if mem.percent > 80:
        color = Fore.RED
    elif mem.percent > 60:
        color = Fore.YELLOW
    else:
        color = Fore.GREEN
    ausis.say("Available RAM: %s" % (format(mem.available)), color)
    ausis.say("RAM used: %s%%" % (mem.percent), color)
