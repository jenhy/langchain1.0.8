"""
任务：为了使模型可用自定义工具，使用bind_tools 绑定工具。并且根据请求并行调用多个工具。
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

model_with_tools = model.bind_tools([get_weather])

response = model_with_tools.invoke("杭州和北京的天气怎么样？")

print(f"response: {response.tool_calls}")
# response: [
#     {'name': 'get_weather', 'args': {'city': '杭州'}, 'id': 'call_9revy10a75vczfbwwmk0x23c', 'type': 'tool_call'}, 
#     {'name': 'get_weather', 'args': {'city': '北京'}, 'id': 'call_bpmp5zr6zvtll740o8r31o75', 'type': 'tool_call'}]


results = []
for tool_call in response.tool_calls:
    print(f"Tool:{tool_call['name']}")
    print(f"Args:{tool_call['args']}")
    # Tool:get_weather
    # Args:{'city': '杭州'}
    # Tool:get_weather
    # Args:{'city': '北京'}
    if tool_call["name"] == 'get_weather':
        result = get_weather.invoke(tool_call)
    results.append(result)
    
print(f"Results: {results}")
# Results: [
#     ToolMessage(content='杭州的天气是晴天，温度是25度。', name='get_weather', tool_call_id='call_9revy10a75vczfbwwmk0x23c'), 
#     ToolMessage(content='北京的天气是晴天，温度是25度。', name='get_weather', tool_call_id='call_bpmp5zr6zvtll740o8r31o75')]


