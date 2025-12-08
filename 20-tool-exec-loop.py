"""
任务：工具执行循环。
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

# 给模型绑定工具
model_with_tools = model.bind_tools([get_weather], tool_choice="get_weather")

# 1.模型生成工具调用
messages = [
    {
        "role": "user",
        "content": "杭州的天气如何？",
    }
]

ai_msg = model_with_tools.invoke(messages)
# print(ai_msg)

# content='我来帮您查询杭州的天气情况。' 
# additional_kwargs={'refusal': None} 
# response_metadata={'token_usage': {'completion_tokens': 29, 'prompt_tokens': 158, 'total_tokens': 187, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': None, 'id': '02176464293123604294245a7216c83957935f5a9394e3b904bc2', 'finish_reason': 'tool_calls', 'logprobs': None} 
# id='lc_run--1d168f66-e829-431f-a100-3070670faf63-0' 
# tool_calls=[{'name': 'get_weather', 'args': {'city': '杭州'}, 'id': 'call_1zqh4fcn7simt5q7cjcy8jqe', 'type': 'tool_call'}] usage_metadata={'input_tokens': 158, 'output_tokens': 29, 'total_tokens': 187, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}

messages.append(ai_msg)
# print(f"ai_msg:{messages}")

# ai_msg:[
#     {'role': 'user', 'content': '杭州的天气如何？'}, 
#     AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 19, 'prompt_tokens': 112, 'total_tokens': 131, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': None, 'id': '021764643207031e04d0ce0cb7c9c575f1fe60733b212fd4b3ca8', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--39a2adaf-a77b-464d-99b0-1626bb4103cc-0', tool_calls=[{'name': 'get_weather', 'args': {'city': '杭州'}, 'id': 'call_o4hqcyqk6k26vm0skr3ihv9t', 'type': 'tool_call'}], usage_metadata={'input_tokens': 112, 'output_tokens': 19, 'total_tokens': 131, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}})]


# 2.执行工具并收集结果
# 工具返回的每个 ToolMessage 都包含一个与原始工具调用匹配的 tool_call_id ，帮助模型将结果与请求关联起来。
for tool_call in ai_msg.tool_calls:
    # 使用生成的参数执行工具
    tool_result = get_weather.invoke(tool_call)
    messages.append(tool_result)
    
# print(f"tool_result:{messages}")
# tool_result:[
#     {'role': 'user', 'content': '杭州的天气如何？'}, 
#     AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 19, 'prompt_tokens': 112, 'total_tokens': 131, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': None, 'id': '021764643207031e04d0ce0cb7c9c575f1fe60733b212fd4b3ca8', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--39a2adaf-a77b-464d-99b0-1626bb4103cc-0', tool_calls=[{'name': 'get_weather', 'args': {'city': '杭州'}, 'id': 'call_o4hqcyqk6k26vm0skr3ihv9t', 'type': 'tool_call'}], usage_metadata={'input_tokens': 112, 'output_tokens': 19, 'total_tokens': 131, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}), 
#     ToolMessage(content='杭州的天气是晴天，温度是25度。', name='get_weather', tool_call_id='call_o4hqcyqk6k26vm0skr3ihv9t')]


# 3.将结果反馈给模型以获取最终响应
final_response = model_with_tools.invoke(messages)
# print(f"final_response:{final_response}")

# final_response:
#     content='根据查询结果，杭州目前的天气情况是：\n- **天气状况**：晴天 ☀️\n- **温度**：25°C\n\n这是一个比较舒适的温度，适合外出活动。' 
#     additional_kwargs={'refusal': None} 
#     response_metadata={'token_usage': {'completion_tokens': 39, 'prompt_tokens': 186, 'total_tokens': 225, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': None, 'id': '0217646468264598147a36f92134ad55b04f079dd3dc4de515354', 'finish_reason': 'stop', 'logprobs': None} 
#     id='lc_run--fdb5b12f-c46f-4008-ad85-cef14879b62e-0' 
#     usage_metadata={'input_tokens': 186, 'output_tokens': 39, 'total_tokens': 225, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}
