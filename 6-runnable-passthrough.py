"""
RunnableParallel和RunnablePassthrough的配合使用。
输入产品名，同时并行生成：1. 广告语；2. 产品简介。
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

import dotenv
dotenv.load_dotenv()


slogan_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一位专业的广告专家，请为产品{product}生成一个吸引人的广告语。"),
        ("human", "请生成一个吸引人的广告语。")
    ]
)

desc_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一位专业的产品专家，请为产品{product}生成一个产品简介。"),
        ("human", "请生成一个产品简介。")
    ]
)

llm = ChatOpenAI(model="deepseek-chat", temperature=0.5)


slogan_chain = slogan_prompt | llm | StrOutputParser()
desc_chain = desc_prompt | llm | StrOutputParser()

# 对应于 RunnableParallel 构造函数__init__中的主要参数steps__
multi_chain = RunnableParallel({
        "original": RunnablePassthrough(),
        "slogan": slogan_chain,
        "desc": desc_chain
    }
)

result = multi_chain.invoke({
    "product": "Nike shoes"
    }
)

print(result)

{
    'original': {'product': 'Nike shoes'}, 
    'slogan': '穿上它，征服每一步。', 
    'desc': '### 产品简介：Nike 运动鞋\n\nNike 运动鞋是专为追求卓越性能与时尚设计的运动爱好者打造的高品质鞋类产品。凭借创新的科技与精湛的工艺，Nike 运动鞋不仅提供出色的舒适度和支撑性，还能满足不同运动场景的需求，帮助用户释放潜能，突破极限。\n\n#### 核心特点：\n1. **先进缓震技术**：采用 Nike Air、Zoom 或 React 等专利科技，有效吸收冲击力，提升运动时的回弹与稳定性。\n2. **轻质透气设计**：鞋面使用 Flyknit 或工程网眼材质，确保轻盈透气，同时增强灵活性与贴合感。\n3. **耐久抓地力**：外底采用高耐磨橡胶与独特纹路设计，适应多种地面条件，提供可靠的抓地表现。\n4. **时尚多元风格**：从经典款式到联名限量版，Nike 运动鞋融合潮流元素，满足日常穿搭与专业运动双重需求。\n\n#### 适用场景：\n- 跑步、训练、篮球等专业运动\n- 日常休闲与街头时尚搭配\n\nNike 运动鞋，以创新为驱动，为每一步注入能量与自信。'}


