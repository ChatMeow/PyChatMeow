<!--
 * @Author: MeowKJ
 * @Date: 2021-11-22 01:41:22
 * @LastEditors: MeowKJ ijink@qq.com
 * @LastEditTime: 2023-01-25 16:31:23
 * @FilePath: /ChatMeow/README.md
-->

## 百度语言识别说明

### 食用方法

使用python 脚本方式测试rest api 识别接口
根目录下创建**key.py**文件
从网页中申请的应用获取appKey和appSecret
同时设置设置 CUID字段， 这是用户唯一标识，用来区分用户，计算 UV 值。建议填写能区分用户的机器 MAC 地址或 IMEI 码，长度为 60 字符以内。

```python
# 填写网页上申请的appkey 如 API_KEY="g8eBUMSokVB1BHGmgxxxxxx"
API_KEY = '4E1BG9lTnlSeIf1NQFlrxxxx'

# 填写网页上申请的APP SECRET 如 SECRET_KEY="94dc99566550d87f8fa8ece112xxxxx"
SECRET_KEY = '544ca4657ba8002e3dea3ac2f5fxxxxx'

#填写一个CUID
CUID = 'PYTHON_MEOW_CHAT'
```

conf.py文件有以下设置
```python
# 需要识别的文件
AUDIO_FILE = "./16k.pcm";
# 文件格式
FORMAT = "pcm"; # 文件后缀 pcm/wav/amr/m4a 格式
# 根据文档填写PID，选择语言及识别模型
DEV_PID = 1537; #  1537 表示识别普通话，使用输入法模型。
```

[百度短语音识别标准版文档](https://ai.baidu.com/ai-doc/SPEECH/ek38lxj1u)
