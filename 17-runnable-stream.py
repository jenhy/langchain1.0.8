"""
任务：
Streaming流式输出：搜索人工智能新闻并总结发现。使用agent，并使用streaming流式输出。
"""

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI(model="deepseek-chat", temperature=0.5)

agent = create_agent(
    model=model,
)

for trunks in agent.stream(
    {"messages": [{"role": "user", "content": "搜索人工智能新闻并总结发现。"}]},
    stream_mode="values"):
    # 每个块包含该点的完整状态
    for trunk in trunks["messages"]:
        if trunk.content:
            print(f"Agent:{trunk.content}")
        elif trunk.tool_calls:
            print(f"Tool:{[tc['name'] for tc in trunk.tool_calls]}")

# Agent:搜索人工智能新闻并总结发现。
# Agent:搜索人工智能新闻并总结发现。
# Agent:我理解您想了解最新的人工智能新闻动态，但作为一个AI模型，我无法实时搜索互联网获取最新信息。不过我可以根据我的训练数据（截至2024年7月）为您总结当前AI领域的主要发展趋势和重要发现：

# ## 🔥 当前AI热点领域

# **大语言模型竞争白热化**
# - GPT-4、Claude 3、Gemini等模型持续迭代
# - 开源模型如Llama、Mistral等快速发展
# - 多模态能力成为标配

# **AI应用场景拓展**
# - 代码生成工具(GitHub Copilot等)普及
# - 创意内容生成(AI绘画、视频、音乐)
# - 科学研究辅助(蛋白质结构预测、药物发现)

# ## 📈 技术突破方向

# **推理能力提升**
# - 思维链(Chain-of-Thought)技术成熟
# - 复杂问题解决能力显著增强

# **多模态融合**
# - 文本、图像、音频统一处理
# - 跨模态理解和生成能力突破

# ## 💡 建议获取最新资讯的方式

# 1. **专业媒体**：机器之心、AI科技评论等
# 2. **学术平台**：arXiv、Papers with Code
# 3. **行业报告**：OpenAI、Google AI等官方博客
# 4. **科技新闻**：TechCrunch、The Verge等

# 如果您有特定方向的AI新闻需求，我很乐意基于我的知识为您提供更详细的介绍！您对哪个细分领域最感兴趣呢？
