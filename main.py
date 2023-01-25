
# coding=utf-8

from key import API_KEY, SECRET_KEY, CUID, OPENAI_API_KEY
from conf import *
from utils import *

if __name__ == '__main__':
    chat = ChatMeow(OPENAI_API_KEY, MAX_PROMPT_LENGTH, PROMPT_PATH, DEFAULT_PROMPT,
                    **OPENAI_PARAMS)
    while True:
        data = input()
        print(chat.chat(data))

    # audio_handle = AudioBase(recording_file=AUDIO_FILE)
    # recognizer = BaiduRecognizer(dev_pid, scope, api_key, secret_key, cuid)
    # while True:
    #     audio_handle.detect_audio()
    #     result = recognizer.recognice(AUDIO_FILE, rate=RATE)
    #     print(result)
    #     time.sleep(5)
