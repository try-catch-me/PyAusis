from plugin import plugin, alias
import socket
from colorama import Fore


def ip_lookup(hostname):
    return str(socket.gethostbyname(hostname))


def hostname_lookup(ip):
    return str(socket.gethostbyaddr(ip)[0])


def dns_lookup(ausis, s, txt, func):
    while True:
        request = str(ausis.input("Please input a " + txt + ": "))
        try:
            if txt == 'ip':
                ausis.say("The hostname for that IP address is: " +
                           func(request), Fore.CYAN)
                return
            else:
                ausis.say("The IP address for that hostname is: " +
                           func(request), Fore.CYAN)
                return
        except Exception as e:
            ausis.say(str(e), Fore.RED)
            ausis.say("Please make sure you are inputing a valid " + txt)
            try_again = ausis.input("Do you want to try again (y/n): ")
            try_again = try_again.lower()
            if try_again != 'y':
                return


@plugin("dns forward")
def ip_lookup1(ausis, s):
    dns_lookup(ausis, s, "hostname", ip_lookup)


@plugin("dns reverse")
def hostname_lookup1(ausis, s):
    dns_lookup(ausis, s, "ip", hostname_lookup)
