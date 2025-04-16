#2nd times with python

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
messages=[
    {
        "role":"developer", # use 'developer' instead of 'system' based on the latest docs from openai
        "content": "You're a genius aquarist, who can help to think deeply and answer the question in Vietnamese."
    }
]

def chat(client, ai_model, is_stream, messages):
    question = input("User: \n")

    messages.append(
        {
            "role": "user",
            "content": question + "?"
        }
    )

    stream = client.chat.completions.create(
        messages=messages,
        model=ai_model,
        stream=is_stream,
        temperature=0.7,
        top_p=0.75
    )

    print("AI: \n")
    answer=""
    for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")
        answer = answer + str(chunk.choices[0].delta.content or "")

    
    print("\n")
    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
    chat(client,ai_model, is_stream, messages)

print("Hi there, i'm a genius aquarist, who can help you to build your own fish tank sucessfully. How can i help?: \n")
chat(client,ai_model, is_stream, messages)