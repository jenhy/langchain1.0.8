from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import wrap_model_call, ModelRequest,ModelResponse

import dotenv
dotenv.load_dotenv()

basic_model = ChatOpenAI(model="deepseek-chat")
advanced_model = ChatOpenAI(model="gpt-4o-mini")

@tool
def get_weather(city: str) -> str:
    """根据给定的城市名称，返回该城市的天气信息。"""
    return f"{city}的天气是晴天，温度是25度。"

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """请根据对话的复杂程度选择模型。"""
    message_count = len(request.state["messages"])
    print(f"当前对话长度为{message_count}条消息。")

    if message_count > 10:
        # 请使用高级模型进行更长的对话
        model = advanced_model
        print(f"使用高级模型{model.model_name}进行对话。")
    else:
        model = basic_model
        print(f"使用基础模型{model.model_name}进行对话。")
    return handler(request.override(model=model))

agents = create_agent(
    model=basic_model,
    tools=[get_weather],
    middleware=[dynamic_model_selection]
)

results = agents.invoke(
    {"messages":[
        {"role": "user", "content": "今天杭州的天气如何？"},
    ]}
)

messages = results["messages"]

for message in messages:
    message.pretty_print()
