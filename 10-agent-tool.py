"""
使用tool来实现agent，模拟查询天气。
1. 创建一个天气查询工具
2. 创建一个agent。提示词、工具、大模型
3. 运行agent
"""

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

import dotenv
dotenv.load_dotenv()

@tool
def get_weather(city: str) -> str:
    """根据给定的城市名称，返回该城市的天气信息。"""
    return f"{city}的天气是晴天，温度是25度。"

agent = create_agent(
    model=ChatOpenAI(model="deepseek-chat", temperature=0),
    tools=[get_weather],
    system_prompt="""
    你是一个专业的天气查询助手，你需要根据用户输入的城市名称，返回该城市的天气信息。"""
)

results = agent.invoke(
    {"messages":[
        {"role": "user", "content": "杭州"}
    ]}
)

messages = results["messages"]

for message in messages:
    message.pretty_print()
    
# C:\Users\Jenhy\.conda\envs\langchain1.0.8\Lib\site-packages\pydantic\v1\main.py:1054: UserWarning: LangSmith now uses UUID v7 for run and trace identifiers. This warning appears when passing custom IDs. Please use: from langsmith import uuid7
#             id = uuid7()
# Future versions will require UUID v7.
#   input_data = validator(cls_, input_data)
# ================================ Human Message =================================

# 杭州
# ================================== Ai Message ==================================
# Tool Calls:
#   get_weather (call_orquj9wcgv85ploh1a3e1w5y)
#  Call ID: call_orquj9wcgv85ploh1a3e1w5y
#   Args:
#     city: 杭州
# ================================= Tool Message =================================
# Name: get_weather

# 杭州的天气是晴天，温度是25度。
# ================================== Ai Message ==================================

# 杭州今天的天气是晴天，温度25度。天气不错，适合外出活动！