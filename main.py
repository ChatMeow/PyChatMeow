
# coding=utf-8


from utils import *
from conf import *

import time

if __name__ == '__main__':
    audio_handle = AudioBase(recording_file=AUDIO_FILE)
    recognizer = BaiduRecognizer(DEV_PID, SCOPE, API_KEY, SECRET_KEY, CUID)
    while True:
        audio_handle.detect_audio()
        result = recognizer.recognice(AUDIO_FILE, format=FORMAT, rate=RATE)
        print(result)
        time.sleep(5)

