"""
AI消息。
"""

from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage, AIMessage

import dotenv
dotenv.load_dotenv()

model = init_chat_model(
    model="openai:deepseek-chat"
)

ai_msg = AIMessage("我很乐意帮助你解答那个问题！")

messages = [
    SystemMessage("你是一个有帮助的助手"),
    HumanMessage("你能帮助我吗？"),
    ai_msg,
    HumanMessage("1+2是什么？")
]

response = model.invoke(messages)

print(response.content)
