"""
模型对数概率。
"""

from langchain.chat_models import init_chat_model

import dotenv
dotenv.load_dotenv()


model = init_chat_model(
    model="openai:deepseek-chat",
    temperature=0.5,
).bind(logprobs=True)

response = model.invoke("为什么鹦鹉会说话？")
print(response)

# content='鹦鹉之所以能够“说话”......' 
# additional_kwargs={'refusal': None} 
# response_metadata={'token_usage': {'completion_tokens': 648, 'prompt_tokens': 9, 'total_tokens': 657, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': 'fp_eaab8d114b_prod0820_fp8_kvcache', 'id': '048a27d4-a75d-4170-9996-ba9c02078c6d', 'finish_reason': 'stop', 'logprobs': 
#     {'content': 
#         [
#             {'token': '鹦鹉', 'bytes': [233, 185, 166, 233, 185, 137], 'logprob': 0.0, 'top_logprobs': []}, 
#             {'token': '之所以', 'bytes': [228, 185, 139, 230, 137, 128, 228, 187, 165], 'logprob': -0.06748644, 'top_logprobs': []}, 
#             {'token': '能够', 'bytes': [232, 131, 189, 229, 164, 159], 'logprob': 0.0, 'top_logprobs': []}, {'token': '“', 'bytes': [226, 128, 156], 'logprob': 0.0, 'top_logprobs': []}, 
#             {'token': '说话', 'bytes': [232, 175, 180, 232, 175, 157], 'logprob': 0.0, 'top_logprobs': []}, {'token': '”，', 'bytes': [226, 128, 157, 239, 188, 140], 'logprob': 0.0, 'top_logprobs': []}, 
#         ], 
#     'refusal': None}}
# id='lc_run--3fd8b9d7-de94-4f0e-93ac-9eed887ee74a-0' 
# usage_metadata={'input_tokens': 9, 'output_tokens': 648, 'total_tokens': 657, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}