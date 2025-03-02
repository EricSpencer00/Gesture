import speech_recognition as sr
import pyttsx3
import pyautogui
import time
import logging

# Initialize and speak a response.
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Process the recognized command and perform corresponding actions.
def process_command(command):
    command = command.lower()
    if "scroll" in command:
        pyautogui.scroll(10)
        speak("Scrolling")
    elif "zoom" in command:
        pyautogui.hotkey('ctrl', '+')
        speak("Zooming in")
    elif "select" in command:
        pyautogui.click()
        speak("Selecting")
    else:
        # For ambiguous queries, one might add logic here to call OpenAI.
        speak("I did not understand that command.")
        logging.error(f"Unrecognized voice command: {command}")

# Continuously listen for voice commands.
def listen_voice_commands():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    print("Voice recognition started. Listening for commands...")
    while True:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Say something...")
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio)
                print(f"Recognized command: {command}")
                process_command(command)
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                logging.error("Voice command not recognized.")
            except sr.RequestError as e:
                logging.error(f"Could not request results; {e}")
            time.sleep(1)  # Prevent busy waiting.
