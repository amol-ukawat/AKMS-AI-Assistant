from memory import remember, recall
from ai_brain import ai_reply
import datetime
import webbrowser
import os
import random
import psutil
import pyautogui

def run_command(command):
    command = command.lower()

    # Time
    if "time" in command:
        return f"The time is {datetime.datetime.now().strftime('%I:%M %p')}"

    # Date
    elif "date" in command:
        return f"Today's date is {datetime.datetime.now().strftime('%d %B %Y')}"

    # Day
    elif "day" in command:
        return f"Today is {datetime.datetime.now().strftime('%A')}"

    # Chrome
    elif "open chrome" in command:
        os.system("start chrome")
        return "Opening Chrome"

    # VS Code
    elif "open vs code" in command or "open vscode" in command:
        os.system("code")
        return "Opening VS Code"

    # WhatsApp
    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        return "Opening WhatsApp"

    # Google
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google"

    # YouTube
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"

    # Calculator
    elif "open calculator" in command:
        os.system("calc")
        return "Opening Calculator"

    # Notepad
    elif "open notepad" in command:
        os.system("notepad")
        return "Opening Notepad"

    # Battery
    elif "battery" in command:
        battery = psutil.sensors_battery()
        if battery:
            return f"Battery is {battery.percent} percent"
        return "Battery information not available"

    # WiFi
    elif "wifi" in command or "wi-fi" in command:
        try:
            result = os.popen("netsh wlan show interfaces").read()

            if "connected" in result.lower():
                return "WiFi is connected"

            return "WiFi is not connected"

        except:
            return "Unable to check WiFi status"

    # Screenshot
    elif "screenshot" in command:
        filename = f"screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png"
        pyautogui.screenshot(filename)
        return f"Screenshot saved as {filename}"

    # Search Google
    elif "search" in command:
        query = command.replace("search", "").strip()

        if query:
            webbrowser.open(
                f"https://www.google.com/search?q={query}"
            )
            return f"Searching for {query}"

        return "What should I search?"

    # Greeting
    elif "hello" in command or "hi" in command:
        return "Hello Amol. How can I help you today?"

    # Joke
    elif "joke" in command:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why did the computer go to the doctor? Because it had a virus.",
            "Why was the math book sad? Because it had too many problems."
        ]
        return random.choice(jokes)

    # Motivation
    elif "motivate me" in command:
        return "Keep going Amol. Every project you build makes you better."

    # Exit
    elif "exit" in command or "bye" in command:
        return "Goodbye Amol. Have a great day."
    elif command.startswith("remember my name is"):
          name = command.replace("remember my name is", "").strip()
          remember("name", name)
          return f"Okay, I will remember your name is {name}"

    elif "what is my name" in command:
          name = recall("name")
          if name:
            return f"Your name is {name}"
          return "I do not know your name yet."

    # Fallback
    else:
        return ai_reply(command)