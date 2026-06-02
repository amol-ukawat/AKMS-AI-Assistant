from voice import speak, listen
from command import run_command

speak("AKMS is running in background")

while True:
    text = listen()

    if "hey akms" in text or "hello akms" in text:
        speak("Yes Amol")

        command = listen()

        if command:
            response = run_command(command)
            speak(response)