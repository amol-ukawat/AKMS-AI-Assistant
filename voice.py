import pyttsx3
import speech_recognition as sr

def speak(text):
    print("A.K.M.S:", text)

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.setProperty("volume", 1.0)

        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print("Voice Error:", e)


def listen():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)

        command = r.recognize_google(audio)
        print("You:", command)
        return command.lower()

    except sr.UnknownValueError:
        print("Sorry, I did not understand.")
        return ""

    except sr.RequestError:
        print("Internet connection problem.")
        return ""

    except Exception as e:
        print("Listen Error:", e)
        return ""