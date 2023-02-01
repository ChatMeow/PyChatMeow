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
    def __init__(self, channels=1, rate=16000, chunk=1024, audio_min_rms=500, max_low_audio_flag=10, max_high_audio_flag=3,
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
        # self.recording_file = recording_file
        self.audio_frames = []

    def __str__(self):
        return "This is AudioBase %s" % self.recording_file

    def play(self, source_file : str="", chunk=None) -> None:
        source_file = source_file if not self.source_file else self.source_file
        chunk = chunk if not self.chunk else self.chunk

        f = wave.open(source_file, "rb")
        p = pyaudio.PyAudio()

        file_format = p.get_format_from_width(f.getsampwidth())
        stream = p.open(format=file_format, channels=f.getnchannels(),
                        rate=f.getframerate(), output=True)

        data = f.readframes(chunk)

        while data != b"":
            stream.write(data)
            data = f.readframes(chunk)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def detect_audio(self, recording_file : str) -> str:
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
        self.record(recording_file)
        return recording_file

    def record(self, recording_file:str) -> None:
        wf = wave.open(recording_file, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.audio_frames))
        wf.close()
        self.audio_frames = []
