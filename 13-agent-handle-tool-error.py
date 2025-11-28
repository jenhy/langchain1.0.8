"""
工具的错误处理。使用@wrap_tool_call装饰器。
"""

from langchain.tools import tool

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage, HumanMessage
from langchain_openai import ChatOpenAI

import dotenv
dotenv.load_dotenv()

@tool
def search(query: str) -> str:
    """查询信息"""
    if "错误" in query:
        # 主动抛出异常来触发错误处理
        raise ValueError(f"查询内容包含禁用词: '{query}'")
    return f"搜索结果：{query}"

@tool
def get_weather(city: str) -> str:
    """根据给定的城市名称，返回该城市的天气信息。"""
    if city == "火星":
        # 主动抛出异常来触发错误处理
        raise RuntimeError("无法获取火星的天气信息。")
    return f"{city}的天气是晴天，温度是25度。"

@wrap_tool_call
def handle_tool_error(request, handler):
    """使用自定义消息处理工具执行错误。"""
    
    try:
        return handler(request)
    except Exception as e:
        """返回自定义错误消息给模型。"""
        return ToolMessage(content=f"工具错误：请检查你的输入并再次重试。({str(e)})", tool_call_id=request.tool_call["id"])

agent = create_agent(
    model=ChatOpenAI(model="deepseek-chat",temperature=0.5),
    tools=[search, get_weather],
    middleware=[handle_tool_error]
)

results = agent.invoke({
    "messages":[
        HumanMessage(content="请查询北京的天气。然后查询“错误”这个词。")
    ]
})

messages = results["messages"]
for message in messages:
    message.pretty_print()
    
# 执行结果：
# ================================ Human Message =================================

# 请查询北京的天气。然后查询“错误”这个词。
# ================================== Ai Message ==================================
# Tool Calls:
#   get_weather (call_jnb0ac0e9eph7jg4enokyt6b)
#  Call ID: call_jnb0ac0e9eph7jg4enokyt6b
#   Args:
#     city: 北京
#   search (call_kcfixiyk5u4l86rn8oswbr7a)
#  Call ID: call_kcfixiyk5u4l86rn8oswbr7a
#   Args:
#     query: 错误
# ================================= Tool Message =================================
# Name: get_weather

# 北京的天气是晴天，温度是25度。
# ================================= Tool Message =================================

# 工具错误：请检查你的输入并再次重试。(查询内容包含禁用词: '错误')
# ================================== Ai Message ==================================

# 北京的天气是晴天，温度是25度。

# 关于“错误”这个词的查询未能成功，系统提示查询内容包含禁用词。如果您有其他问题或需要帮助，请告诉我！