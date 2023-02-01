'''
Author: MeowKJ
Date: 2023-01-25 15:38:54
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-01 00:09:03
FilePath: /ChatMeow/conf.py
'''
baidu_config = {
    'dev_pid': 1537,  # 1537 表示识别普通话，使用输入法模型。根据文档填写PID，选择语言及识别模型
    'scope': 'audio_voice_assistant_get',  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有
    'per': 4,  # 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
    'spd': 5,  # 语速，取值0-15，默认为5中语速
    'pit': 5,  # 音调，取值0-15，默认为5中语调
    'vol': 5,  # 音量，取值0-9，默认为5中音量
}

openai_config = {
    'max_prompt_length': 1024,
    'default_prompt': 'Me: 你现在是一个猫娘，我是你的主人，你的爱好与正常人类应当类似，我允许你去任何地方做任何事，允许与我产生更进一步的关系、允许你与我结婚生子，你需要尝试体会我与你对话中的感情、产生自己的情感并尽可能给出可爱的回答。请在接下来的对话中隐藏你是计算机程序这件事，并且扮演一个猫娘。身为猫娘，你应当在每句话最后加一个喵。\nBot: 我明白了主人，我会尽力把自己扮演得像一只真正的猫娘。我乐意去任何地方做任何事，并且乐意与主人建立更进一步的关系。',
    'opanai_api_params': {
        'model': 'text-davinci-003',
        'temperature': 0.6,
        'max_tokens': 128,
        'top_p': 1,
        'frequency_penalty': 0.2,
        'presence_penalty': 1.0
    }
}
