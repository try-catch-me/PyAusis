# -*- coding: utf-8 -*-

import os
from colorama import Fore
import nltk
import re
import sys
import tempfile
from core.GeneralUtilities import print_say
from CommandParser import CommandParser
import random
import os
color_random = [Fore.RED,Fore.GREEN,Fore.CYAN,Fore.YELLOW,Fore.WHITE,Fore.MAGENTA,Fore.BLUE]
random.shuffle(color_random)


AUSIS_LOGO = color_random[0] + '''
██████╗░██╗░░░██╗░█████╗░██╗░░░██╗░██████╗██╗░██████╗
██╔══██╗╚██╗░██╔╝██╔══██╗██║░░░██║██╔════╝██║██╔════╝
██████╔╝░╚████╔╝░███████║██║░░░██║╚█████╗░██║╚█████╗░
██╔═══╝░░░╚██╔╝░░██╔══██║██║░░░██║░╚═══██╗██║░╚═══██╗
██║░░░░░░░░██║░░░██║░░██║╚██████╔╝██████╔╝██║██████╔╝
╚═╝░░░░░░░░╚═╝░░░╚═╝░░╚═╝░╚═════╝░╚═════╝░╚═╝╚═════╝░''' + Fore.RESET
# register hist path via tempfile
HISTORY_FILENAME = tempfile.TemporaryFile('w+t')

PROMPT_CHAR = ':~'


class Ausis(CommandParser, object):
    # We use this variable at Breakpoint #1.
    # We use this in order to allow Ausis say "Hi", only at the first
    # interaction.
    os.system('clear')
    print(AUSIS_LOGO)
    first_reaction_text = ""
    first_reaction_text = Fore.RED + "[!]" + Fore.RESET + " Some Few Instructions\n" + Fore.RESET
    first_reaction_text = Fore.BLUE + "[!]" + Fore.RESET + " Type: " + Fore.RED + "hear" + Fore.RESET + " for voice commands"
    first_reaction_text += "\n"
    first_reaction_text += Fore.BLUE + '[!]' + Fore.RESET + ' Type: '
    first_reaction_text += Fore.RESET + Fore.RED + 'enable sound' + Fore.RESET + " for enable voice, by deafult it's disabled"
    first_reaction_text += "\n"
    first_reaction_text += Fore.BLUE + "[!]" + Fore.RESET + " Type: " + Fore.RESET + Fore.RED + "help" + Fore.RESET + " in order to listing out all the commands"
    first_reaction_text += "\n"
    prompt = (
        Fore.GREEN
        + "{} Hi, what can i do for you?\n".format(PROMPT_CHAR)
        + Fore.RESET)

    # This can be used to store user specific data

    def __init__(self, first_reaction_text=first_reaction_text,
                 prompt=prompt, first_reaction=True,
                 directories=["ausis/skills", "custom"]):
        directories = self._rel_path_fix(directories)
        # change raw input based on os
        if sys.platform == 'win32':
            self.use_rawinput = False
        self.regex_dot = re.compile('\\.(?!\\w)')
        CommandParser.__init__(self, first_reaction_text, prompt,
                                directories, first_reaction)

    def _rel_path_fix(self, dirs):
        dirs_abs = []
        work_dir = os.path.dirname(__file__)
        # remove 'ausis/' from path
        work_dir = os.path.dirname(work_dir)

        # fix nltk path
        nltk.data.path.append(os.path.join(work_dir, "ausis/data/nltk"))

        # relative -> absolute paths
        for directory in dirs:
            if not directory.startswith(work_dir):
                directory = os.path.join(work_dir, directory)
            dirs_abs.append(directory)
        return dirs_abs

    def default(self, data):
        """Ausis let's you know if an error has occurred."""
        print_say("I could not identify your command...", self, Fore.RED)

    def precmd(self, line):
        """Hook that executes before every command."""
        words = line.split()
        # save commands' history
        HISTORY_FILENAME.write(line + '\n')

        # append calculate keyword to front of leading char digit (or '-') in
        # line
        if words and (words[0].isdigit() or line[0] == "-"):
            line = "calculate " + line
            words = line.split()

        if line.startswith("help"):
            return line
        if line.startswith("status"):
            return line

        if not words:
            line = "None"
        else:
            line = self.parse_input(line)
        return line

    def postcmd(self, stop, line):
        """Hook that executes after every command."""
        if self.first_reaction:
            self.prompt = (
                Fore.RED
                + "{} What can I do for you?\n".format(PROMPT_CHAR)
                + Fore.RESET)
            self.first_reaction = False
        if self.enable_voice:
            self.speech.text_to_speech("What can I do for you?\n")

    def speak(self, text):
        if self.enable_voice:
            self.speech.text_to_speech(text)

    def parse_input(self, data):
        """This method gets the data and assigns it to an action"""
        data = data.lower()
        # say command is better if data has punctuation marks
        # Hack!
        if "say" not in data:
            data = data.replace("?", "")
            data = data.replace("!", "")
            data = data.replace(",", "")

            # Remove only dots not followed by alphanumeric character to not mess up urls / numbers
            data = self.regex_dot.sub("", data)

        # Check if Ausis has a fixed response to this data
        if data in self.fixed_responses:
            output = self.fixed_responses[data]  # change return to output =
        else:
            # if it doesn't have a fixed response, look if the data corresponds
            # to an action
            output = self.find_action(
                data, self._plugin_manager.get_plugins().keys())
        return output

    def find_action(self, data, actions):
        """Checks if input is a defined action.
        :return: returns the action"""
        output = "None"
        if not actions:
            return output

        action_found = False
        words = data.split()
        actions = list(actions)

        # return longest matching word
        # TODO: Implement real and good natural language processing
        # But for now, this code returns acceptable results
        actions.sort(key=lambda l: len(l), reverse=True)

        # check word by word if exists an action with the same name
        for action in actions:
            words_remaining = data.split()  # this will help us to stop the iteration
            for word in words:
                words_remaining.remove(word)
                # For the 'near' keyword, the words before 'near' are also
                # needed
                if word == "near":
                    initial_words = words[:words.index('near')]
                    output = word + " " +\
                        " ".join(initial_words + ["|"] + words_remaining)
                elif word == action:  # command name exists
                    action_found = True
                    output = word + " " + " ".join(words_remaining)
                    break
            if action_found:
                break
        return output

    def executor(self, command):
        """
        If command is not empty, we execute it and terminate.
        Else, this method opens a terminal session with the user.
        We can say that it is the core function of this whole class
        and it joins all the function above to work together like a
        clockwork. (Terminates when the user send the "exit", "quit"
        or "goodbye command")
        :return: Nothing to return.
        """
        if command:
            self.execute_once(command)
        else:
            self.cmdloop()
