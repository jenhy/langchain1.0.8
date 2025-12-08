"""智能体中总结消息中间件的应用SummarizationMiddleware。"""

from langchain.agents.middleware import SummarizationMiddleware
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI

import dotenv
dotenv.load_dotenv()

agent = create_agent(
    model=ChatOpenAI(model="gpt-4o-mini", temperature=1.0),
    middleware=[
        SummarizationMiddleware(
            model=ChatOpenAI(model="gpt-4o-mini", temperature=0.5),
            trigger=("tokens", 1000),
            keep=("messages", 20)
        )
    ],
    checkpointer=InMemorySaver(),
)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

agent.invoke({"messages": "你好，我的名字是bob。"}, config)
agent.invoke({"messages": "写一首关于猫的短诗。"}, config)
agent.invoke({"messages": "现在也对狗做同样的操作。"}, config)
final_response = agent.invoke({"messages": "我叫什么名字？"}, config)

final_response["messages"][-1].pretty_print()

# ================================== Ai Message ==================================

# 你叫Bob。
