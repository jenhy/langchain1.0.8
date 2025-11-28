"""
结构化输出两种策略。工具策略ToolStrategy和提供者策略ProviderStrategy。

"""

from pydantic import BaseModel  
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy, ProviderStrategy
from langchain_openai import ChatOpenAI
from langchain.tools import tool

import dotenv
dotenv.load_dotenv()

class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str
    
@tool
def search_tool(query: str) -> str:
    """查询信息"""
    return f"搜索结果：{query}"

## 使用工具策略    
agent = create_agent(
    model=ChatOpenAI(model="deepseek-chat", temperature=0),
    tools=[search_tool],
    response_format=ToolStrategy(ContactInfo),
)

result = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "从：John Doe，john@example.com，(555) 123-4567中提取联系信息"}
        ]
    }
)

print(f"len:{len(result)}") # 2

messages = result["messages"]
for message in messages:
    message.pretty_print()
    
structured_response = result["structured_response"]
print(f"structured_response:{structured_response}")

# len:2
# ================================ Human Message =================================

# 从：John Doe，john@example.com，(555) 123-4567中提取联系信息
# ================================== Ai Message ==================================
# Tool Calls:
#   ContactInfo (call_2mwkf2jzaiysk2zey5xeahxk)
#  Call ID: call_2mwkf2jzaiysk2zey5xeahxk
#   Args:
#     name: John Doe
#     email: john@example.com
#     phone: (555) 123-4567
# ================================= Tool Message =================================
# Name: ContactInfo

# Returning structured response: name='John Doe' email='john@example.com' phone='(555) 123-4567'
# structured_response:name='John Doe' email='john@example.com' phone='(555) 123-4567'

## 使用提供者策略
agent = create_agent(
    model=ChatOpenAI(model="deepseek-chat", temperature=0),
    tools=[search_tool],
    response_format=ProviderStrategy(ContactInfo),
)

result = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "从：John Doe，john@example.com，(555) 123-4567中提取联系信息"}
        ]
    }
)

print(f"len:{len(result)}") # 2

messages = result["messages"]
for message in messages:
    message.pretty_print()
    
structured_response = result["structured_response"]
print(f"structured_response:{structured_response}")

# len:2
# ================================ Human Message =================================

# 从：John Doe，john@example.com，(555) 123-4567中提取联系信息
# ================================== Ai Message ==================================

# {"name": "John Doe", "email": "john@example.com", "phone": "(555) 123-4567"}
# structured_response:name='John Doe' email='john@example.com' phone='(555) 123-4567'