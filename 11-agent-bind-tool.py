"""
不用 Agent 框架，手动让 ChatModel 决定是否调用工具。
"""

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

import dotenv
dotenv.load_dotenv()

@tool
def get_weather(city: str) -> str:
    """根据给定的城市名称，返回该城市的天气信息。"""
    return f"{city}的天气是晴天，温度是25度。"


llm = ChatOpenAI(model="deepseek-chat", temperature=0)

llm_with_tools = llm.bind_tools(tools=[get_weather])

results = llm_with_tools.invoke(
    [HumanMessage(content="今天杭州的天气如何？")]
)
print(f"type:{type(results)}")
# type:<class 'langchain_core.messages.ai.AIMessage'>

print(results)

# content='我来帮您查询杭州今天的天气情况。' 
# additional_kwargs={'refusal': None} 
# response_metadata={
#     'token_usage': {'completion_tokens': 23, 'prompt_tokens': 159, 'total_tokens': 182, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': None}, 'input_tokens': 0, 'output_tokens': 0, 'input_token_details': None}, 
#     'model_provider': 'openai', 
#     'model_name': 'deepseek-chat', 
#     'system_fingerprint': None, 
#     'id': '0217640757356815b683ea6c70a7e1d7277ef2ab8257e0f3e1645', 
#     'finish_reason': 'tool_calls', 
#     'logprobs': None} 
# id='lc_run--33006807-9310-47d3-ac37-04b06e0f1cac-0' 
# tool_calls=[{'name': 'get_weather', 'args': {'city': '杭州'}, 'id': 'call_r332sqly74225pk7verb6zvl', 'type': 'tool_call'}] 
# usage_metadata={'input_tokens': 159, 'output_tokens': 23, 'total_tokens': 182, 'input_token_details': {}, 'output_token_details': {}}

if results.tool_calls:
    print("触发了工具：")
    print(results.tool_calls)
else:
    print("没有触发工具。")
    
# 触发了工具：
# [{
#     'name': 'get_weather', 
#     'args': {'city': '杭州'}, 
#     'id': 'call_rpddi0snrynmye209jeq608j', 
#     'type': 'tool_call'}]