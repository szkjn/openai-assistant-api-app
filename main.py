import openai
import os

api_key = os.environ.get('OPENAI_API_KEY1')
client = openai.OpenAI(api_key=api_key)
model = "gpt-4-turbo"

