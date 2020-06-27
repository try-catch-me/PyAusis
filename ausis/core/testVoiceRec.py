from test import VoiceLinux
from mic_recording import Engine
from packages.weather import main

engObj = Engine()
text = engObj.get_audio()


if "weather" in text:
	main("haripur")
p1 = VoiceLinux(70)
p1.create()
#p1.text_to_speech(text)
