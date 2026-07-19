# #装饰器
# import time

# def log_time(func):
#     def wrapper(*args, **kwargs):
#         start = time.time()
#         result = func(*args, **kwargs)
#         end = time.time()
#         print(f"[{func.__name__}] 耗时: {end - start:.4f} 秒")
#         return result
#     return wrapper
# @log_time
# def slow_function():
#     time.sleep(0.5)
#     return "done"

# if __name__ == "__main__":
#     print(slow_function())

import time
def log_time(prefix: str = ""):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            name = f"{prefix}:{func.__name__}" if prefix else func.__name__
            print(f"[{name}] 耗时: {end - start:.4f} 秒")
            return result
        return wrapper
    return decorator

# 使用
@log_time(prefix="API")
def fetch_data():
    time.sleep(0.2)
    return {"data": "ok"}

print(fetch_data())