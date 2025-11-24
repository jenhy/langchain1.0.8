"""
任务：
使用LCEL链式语法，调用提示词、模型和输出解析器，将中文翻译成法文。我爱中国。
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI(model="deepseek-chat", temperature=0.5)

template = ChatPromptTemplate([("human", "{question}")])

output = StrOutputParser()

chain = template | model | output

result = chain.invoke({"question": "请将中文翻译成法文。我爱中国。"})

print(result)   # J'aime la Chine.

