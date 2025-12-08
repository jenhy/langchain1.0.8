"""
使用agent创建工具，工具中通过 ToolRuntime 流写入器，从工具执行时流式传输。
"""

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_openai import ChatOpenAI

import dotenv
dotenv.load_dotenv()

@tool
def get_weather(city: str, runtime: ToolRuntime) -> str:
    """获取指定城市的天气。"""
    
    writer = runtime.stream_writer
    
    # 在工具执行时流式传输自定义更新
    writer(f"正在查找城市数据:{city}")
    writer(f"获取城市数据：{city}")
    
    return f"{city}的天气是晴天，温度是25度。"

agent = create_agent(
    model=ChatOpenAI(model="deepseek-chat", temperature=0),
    tools=[get_weather],
)

for chunk in agent.stream(
    {
        "messages": [
            {"role": "user", "content": "帮我查一下杭州的天气。"}
        ]
    },
    stream_mode="custom",
):
    print(chunk)
    
# 正在查找城市数据:杭州
# 获取城市数据：杭州

# custom 流模式 只会输出工具内部通过 runtime.stream_writer() 主动推送的内容，而不会自动输出：

# 模型的正常回答

# 工具的最终 return 值

# Agent 的最终输出
    
