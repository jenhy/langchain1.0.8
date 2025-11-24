"""
任务：
Runnable batch的使用,max_concurrency参数的使用。输入10条用户评论同时进行情感分析，输出一批答案，并且要求统计运行时间。
提示词编写：你是一位专业的情感分析师，请判断以下评论是 '正面 (Positive)'、'负面 (Negative)' 还是 '中性 (Neutral)'。只返回判断结果。
"""


from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

import time
import dotenv
dotenv.load_dotenv()

# start_time = time.time()

# all_result = []

# prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是一位专业的情感分析师，请判断以下评论是 '正面 (Positive)'、'负面 (Negative)' 还是 '中性 (Neutral)'。只返回判断结果。"),
#     ("human", "{content}")
# ])

# input = [
#     {"content":"这次服务很满意，超出了我的意料。"}, 
#     {"content":"这次服务很差，下次不来。"},
#     {"content":"这次服务一般，下次来。"},
#     {"content":"这次服务很棒，下次来。"},
#     {"content":"产品还行，下次来。"},
#     {"content":"产品很差，下次不要来。"},
#     {"content":"送货很慢，下次不要来。"},
#     {"content":"外卖小哥态度差，下次不要来。"},
#     {"content":"这个师傅理发好，下次来。"},
#     {"content":"物业态度差，我要投诉。"}
# ]

# llm = ChatOpenAI(model="deepseek-chat", temperature=0.5)

# chain = prompt | llm | StrOutputParser()

# for item in input:
#     result = chain.invoke(item)
#     all_result.append(result)

# print(all_result)
# end_time = time.time()

# print(f"运行时间：{end_time - start_time}秒")

# ['正面', '负面', '中性', '正面 (Positive)', '中性', '负面', '负面', '负面', '正面 (Positive)', '负面']
# 运行时间：17.598642587661743秒


start_time = time.time()

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一位专业的情感分析师，请判断以下评论是 '正面 (Positive)'、'负面 (Negative)' 还是 '中性 (Neutral)'。只返回判断结果。"),
    ("human", "{content}")
])

input = [
    {"content":"这次服务很满意，超出了我的意料。"}, 
    {"content":"这次服务很差，下次不来。"},
    {"content":"这次服务一般，下次来。"},
    {"content":"这次服务很棒，下次来。"},
    {"content":"产品还行，下次来。"},
    {"content":"产品很差，下次不要来。"},
    {"content":"送货很慢，下次不要来。"},
    {"content":"外卖小哥态度差，下次不要来。"},
    {"content":"这个师傅理发好，下次来。"},
    {"content":"物业态度差，我要投诉。"}
]

llm = ChatOpenAI(model="deepseek-chat", temperature=0.5)

chain = prompt | llm | StrOutputParser()

result = chain.batch(input, config={"max_concurrency": 3})

print(result)

end_time = time.time()

print(f"运行时间：{end_time - start_time}秒")

# 使用默认的并发控制参数，运行时间短
# ['正面', '负面', '中性', '正面', '正面', '负面', '负面', '负面', '正面 (Positive)', '负面']
# 运行时间：5.87251877784729秒

# 加了并发控制参数max_concurrency为3，运行时间变长
# ['正面', '负面', '中性', '正面', '正面 (Positive)', '负面', '负面', '负面', '正面', '负面']
# 运行时间：7.418030261993408秒
