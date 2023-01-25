
from key import API_KEY, SECRET_KEY, CUID

# 百度识别

# 需要识别的文件
AUDIO_FILE = './audio/test.pcm'  # 只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
# 文件格式
FORMAT = AUDIO_FILE[-3:]  # 文件后缀只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式

# 采样率
RATE = 16000  # 固定值

# 普通版

DEV_PID = 1537  # 1537 表示识别普通话，使用输入法模型。根据文档填写PID，选择语言及识别模型
SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有
