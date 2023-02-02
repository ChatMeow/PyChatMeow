'''
Author: MeowKJ
Date: 2023-01-25 00:57:53
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-02 16:38:12
FilePath: /ChatMeow/main.py
'''
# coding=utf-8
from meow.audio.play import play
from meow.utils.context import get_audio_handler, get_openai_handler, get_baidu_handler
import logging
from meow.utils.context import baidu_lock, openai_lock
from threading import Thread
from meow.utils.conf import init_context

def main_loop():
    while True:
        audio_detect_file = audio_handler.detect_audio()

        baidu_lock.acquire()
        code, result_text = baidu_handler.recog(audio_detect_file)
        baidu_lock.release()
        openai_lock.acquire()

        code, openai_output = openai_handler.chat(result_text)
        openai_lock.release()

        print(openai_output)
        baidu_lock.acquire()

        code, output_audio = baidu_handler.tts(openai_output)
        baidu_lock.release()

        play(output_audio)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', encoding='utf-8')

    # output_txt = baidu.tts("你好")
    init_context()
    # play(output_txt)

    # # print(baidu.per)
    
    audio_handler = get_audio_handler()
    openai_handler = get_openai_handler()
    baidu_handler = get_baidu_handler()

    Thread(target=main_loop).start()
