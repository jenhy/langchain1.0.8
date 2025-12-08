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

# @tool
# def get_weather(city: str) -> str:
#     """根据给定的城市名称，返回该城市的天气信息。
    
#     Args:
# 	    query:输入查询信息。
#     """
#     return f"{city}的天气是晴天，温度是25度。"

# agent = create_agent(
#     model=ChatOpenAI(model="deepseek-chat", temperature=0),
#     tools=[get_weather],
#     system_prompt="""
#     你是一个专业的天气查询助手，你需要根据用户输入的城市名称，返回该城市的天气信息。"""
# )

# results = agent.invoke(
#     {"messages":[
#         {"role": "user", "content": "杭州"}
#     ]}
# )

# messages = results["messages"]

# for message in messages:
#     message.pretty_print()
    
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


## 自定义工具名称
# @tool("web_search")
# def search(query: str) -> str:
#     """
#     查询网络信息。
#     Args:
#         query: 输入查询信息。
#     """
    
#     return f"搜索结果：{query}"
    
# print(search.name)

# web_search

## 自定义工具描述
# @tool("calculator", description="执行算术计算。用于任何数学问题。")
# def calc(expression: str) -> str:
#     """
#     评估数学表达式。
#     """
    
#     return str(eval(expression))
    
# print(calc.description)

# 执行算术计算。用于任何数学问题。

## 使用pydantic定义高级模式
# Pydantic 作用体现： 由于 units 和 include_forecast 在 WeatherInput 中都有设置了默认值 (default="celsius", default=False)，因此模型不需要主动提供这些参数，它们会使用默认值进行调用。这证明了高级模式定义中的默认值生效。
# from pydantic import BaseModel, Field
# from typing import Literal

# class WeatherInput(BaseModel):
#     """输入天气查询。"""
#     location: str = Field(description="城市名称或坐标")
#     units: Literal["celsius", "fahrenheit"] = Field(
#         default="celsius",
#         description="温度单位偏好"
#     )
#     include_forecast: bool = Field(
#         default=False,
#         description="包含五天预报"
#     )

# @tool(args_schema=WeatherInput)
# def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
#     """获取当前天气和可选的预报。"""
#     temp = 22 if units == "celsius" else 72
#     result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
#     if include_forecast:
#         result += "\nNext 5 days: Sunny"
#     return result

# agent = create_agent(
#     model=ChatOpenAI(model="deepseek-chat", temperature=0),
#     tools=[get_weather],
#     system_prompt="""
#     你是一个专业的天气查询助手，你需要根据用户输入的城市名称，温度单位偏好，是否包含预报，返回该城市的天气信息。"""
# )

# results = agent.invoke(
#     {"messages":[
#         {"role": "user", "content": "杭州"}
#     ]}
# )

# messages = results["messages"]

# for message in messages:
#     message.pretty_print()
   
# ================================ Human Message =================================

# 杭州
# ================================== Ai Message ==================================
# Tool Calls:
#   get_weather (call_ozvm7f7wxor9so8r7sskphv5)
#  Call ID: call_ozvm7f7wxor9so8r7sskphv5
#   Args:
#     location: 杭州
# ================================= Tool Message =================================
# Name: get_weather

# Current weather in 杭州: 22 degrees C
# ================================== Ai Message ==================================

# 杭州当前的天气是22摄氏度。 


## 使用JSON模式定义高级模式
weather_schema = {
    "type": "object",
    "properties": {
        "location": {"type": "string"},
        "units": {"type": "string"},
        "include_forecast": {"type": "boolean"}
    },
    "required": ["location", "units", "include_forecast"]
}

@tool(args_schema=weather_schema)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """获取当前天气和可选的预报。"""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days: Sunny"
    return result

agent = create_agent(
    model=ChatOpenAI(model="deepseek-chat", temperature=0),
    tools=[get_weather],
    system_prompt="""
    你是一个专业的天气查询助手，你需要根据用户输入的城市名称，温度单位偏好，是否包含预报，返回该城市的天气信息。"""
)

results = agent.invoke(
    {"messages":[
        {"role": "user", "content": "杭州，华氏度，需要天气预报"}
    ]}
)

messages = results["messages"]

for message in messages:
    message.pretty_print()

# ================================ Human Message =================================

# 杭州，华氏度，需要天气预报
# ================================== Ai Message ==================================

# 我来为您查询杭州的天气信息，使用华氏度单位并包含天气预报。
# Tool Calls:
#   get_weather (call_kd582v4ybnuav2ryvfmdbf22)
#  Call ID: call_kd582v4ybnuav2ryvfmdbf22
#   Args:
#     location: 杭州
#     units: 华氏度
#     include_forecast: True
# ================================= Tool Message =================================
# Name: get_weather

# Current weather in 杭州: 72 degrees 华
# Next 5 days: Sunny
# ================================== Ai Message ==================================

# 杭州当前的天气为72华氏度，未来5天的天气预报为晴天。