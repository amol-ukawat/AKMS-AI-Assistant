import customtkinter as ctk
import threading
import time
from voice import speak, listen
from command import run_command

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("AKMS Assistant")
app.geometry("1000x680")
app.resizable(False, False)

wake_active = True
is_listening = False


def speak_now(text):
    speak(text)


def add_message(sender, message):
    chat_box.configure(state="normal")

    if sender == "You":
        chat_box.insert("end", f"\nYou\n{message}\n", "user")
    elif sender == "AKMS":
        chat_box.insert("end", f"\nAKMS\n{message}\n", "akms")
    else:
        chat_box.insert("end", f"\n{sender}: {message}\n", "system")

    chat_box.configure(state="disabled")
    chat_box.see("end")


def set_status(text):
    status_label.configure(text=text)


def process_command(command):
    if not command:
        return

    add_message("You", command)
    set_status("Thinking...")

    response = run_command(command.lower())

    add_message("AKMS", response)
    set_status("Speaking...")
    speak_now(response)
    set_status("Online")

    if "bye" in command.lower() or "exit" in command.lower():
        app.after(2000, app.destroy)


def send_text_command():
    command = entry.get().strip()
    entry.delete(0, "end")
    process_command(command)


def voice_command_thread():
    global is_listening

    if is_listening:
        return

    is_listening = True
    set_status("Listening...")

    command = listen()

    if command:
        process_command(command)

    set_status("Online")
    is_listening = False


def voice_command():
    threading.Thread(target=voice_command_thread, daemon=True).start()


def toggle_wake_word():
    global wake_active
    wake_active = not wake_active

    if wake_active:
        wake_button.configure(text="Wake Word ON")
        set_status("Wake Active")
        speak_now("Wake word activated")
    else:
        wake_button.configure(text="Wake Word OFF")
        set_status("Wake Off")
        speak_now("Wake word deactivated")


def wake_word_listener():
    global is_listening

    while True:
        try:
            if not wake_active or is_listening:
                time.sleep(0.5)
                continue

            text = listen()

            if not text:
                continue

            if "hello akms" in text.lower() or "hey akms" in text.lower():
                is_listening = True

                add_message("System", "Wake word detected")
                set_status("Listening...")

                speak_now("Yes Amol, I am listening")

                command = listen()

                if command:
                    process_command(command)

                set_status("Online")
                is_listening = False

        except Exception as e:
            print("Wake Word Error:", e)
            is_listening = False


def clear_chat():
    chat_box.configure(state="normal")
    chat_box.delete("1.0", "end")
    chat_box.configure(state="disabled")
    add_message("AKMS", "Chat cleared. How can I help you?")
    speak_now("Chat cleared. How can I help you?")


app.configure(fg_color="#0F172A")

sidebar = ctk.CTkFrame(app, width=240, corner_radius=0, fg_color="#111827")
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(
    sidebar,
    text="AKMS",
    font=("Segoe UI", 38, "bold"),
    text_color="#38BDF8"
)
logo.pack(pady=(38, 5))

tagline = ctk.CTkLabel(
    sidebar,
    text="AI Voice Assistant",
    font=("Segoe UI", 14),
    text_color="#94A3B8"
)
tagline.pack(pady=(0, 25))

status_card = ctk.CTkFrame(sidebar, corner_radius=18, fg_color="#1E293B")
status_card.pack(padx=22, pady=10, fill="x")

status_label = ctk.CTkLabel(
    status_card,
    text="Online",
    font=("Segoe UI", 16, "bold"),
    text_color="#22C55E"
)
status_label.pack(pady=16)

mic_button = ctk.CTkButton(
    sidebar,
    text="🎤 Voice Command",
    height=44,
    corner_radius=14,
    font=("Segoe UI", 14, "bold"),
    fg_color="#0EA5E9",
    hover_color="#0284C7",
    command=voice_command
)
mic_button.pack(pady=8, padx=22, fill="x")

wake_button = ctk.CTkButton(
    sidebar,
    text="Wake Word ON",
    height=42,
    corner_radius=14,
    fg_color="#1E293B",
    hover_color="#334155",
    text_color="#E5E7EB",
    command=toggle_wake_word
)
wake_button.pack(pady=8, padx=22, fill="x")

clear_button = ctk.CTkButton(
    sidebar,
    text="Clear Chat",
    height=42,
    corner_radius=14,
    fg_color="#1E293B",
    hover_color="#334155",
    text_color="#E5E7EB",
    command=clear_chat
)
clear_button.pack(pady=8, padx=22, fill="x")

exit_button = ctk.CTkButton(
    sidebar,
    text="Exit",
    height=42,
    corner_radius=14,
    fg_color="#DC2626",
    hover_color="#B91C1C",
    command=app.destroy
)
exit_button.pack(side="bottom", pady=30, padx=22, fill="x")

main = ctk.CTkFrame(app, fg_color="#0F172A", corner_radius=0)
main.pack(side="right", fill="both", expand=True)

header = ctk.CTkFrame(main, fg_color="#0F172A")
header.pack(fill="x", padx=35, pady=(35, 18))

title = ctk.CTkLabel(
    header,
    text="Welcome back, Amol 👋",
    font=("Segoe UI", 32, "bold"),
    text_color="#F8FAFC"
)
title.pack(anchor="w")

subtitle = ctk.CTkLabel(
    header,
    text="Say 'Hello AKMS' or type your command below.",
    font=("Segoe UI", 15),
    text_color="#94A3B8"
)
subtitle.pack(anchor="w", pady=(4, 0))

chat_card = ctk.CTkFrame(main, fg_color="#111827", corner_radius=24)
chat_card.pack(fill="both", expand=True, padx=35, pady=(0, 20))

chat_box = ctk.CTkTextbox(
    chat_card,
    font=("Segoe UI", 16),
    corner_radius=18,
    fg_color="#020617",
    text_color="#E5E7EB",
    border_width=1,
    border_color="#1E293B"
)
chat_box.pack(fill="both", expand=True, padx=18, pady=18)

chat_box.tag_config("user", foreground="#F8FAFC")
chat_box.tag_config("akms", foreground="#38BDF8")
chat_box.tag_config("system", foreground="#94A3B8")

chat_box.insert("end", "\nAKMS\nHello Amol, I am ready to assist you.\n", "akms")
chat_box.configure(state="disabled")

bottom = ctk.CTkFrame(main, fg_color="#0F172A")
bottom.pack(fill="x", padx=35, pady=(0, 28))

entry = ctk.CTkEntry(
    bottom,
    height=54,
    corner_radius=18,
    placeholder_text="Ask AKMS anything...",
    font=("Segoe UI", 16),
    fg_color="#111827",
    text_color="#F8FAFC",
    border_color="#334155"
)
entry.pack(side="left", fill="x", expand=True, padx=(0, 12))

send_button = ctk.CTkButton(
    bottom,
    text="Send",
    height=54,
    width=120,
    corner_radius=18,
    font=("Segoe UI", 15, "bold"),
    fg_color="#0EA5E9",
    hover_color="#0284C7",
    command=send_text_command
)
send_button.pack(side="right")

entry.bind("<Return>", lambda event: send_text_command())

app.after(
    1000,
    lambda: speak_now("Hello Amol, I am AKMS. Say Hello AKMS to activate me.")
)

threading.Thread(target=wake_word_listener, daemon=True).start()

app.mainloop()