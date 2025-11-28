"""
自定义状态来维护历史对话。
通过中间件自定义状态。
通过state_schema自定义状态。
"""

from pydantic import BaseModel  
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import AgentMiddleware
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from typing import Any

import dotenv
dotenv.load_dotenv()

"""
工具1和工具2必须提供docstring，否则会报错：ValueError: Function must have a docstring if description not provided.
"""
@tool
def tool1(query: str) -> str:
    """工具1"""
    return f"Tool 1: {query}"

@tool
def tool2(query: str) -> str:
    """工具2"""
    return f"Tool 2: {query}"


class CustomState(AgentState):
    user_preferences: dict  # 添加自定义状态
    
class CustomMiddleware(AgentMiddleware):
    state_schema = CustomState
    tools = [tool1, tool2]
    
    def before_model(self, state, runtime) -> dict[str, Any] | None:
        user_prefs = state['user_preferences']
        
        system_instructions = (
            f"用户的偏好是：风格为'{user_prefs['style']}',"
            f"详细程度为'{user_prefs['verbosity']}'。"
            f"请严格按照这些偏好来回答用户的问题。"
        )
        
        system_message = {"role": "system", "content": system_instructions}
        
        current_message = state['messages']
        
        # print(f"system_message: {system_message}\n")
        # print(f"current_message: {current_message}\n")
        # system_message: {'role': 'system', 'content': "用户的偏好是：风格为'技术性解释',详细程度为'详细'。请严格按照这些偏好来回答用户的问题。"}

        # current_message: [HumanMessage(content='我更喜欢技术性解释', additional_kwargs={}, response_metadata={}, id='9277e804-18e1-4e22-8279-0791a1718c9d')]
        
        new_messages = [system_message] + current_message
        
        return {"messages": new_messages}
        
## 通过中间件自定义状态。
# 该中间件不仅需要存储和验证数据，并且自定义逻辑会动态改变智能体Agent来影响LLM的行为。
# 以下结果改变输出内容。
agent = create_agent(
    model=ChatOpenAI(model="deepseek-chat", temperature=0),
    tools=[tool1, tool2],
    middleware=[CustomMiddleware()]
)

# 该代理现在可以跟踪消息之外的其他状态
result = agent.invoke(
    {
        "messages":[
            {"role": "user", "content": "我更喜欢技术性解释"}
        ],
        "user_preferences": {"style": "技术性解释", "verbosity": "详细"}
    }
)

print(f"len:\n{len(result)}")

messages = result["messages"]
for message in messages:
    message.pretty_print()
    
# 自定义状态
print(f"user_preferences:\n{result['user_preferences']}")

# len:
# 2
# ================================ Human Message =================================

# 我更喜欢技术性解释
# ================================ System Message ================================

# 用户的偏好是：风格为'技术性解释',详细程度为'详细'。请严格按照这些偏好来回答用户的问题。
# ================================== Ai Message ==================================

# 我理解您偏好技术性解释。根据我的设置，我已经将回答风格调整为技术性解释，并会提供详细的技术说明。

# 不过，目前我无法直接处理您可能想要询问的具体技术问题。我的工具功能暂时受限，无法进行深入的技术分析或数据查询。

# 如果您有特定的技术问题需要解答，建议您：
# - 直接描述您遇到的技术问题或需要解释的概念
# - 提供相关的技术背景信息
# - 我会基于现有的知识库为您提供详细的技术性解释

# 请告诉我您想要了解什么具体的技术内容，我会尽力为您提供专业、详细的技术解释。
# user_preferences:
# {'style': '技术性解释', 'verbosity': '详细'}




## 通过state_schema自定义状态。
# 该参数只是需要存储和验证数据的时候使用，本身并不会改变智能体Agent来影响LLM的行为。
# 以下输出结果并没有改变输出的内容。
agent = create_agent(
    model=ChatOpenAI(model="deepseek-chat", temperature=0),
    tools=[tool1, tool2],
    state_schema=CustomState,
)

# 该代理现在可以跟踪消息之外的其他状态
result = agent.invoke(
    {
        "messages":[
            {"role": "user", "content": "我更喜欢技术性解释"}
        ],
        "user_preferences": {"style": "技术性解释", "verbosity": "详细"}
    }
)

print(f"len:\n{len(result)}")

messages = result["messages"]
for message in messages:
    message.pretty_print()
    
# 自定义状态
print(f"user_preferences:\n{result['user_preferences']}")

# len:
# 2
# ================================ Human Message =================================

# 我更喜欢技术性解释
# ================================== Ai Message ==================================

# 我理解您更倾向于技术性的解释。不过，我需要先了解一下您具体想了解什么技术内容，这样我才能为您提供准确、深入的技术性解释。

# 请问您是想了解：
# - 某个特定的技术概念或原理？
# - 某种编程语言或框架的技术细节？
# - 某个技术问题的解决方案？
# - 还是其他特定的技术主题？

# 请告诉我您具体感兴趣的技术领域或问题，我会尽力为您提供专业、详细的技术性解释。
# user_preferences:
# {'style': '技术性解释', 'verbosity': '详细'}