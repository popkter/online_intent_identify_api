import requests
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse

from deepseek import send_messages_sample
from intent import intent_identify

app = FastAPI()

@app.post("/query_intent")
async def process_weather_query(request: Request):
    data = await request.json()
    print("Raw request body:", data)  # 打印原始请求体
    user_query = data.get("user_query", "")
    token = data.get("token", "1008611")

    if token == "1008611":
        intent_result = intent_identify(user_query)
        print("Intent result:", intent_result)
        if intent_result.__contains__("Weather"):
            return StreamingResponse(requests.post("http://124.221.124.238:10100/query_weather",
                                                   json={"user_query": user_query, "token": token}))
        if intent_result.__contains__("UserAdd"):
            return {
                "action": "UserAdd",
                "name": get_user_name(user_query)
            }
        if intent_result.__contains__("UserQuery"):
            return {
                "action": "UserQuery",
                "name": ""
            }
        else:
            return {'data':'Not Ready'}
    else:
        return HTTPException(status_code=401, detail="Invalid token")


def get_user_name(user_query):
    messages = [
        {"role": "user",
         "content": "你是一个很有帮助的语言助手，能够提取输入的文本中的参数信息。下面是一个用户的输入，请帮我提取出文本中用户的名字: " + user_query+
         f"，直接输入用户的名字，不需要输出其他符号"}
    ]
    message = send_messages_sample(messages)
    return message.content


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=10000)
