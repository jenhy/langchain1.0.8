"""
RunnableParallel使用。
输入产品名，同时并行生成：1. 广告语；2. 产品简介。
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableParallel
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
        "slogan": slogan_chain,
        "desc": desc_chain
    }
)

result = multi_chain.invoke({
    "product": "Nike shoes"
}
)

print(result)

# {
#     'slogan': '穿上它，征服每一步。', 
#     'desc': '### 产品简介：Nike 运动鞋\n\nNike 运动鞋是专为追求卓越性能与时尚设计的运动员和日常穿着者打造的高品质鞋类产品。凭借创新的科技、优质的材料和独特的设计理念，Nike 运动鞋不仅提供出色的舒适度和支撑性，还帮助用户在运动与生活中释放潜能。\n\n#### 核心特点：\n1. **创新科技**：采用 Nike 独家研发的缓震技术（如 Air Max、Zoom Air 和 React 泡沫），有效吸收冲击力，提升运动表现并减少疲劳。\n2. **优质材料**：选用轻量、透气的面料与耐用橡胶外底，确保鞋子在长时间使用中保持舒适与稳定性。\n3. **时尚设计**：融合现代美学与功能性，提供多种颜色和款式选择，满足不同场合的穿搭需求。\n4. **多功能适用**：无论是跑步、训练、篮球还是日常休闲，Nike 运动鞋都能提供针对性的支撑与灵活性。\n\n#### 适用人群：\n- 专业运动员及运动爱好者\n- 注重健康生活方式的日常用户\n- 追求时尚与舒适结合的潮流人士\n\n#### 品牌承诺：\nNike 始终致力于通过前沿科技与可持续设计，为全球用户带来卓越的运动体验。选择 Nike 运动鞋，迈出自信步伐，成就更好的自己。\n\n---  \n*探索 Nike 运动鞋系列，开启你的无限可能！*'}