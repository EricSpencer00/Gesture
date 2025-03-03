import cv2
import mediapipe as mp
import numpy as np
import os
import platform

def capture_gesture_data(gesture_label, num_samples=50, save_dir="data"):
    mp_holistic = mp.solutions.holistic
    holistic = mp_holistic.Holistic()
    
    # Modified camera initialization for macOS
    if platform.system() == "Darwin":
        os.environ["OPENCV_VIDEOIO_AVFOUNDATION"] = "1"
        cap = cv2.VideoCapture(-1, cv2.CAP_AVFOUNDATION)  # -1 for auto-select
    else:
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Failed to initialize camera!")
        return

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
            landmarks = np.array([[lm.x, lm.y, lm.z] 
                for lm in results.left_hand_landmarks.landmark])
            
            file_path = os.path.join(gesture_dir, f"sample_{count}.npy")
            np.save(file_path, landmarks)
            count += 1
            print(f"Captured sample {count}/{num_samples}")
            
        cv2.imshow("Capturing Gesture Data", frame)
        if cv2.waitKey(5) & 0xFF == 27:
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # First verify camera access
    if platform.system() == "Darwin":
        print("Make sure to:")
        print("1. Have iPhone connected via Continuity Camera")
        print("2. Grant camera permissions in System Preferences")
        print("3. Keep iPhone unlocked and nearby")
    
    gesture_label = input("Enter gesture label: ")
    num_samples = int(input("Enter number of samples to capture: "))
    capture_gesture_data(gesture_label, num_samples)