from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
  api_key= os.getenv("OPEN_AI_API_KEY")
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  store=True,
  messages=[
    {"role": "user", "content": "Tell me about UWI"}
  ]
)

print(completion.choices[0].message.content);
