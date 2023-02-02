'''
Author: MeowKJ
Date: 2023-01-25 14:25:18
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-01 14:27:17
FilePath: /ChatMeow/utils/audio/record.py
'''
import audioop
from multiprocessing import Process
import pyaudio
import wave

stream_format = pyaudio.paInt16
pyaudio_instance = pyaudio.PyAudio()
sample_width = pyaudio_instance.get_sample_size(stream_format)
# global audio_frames


def terminate():
    pyaudio_instance.terminate()


class AudioBase(object):
    def __init__(self, channels=1, rate=16000, chunk=1024, audio_min_rms=2000, max_low_audio_flag=10, max_high_audio_flag=5):
        # self.source_file = source_file
        self.source_file = ""
        self.recording = True
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.audio_min_rms = audio_min_rms
        self.max_low_audio_flag = max_low_audio_flag
        self.max_high_audio_flag = max_high_audio_flag
        # self.recording_file = recording_file
        self.audio_frames = []

    def __str__(self):
        return "This is AudioBase %s" % self.recording_file

    def detect_audio(self):
        stream = pyaudio_instance.open(format=stream_format,
                                       channels=self.channels,
                                       rate=self.rate,
                                       input=True,
                                       frames_per_buffer=self.chunk)
        low_audio_flag = 0
        high_audio_flag = 0
        detect_count = 0
        print("* start detecting audio ~")

        while True:
            detect_count += 1

            stream_data = stream.read(self.chunk)

            rms = audioop.rms(stream_data, 2)
            # print(f"the {detect_count} time detecting：", rms)
            if rms > self.audio_min_rms:
                high_audio_flag = high_audio_flag + 1
                low_audio_flag = 0
                self.audio_frames.append(stream_data)

            else:
                low_audio_flag = low_audio_flag + 1
            # 100 为经验值，即连续 100 次采样都是小音量，则可以认为没有音频，根据实际情况设置
            if low_audio_flag > self.max_low_audio_flag and high_audio_flag > self.max_high_audio_flag:

                print("* no audio detected, stop detecting ~")
                break
        stream.stop_stream()
        stream.close()
        txt = b''.join(self.audio_frames)
        self.audio_frames = []
        return txt