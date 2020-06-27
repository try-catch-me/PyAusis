from plugin import alias, plugin


@alias("bye", "goodbye", "q", "quit")
@plugin('exit')
def exit(ausis, s):
    """Closing ausis"""
    ausis.exit()
