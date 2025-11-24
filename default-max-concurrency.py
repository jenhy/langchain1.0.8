import os
import math

def get_default_max_concurrency():
    """
    计算 LangChain (基于 ThreadPoolExecutor) 的默认最大并发数。
    公式: min(32, os.cpu_count() + 4)
    """
    # 1. 获取 CPU 逻辑核心数
    cpu_count = os.cpu_count()

    if cpu_count is None:
        print("警告：无法获取 CPU 核心数，默认值将按保守估计计算。")
        # 假设一个安全值，例如 8
        default_concurrency = min(32, 8 + 4)
    else:
        # 2. 应用 ThreadPoolExecutor 的默认公式
        # min(32, cores + 4)
        default_concurrency = min(32, cpu_count + 4)

    print(f"--- 系统信息 ---")
    print(f"逻辑 CPU 核心数 (os.cpu_count()): {cpu_count}")
    print(f"默认 ThreadPoolExecutor 线程数 (min(32, cores + 4)): {default_concurrency}")
    print(f"因此，LangChain 默认的 max_concurrency 约为: {default_concurrency}")

    return default_concurrency

# 执行函数
default_limit = get_default_max_concurrency()

# 示例：将这个默认值应用到您的 Chain 中进行测试
# config_default = {"max_concurrency": default_limit}
# chain.batch(input, config=config_default)


# --- 系统信息 ---
# 逻辑 CPU 核心数 (os.cpu_count()): 8
# 默认 ThreadPoolExecutor 线程数 (min(32, cores + 4)): 12
# 因此，LangChain 默认的 max_concurrency 约为: 12