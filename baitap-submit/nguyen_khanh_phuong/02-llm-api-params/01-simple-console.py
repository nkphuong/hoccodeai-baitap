#1st times with python
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(
    base_url=os.getenv("AI_BASE_URL"),
    api_key=os.getenv("AI_SECRET_KEY")
)
ai_model="gpt-4o-mini"
is_stream=True

print('Please input your question about your aquarium:')
q = input()

stream = client.chat.completions.create(
    messages=[
        {
            "role":"developer",
            "content": "You're a genius aquarist, who can help to think deeply and answer the question in Vietnamese."
        },
        {
            "role":"user",
            "content": q + "?"
        }
    ],
    model=ai_model,
    stream=is_stream
)

print("answer: \n")
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")

print("\n")