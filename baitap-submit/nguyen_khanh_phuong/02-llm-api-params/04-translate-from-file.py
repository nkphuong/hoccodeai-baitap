#4th times with python

import os
from openai import OpenAI
from dotenv import load_dotenv
import tiktoken

load_dotenv()

def get_content_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def remove_output_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def get_paragraphs_from_file(file_path):
    # read from file
    content = get_content_from_file(file_path)
    # Split content into words
    sentences = content.split(".")

    paragraphs = []
    count = 0
    current_paragraph = ""
    for sentence in sentences:
        count += len(sentence.split())
        if count < 1500:
            current_paragraph += sentence + "."
        else:
            paragraphs.append(current_paragraph)
            count = len(sentence.split())
            current_paragraph = sentence + "."


    if current_paragraph:
        paragraphs.append(current_paragraph)

    return paragraphs


def write_file(file_path,content):

    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write("\n")
            f.write(content)
    except Exception as e:
        print(f"Error saving file: {e}")


def should_summarize(messages,ai_model, max_tokens):
    prompt = ""
    
    for mess in messages:
        prompt += mess["content"]
    
    encoding = tiktoken.encoding_for_model(ai_model)
    tokens = encoding.encode(prompt)

    return len(tokens) > max_tokens


def translate_by_llm(messages,ai_model):
    client = OpenAI(
        base_url=os.getenv("AI_BASE_URL"),
        api_key=os.getenv("AI_SECRET_KEY")
    )
  
    is_stream=False
    stream = client.chat.completions.create(
        messages=messages,
        model=ai_model,
        stream=is_stream
    )
    return stream.choices[0].message.content

def summarize(prompt, sysmtem_message, ai_model):

    messages = [{
        "role": "developer",
        "content": sysmtem_message
    }]
    
    
    messages.append({
                "role":"user",
                "content": f"Please summarize this text: ```{prompt}```"
        })
    
    return translate_by_llm(messages, ai_model) 

def translate_first_paragraph(paragraphs, ai_model):
    messages=[
            {
                "role":"developer", # use 'developer' instead of 'system' based on the latest docs from openai
                "content": "You're a genius translator, who can help to translate English to Vietnamese with high quality and natural language."+
                            "I will give you a paragraph, it will be a few chapters of a book," +
                            " and I will give you paragraph by paragraph of those chapters. "+
                            "You will only translate the paragraph, and your response will be the translated paragraph without any ```." 
            },
            {
                "role":"user",
                "content": f"Please translate this text to Vietnamese: ```{paragraphs[0]}```"
            }
        ]
    translated_content = translate_by_llm(messages,ai_model)
        

    write_file(output_file, translated_content)

    return [messages, translated_content]

def translate_content(input_file, output_file, ai_model, max_tokens):
   
    paragraphs = get_paragraphs_from_file(input_file)
    print(f"Number of paragraphs: {len(paragraphs)}")
    previous_content = []
    
    messages, translated_content = translate_first_paragraph(paragraphs, ai_model)
    previous_content.append(translated_content)
    
    is_need_summarize = False
    for index in range(1, len(paragraphs)):
        messages.append({
                    "role":"system",
                    "content": translated_content
            })
        messages.append({
                "role":"user",
                "content": f"Please translate this text to Vietnamese: ```{paragraphs[index]}```"
            })
        
        if should_summarize(messages, ai_model, max_tokens):
            is_need_summarize = True    
            break

        translated_content = translate_by_llm(messages,ai_model)
        previous_content.append(translated_content)
        write_file(output_file, translated_content)
    
    if(is_need_summarize and index < len(paragraphs)):
        for y in range(index, len(paragraphs)):
            print(f"Summarizing the paragraph {y} of {len(paragraphs)}")
            prompt = ""
            for i in range(0, index):
                prompt += paragraphs[i]

            input_system_message = "You're a genius translator, who can help to summarize a paragraph of a book. " + \
                                "I will give you a paragraph, " + \
                                "You will only summarize the paragraph, and you will not add any other text or comments."
            summary_input = summarize(prompt, input_system_message, ai_model)

            previous_content_str = ""
            for content in previous_content:
                previous_content_str += content + "\n"

            output_system_message = "You're a genius translator, who can help to summarize a translated paragraph of a book." + \
                            "I will give you a paragraph which is the result of your previous work." + \
                            "You will only summarize the paragraph, and you will not add any other text or comments."
            
            summary_output = summarize(previous_content_str,output_system_message, ai_model)
            
            
            messages=[
                    {
                        "role":"developer", # use 'developer' instead of 'system' based on the latest docs from openai
                        "content": "You're a genius translator, who can help to translate English to Vietnamese with high quality and natural language."+
                                    "I will give you a paragraph, it will a few chapters of a book," +
                                    " and I will give you paragraph by paragraph of those chapters. " +
                                    f"This is the summary of the previous part of the total paragraph: ```{summary_input}``` " + 
                                    f"This is the summary of the previous part of the translated paragraph: ```{summary_output}``` " + 
                                    "You must read the summary of the previous part of the total paragraph and the summary of the previous part of the translated paragraph, and then translate the new paragraph." + 
                                    "Make sure the translated paragraph is natural and fluent, and the translation is accurate." + 
                                    "You will only translate the paragraph, and your response will be the translated paragraph without any ```." 
                    }
                ]
            messages.append({
                    "role":"user",
                    "content": f"Please translate this text to Vietnamese: ```{paragraphs[y]}```"
                })

            translated_content = translate_by_llm(messages,ai_model)

            previous_content.append(translated_content)
            
            write_file(output_file, translated_content)


    
################################################

output_file = 'translated_text.txt'
input_file = 'alice_in_wonderland.txt'

ai_model="gpt-4o-mini"
max_tokens = 5000
remove_output_file(output_file)

translate_content(input_file, output_file, ai_model, max_tokens)


