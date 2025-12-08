"""
工具消息。
"""

from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage, AIMessage

import dotenv
dotenv.load_dotenv()

def get_weather(city: str) -> str:
    """获取城市的天气信息。"""
    return f"{city}的天气是晴天，温度是25度。"

model = init_chat_model(
    model="openai:deepseek-chat"
)

model_with_tools = model.bind_tools([get_weather])
response = model_with_tools.invoke("杭州的天气怎么样？")

print(response)

# content='' 
# additional_kwargs={'refusal': None} 
# response_metadata={'token_usage': {'completion_tokens': 19, 'prompt_tokens': 106, 'total_tokens': 125, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': None, 'id': '02176481748496902e023d72136319b9e76df1944774f54fc0af3', 'finish_reason': 'tool_calls', 'logprobs': None} 
# id='lc_run--387c64f5-91e2-4218-a91d-2b670739af85-0' 
# tool_calls=[{'name': 'get_weather', 'args': {'city': '杭州'}, 'id': 'call_0at8gannlbld5tw1s5kj2uny', 'type': 'tool_call'}] 
# usage_metadata={'input_tokens': 106, 'output_tokens': 19, 'total_tokens': 125, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}

for tool_call in response.tool_calls:
    print(f"Tool: {tool_call['name']}")
    print(f"Arguments: {tool_call['args']}")
    print(f"ID: {tool_call['id']}")
    
# Tool: get_weather
# Arguments: {'city': '杭州'}
# ID: call_0at8gannlbld5tw1s5kj2uny