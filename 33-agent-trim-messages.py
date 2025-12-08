"""
截断消息。可以使用 trim messages 工具，并指定要保留的 tokens 数量，以及用于处理边界的 strategy。
"""


from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import before_model
from langgraph.runtime import Runtime
from typing import Any
from langchain.tools import tool
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig

import dotenv
dotenv.load_dotenv()

@tool
def search(query: str) -> str:
    """这是一个模拟的搜索工具，当用户询问需要联网的信息时使用。"""
    return f"这是关于{query}的模拟搜索结果。"

@before_model
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """仅保留最后几条消息以适应上下文窗口。"""
    
    # print(f"state: {state}")
    messages = state["messages"]
    
    
    if len(messages) <= 3:
        return None
    
    first_msg = messages[0]
    
    # 如果消息总数是偶数，保留最后 3 条；否则保留最后 4 条
    recent_msg = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    new_msg = [first_msg] + recent_msg
    
    # 这个语句的作用是删除所有消息，并添加新的消息。*new_msg是解包的语法。
    # 如：new_msg = ["消息A", "消息B", "消息C"] delete_cmd = "删除指令"
    # 结果为：{"messages": [delete_cmd, "消息A", "消息B", "消息C"]}
    return {
        "messages":[
            RemoveMessage(id=REMOVE_ALL_MESSAGES),
            *new_msg
        ]
    }
    
agent = create_agent(
    model=ChatOpenAI(model="deepseek-chat", temperature=0),
    tools=[search],
    middleware=[trim_messages],
    checkpointer=InMemorySaver(),
)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

agent.invoke({"messages": "你好，我的名字是bob。"}, config)
agent.invoke({"messages": "写一首关于猫的短诗"}, config)
agent.invoke({"messages": "现在也对狗做同样的操作。"}, config)
final_response = agent.invoke({"messages": "我叫什么名字？"}, config)
final_response["messages"][-1].pretty_print()

# ================================== Ai Message ==================================

# 根据我们的对话记录，你之前提到过你的名字是**bob**。

"""分析结果
因为显式地写了 new_msg = [first_msg] + recent_msg，所以系统提示（或者第一轮对话）被强行保留了下来。这就是为什么即使中间聊了猫和狗，AI 依然知道它（或者你）叫 Bob。这是非常棒的 Memory 管理策略（保留首尾）！
"""

## 打印一下AgentState的结果看看是什么
# state: {
#     'messages': [HumanMessage(content='你好，我的名字是bob。', additional_kwargs={}, response_metadata={}, id='243130a2-51d6-419a-87e5-19ac000327b6')]}
# state: {
#     'messages': [HumanMessage(content='你好，我的名字是bob。', additional_kwargs={}, response_metadata={}, id='243130a2-51d6-419a-87e5-19ac000327b6'), AIMessage(content='你好！我是DeepSeek，不过你可以叫我Bob！😊 \n\n很高兴认识你！我是一个AI助手，由深度求索公司创造。我可以帮你解答问题、协助写作、进行对话交流等等。\n\n有什么我可以帮助你的吗？', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 49, 'prompt_tokens': 163, 'total_tokens': 212, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': None, 'id': '0217651978616016cacdbb323ed1672e3f8caec678da1112201fb', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--6b160aa7-3fec-410d-a4d6-1eda559c988f-0', usage_metadata={'input_tokens': 163, 'output_tokens': 49, 'total_tokens': 212, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}), HumanMessage(content='写一首关于猫的短诗', additional_kwargs={}, response_metadata={}, id='7f74389e-bb8e-4ae0-8b6f-1d495c011294')]}
# state: {
#     'messages': [HumanMessage(content='你好，我的名字是bob。', additional_kwargs={}, response_metadata={}, id='243130a2-51d6-419a-87e5-19ac000327b6'), AIMessage(content='你好！我是DeepSeek，不过你可以叫我Bob！😊 \n\n很高兴认识你！我是一个AI助手，由深度求索公司创造。我可以帮你解答问题、协助写作、进行对话交流等等。\n\n有什么我可以帮助你的吗？', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 49, 'prompt_tokens': 163, 'total_tokens': 212, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': None, 'id': '0217651978616016cacdbb323ed1672e3f8caec678da1112201fb', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--6b160aa7-3fec-410d-a4d6-1eda559c988f-0', usage_metadata={'input_tokens': 163, 'output_tokens': 49, 'total_tokens': 212, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}), HumanMessage(content='写一首关于猫的短诗', additional_kwargs={}, response_metadata={}, id='7f74389e-bb8e-4ae0-8b6f-1d495c011294'), AIMessage(content='《猫的慵懒时光》\n\n阳光斜照窗台暖，\n绒球蜷缩梦正酣。\n胡须轻颤捕风影，\n尾巴微摇画弧圈。\n\n忽见飞蛾扑纱窗，\n瞳仁骤缩如闪电。\n一跃而起似猎豹，\n落地依旧优雅仙。\n\n午后时光慢流淌，\n猫儿世界无烦忧。\n你若问它何所思，\n唯有鱼干与自由。\n\n这首诗描绘了猫咪慵懒又敏捷的特质，从晒太阳到捕猎的本能，最后点出它们简单快乐的世界。 希望你喜欢！🐱', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 120, 'prompt_tokens': 383, 'total_tokens': 503, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': None}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': None, 'id': '3fe1c0f061e1f9b6827561484b9be14d', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--90c4fb4b-7b9c-4189-8945-c2338fc3993e-0', usage_metadata={'input_tokens': 383, 'output_tokens': 120, 'total_tokens': 503, 'input_token_details': {}, 'output_token_details': {}}), HumanMessage(content='现在也对狗做同样的操作。', additional_kwargs={}, response_metadata={}, id='6f76306f-0d39-47af-959d-7abf1e4955fb')]}
# state: {
#     'messages': [HumanMessage(content='你好，我的名字是bob。', additional_kwargs={}, response_metadata={}, id='243130a2-51d6-419a-87e5-19ac000327b6'), AIMessage(content='你好！我是DeepSeek，不过你可以叫我Bob！😊 \n\n很高兴认识你！我是一个AI助手，由深度求索公司创造。我可以帮你解答问题、协助写作、进行对话交流等等。\n\n有什么我可以帮助你的吗？', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 49, 'prompt_tokens': 163, 'total_tokens': 212, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': None, 'id': '0217651978616016cacdbb323ed1672e3f8caec678da1112201fb', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--6b160aa7-3fec-410d-a4d6-1eda559c988f-0', usage_metadata={'input_tokens': 163, 'output_tokens': 49, 'total_tokens': 212, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}), HumanMessage(content='写一首关于猫的短诗', additional_kwargs={}, response_metadata={}, id='7f74389e-bb8e-4ae0-8b6f-1d495c011294'), AIMessage(content='《猫的慵懒时光》\n\n阳光斜照窗台暖，\n绒球蜷缩梦正酣。\n胡须轻颤捕风影，\n尾巴微摇画弧圈。\n\n忽见飞蛾扑纱窗，\n瞳仁骤缩如闪电。\n一跃而起似猎豹，\n落地依旧优雅仙。\n\n午后时光慢流淌，\n猫儿世界无烦忧。\n你若问它何所思，\n唯有鱼干与自由。\n\n这首诗描绘了猫咪慵懒又敏捷的特质，从晒太阳到捕猎的本能，最后点出它们简单快乐的世界。 希望你喜欢！🐱', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 120, 'prompt_tokens': 383, 'total_tokens': 503, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': None, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': None}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': None, 'id': '3fe1c0f061e1f9b6827561484b9be14d', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--90c4fb4b-7b9c-4189-8945-c2338fc3993e-0', usage_metadata={'input_tokens': 383, 'output_tokens': 120, 'total_tokens': 503, 'input_token_details': {}, 'output_token_details': {}}), HumanMessage(content='现在也对狗做同样的操作。', additional_kwargs={}, response_metadata={}, id='6f76306f-0d39-47af-959d-7abf1e4955fb'), AIMessage(content='《狗的欢腾岁月》\n\n晨光洒落庭院中，  \n尾巴摇成小旋风。  \n耳朵竖起听门响，  \n爪印满地写匆匆。  \n\n球飞远处如流星，  \n狂奔追逐似闪电。  \n叼回战利品炫耀，  \n湿漉漉的眼亮晶晶。  \n\n夕阳西下炊烟起，  \n趴卧门前等主人。  \n你若问它何所求，  \n唯有抚摸与忠诚。  \n\n这首诗捕捉了狗狗的热情与活力，从玩耍到等待主人的温情，最 后点出它们简单纯粹的快乐和忠诚。希望你也喜欢！🐶', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 123, 'prompt_tokens': 303, 'total_tokens': 426, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'input_tokens': 0, 'output_tokens': 0, 'input_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-chat', 'system_fingerprint': None, 'id': '021765197875333b840dd7b9652efdc537cb0c7fa5f038f5701b6', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--6f144505-e708-4d57-b8a8-4dd656b78be7-0', usage_metadata={'input_tokens': 303, 'output_tokens': 123, 'total_tokens': 426, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}), HumanMessage(content='我叫什么名 字？', additional_kwargs={}, response_metadata={}, id='fc7f72f5-679e-42c4-a597-b8507a4da213')]}