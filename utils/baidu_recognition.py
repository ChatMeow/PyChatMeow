
# coding=utf-8
import json
import base64
import time

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from utils import AudioBase

TOKEN_URL = 'http://aip.baidubce.com/oauth/2.0/token'
ASR_URL = 'http://vop.baidu.com/server_api'
timer = time.perf_counter


class DemoError(Exception):
    pass


class BaiduRecognizer():
    def __init__(self, dev_pid, scope, api_key, secret_key, cuid):
        self.dev_pid = dev_pid
        self.scope = scope
        self.api_key = api_key
        self.secret_key = secret_key
        self.cuid = cuid
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
                raise DemoError('scope is not correct')
            print('SUCCESS WITH TOKEN: %s  EXPIRES IN SECONDS: %s' %
                  (result['access_token'], result['expires_in']))
            self.token = result['access_token']
        else:
            raise DemoError(
                'MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

    def recognice(self, audio_file, format="pcm", rate=16000):
        speech_data = []
        with open(audio_file, 'rb') as speech_file:
            speech_data = speech_file.read()

        length = len(speech_data)
        if length == 0:
            raise DemoError('file %s length read 0 bytes' % audio_file)
        speech = base64.b64encode(speech_data)
        speech = str(speech, 'utf-8')
        params = {'dev_pid': self.dev_pid,
                  'format': format,
                  'rate': rate,
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
            print('asr http response http code : ' + str(err.code))
            result_str = err.read()
            return 1, result_str

        result_str = str(result_str, 'utf-8')
        return 0, result_str
