from os import system

from plugin import LINUX, MACOS, plugin, require


@require(platform=LINUX, native="pactl")
@plugin('increase volume')
def increase_volume__LINUX(ausis, s):
    """Increases your speaker's sound."""
    system("pactl -- set-sink-volume 0 +3%")


@require(platform=MACOS, native="osascript")
@plugin('increase volume')
def increase_volume__MAC(ausis, s):
    """Increases your speaker's sound."""
    system(
        'osascript -e "set volume output volume '
        '(output volume of (get volume settings) + 10) --100%"'
    )


@require(platform=MACOS, native="osascript")
@plugin('max volume')
def max_volume__MAC(ausis, s):
    """Maximizes your speaker's sound."""
    system(
        'osascript -e "set volume output volume 100"'
    )


@require(platform=MACOS, native="osascript")
@plugin('mute')
def mute__MAC(ausis, s):
    """Mute: Silence your speaker's sound."""
    system(
        'osascript -e "set volume output volume 0"'
    )


@require(platform=LINUX, native="pactl")
@plugin('decrease volume')
def decrease_volume__LINUX(ausis, s):
    """Decreases your speaker's sound."""
    system("pactl -- set-sink-volume 0 -10%")


@require(platform=MACOS, native="osascript")
@plugin('decrease volume')
def decrease_volume__MAC(ausis, s):
    """Decreases your speaker's sound."""
    system(
        'osascript -e "set volume output volume '
        '(output volume of (get volume settings) - 10) --100%"'
    )


@require(platform=LINUX, native="pactl")
@plugin('mute')
def mute__LINUX(ausis, s):
    """Mute: Silence your speaker's sound."""
    system("pactl -- set-sink-mute 0 toggle")
