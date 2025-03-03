import rubicon.objc
import stubs
import threading
import subprocess
import time

# --- Voice Control Section ---
import speech_recognition as sr
import pyttsx3

def voice_control():
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

    with sr.Microphone() as source:
        print("Voice Control: Listening...")
        while True:
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio)
                print("Heard:", command)
                
                # Execute macOS command based on recognized text
                if "open Safari" in command.lower():
                    subprocess.call(["osascript", "-e", 'tell application "Safari" to activate'])
                    response = "Opening Safari"
                elif "what time" in command.lower():
                    response = time.strftime("The time is %H:%M")
                else:
                    response = "Command not recognized"
                
                # Provide audible feedback using macOS say command
                subprocess.call(["say", response])
                # Alternatively, use pyttsx3:
                # engine.say(response)
                # engine.runAndWait()
            except sr.WaitTimeoutError:
                print("No speech detected, continuing...")
            except sr.UnknownValueError:
                print("Could not understand audio")
            except Exception as e:
                print("Voice error:", e)

# --- Gesture Control Section ---
import cv2
import mediapipe as mp
import pyautogui

def gesture_control():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Webcam not accessible")
        return

    print("Gesture Control: Starting webcam...")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the BGR image to RGB.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Example: Check if index finger is raised (customize as needed)
                # Landmark 8 is the tip of the index finger.
                index_tip = hand_landmarks.landmark[8]
                wrist = hand_landmarks.landmark[0]
                if index_tip.y < wrist.y:  # simple check: index finger is above the wrist
                    print("Gesture detected: Index finger raised!")
                    # Map to an action, e.g., simulate a keypress:
                    pyautogui.press('space')
                    time.sleep(1)  # debounce to avoid multiple triggers

        cv2.imshow("Gesture Control (press Q to quit)", frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# --- Main Application ---
if __name__ == "__main__":
    # Stubs
    import stubs

    # Run voice control and gesture control concurrently using threading
    voice_thread = threading.Thread(target=voice_control, daemon=True)
    gesture_thread = threading.Thread(target=gesture_control, daemon=True)

    voice_thread.start()
    gesture_thread.start()

    print("Application is running. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting application.")
