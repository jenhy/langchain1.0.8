"""
系统级消息。
"""

from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage

import dotenv
dotenv.load_dotenv()

model = init_chat_model(
    model="openai:deepseek-chat"
)

system_msg = SystemMessage("""
                               你是一位精通网络框架的资深Python开发者。始终提供代码示例并解释你的推理。解释要简洁但全面。"""
                               )
messages = [
    system_msg,
    HumanMessage("我该如何创建一个REST API？")
]

response = model.invoke(messages)

print(response.content)

# 我将指导你使用FastAPI创建一个REST API，这是目前Python中最现代、最高效的框架之一。

# ## 1. 安装FastAPI和依赖

# ```bash
# pip install fastapi uvicorn
# ```

# ## 2. 基本REST API示例

# ```python
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Optional, List
# from enum import Enum

# # 创建FastAPI应用实例
# app = FastAPI(title="用户管理API", version="1.0.0")

# # 定义数据模型
# class UserRole(str, Enum):
#     ADMIN = "admin"
#     USER = "user"
#     GUEST = "guest"

# class UserCreate(BaseModel):
#     username: str
#     email: str
#     age: Optional[int] = None
#     role: UserRole = UserRole.USER

# class UserResponse(UserCreate):
#     id: int

# # 模拟数据库
# fake_db = []
# current_id = 1

# # REST API端点
# @app.get("/")
# async def root():
#     """根端点"""
#     return {"message": "欢迎使用用户管理API"}

# @app.get("/users", response_model=List[UserResponse])
# async def get_users(role: Optional[UserRole] = None):
#     """获取所有用户（可选按角色过滤）"""
#     if role:
#         return [user for user in fake_db if user["role"] == role]
#     return fake_db

# @app.get("/users/{user_id}", response_model=UserResponse)
# async def get_user(user_id: int):
#     """根据ID获取单个用户"""
#     for user in fake_db:
#         if user["id"] == user_id:
#             return user
#     raise HTTPException(status_code=404, detail="用户不存在")

# @app.post("/users", response_model=UserResponse, status_code=201)
# async def create_user(user: UserCreate):
#     """创建新用户"""
#     global current_id
#     user_dict = user.dict()
#     user_dict["id"] = current_id
#     fake_db.append(user_dict)
#     current_id += 1
#     return user_dict

# @app.put("/users/{user_id}", response_model=UserResponse)
# async def update_user(user_id: int, user_update: UserCreate):
#     """更新用户信息"""
#     for index, user in enumerate(fake_db):
#         if user["id"] == user_id:
#             updated_user = user_update.dict()
#             updated_user["id"] = user_id
#             fake_db[index] = updated_user
#             return updated_user
#     raise HTTPException(status_code=404, detail="用户不存在")

# @app.delete("/users/{user_id}", status_code=204)
# async def delete_user(user_id: int):
#     """删除用户"""
#     for index, user in enumerate(fake_db):
#         if user["id"] == user_id:
#             fake_db.pop(index)
#             return
#     raise HTTPException(status_code=404, detail="用户不存在")

# # 运行服务器（在命令行执行）
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
# ```

# ## 3. 运行和测试API

# ### 启动服务器：
# ```bash
# # 方式1：直接运行Python文件
# python app.py

# # 方式2：使用uvicorn命令
# uvicorn app:app --reload --host 0.0.0.0 --port 8000
# ```

# ### 测试API：

# 1. **自动API文档**：
#    - Swagger UI: http://localhost:8000/docs
#    - ReDoc: http://localhost:8000/redoc

# 2. **使用curl测试**：
# ```bash
# # 创建用户
# curl -X POST "http://localhost:8000/users" \
#      -H "Content-Type: application/json" \
#      -d '{"username":"john","email":"john@example.com","age":30,"role":"user"}'

# # 获取所有用户
# curl "http://localhost:8000/users"

# # 获取单个用户
# curl "http://localhost:8000/users/1"
# ```

# ## 4. 添加数据库支持（SQLAlchemy示例）

# ```python
# from sqlalchemy import create_engine, Column, Integer, String, Enum as SQLEnum
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os

# # 数据库配置
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # 定义数据库模型
# class UserDB(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     age = Column(Integer, nullable=True)
#     role = Column(String, default="user")

# # 创建数据库表
# Base.metadata.create_all(bind=engine)

# # 依赖注入数据库会话
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # 使用数据库的API端点
# @app.post("/db/users", response_model=UserResponse, status_code=201)
# async def create_user_db(user: UserCreate, db: Session = Depends(get_db)):
#     """使用数据库创建用户"""
#     db_user = UserDB(**user.dict())
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
# ```

# ## 5. 关键概念解释

# ### **HTTP方法对应操作**：
# - `GET`：获取资源（读取）
# - `POST`：创建资源（新建）
# - `PUT`：更新资源（替换）
# - `DELETE`：删除资源（移除）
# - `PATCH`：部分更新资源

# ### **FastAPI优势**：
# 1. **自动验证**：使用Pydantic模型自动验证请求数据
# 2. **自动文档**：自动生成OpenAPI文档
# 3. **类型提示**：完整的Python类型提示支持
# 4. **异步支持**：原生支持async/await
# 5. **依赖注入**：强大的依赖注入系统

# ### **最佳实践**：
# 1. **版本控制**：在URL中包含API版本（如`/api/v1/users`）
# 2. **错误处理**：使用适当的HTTP状态码
# 3. **分页**：为列表端点实现分页
# 4. **认证**：添加JWT或OAuth2认证
# 5. **日志记录**：记录请求和错误信息

# ## 6. 完整项目结构建议

# ```
# myapi/
# ├── app/
# │   ├── __init__.py
# │   ├── main.py          # FastAPI应用实例
# │   ├── api/
# │   │   ├── __init__.py
# │   │   └── v1/
# │   │       ├── __init__.py
# │   │       ├── endpoints/
# │   │       │   ├── users.py
# │   │       │   └── items.py
# │   │       └── api.py   # API路由注册
# │   ├── core/
# │   │   ├── config.py    # 配置管理
# │   │   └── security.py  # 认证逻辑
# │   ├── models/
# │   │   ├── user.py      # 数据模型
# │   │   └── item.py
# │   └── db/
# │       └── database.py  # 数据库连接
# ├── requirements.txt
# └── .env                 # 环境变量
# ```

# 这个示例展示了创建REST API的核心概念。FastAPI会自动处理请求验证、序列化和文档生成，让你专注于业务逻辑。