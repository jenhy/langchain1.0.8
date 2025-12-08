"""
使用agent创建工具，工具中通过 ToolRuntime 访问和更新存储。
"""

from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_openai import ChatOpenAI
from langgraph.store.memory import InMemoryStore

import dotenv
dotenv.load_dotenv()

# 访问内存
@tool
def get_user_info(user_id: str, runtime: ToolRuntime) -> str:
    """查询用户信息。"""
    store = runtime.store
    user_info = store.get(("user_id",), user_id)
    return str(user_info.value) if user_info else "用户不存在"

# 更新内存
@tool
def save_user_info(user_id: str, user_info: dict[str, any], runtime: ToolRuntime) -> str:
    """保存用户信息。"""
    store = runtime.store
    store.put(("user_id",), user_id, user_info)
    return "成功保存用户信息"

store = InMemoryStore()

agent = create_agent(
    model=ChatOpenAI(model="deepseek-chat"),
    tools=[get_user_info, save_user_info],
    store=store,
)

# 第1次会话：保存用户信息
response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "保存以下用户：用户ID：abc123，姓名：Foo，年龄：25，电子邮件：foo@langchain.dev"}
        ]
    }
)
messages = response["messages"]

for message in messages:
    message.pretty_print()
    
# ================================ Human Message =================================

# 保存以下用户：用户ID：abc123，姓名：Foo，年龄：25，电子邮件：foo@langchain.dev
# ================================== Ai Message ==================================

# 我来帮您保存这个用户信息。根据您提供的信息，我将使用用户ID abc123来保存用户信息。
# Tool Calls:
#   save_user_info (call_qdk7ika6onpi96ey824m9nbg)
#  Call ID: call_qdk7ika6onpi96ey824m9nbg
#   Args:
#     user_id: abc123
#     user_info: {'姓名': 'Foo', '年龄': 25, '电子邮件': 'foo@langchain.dev'}
# ================================= Tool Message =================================
# Name: save_user_info

# 成功保存用户信息
# ================================== Ai Message ==================================

# 用户信息已成功保存！以下是保存的详细信息：

# - **用户ID**: abc123
# - **姓名**: Foo
# - **年龄**: 25
# - **电子邮件**: foo@langchain.dev

# 如果需要进一步操作或查询，请随时告诉我！
    

# 第2次会话：查询用户信息
response = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "请查询用户ID为abc123的用户信息"}
        ]
    }
)
messages = response["messages"]

for message in messages:
    message.pretty_print()
    
# ================================ Human Message =================================

# 请查询用户ID为abc123的用户信息
# ================================== Ai Message ==================================
# Tool Calls:
#   get_user_info (call_6h52huxre1ofuvu04owzj7cp)
#  Call ID: call_6h52huxre1ofuvu04owzj7cp
#   Args:
#     user_id: abc123
# ================================= Tool Message =================================
# Name: get_user_info

# {'姓名': 'Foo', '年龄': 25, '电子邮件': 'foo@langchain.dev'}
# ================================== Ai Message ==================================

# 用户ID为 `abc123` 的用户信息如下：

# - 姓名：Foo
# - 年龄：25
# - 电子邮件：foo@langchain.dev

