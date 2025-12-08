"""
删除消息。
"""

from langchain.agents.middleware import after_model
from langchain.agents import create_agent, AgentState
from langgraph.runtime import Runtime
from langchain.messages import RemoveMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig

import dotenv
dotenv.load_dotenv()
@after_model
def delete_messages(state: AgentState, runtime: Runtime) -> dict | None:
    """删除旧消息以保持对话可管理。"""
    
    messages = state['messages']
    
    # for message in messages:
        # print(message.content)
    
    if len(messages) > 2:
        # 删除最早的两条消息
        return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}
    return None

agent = create_agent(
    model=ChatOpenAI(model="deepseek-chat", temperature=0),
    tools=[],
    system_prompt="请简洁明了。",
    middleware=[delete_messages],
    checkpointer=InMemorySaver(),
)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

for event in agent.stream({"messages": [{"role": "user","content": "你好！我是bob。"}]},
    config,
    stream_mode="values",
):
   print([(message.type, message.content) for message in event["messages"]]) 

for event in agent.stream({"messages": [{"role": "user","content": "你的名字是什么？"}]},
    config,
    stream_mode="values",
):
   print([(message.type, message.content) for message in event["messages"]]) 

## 运行结果看：最后的消息列表中，删除了最早的2条消息，只剩下最新的2条消息。
# [('human', '你好！我是bob。')]
# [('human', '你好！我是bob。'), ('ai', '你好Bob！很高兴认识你！😊 有什么我可以帮助你的吗？')]
# [('human', '你好！我是bob。'), ('ai', '你好Bob！很高兴认识你！😊 有什么我可以帮助你的吗？'), ('human', '你的名字是什么？')]
# [('human', '你好！我是bob。'), ('ai', '你好Bob！很高兴认识你！😊 有什么我可以帮助你的吗？'), ('human', '你的名字是什么？'), ('ai', '我是DeepSeek，由深度求索公司创造的AI助手！很高兴为你 提供帮助。有什么问题或者想聊的话题吗？😊')]
# [('human', '你的名字是什么？'), ('ai', '我是DeepSeek，由深度求索公司创造的AI助手！很高兴为你提供帮助。有什么问题或者想聊的话题吗？😊')]
