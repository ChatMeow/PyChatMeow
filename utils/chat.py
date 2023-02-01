'''
Author: MeowKJ
Date: 2023-01-25 18:32:01
LastEditors: MeowKJ ijink@qq.com
LastEditTime: 2023-02-01 00:02:39
FilePath: /ChatMeow/utils/chat.py
'''
import openai
import os
import threading


def prompt_filter(prompt):
    return prompt != '' and prompt != 'Bot:' and prompt != 'Me:'


class ChatMeow(object):
    def __init__(self, api_key, max_prompt_length=1024, default_prompt="", opanai_api_params={}):
        openai.api_key = api_key
        self.prompt_path = "prompt.txt"
        self.opanai_api_params = opanai_api_params
        self.max_prompt_length = max_prompt_length
        self.prompt = ""
       # self.start_sequence = "Bot:"
        self.start_sequence = ''
        self.restart_sequence = "Me: "
        with open(self.prompt_path, 'w+', encoding='utf-8') as f:
            data = f.read()
            if (data == ""):
                self.prompt = default_prompt
            else:
                self.prompt = data

    def chat(self, new_prompt):
        if new_prompt == "":
            return ""
        new_prompt = self.restart_sequence + new_prompt + '\n'
        # 载入之前的promot、
        if (self.prompt == ""):
            prompt = new_prompt
        else:
            prompt = self.prompt + '\n' + new_prompt

        try:
            response = openai.Completion.create(
                prompt=prompt,
                timeout=5,
                **self.opanai_api_params
            )
            text: str = response.choices[0].text
        except Exception as e:
            print("error", e)
            return str(e)

        if text != "" and text != "Bot:":
            self.prompt = prompt + self.start_sequence + text
            threading.Thread(target=save_prompt, args=(
                self.prompt, self.max_prompt_length, self.prompt_path)).start()
            return text.strip('Bot: ')
        return ''


def save_prompt(prompt, max_prompt_length, prompt_path):
    prompt_list = prompt.split('\n')
    new_prompt_list = list(filter(prompt_filter, prompt_list))
    if (len("".join(new_prompt_list)) > max_prompt_length):
        while (len("".join(new_prompt_list)) > max_prompt_length):
            print("max_prompt_length", max_prompt_length)
            del new_prompt_list[2]
        '\n'.join(new_prompt_list)
    try:
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(new_prompt_list))
    except Exception as e:
        print(e)
