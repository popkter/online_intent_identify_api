from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()
CHAT_API_KEY = os.getenv("CHAT_API_KEY")

CLIENT = OpenAI(api_key=CHAT_API_KEY, base_url="https://api.deepseek.com")


# 发送消息
def send_messages_sample(messages):
    response = CLIENT.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
    )
    print("response: ", response)
    return response.choices[0].message

def send_messages(messages):
    response = CLIENT.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )
    print("response: ", response)
    return response.choices[0].message

# 流式响应
def stream_response(messages):
    return CLIENT.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True
    )