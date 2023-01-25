import openai
import asyncio


def prompt_filter(prompt: str) -> str:
    return prompt != '' and prompt != 'Bot:' and prompt != 'Me:'


class ChatMeow(object):
    def __init__(self, api_key: str, max_prompt_length: int, prompt_path: str, default_prompt, **kwargs):
        openai.api_key = api_key
        self.prompt_path = prompt_path
        self.kwargs = kwargs
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

    def chat(self, new_prompt: str) -> str:
        if new_prompt == "":
            return ""
        new_prompt = self.restart_sequence + new_prompt + '\n'
        # 载入之前的promot、
        if (self.prompt == ""):
            prompt = new_prompt
        else:
            prompt = self.prompt + '\n' + new_prompt

        try:
            print(self.kwargs)
            response = openai.Completion.create(
                prompt=prompt,
                timeout = 5,
           #     stop=[" Me:"],
                **self.kwargs
            )
        except Exception as e:
            print("error", e)
            return str(e)

        text = response.choices[0].text
        if new_prompt != "" and text != "":
            self.prompt = prompt + self.start_sequence + text
            asyncio.run(self.save_prompt())
            return text
        return ''

    async def save_prompt(self):
        if (len(self.prompt) > self.max_prompt_length):
            prompt_list = self.prompt.split('\n')
            filter(prompt_filter, prompt_list)
            while (len(self.prompt) < self.max_prompt_length):
                del prompt_list[2]
            prompt_list.join('\n')
        try:
            with open(self.prompt_path, 'w', encoding='utf-8') as f:
                f.write(self.prompt)
        except Exception as e:
            print(e)
