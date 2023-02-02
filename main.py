'''
Author: MeowKJ
Date: 2023-01-25 00:57:53
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-02 17:53:10
FilePath: /ChatMeow/main.py
'''
from threading import Thread
from meow.web.app import create_app
from chat import chat_loop
import logging
import time

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
    
    chat_thread = Thread(target=chat_loop, name='chat_thread')
    chat_thread.setDaemon(True)
    chat_thread.start()
    # time.sleep(20)
    # chat_loop()
    # create_app()
    create_app()
