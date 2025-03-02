import os
import numpy as np
import pickle
from sklearn.neighbors import KNeighborsClassifier

def load_training_data(data_dir="data"):
    X = []
    y = []
    # Loop through each gesture folder.
    for gesture in os.listdir(data_dir):
        gesture_path = os.path.join(data_dir, gesture)
        if os.path.isdir(gesture_path):
            for file in os.listdir(gesture_path):
                if file.endswith(".npy"):
                    data = np.load(os.path.join(gesture_path, file))
                    # Flatten the landmark array for the classifier.
                    X.append(data.flatten())
                    y.append(gesture)
    return np.array(X), np.array(y)

def train_model():
    X, y = load_training_data()
    if len(X) == 0:
        print("No training data found. Please capture some gesture data first.")
        return
    classifier = KNeighborsClassifier(n_neighbors=3)
    classifier.fit(X, y)
    # Save the trained model.
    with open("model.extension", "wb") as f:
        pickle.dump(classifier, f)
    print("Model trained and saved successfully.")

if __name__ == "__main__":
    train_model()
