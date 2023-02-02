import yaml
import logging
from meow.database.db import DatabaseManager

from meow.audio.record import AudioBase
from meow.baidu.baidu_audio import BaiduAudio
from meow.ai.openai_api import ChatMeow

from meow.utils.context import baidu_lock
from meow.utils.context import openai_lock

import meow.utils.context

def init_context():
    generate_all_context()

def get_conf_data():
    # 打开yaml文件
    logging.debug("***获取yaml文件数据***")
    with open('config.yml', 'r', encoding='utf-8') as f:
        file_data = f.read()
    data = yaml.safe_load(file_data)
    return data


def get_key_data():
    # 打开yaml文件
    logging.debug("***获取yaml文件数据***")
    with open('key.yml', 'r', encoding='utf-8') as f:
        file_data = f.read()
    data = yaml.safe_load(file_data)
    return data


def generate_all_context():

    conf_data = get_conf_data()
    logging.debug(conf_data)
    
    openai_config = conf_data['openai']
    baidu_config = conf_data['baidu']
    
    key_data = get_key_data()

    openai_api_key = key_data['OPENAI_API_KEY']
    baidu_key = key_data['BAIDU_KEY']

    audio = AudioBase()
    openai = ChatMeow(openai_api_key, **openai_config)
    baidu = BaiduAudio(*baidu_key, **baidu_config)

    meow.utils.context.set_openai_handler(openai)
    meow.utils.context.set_baidu_handler(baidu)
    meow.utils.context.set_audio_handler(audio)

    retry_conf = conf_data['retry']
    meow.utils.context.set_retries(
        retry_conf['timewait'], retry_conf['max_retry_times'])

    db = DatabaseManager('database.sqlite')
    meow.utils.context.set_db_manager(db)


def set_conf_data(handler, key, value):
    logging.debug("***设置yaml文件数据***")
    data = get_conf_data()[handler]
    data.update({key: value})

    with open('config.yaml', 'w', encoding='utf-8') as f:
        f.write(yaml.dump(data, default_flow_style=False))
    return data


def set_config(handler, key, value):
    if handler == 'baidu':
        baidu_lock.acquire()
        set_conf_data('baidu', key, value)
        baidu_handler = meow.utils.context.get_baidu_handler()
        baidu_handler.set_config(key, value)
        setattr(baidu_handler, key, value)
        baidu_lock.release()
        return 0
    elif handler == 'openai':
        openai_lock.acquire()
        set_conf_data('openai', key, value)
        openai_handler = meow.utils.context.get_openai_handler()
        setattr(openai_handler, key, value)
        baidu_lock.release()
    else:
        logging.error("不支持的handler")
        return 1

