import os
from plugin import plugin, require
from colorama import Fore
import random

color_random = [Fore.RED,Fore.GREEN,Fore.CYAN,Fore.YELLOW,Fore.WHITE,Fore.MAGENTA,Fore.BLUE]
random.shuffle(color_random)

voice_control_installed = True
try:
    import speech_recognition as sr
    import pyaudio
except ImportError:
    voice_control_installed = False

if voice_control_installed:
    requirements = []
else:
    requirements = [
        'voice_control_requirements (install portaudio + re-run setup.sh)']


@require(native=requirements)
@plugin("hear")
def hear(ausis, s):
    r = sr.Recognizer()  # intializing the speech_recognition
    listen = False
    _ausis = ausis._ausis  # calling ausis object.
    _ausis.speech.text_to_speech(Fore.GREEN + "Say listen to start voice mode" + Fore.RESET)
    while listen is False:
        try:
            with sr.Microphone() as source:
                os.system('reset')  # for clearing the terminal.
                print(Fore.GREEN + "Say listen to start listening" + Fore.RESET)
                r.adjust_for_ambient_noise(source)  # Eleminating the noise.
                audio = r.listen(source)  # Storing audio.
                pinger = r.recognize_google(audio)  # Converting speech to text
            try:
                if (pinger.lower() == "listen"):
                    listen = True
                    _ausis.speech.text_to_speech(Fore.CYAN + "Voice mode activated" + Fore.RESET)

                    voice_act = color_random[0] + '''
██╗░░░██╗░█████╗░██╗░█████╗░███████╗  ░█████╗░░█████╗░████████╗██╗██╗░░░██╗░█████╗░████████╗███████╗██████╗░
██║░░░██║██╔══██╗██║██╔══██╗██╔════╝  ██╔══██╗██╔══██╗╚══██╔══╝██║██║░░░██║██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
╚██╗░██╔╝██║░░██║██║██║░░╚═╝█████╗░░  ███████║██║░░╚═╝░░░██║░░░██║╚██╗░██╔╝███████║░░░██║░░░█████╗░░██║░░██║
░╚████╔╝░██║░░██║██║██║░░██╗██╔══╝░░  ██╔══██║██║░░██╗░░░██║░░░██║░╚████╔╝░██╔══██║░░░██║░░░██╔══╝░░██║░░██║
░░╚██╔╝░░╚█████╔╝██║╚█████╔╝███████╗  ██║░░██║╚█████╔╝░░░██║░░░██║░░╚██╔╝░░██║░░██║░░░██║░░░███████╗██████╔╝
░░░╚═╝░░░░╚════╝░╚═╝░╚════╝░╚══════╝  ╚═╝░░╚═╝░╚════╝░░░░╚═╝░░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═════╝░''' + Fore.RESET
                    print("{}".format(voice_act))
                    break
                else:
                    continue
            except LookupError:
                continue   # For ignoring if your are not speaking anything.
        except sr.UnknownValueError:
            continue  # For ignoring the unreconized words error
    while listen is True:
        print(Fore.WHITE + "Say somthing" + Fore.RESET)
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                pinger = r.recognize_google(audio).lower()

            if (pinger == "stop"):
                listen = False
                print(Fore.RED + "Listening stopped." + Fore.RESET)
                _ausis.speech.text_to_speech(Fore.RED + "Listening stopped." + Fore.RESET)
                break
            else:
                print(pinger)
                if listen:
                    line = pinger
                    ausis.eval(line)

        except LookupError:
            _ausis.speech.text_to_speech(Fore.RED + 'Audio cannot be read!' + Fore.RESET)
            print(Fore.RED + "Could not understand audio" + Fore.RESET)
            _ausis.speech.text_to_speech(Fore.RED + "unable to recognize voice" + Fore.RESET)
        except sr.UnknownValueError:
            continue
        except sr.RequestError:
            print(Fore.RED + "Could not request results from Google Recognition service" + Fore.RESET)
            continue  # It will ignore connecting server error.
