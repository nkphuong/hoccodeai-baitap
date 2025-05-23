#5th times with python

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(
    base_url=os.getenv("AI_BASE_URL"),
    api_key=os.getenv("AI_SECRET_KEY")
)
ai_model="gpt-4o-mini"
is_stream=False

print('Please input the excercise:')
q = input()
stream = client.chat.completions.create(
    messages=[
        {
            "role":"developer",
            "content": "You're a principal python developer. The user will give you a development excercise, you need to think deeply, analyze the excercise step by step, and then give the code to solve the excercise only on Python." +
            "Your answer should be in the format of a python code block and will be use as a separate python file."+
            "After have the code, you need to run the code, if the code is not runnable, you need to fix the code and run again."+
            "Your answer only contain the code, no other text,or formatting, marking, ```python, nor comment."
        },
        {
            "role":"user",
            "content": q 
        }
        
    ],
    model=ai_model,
    stream=is_stream
)
def write_file(file_path,content):

    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write("\n")
            f.write(content)
    except Exception as e:
        print(f"Error saving file: {e}")


print(stream.choices[0].message.content)

write_file("./exercise.py",stream.choices[0].message.content)