# -*- coding: utf-8 -*-
import Ausis
import colorama
import sys


def check_python_version():
    return sys.version_info[0] == 3


def main():
    # enable color on windows
    colorama.init()
    # start Ausis
    ausis = Ausis.Ausis()
    command = " ".join(sys.argv[1:]).strip()
    ausis.executor(command)


if __name__ == '__main__':
    if check_python_version():
        main()
    else:
        print("Sorry! Only Python 3 supported.")