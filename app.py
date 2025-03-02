import cv2
import mediapipe as mp
import numpy as np
import pickle
import pyautogui
import time
import threading
from voice_recog import listen_voice_commands

# Logging function: append errors or unrecognized commands to log.txt.
def log_message(message):
    with open("log.txt", "a") as log_file:
        log_file.write(f"{time.ctime()}: {message}\n")

# Load the trained gesture model.
def load_model(model_path="model.extension"):
    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        log_message(f"Error loading model: {e}")
        return None

# Process landmarks using the loaded model.
def process_gesture(landmarks, model):
    if landmarks is None:
        return None
    # Flatten landmarks as a placeholder for a real feature vector extraction.
    feature_vector = np.array([landmarks.flatten()])
    try:
        prediction = model.predict(feature_vector)
        return prediction[0]
    except Exception as e:
        log_message(f"Error in gesture prediction: {e}")
        return None

# Map a recognized gesture to a system action.
def perform_action(gesture):
    if gesture == "scroll":
        pyautogui.scroll(10)
    elif gesture == "zoom":
        pyautogui.hotkey('ctrl', '+')
    elif gesture == "select":
        pyautogui.click()
    else:
        log_message(f"Unrecognized gesture: {gesture}")

# Main loop: captures camera frames, processes gestures, and optionally displays the feed.
def gesture_recognition_loop(model):
    mp_holistic = mp.solutions.holistic
    holistic = mp_holistic.Holistic(min_detection_confidence=0.5, 
                                    min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0)
    real_time_feed = True  # Optionally controlled via GUI in an extended version.
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                log_message("Failed to grab frame from camera.")
                break
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = holistic.process(image)
            # Check for left-hand landmarks; similar logic can be added for right-hand or body posture.
            if results.left_hand_landmarks:
                landmarks = np.array([[lm.x, lm.y, lm.z] for lm in results.left_hand_landmarks.landmark])
                gesture = process_gesture(landmarks, model)
                if gesture:
                    print(f"Detected gesture: {gesture}")
                    perform_action(gesture)
            # Display the camera feed (optional).
            if real_time_feed:
                cv2.imshow('AI Control - Gesture Recognition', frame)
            if cv2.waitKey(5) & 0xFF == 27:  # Press ESC to exit.
                break
    except Exception as e:
        log_message(f"Error in gesture recognition loop: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()

def main():
    model = load_model()
    if model is None:
        print("Failed to load model. Exiting.")
        return

    # Start voice recognition in a separate thread.
    voice_thread = threading.Thread(target=listen_voice_commands, daemon=True)
    voice_thread.start()

    # Begin gesture recognition.
    gesture_recognition_loop(model)

if __name__ == "__main__":
    main()
