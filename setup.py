from setuptools import setup

APP = ['app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': [
        'cv2',  # OpenCV core module
        'mediapipe',
        'numpy',
        'pyautogui',
        'pyttsx3',
        'scikit_learn',  # Fix scikit-learn issue
        'SpeechRecognition',  # Fix SpeechRecognition issue
    ],
    'includes': [
        'cv2', 
        'opencv-contrib-python',
        'SpeechRecognition',
        'scikit-learn'
    ],
    'excludes': [
        'pytest',  # Exclude unnecessary test dependencies
    ]
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
