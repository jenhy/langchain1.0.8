"""
使用agent创建工具，工具中通过 ToolRuntime 访问运行时上下文。
"""

from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_openai import ChatOpenAI

import dotenv
dotenv.load_dotenv()


USER_DATABASE = {
    "user123": {
        "name": "张三",
        "account_type": "普通用户",
        "balance": 1000.0,
        "email": "zhangsan@example.com"
    },
    "user456": {
        "name": "李四",
        "account_type": "普通用户",
        "balance": 500.0,
        "email": "lisi@example.com"
    }
}

@dataclass
class UserContext:
    user_id: str
    
@tool
def get_account_info(runtime: ToolRuntime[UserContext]) -> str:
    """获取当前用户的账户信息。"""
    user_id = runtime.context.user_id
    if user_id in USER_DATABASE:
        user = USER_DATABASE[user_id]
        return f"账户持有人：{user['name']}\n账户类型：{user['account_type']}\n账户余额：{user['balance']}\n邮箱地址：{user['email']}"
    return f"用户 {user_id} 不存在"

agent = create_agent(
    model=ChatOpenAI(model="deepseek-chat"),
    tools=[get_account_info],
    context_schema=UserContext,
    system_prompt="你是财务助理。"
)

response = agent.invoke(
    {
        "messages": [{
            "role": "user",
            "content": "我目前的余额是多少？"
        }]
    },
    context=UserContext(user_id="user123")
)

messages = response["messages"]

for message in messages:
    message.pretty_print()
    
# ================================ Human Message =================================

# 我目前的余额是多少？
# ================================== Ai Message ==================================

# 我来帮您查询当前的账户余额信息。
# Tool Calls:
#   get_account_info (call_cb94rsf791izfdkriv0g3k9o)
#  Call ID: call_cb94rsf791izfdkriv0g3k9o
#   Args:
# ================================= Tool Message =================================
# Name: get_account_info

# 账户持有人：张三
# 账户类型：普通用户
# 账户余额：1000.0
# 邮箱地址：zhangsan@example.com
# ================================== Ai Message ==================================

# 根据查询结果，您目前的账户余额是 **1000.0 元**。

# 账户信息摘要：
# - 账户持有人：张三
# - 账户类型：普通用户
# - 当前余额：1000.0元
# - 邮箱地址：zhangsan@example.com

# 如果您需要查看更详细的交易记录或有其他财务问题，请随时告诉我！




# ================================ Human Message =================================

# 我目前的余额是多少？
# ================================== Ai Message ==================================

# 我来帮您查询账户余额信息。
# Tool Calls:
#   get_account_info (call_bg5l0p4k2ar3nsace17meo2a)
#  Call ID: call_bg5l0p4k2ar3nsace17meo2a
#   Args:
# ================================= Tool Message =================================
# Name: get_account_info

# 用户 user1234 不存在
# ================================== Ai Message ==================================

# 很抱歉，查询时遇到了问题。系统提示用户账户不存在，这可能是因为：

# 1. 您的账户信息可能尚未在系统中注册
# 2. 当前查询工具暂时无法访问您的账户数据

# 建议您：
# - 联系系统管理员确认账户状态
# - 通过其他渠道（如银行APP、网上银行）查看余额
# - 稍后再尝试查询

# 如果您需要其他财务相关的帮助，我很乐意为您提供支持。