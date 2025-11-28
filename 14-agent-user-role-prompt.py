"""
基于用户的角色来动态生成提示词。使用@dynamic_prompt装饰器。
"""

from typing import TypedDict

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain_openai import ChatOpenAI
from langchain.tools import tool

import dotenv
dotenv.load_dotenv()

class Context(TypedDict):
    user_role: str
    
@tool
def web_search(query: str) -> str:
    """使用网络查询获取信息。"""
    return f"搜索结果：{query}"
    
@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """基于用户的角色来动态生成提示词。"""
    user_role = request.runtime.context.get("user_role", "user")
    base_prompt = """
    你是一个有帮助的助手。
    """

    if user_role == "expert":
        return f"{base_prompt} 提供详细的技术回复。"
    elif user_role == "beginner":
        return f"{base_prompt} 用简单的方式解释概念，避免使用术语。"
    
    return base_prompt

agent = create_agent(
    model=ChatOpenAI(model="deepseek-chat", temperature=0.5),
    tools=[web_search],
    middleware=[user_role_prompt],
    context_schema=Context,
)
    

# 系统提示将基于上下文动态生成。
results = agent.invoke(
    {"messages":[
        {"role": "user", "content": "解释机器学习"}
    ]},
    context={"user_role": "expert"} # 传递角色信息
)

messages = results["messages"]
for message in messages:
    message.pretty_print()
    
# ================================ Human Message =================================

# 解释机器学习
# ================================== Ai Message ==================================

# 我来为您详细解释机器学习的基本概念、原理和应用。
# Tool Calls:
#   web_search (call_j80cv0f72veqoqjap5v8ismd)
#  Call ID: call_j80cv0f72veqoqjap5v8ismd
#   Args:
#     query: 机器学习基本概念 定义 工作原理
# ================================= Tool Message =================================
# Name: web_search

# 搜索结果：机器学习基本概念 定义 工作原理
# ================================== Ai Message ==================================

# 机器学习是人工智能的一个重要分支，它让计算机能够通过数据和经验自动学习和改进，而无需明确编程。让我为您详细解释：

# ## 什么是机器学习？

# **机器学习**是一种让计算机系统从数据中学习并做出预测或决策的技术。与传统编程不同，机器学习不是通过编写明确的规则来解决问题，而是让算法从数据中自动发现模式和规律。

# ## 机器学习的核心原理

# 1. **数据驱动**：机器学习模型通过分析大量数据来学习
# 2. **模式识别**：从数据中发现隐藏的模式和关系
# 3. **预测能力**：基于学到的模式对新数据进行预测

# ## 主要类型

# ### 1. 监督学习
# - **有标签数据**：每个输入都有对应的输出标签
# - **目标**：学习输入到输出的映射关系
# - **应用**：分类（如垃圾邮件识别）、回归（如房价预测）

# ### 2. 无监督学习
# - **无标签数据**：只有输入数据，没有输出标签
# - **目标**：发现数据中的内在结构
# - **应用**：聚类（如客户分群）、降维

# ### 3. 强化学习
# - **通过试错学习**：智能体与环境交互获得奖励
# - **目标**：学习最优策略以最大化累积奖励
# - **应用**：游戏AI、机器人控制

# ## 基本工作流程

# 1. **数据收集** - 获取相关数据集
# 2. **数据预处理** - 清洗、转换数据
# 3. **特征工程** - 选择和构建特征
# 4. **模型选择** - 选择合适的算法
# 5. **模型训练** - 用数据训练模型
# 6. **模型评估** - 测试模型性能
# 7. **部署应用** - 将模型投入实际使用

# ## 常见算法

# - **线性回归**：预测连续值
# - **逻辑回归**：分类问题
# - **决策树**：树形结构决策
# - **支持向量机**：寻找最优分类边界
# - **神经网络**：模拟人脑神经元
# - **K均值聚类**：无监督聚类

# ## 实际应用领域

# - **图像识别**：人脸识别、物体检测
# - **自然语言处理**：机器翻译、情感分析
# - **推荐系统**：电商推荐、内容推荐
# - **医疗诊断**：疾病预测、影像分析
# - **金融风控**：欺诈检测、信用评分
# - **自动驾驶**：环境感知、路径规划

# 机器学习正在改变我们生活的方方面面，从智能手机的语音助手到医疗诊断系统，都离不开机器学习技术的支持。随着数据量的增长和计算能力的提升，机器学习的应用前景将更加广阔。