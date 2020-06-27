import os
from colorama import Fore
from plugin import plugin, require, LINUX, MACOS


@require(native="cheese", platform=LINUX)
@plugin('open camera')
def open_camera__LINUX(ausis, s):
    """ausis will open the camera for you."""
    ausis.say("Opening cheese.......", Fore.RED)
    os.system("cheese")


@require(platform=MACOS)
@plugin('open camera')
def open_camera__MAC(ausis, s):
    """ausis will open the camera for you."""
    os.system('open /Applications/Photo\\ Booth.app')
