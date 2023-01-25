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
    def __init__(self, channels=1, rate=16000, chunk=1024, audio_min_rms=1000, max_low_audio_flag=30,max_high_audio_flag = 3,
                 recording_file=""):
        # self.source_file = source_file
        self.source_file = ""
        self.recording = True
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.audio_min_rms = audio_min_rms
        self.max_low_audio_flag = max_low_audio_flag
        self.max_high_audio_flag = max_high_audio_flag
        self.recording_file = recording_file
        self.audio_frames = []

    def __str__(self):
        return "This is AudioBase %s" % self.recording_file

    def play(self, source_file="", chunk=None):
        source_file = source_file if not self.source_file else self.source_file
        chunk = chunk if not self.chunk else self.chunk

        f = wave.open(source_file, "rb")
        p = pyaudio.PyAudio()

        file_format = p.get_format_from_width(f.getsampwidth())
        stream = p.open(format=file_format, channels=f.getnchannels(), rate=f.getframerate(), output=True)

        data = f.readframes(chunk)

        while data != b"":
            stream.write(data)
            data = f.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()
        return self

    def detect_audio(self):
        print("* start detecting audio ~")

        stream = pyaudio_instance.open(format=stream_format,
                                       channels=self.channels,
                                       rate=self.rate,
                                       input=True,
                                       frames_per_buffer=self.chunk)
        low_audio_flag = 0
        high_audio_flag = 0
        detect_count = 0
        while True:
            detect_count += 1

            stream_data = stream.read(self.chunk)

            rms = audioop.rms(stream_data, 2)
            print(f"the {detect_count} time detecting：", rms)
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
        self.record()
        return self

    def record(self):
        wf = wave.open(self.recording_file, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.audio_frames))
        wf.close()
        self.audio_frames = []
        return self

    def play_and_detect(self, source_file, channels, rate, chunk, audio_min_rms, max_low_audio_flag, recording,
                        recording_file):
        self.source_file = source_file
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.audio_min_rms = audio_min_rms
        self.max_low_audio_flag = max_low_audio_flag
        self.recording = recording
        self.recording_file = recording_file

        play_process = Process(target=self.play)
        detect_process = Process(target=self.detect_audio)
        play_process.start()
        detect_process.start()

        play_process.join()
        detect_process.join()
        return self
