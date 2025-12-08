"""
模型速率限制。
"""

from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain.chat_models import init_chat_model
import time

import dotenv
dotenv.load_dotenv()

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.1,    # 每10秒请求一次
    check_every_n_seconds=0.1,  # 每100毫秒检查是否允许发起请求
    max_bucket_size=10  # 允许的请求次数
)

model = init_chat_model(
    model="openai:deepseek-chat",
    temperature=0.5,
    rate_limiter=rate_limiter,
)

for i in range(1, 4):
    start_time = time.time()
    result = model.invoke(f"给我写一首关于第{i}次调用的短诗。")
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    print(f"第{i}次调用完成，响应内容：{result.content[:50]}，本次调用耗时：{elapsed_time:.2f}秒\n\n")


# 第1次调用完成，响应内容：## 《初唤》

# 拨号音在铜芯里蜷成弹簧，
# 我数到第七次振铃，
# 像解开一串生锈的锁链。
# 突然，电流接，本次调用耗时：16.88秒


# 第2次调用完成，响应内容：## 《第二次调用》

# 我熟悉这串数字的凉意，
# 像旧琴键在暗处自己凹陷。
# 拨号音漫过听筒的斜坡，
# 等，本次调用耗时：10.23秒


# 第3次调用完成，响应内容：## 《第三次调用》

# 我俯身向无应答的终端，
# 指节叩击三遍。
# 每道裂纹都长出新的歧路，
# 而旧地址在，本次调用耗时：9.79秒