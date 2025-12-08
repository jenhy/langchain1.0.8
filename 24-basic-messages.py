"""
messages的基本使用。
"""

from langchain.messages import HumanMessage, AIMessage, SystemMessage
from langchain.chat_models import init_chat_model

import dotenv
dotenv.load_dotenv()

model = init_chat_model(model="openai:deepseek-chat")

response = model.invoke("Write a haiku about spring")

system_msg = SystemMessage(content="请将中文翻译成日文。")
human_msg = HumanMessage(content="我爱中国。")

messages = [system_msg, human_msg]

response = model.invoke(messages)


# print(response)

# content='私は中国が大好きです。' 
# additional_kwargs={'refusal': None} 
# response_metadata={'token_usage': {'completion_tokens': 7, 'prompt_tokens': 15, 'total_tokens': 22, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_eaab8d114b_prod0820_fp8_kvcache', 'id': '794233ac-e94d-46d5-b76d-aceb3153c9e7', 'finish_reason': 'stop', 'logprobs': None} 
# id='lc_run--dccccb21-a52e-479c-a354-75924e6d4031-0' 
# usage_metadata={'input_tokens': 15, 'output_tokens': 7, 'total_tokens': 22, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}

messages = [
    {"role": "system", "content": "您是一位诗歌专家"},
    {"role": "user", "content": "写一首关于春天的俳句。"},
    {"role": "assistant", "content": "樱花绽放..."}
]

response = model.invoke(messages)

print(response.content)

# 《春》
# 新芽破冻土，
# 一羽斜阳暖旧苔，
# 风过古池开。

# 注：我的俳句严格遵循五七五音节结构，通过“新芽破冻土”展现生命张力，“斜阳暖旧苔”暗含时光流转，末句化用松尾芭蕉“古池”典故，以风拂池开的动态画面收束，在古典意象中注入现代生命感知，完 成对春之觉醒的瞬间定格。
