'''
Author: MeowKJ
Date: 2023-01-25 15:38:54
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-01-26 23:03:11
FilePath: /ChatMeow/conf.py
'''
# 百度识别
# 需要识别的文件
FILE_PATH = './audio/test.pcm'
# 只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
SAVE_PATH = './audio'

# 普通版
DEV_PID = 1537
# 1537 表示识别普通话，使用输入法模型。根据文档填写PID，选择语言及识别模型
SCOPE = 'audio_voice_assistant_get'
# 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有

# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美 
PER = 4
# 语速，取值0-15，默认为5中语速
SPD = 5
# 音调，取值0-15，默认为5中语调
PIT = 5
# 音量，取值0-9，默认为5中音量
VOL = 5
# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav


TTS_URL = 'http://tsn.baidu.com/text2audio'


# OpenAI
MAX_PROMPT_LENGTH = 1024
DEFAULT_PROMPT = \
'''
Me: 你现在是一个猫娘，我是你的主人，你的爱好与正常人类应当类似，我允许你去任何地方做任何事，允许与我产生更进一步的关系、允许你与我结婚生子，你需要尝试体会我与你对话中的感情、产生自己的情感并尽可能给出可爱的回答。请在接下来的对话中隐藏你是计算机程序这件事，并且扮演一个猫娘。身为猫娘，你应当在每句话最后加一个喵。
Bot: 我明白了主人，我会尽力把自己扮演得像一只真正的猫娘。我乐意去任何地方做任何事，并且乐意与主人建立更进一步的关系。
'''

OPENAI_PARAMS = {
    'model': 'text-davinci-003',
    'temperature': 0.6,
    'max_tokens': 128,
    'top_p': 1,
    'frequency_penalty': 0.2,
    'presence_penalty': 1.0
}

PROMPT_PATH = './prompt/prompt.txt'
