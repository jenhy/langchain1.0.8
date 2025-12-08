"""
人类消息。
"""

from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage

import dotenv
dotenv.load_dotenv()

model = init_chat_model(
    model="openai:deepseek-chat"
)


response = model.invoke([
    HumanMessage("什么是机器学习？")
])

# print(response.content)

# 消息元数据
human_msg = HumanMessage(
    content="你好！",
    name="Alice",
    id="msg_123"
)

response = model.invoke([human_msg])

print(response.content)