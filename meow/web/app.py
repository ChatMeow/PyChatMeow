'''
Author: MeowKJ
Date: 2023-02-02 14:41:56
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-02 16:50:52
FilePath: /ChatMeow/meow/web/app.py
'''
from flask import Flask
from flask import request
import logging

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome! PyChatMeow'


@app.route('/get_config', methods=['GET'])
def get_config():
    s = request.args.get('s')
    if s == 'baidu':
        return 
    

@app.route('/set_config', methods=['GET', 'POST'])
def set_config():
    handler = request.json.get('handler')
    name = request.json.get('name')
    value = request.json.get('value')
    logging.info('set_config -> handler: %s name: %s, value: %s' % (handler, name, value))
    if(handler.strip() == ''):
        return 'the handler is None', 400

    if(name.strip() == ''):
        return 'the name is None', 400

    if str(value.strip()) == '':
        return 'the value is None', 400

    return 'ok', 200
