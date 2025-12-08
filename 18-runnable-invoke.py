"""
任务：invoke 方法使用
"""

from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage

import dotenv
dotenv.load_dotenv()

model = init_chat_model(
    model="openai:deepseek-chat",
    temperature=0.5,
    timeout=30,
    max_tokens=1000,
)

response = model.invoke("请将中文翻译成日文。我爱中国。")
print(f"single message response:{response}")

conversation = [
    {"role": "system", "content": "你是一个乐于助人的助手，请将英文翻译成中文。"},
    {"role": "user", "content": "Translate: I love programming."},
    {"role": "assistant", "content": "我非常喜欢编程。"},
    {"role": "user", "content": "Translate: I love building applications."}
]

response = model.invoke(conversation)
print(f"dictionary format response:{response}")

conversation = [
    SystemMessage(content="你是一个乐于助人的助手，请将英文翻译成中文。"),
    HumanMessage(content="Translate: I love programming."),
    AIMessage(content="我非常喜欢编程。"),
    HumanMessage(content="Translate: I love building applications.")
]
response = model.invoke(conversation)
print(f"message objects response:{response}")

# single message response:
#     content='私は中国が大好きです。' 
#     additional_kwargs={'refusal': None} 
#     response_metadata={'token_usage': {'completion_tokens': 7, 'prompt_tokens': 15, 'total_tokens': 22, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_eaab8d114b_prod0820_fp8_kvcache', 'id': 'a232650f-da11-497c-9bff-87e83f6534ac', 'finish_reason': 'stop', 'logprobs': None} 
#     id='lc_run--be511344-6f88-4533-a5a8-01ed8f0a420a-0' 
#     usage_metadata={'input_tokens': 15, 'output_tokens': 7, 'total_tokens': 22, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}
# dictionary format response:
#     content='我喜欢开发应用程序。' 
#     additional_kwargs={'refusal': None} 
#     response_metadata={'token_usage': {'completion_tokens': 4, 'prompt_tokens': 39, 'total_tokens': 43, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_eaab8d114b_prod0820_fp8_kvcache', 'id': 'abd85b51-9b56-43d2-9948-36bde54fb300', 'finish_reason': 'stop', 'logprobs': None} 
#     id='lc_run--ea35b28a-7023-47c4-9c74-321bb9cbbf87-0' 
#     usage_metadata={'input_tokens': 39, 'output_tokens': 4, 'total_tokens': 43, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}
# message objects response:
#     content='我喜欢开发应用程序。' 
#     additional_kwargs={'refusal': None} 
#     response_metadata={'token_usage': {'completion_tokens': 4, 'prompt_tokens': 39, 'total_tokens': 43, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_eaab8d114b_prod0820_fp8_kvcache', 'id': '5274fa4a-a59c-45b4-9783-98ed638288c3', 'finish_reason': 'stop', 'logprobs': None} 
#     id='lc_run--65cb193d-a2dc-4a82-a3b4-76f184c3d7ba-0' 
#     usage_metadata={'input_tokens': 39, 'output_tokens': 4, 'total_tokens': 43, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}

