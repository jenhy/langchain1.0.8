"""
任务：流式工具调用。
"""

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_openai import ChatOpenAI

import dotenv
dotenv.load_dotenv()

@tool
def get_weather(city: str) -> str:
    """根据给定的城市名称，返回该城市的天气信息。"""
    return f"{city}的天气是晴天，温度是25度。"

model = init_chat_model(
    model="openai:deepseek-chat",
    temperature=0.5,
    timeout=30,
    max_tokens=1000,

)


model_with_tools = model.bind_tools([get_weather], tool_choice="auto")

# 流式工具调用
for chunk in model_with_tools.stream(
    "杭州和北京的天气如何？",
):
    for tool_chunk in chunk.tool_call_chunks:
        if name := tool_chunk['name']:  ## 海象运算符:=。将name = tool_chunk['name'] \ if name: 合并成一行
            print(f"Tool: {name}")
        if id_ := tool_chunk['id']:
            print(f"ID: {id_}")
        if args := tool_chunk['args']:
            print(f"Args: {args}")
    
# Tool: get_weather
# ID: call_x9vrvwbxy9sjd4ubsx65s584
# Args: {"
# Args: city
# Args: ":
# Args:  "\
# Args: u
# Args: 676
# Args: d
# Args: \u
# Args: 5
# Args: d
# Args: de
# Args: "}
# Tool: get_weather
# ID: call_7968hlog4d259q6q1f7srnnn
# Args: {"
# Args: city
# Args: ":
# Args:  "\
# Args: u
# Args: 531
# Args: 7
# Args: \u
# Args: 4
# Args: e
# Args: ac
# Args: "}

gathered = None
for chunk in model_with_tools.stream(
    "杭州和北京的天气如何？",
):
    gathered = chunk if gathered is None else gathered + chunk
    print(gathered.tool_calls)
    
# [{'name': 'get_weather', 'args': {}, 'id': 'call_pne4nqzb90m47rxj6vib71ol', 'type': 'tool_call'}]
# [{'name': 'get_weather', 'args': {}, 'id': 'call_pne4nqzb90m47rxj6vib71ol', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}]
# [{'name': 'get_weather', 'args': {}, 'id': 'call_pne4nqzb90m47rxj6vib71ol', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}]
# [{'name': 'get_weather', 'args': {}, 'id': 'call_pne4nqzb90m47rxj6vib71ol', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}]
# [{'name': 'get_weather', 'args': {}, 'id': 'call_pne4nqzb90m47rxj6vib71ol', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}]
# [{'name': 'get_weather', 'args': {}, 'id': 'call_pne4nqzb90m47rxj6vib71ol', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}]
# [{'name': 'get_weather', 'args': {}, 'id': 'call_pne4nqzb90m47rxj6vib71ol', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}]
# [{'name': 'get_weather', 'args': {}, 'id': 'call_pne4nqzb90m47rxj6vib71ol', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}, {'name': 'get_weather', 'args': {}, 'id': 'call_6p3q9d8nqz64bn80aihr79fd', 'type': 'tool_call'}]
# [{'name': 'get_weather', 'args': {}, 'id': 'call_pne4nqzb90m47rxj6vib71ol', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}, {'name': 'get_weather', 'args': {}, 'id': 'call_6p3q9d8nqz64bn80aihr79fd', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}]
# [{'name': 'get_weather', 'args': {}, 'id': 'call_pne4nqzb90m47rxj6vib71ol', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}, {'name': 'get_weather', 'args': {}, 'id': 'call_6p3q9d8nqz64bn80aihr79fd', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}]
# [{'name': 'get_weather', 'args': {}, 'id': 'call_pne4nqzb90m47rxj6vib71ol', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}, {'name': 'get_weather', 'args': {}, 'id': 'call_6p3q9d8nqz64bn80aihr79fd', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}]
# [{'name': 'get_weather', 'args': {}, 'id': 'call_pne4nqzb90m47rxj6vib71ol', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}, {'name': 'get_weather', 'args': {}, 'id': 'call_6p3q9d8nqz64bn80aihr79fd', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}]
# [{'name': 'get_weather', 'args': {}, 'id': 'call_pne4nqzb90m47rxj6vib71ol', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}, {'name': 'get_weather', 'args': {}, 'id': 'call_6p3q9d8nqz64bn80aihr79fd', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}]
# [{'name': 'get_weather', 'args': {}, 'id': 'call_pne4nqzb90m47rxj6vib71ol', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}, {'name': 'get_weather', 'args': {}, 'id': 'call_6p3q9d8nqz64bn80aihr79fd', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}]
# [{'name': 'get_weather', 'args': {}, 'id': 'call_pne4nqzb90m47rxj6vib71ol', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}, {'name': 'get_weather', 'args': {}, 'id': 'call_6p3q9d8nqz64bn80aihr79fd', 'type': 'tool_call'}, {'name': '', 'args': {}, 'id': None, 'type': 'tool_call'}]