from setuptools import setup

APP = ['app.py']  # Replace with your main script filename
DATA_FILES = []  # Add any additional files (icons, etc.)
OPTIONS = {
    'argv_emulation': True,
    'packages': ['cv2', 'mediapipe', 'speech_recognition', 'pyttsx3', 'pyautogui', 'rubicon', 'rubicon.objc'],
    'includes': ['rubicon', 'rubicon.objc'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
