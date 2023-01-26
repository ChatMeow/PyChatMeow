
# coding=utf-8

from key import API_KEY, SECRET_KEY, CUID, OPENAI_API_KEY
from conf import *
from utils import *

if __name__ == '__main__':

    # while True:
    #     data = input()
    #     print(chat.chat(data))
    audio_handle = AudioBase(recording_file=FILE_PATH)
    chat = ChatMeow(OPENAI_API_KEY, MAX_PROMPT_LENGTH, PROMPT_PATH, DEFAULT_PROMPT,
                    **OPENAI_PARAMS)

    baidu = BaiduAudio(DEV_PID, SCOPE, API_KEY, SECRET_KEY,
                       CUID, FILE_PATH, SAVE_PATH, PER, SPD, PIT, VOL)
    while True:

        try:
            audio_handle.detect_audio()
        except Exception as e:
            print("语音捕获错误")
            print(e)
            continue
        try:
            result = baidu.recognice()

        except Exception as e:
            print("语音识别错误")
            print(e)
            continue

        try:
            open_ai_output = chat.chat(result)
        except Exception as e:
            print("OpenAI错误")
            print(e)
            continue

        try:
            file = baidu.tts(open_ai_output)
        except Exception as e:
            print("语音转换错误")
            print(e)
            continue

        try:
            audio_handle.play(file)
        except Exception as e:
            print("语音播报错误")
            print(e)
            continue
