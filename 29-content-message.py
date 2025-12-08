"""
消息中content属性的应用
支持3种主要格式：
1.字符串（String）： 最简单的格式，用于纯文本输入/输出。
2.提供商原生列表： 兼容模型提供商（如 OpenAI）特定的多模态数据结构。
3.LangChain 标准内容块（Standard Content Blocks）： 这是最核心的部分,解决了多模态不统一的问题。LangChain 提供了一个类型安全、跨提供商的统一标准来表示复杂内容，例如：
TextContentBlock (文本)
ImageContentBlock (图像)
ReasoningContentBlock (模型内部的思考逻辑)，解决了模型推理不透明的问题。
FileContentBlock (通用文件，如 PDF)
"""

## 多模态输入示例
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI

import dotenv
dotenv.load_dotenv()

human_msg = HumanMessage(
    content_blocks=[
        {"type": "text", "text": "你好，请识别这张图是什么？"},
        {"type": "image_url", "image_url": "https://img-s-msn-com.akamaized.net/tenant/amp/entityid/AAOEcdM.img"}
    ]
)

llm = ChatOpenAI(model="gpt-4o")


response = llm.invoke([human_msg])
print(response.content)

# 这是一张城市高速公路上方的鸟瞰图/航拍图，显示了一个多层的高速公路立交桥。有多条车道以及互相交错的道路设计，车辆在道路上 行驶。这种结构通常用于优化交通流量，提高车辆通行效率。