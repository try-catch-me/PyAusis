from helper import *
from os.path import expanduser, exists
import unix_windows


# TODO Windows Install options?
if unix_windows.IS_WIN:
    fw = open('ausis.bat', 'w')
    fw.write("""\
@ECHO off
CALL {AUSISPATH}\\env\\Scripts\\activate.bat
python {AUSISPATH}\\ausis\\
    """.format(AUSISPATH=os.getcwd()))
    section("FINISH")

    printlog("Installation Successful! Use 'Ausis' in cmd to start Ausis!")
else:

    section("Write Ausis starter")

    AUSIS_MACRO = """\
    #!/bin/bash
    source {PATH}/env/bin/activate
    python {PATH}/ausis "$@"
    """

    fw = open('Ausis', 'w')
    fw.write(AUSIS_MACRO.format(PATH=os.getcwd()))
    fw.close()

    shell('chmod +x Ausis').should_not_fail()

    install_options = [("Install Ausis /usr/local/bin starter (requires root)", 0),
                       ("Add {} to $PATH (.bashrc)".format(os.getcwd()), 1),
                       ("Do nothing (Call ausis by full path)", 2)]
    selection = user_input(install_options)

    if selection == 0:
        os.system('sudo cp Ausis /usr/local/bin')
    elif selection == 1:
        line_to_add = 'export PATH="$PATH:{}"'.format(os.getcwd())
        bashrc = '{}/.bashrc'.format(expanduser("~"))

        if not os.path.exists(bashrc):
            print("NO .bashrc found!")
        else:
            line_already_exists = False

            fr = open(bashrc)
            for line in fr.readlines():
                if line.startswith(line_to_add):
                    line_already_exists = True

            if line_already_exists:
                print("Ausis path already added to $PATH in bashrc!")
            else:
                fw = open(bashrc, 'a')
                fw.write(line_to_add)
                fw.write('\n')
                fw.close()

    printlog('\n\nInstallation complete. Try using Ausis!')
    if selection != 2:
        printlog('$ ausis')
    else:
        printlog('$ {}/ausis'.format(os.getcwd()))
