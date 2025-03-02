from create_data import capture_gesture_data

def user_train():
    gesture_label = input("Enter new gesture label: ")
    num_samples = int(input("Enter number of samples to capture for training: "))
    camera_index = int(input("Enter camera index: "))
    capture_gesture_data(gesture_label, num_samples, camera_index=camera_index)
    print(f"Gesture data for '{gesture_label}' captured successfully.")

if __name__ == "__main__":
    user_train()
