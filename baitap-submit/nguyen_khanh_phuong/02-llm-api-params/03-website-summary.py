#3rd times with python

import os
from openai import OpenAI
from dotenv import load_dotenv
import bs4 as bs
import urllib.request

load_dotenv()

client = OpenAI(
    base_url=os.getenv("AI_BASE_URL"),
    api_key=os.getenv("AI_SECRET_KEY")
)
ai_model="gpt-4o-mini"
is_stream=True

print("Hi there, i'm your assistant, i'm here to help you summary today news \n")
link=input("Give me the article link: \n")
source = urllib.request.urlopen(link).read()
soup = bs.BeautifulSoup(source,'lxml')
article=soup.find('section',class_='section page-detail top-detail').text

content= "Give you the content of an article  ```" + article + "```. Your job is read it carefully, analysis it, then give back the summary of it" 

stream = client.chat.completions.create(
    messages=[
        {
            "role":"developer",
            "content": "You're a brilliant assistant, who can help to sumary an given article in Vietnamese."
        },
        {
            "role":"user",
            "content": content
        }
    ],
    model=ai_model,
    stream=is_stream,
    temperature=0.8,
    top_p=1
)

print("answer: \n")
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")

print("\n")