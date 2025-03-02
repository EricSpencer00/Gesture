import cv2
import mediapipe as mp
import numpy as np
import os
import platform

def capture_gesture_data(gesture_label, num_samples=50, save_dir="data", camera_index=0):
    mp_holistic = mp.solutions.holistic
    holistic = mp_holistic.Holistic()
    if platform.system() == "Darwin":
        cap = cv2.VideoCapture(camera_index, cv2.CAP_AVFOUNDATION)
    else:
        cap = cv2.VideoCapture(camera_index)
    gesture_dir = os.path.join(save_dir, gesture_label)
    os.makedirs(gesture_dir, exist_ok=True)
    count = 0
    while cap.isOpened() and count < num_samples:
        ret, frame = cap.read()
        if not ret:
            break
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)
        if results.left_hand_landmarks:
            landmarks = np.array([[lm.x, lm.y, lm.z] for lm in results.left_hand_landmarks.landmark])
            # Save the landmark data as a .npy file.
            file_path = os.path.join(gesture_dir, f"sample_{count}.npy")
            np.save(file_path, landmarks)
            count += 1
            print(f"Captured sample {count}/{num_samples}")
        cv2.imshow("Capturing Gesture Data", frame)
        if cv2.waitKey(5) & 0xFF == 27:  # Exit on ESC key.
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    for i in range(100):  # Check first 5 indices
        cap = cv2.VideoCapture(i)
        ret, frame = cap.read()
        if ret:
            print(f"Camera index {i} works!")
            cap.release()
        else:
            print(f"Camera index {i} not working.")

    gesture_label = input("Enter gesture label: ")
    num_samples = int(input("Enter number of samples to capture: "))
    camera_index = int(input("Enter working camera index from above: "))
    capture_gesture_data(gesture_label, num_samples, camera_index=camera_index)
