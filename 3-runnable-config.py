"""
Runnable config的使用。针对同一个 Chain，根据不同场景动态调整 Temperature 参数。
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import ConfigurableField

import dotenv
dotenv.load_dotenv()


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一位专业的翻译家，请将提供的诗歌翻译成英文。你不需要提供任何解释，只需输出英文译文。"),
        ("human", "{text}")
    ]
)

## langchain0.x版本写法用with_config
# llm = ChatOpenAI(model="deepseek-chat", temperature=0.5).with_config(
#     configurable={
#         "temperature":ConfigurableField(
#             id="llm_temperature",
#             description="LLM 的温度参数,用于控制模型输出的随机性。"
#         )
#     }
# )

## langchain1.x版本写法用configurable_fields
llm = ChatOpenAI(model="deepseek-chat", temperature=0.5).configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",
        description="LLM 的温度参数,用于控制模型输出的随机性。"
    )
)

chain = prompt | llm | StrOutputParser()

config_strict = {"configurable":{"llm_temperature":0.0}}

config_creative = {"configurable":{"llm_temperature":0.9}}

content = """
《夜行》
微风掠过江面，
灯火散作星尘。
行人独步长街，
心事悄落无痕。
"""

result = chain.invoke({"text": content,"config":config_strict})

print(f"config_strict(0.0):{result}\n")

result = chain.invoke({"text": content,"config":config_creative})

print(f"config_creative(0.9):{result}")

# 运行结果
# config_strict(0.0):"Night Walk"
# A breeze skims the river's face,
# Lanterns scatter as stardust in space.
# A lone soul treads the lengthy street,
# With silent thoughts in hushed retreat.

# config_creative(0.9):"Night Walk"
# A light breeze skims the river's face,
# Lanterns scatter into stardust trace.
# A lone soul treads the lengthy street,
# Silent thoughts fall without a beat.
