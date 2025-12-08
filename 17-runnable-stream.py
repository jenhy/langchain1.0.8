"""
任务：
Streaming流式输出：搜索人工智能新闻并总结发现。
使用agent，并使用streaming流式输出。
使用init_chat_model初始化模型，并使用streaming流式输出。
"""

# from langchain.agents import create_agent
# from langchain_openai import ChatOpenAI

# from dotenv import load_dotenv
# load_dotenv()

# model = ChatOpenAI(model="deepseek-chat", temperature=0.5)

# agent = create_agent(
#     model=model,
# )

# for trunks in agent.stream(
#     {"messages": [{"role": "user", "content": "搜索人工智能新闻并总结发现。"}]},
#     stream_mode="values"):
#     # 每个块包含该点的完整状态
#     for trunk in trunks["messages"]:
#         if trunk.content:
#             print(f"Agent:{trunk.content}")
#         elif trunk.tool_calls:
#             print(f"Tool:{[tc['name'] for tc in trunk.tool_calls]}")

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


from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage

import dotenv
dotenv.load_dotenv()

model = init_chat_model(
    model="openai:deepseek-chat",
    temperature=0.5,
    timeout=30,
    max_tokens=1000,
)

for chunk in model.stream("为什么鹦鹉有彩色的羽毛？"):
    print(chunk.text, end="|", flush=True)
    
# |鹦鹉|拥有|彩色|羽毛|的原因|是多|方面的|，|主要|涉及|**|进化|适应|、|生存|策略|和|生理|结构|**|。|以下是|详细的|科学|解释|：

# |---

# |###| **|1|.| |结构|色|与|色素|色的|结合|**
# |鹦鹉|羽毛|的颜色|并非|仅|靠|色素|，|而是|**|结构|色|与|色素|色的|共同|作用|**|：
# |-| **|色素|色|**|：|由|化学|色素|产生|，|如|**|黑色|素|**|（|黑|、|褐色|）|和|**|类|胡萝卜|素|**|（|红|、|黄|、|橙色|）。|鹦鹉|通过|食物|摄取|类|胡萝卜|素|，|并在|体内|转化|后|沉积|在|羽毛|中|。
# |-| **|结构|色|**|：|羽毛|的|微观|结构|（|如|羽毛|表面的|**|纳米|级|沟|槽|或|气泡|状|结构|**|）|能|反射|特定|波|长的|光|，|产生|**|虹|彩|效应|**|（|如|蓝色|、|绿色|、|金属|光泽|）。|例如|，|许多|鹦鹉|的|蓝色|和|绿色|羽毛|实际|缺乏|蓝色|色素|，|而是|通过|结构|反射|出|蓝|光|，|与|黄色|色素|叠加|后|呈现|绿色|。

# |---

# |###| **|2|.| |进化|与|生存|优势|**
# |-| **|求|偶|与|性|选择|**|：|鲜艳|的|羽毛|是|**|健康|与|基因|优越|的信号|**|。|色彩|越|鲜艳|，|通常|代表|个体|觅|食|能力强|（| 能|获取|更多|类|胡萝卜|素|）、|免疫|系统|健康|，|更容易|吸引|配偶|。
# |-| **|伪装|与|保护|**|：|在|热带|雨|林中|，|五彩|斑斓|的|羽毛|可能与|**|花朵|、|果实|或|斑|驳|的光|影|**|混合|，|形成|保护|色| ，|帮助|鹦鹉|隐藏|于|环境中|。
# |-| **|种|内|识别|**|：|不同|种类的|鹦鹉|通过|羽毛|颜色|和|图案|区分|同类|，|减少|杂交|可能|，|维持|物种|独|特性|。

# |---

# |###| **|3|.| |生态|与|行为|因素|**
# |-| **|食|性|影响|**|：|鹦鹉|以|水果|、|花朵|、|种子|为|食|，|这些|食物|富含|类|胡萝卜|素|，|直接|影响了|羽毛|的|红色|、|黄色|色调|。
# |-| **|社交|沟通|**|：|彩色|羽毛|在|群体|互动|中|起到|视觉|信号|作用|，|如|示威|、|警告|或|表达|情绪|。

# |---

# |###| **|4|.| |与其他|鸟|类的|对比|**
# |-| |鹦鹉|的|彩色|羽毛|与|**|极|乐|鸟|、|蜂|鸟|**|等|类似|，|是|热带|鸟类|适应|高|竞争|环境的|典型|特征|。|相比之下|，|温|带|或|地|栖|鸟类|（|如|麻雀|）|颜色|更|朴素|，|以减少|被捕|食|的风险|。

# |---

# |###| **|5|.| |人工|驯|养|的影响|**
# |在|人工|育种|中|，|人们|通过|选择性|繁殖|强化|了|某些|颜色|变异|（|如|纯|白|、|亮|黄|等|），|因此|宠物|鹦鹉|的颜色|可能|比|野生|个体|更加|丰富|多样|。

# |---

# |###| **|总结|**
# |鹦鹉|的|彩色|羽毛|是|**|自然|选择|、|性|选择|、|生理|结构和|生态环境|共同|塑造|的结果|**|。|它|不仅是|生存|工具|，|也是|自然|美|学的|体现|，|反映了|生物|进化|中|形式|与|功能的|精|妙|平衡|。||


for chunk in model.stream("天空是什么颜色？"):
    for block in chunk.content_blocks:
        if block["type"] == "reasoning" and (reasoning := block.get("reasoning")):
            print(f"Reasoning: {reasoning}")
        elif block["type"] == "tool_call_chunk":
            print(f"Tool call chunk: {block}")
        elif block["type"] == "text":
            print(block["text"])
        else:
            break

full = None
for chunk in model.stream("给我写一句话？"):
    full = chunk if full is None else full + chunk
    print(full.text)

print(full.content_blocks)

# “
# “晨
# “晨光
# “晨光吻
# “晨光吻醒
# “晨光吻醒花瓣
# “晨光吻醒花瓣时
# “晨光吻醒花瓣时，
# “晨光吻醒花瓣时，露
# “晨光吻醒花瓣时，露珠
# “晨光吻醒花瓣时，露珠正
# “晨光吻醒花瓣时，露珠正偷
# “晨光吻醒花瓣时，露珠正偷听
# “晨光吻醒花瓣时，露珠正偷听风的
# “晨光吻醒花瓣时，露珠正偷听风的呢
# “晨光吻醒花瓣时，露珠正偷听风的呢喃
# “晨光吻醒花瓣时，露珠正偷听风的呢喃。”
# “晨光吻醒花瓣时，露珠正偷听风的呢喃。”
# [{'type': 'text', 'text': '“晨光吻醒花瓣时，露珠正偷听风的呢喃。”'}]