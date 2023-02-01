'''
Author: MeowKJ
Date: 2023-01-25 15:40:12
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-01-31 23:55:13
FilePath: /ChatMeow/utils/baidu_audio.py
'''

# coding=utf-8
import json
import base64
import time
import os
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.parse import quote_plus

TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'
ASR_URL = 'http://vop.baidu.com/server_api'
TTS_URL = 'http://tsn.baidu.com/text2audio'

FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
timer = time.perf_counter

class BaiduAudio():
    def __init__(self, api_key, secret_key, cuid, dev_pid=1537, scope="audio_voice_assistant_get", per=4, spd=5, pit=5, vol=5):
        self.dev_pid = dev_pid
        self.scope = scope
        self.api_key = api_key
        self.secret_key = secret_key
        self.cuid = cuid
        self.per = per
        self.spd = spd
        self.pit = pit
        self.vol = vol
        self.format = "pcm"
        self.save_path = "./audio/"
        self.tts_format = "wav"
        self.get_token()

    def get_token(self):
        params = {'grant_type': 'client_credentials',
                  'client_id': self.api_key,
                  'client_secret': self.secret_key}

        post_data = urlencode(params)
        post_data = post_data.encode('utf-8')
        req = Request(TOKEN_URL, post_data)
        try:
            f = urlopen(req)
            result_str = f.read()
        except URLError as err:
            print('token http response http code : ' + str(err.code))
            result_str = err.read()
        result_str = result_str.decode()

        result = json.loads(result_str)
        if 'access_token' in result.keys() and 'scope' in result.keys():
            # SCOPE = False 忽略检查
            if self.scope and (not self.scope in result['scope'].split(' ')):
                raise Exception('scope is not correct')
            print('SUCCESS WITH TOKEN: %s  EXPIRES IN SECONDS: %s' %
                  (result['access_token'], result['expires_in']))
            self.token = result['access_token']
        else:
            raise Exception(
                'MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

    def recognice(self, audio_file):
        speech_data = []
        with open(audio_file, 'rb') as speech_file:
            speech_data = speech_file.read()

        length = len(speech_data)
        if length == 0:
            raise Exception('file %s length read 0 bytes' % audio_file)
        speech = base64.b64encode(speech_data)
        speech = str(speech, 'utf-8')
        params = {'dev_pid': self.dev_pid,
                  'format': self.format,
                  'rate': 16000,
                  'token': self.token,
                  'cuid': self.cuid,
                  'channel': 1,
                  'speech': speech,
                  'len': length
                  }
        post_data = json.dumps(params, sort_keys=False)
        # print post_data
        req = Request(ASR_URL, post_data.encode('utf-8'))
        req.add_header('Content-Type', 'application/json')
        try:
            begin = timer()
            f = urlopen(req)
            result_str = f.read()
            print("Request time cost %f" % (timer() - begin))
        except URLError as err:
            raise Exception('asr http response http code : ' + str(err.code))

        result_str = str(result_str, 'utf-8')

        text = dict(json.loads(result_str))["result"][0]
        return text

    def tts(self, text):
        tex = quote_plus(text)  # 此处TEXT需要两次urlencode
        print(tex)
        params = {'tok': self.token, 'tex': tex, 'per': self.per, 'spd': self.spd, 'pit': self.pit, 'vol': self.vol, 'aue': 6, 'cuid': self.cuid,
                  'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

        data = urlencode(params)
        print('test on Web Browser' + TTS_URL + '?' + data)

        req = Request(TTS_URL, data.encode('utf-8'))
        has_error = False
        try:
            f = urlopen(req)
            result_str = f.read()

            headers = dict((name.lower(), value)
                           for name, value in f.headers.items())

            # has_error = ('content-type' not in headers.keys()
            #              or headers['content-type'].find('audio/') < 0)
        except URLError as err:
            raise Exception('asr http response http code : ' + str(err.code))
        
        save_file = os.path.join(self.save_path, 'result.' + self.tts_format)

        with open(save_file, 'wb') as of:
            of.write(result_str)

        return save_file
