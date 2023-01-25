from key import OPENAI_API_KEY
import openai
import requests
from requests.auth import HTTPBasicAuth

# meow = ChatMeow(OPENAI_API_KEY)
openai.api_key = OPENAI_API_KEY

# OPENAI_AUTH = HTTPBasicAuth("Bearer", OPENAI_API_KEY)
# COMPLETIONS_API = "https://api.openai.com/v1/completions"
response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)

print(response)