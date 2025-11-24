"""
结构化输出。使用Pydantic 定义结构化数据。使用llm的with_structured_output方法，将llm的输出结果解析为结构化数据。
任务：从招聘 JD 中提取职位、薪资、技能列表为 Python 对象。

"""

from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
# from langchain_core.output_parsers import PydanticOutputParser

import dotenv
dotenv.load_dotenv()

class JobDescription(BaseModel):
    position: str = Field(description="职位名称")
    salary: str = Field(description="职位薪资")
    skills: list[str] = Field(description="职位技能列表")

prompt = ChatPromptTemplate(
    messages=[
        ("system", "你是一位专业的招聘分析专家，请从职位 JD 中提取职位、薪资、技能列表。"),
        ("human", "{jd}")
    ]
)

llm = ChatOpenAI(model="deepseek-v3", temperature=0.5)

# output_parser = PydanticOutputParser(pydantic_object=JobDescription)

chain = prompt | llm.with_structured_output(schema=JobDescription, method="json_schema", include_raw=True)


content = """
Python 开发工程师（10k-20k）
岗位职责：
负责公司后端业务系统的设计、开发与维护，确保系统高性能与高可用性。
使用 Django / Flask 等框架构建 Web 服务及 API 接口。
参与数据库结构设计与性能优化，熟练运用 MySQL、Redis 等存储与缓存技术。
配合前端、测试、运维等团队，推动产品迭代与线上稳定运行。
使用 Docker、Kubernetes 完成服务容器化与部署上线工作。
编写技术文档，提升代码质量，并持续优化系统架构。
岗位要求：
计算机相关专业，本科及以上学历（能力优秀者可放宽）。
扎实的 Python 编程基础，熟悉常见数据结构、算法及网络编程。
熟练掌握 Django 或 Flask，能独立完成后端模块开发。
熟悉 MySQL、Redis 设计与优化，有实际项目经验。
熟悉 Git 工作流，可使用 Docker 进行环境搭建与部署，了解 Kubernetes 使用优先。
思维清晰，具有优秀的沟通能力和团队协作意识，对技术有持续学习兴趣。
加分项：
有大型分布式系统开发经验
熟悉消息队列（Kafka/RabbitMQ）
有 DevOps、CI/CD 实践经验
有开源项目或技术博客者优先
"""

result = chain.invoke(
    {"jd": content}
)

print(result)

## gpt-3.5-turbo
# C:\Users\Jenhy\.conda\envs\langchain1.0.8\Lib\site-packages\langchain_openai\chat_models\base.py:2018: UserWarning: Cannot use method='json_schema' with model gpt-3.5-turbo since it doesn't support OpenAI's Structured Output API. You can see supported models here: https://platform.openai.com/docs/guides/structured-outputs#supported-models. To fix this warning, set `method='function_calling'. Overriding to method='function_calling'.
#   warnings.warn(
# position='Python 开发工程师' salary='10k-20k' skills=['Python 编程基础', '数据结构', '算法', '网络编程', 'Django', 'Flask', 'MySQL', 'Redis', 'Git 工作流', 'Docker', 'Kubernetes', '大型分布式系统开发', '消息队列（Kafka/RabbitMQ）', 'DevOps', 'CI/CD', '开源项目或技术博客']

## deepseek-v3
# position='Python 开发工程师' salary='10k-20k' skills=['Python', 'Django', 'Flask', 'MySQL', 'Redis', 'Docker', 'Kubernetes', 'Git', 'Kafka', 'RabbitMQ', 'DevOps', 'CI/CD']


## include_raw=True
# {
#     'raw': AIMessage(
#         content='{\n  "position": "Python 开发工程师",\n  "salary": "10k-20k",\n  "skills": [\n    "Python",\n    "Django",\n    "Flask",\n    "MySQL",\n    "Redis",\n    "Docker",\n    "Kubernetes",\n    "Git",\n    "Kafka",\n    "RabbitMQ",\n    "DevOps",\n    "CI/CD"\n  ]\n}', 
#         additional_kwargs={'parsed': JobDescription(position='Python 开发工程师', salary='10k-20k', skills=['Python', 'Django', 'Flask', 'MySQL', 'Redis', 'Docker', 'Kubernetes', 'Git', 'Kafka', 'RabbitMQ', 'DevOps', 'CI/CD']), 'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 89, 'prompt_tokens': 467, 'total_tokens': 556, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}, 'input_tokens': 0, 'output_tokens': 0, 'input_token_details': None}, 'model_provider': 'openai', 'model_name': 'deepseek-v3', 'system_fingerprint': None, 'id': '02176395378298375aeae14c82856eca08eecb5e75c0575c187a3', 'finish_reason': 'stop', 'logprobs': None}, 
#         id='lc_run--f7b4676a-ceda-4826-b034-193eda6c620e-0', 
#         usage_metadata={'input_tokens': 467, 'output_tokens': 89, 'total_tokens': 556, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}), 
#     'parsed': JobDescription(position='Python 开发工程师', salary='10k-20k', skills=['Python', 'Django', 'Flask', 'MySQL', 'Redis', 'Docker', 'Kubernetes', 'Git', 'Kafka', 'RabbitMQ', 'DevOps', 'CI/CD']), 
#     'parsing_error': None}