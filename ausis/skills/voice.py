from colorama import Fore
from plugin import LINUX, UNIX, MACOS, WINDOWS, plugin, require


@plugin('enable sound')
def enable_sound(ausis, s):
    """Let ausis use his voice."""
    ausis.speech = ausis.enable_voice()
    ausis.say(Fore.BLUE + "ausis uses Googles speech engine.\nDo you consent with data "
    + "collection when ausis talks out loud? If yes, type:" + Fore.RED + " gtts")
    ausis.say(Fore.BLUE + "If not, ausis will talk using the built-in speech engine. "
    + " If you wish to disable GTTS, type: " + Fore.RED + "disable gtts")


@plugin('disable sound')
def disable_sound(ausis, s):
    """Deny ausis his voice."""
    ausis.disable_voice()


@plugin('say')
def say(ausis, s):
    """Reads what is typed."""
    if not s:
        ausis.say("What should I say?")
    else:
        voice_state = ausis.is_voice_enabled()
        ausis.enable_voice()
        ausis.say(s)
        if not voice_state:
            ausis.disable_voice()


@plugin('disable gtts')
def disable_gtts(ausis, s):
    """Reads what is typed without using gtts."""
    voice_state = ausis.is_voice_enabled
    ausis.disable_gtts()
    ausis.speech = ausis.enable_voice()

    if not voice_state:
        ausis.disable_voice()


@plugin('gtts')
def gtts(ausis, s):
    """Reads what is typed using gtts."""
    voice_state = ausis.is_voice_enabled
    ausis.enable_gtts()

    if not voice_state:
        ausis.disable_voice()


@require(platform=[LINUX, WINDOWS])
@plugin('talk faster')
def talk_faster(ausis, s):
    """Make ausis' speech engine talk faster.
    """
    if ausis.is_voice_enabled():
        ausis.change_speech_rate(40)
    else:
        ausis.say("Type 'enable sound' to allow ausis to talk out loud.",
            Fore.BLUE)


@require(platform=[LINUX, WINDOWS])
@plugin('talk slower')
def talk_slower(ausis, s):
    """Make ausis' speech engine talk slower.
    """
    if ausis.is_voice_enabled():
        ausis.change_speech_rate(-40)
    else:
        ausis.say("Type 'enable sound' to allow ausis to talk out loud.",
            Fore.BLUE)
