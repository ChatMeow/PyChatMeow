
# coding=utf-8

from key import BAIDUKEY, OPENAI_API_KEY
from conf import baidu_config, openai_config
from utils import AudioBase, ChatMeow, BaiduAudio

if __name__ == '__main__':

    audio_handle = AudioBase()
    chat = ChatMeow(OPENAI_API_KEY, **openai_config)
    baidu = BaiduAudio(*BAIDUKEY, **baidu_config)
    # print(baidu.per)
    while True:
        audio_detect_file = audio_handle.detect_audio('./audio/audio.pcm')

        result_text = baidu.recognice(audio_detect_file)
        print(result_text)

        openai_output = chat.chat(result_text)

        output_audio = baidu.tts(openai_output)

        audio_handle.play(output_audio)
