'''
Author: MeowKJ
Date: 2023-01-25 00:57:53
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-02 02:30:16
FilePath: /ChatMeow/main.py
'''

# coding=utf-8

from key import BAIDUKEY, OPENAI_API_KEY
from conf import baidu_config, openai_config, max_retry_times, timewait
from utils.baidu.baidu_audio import BaiduAudio
from utils.ai.openai_api import ChatMeow
from utils.audio.record import AudioBase
from utils.audio.play import play
from utils.database.db import DatabaseManager
from utils.context import set_db_manager, set_retries
import logging
import time


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    db = DatabaseManager('database.sqlite')
    set_db_manager(db)
    set_retries(timewait, max_retry_times)
    audio_handle = AudioBase()
    chat = ChatMeow(OPENAI_API_KEY, **openai_config)
    baidu = BaiduAudio(*BAIDUKEY, **baidu_config)
    # output_txt = baidu.tts("你好")
    # play(output_txt)

    # # print(baidu.per)
    while True:
        audio_detect_file = audio_handle.detect_audio()

        code, result_text = baidu.recog(audio_detect_file)

        code, openai_output = chat.chat(result_text)
        
        print(openai_output)
        
        code, output_audio = baidu.tts(openai_output)
        play(output_audio)
