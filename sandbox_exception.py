import random
class AppException(Exception):
    """所有自定义异常的基类"""
    pass

class APIError(AppException):
    """调用外部 API 失败"""
    def __init__(self, service: str, status_code: int, message: str):
        self.service = service
        self.status_code = status_code
        self.message = message
        super().__init__(f"[{service}] {status_code}: {message}")

class ValidationError(AppException):
    """数据校验失败（区别于 Pydantic 的校验，这里指业务逻辑校验）"""
    pass

class ResourceNotFoundError(AppException):
    """资源不存在"""
    pass


def call_llm_api(prompt: str) -> str:
    """模拟调用大模型接口，有 30% 概率失败"""
    if random.random() < 0.3:   # 30% 概率模拟错误
        error_code = random.choice([429, 500, 502])
        if error_code == 429:
            raise APIError("OpenAI", 429, "Rate limit exceeded")
        elif error_code == 500:
            raise APIError("OpenAI", 500, "Internal server error")
        else:
            raise APIError("OpenAI", 502, "Bad gateway")
    return f"模型回复: 你说了 '{prompt}'"

def process_with_retry(prompt: str, max_retries: int = 3):
    for attempt in range(1, max_retries + 1):
        try:
            result = call_llm_api(prompt)
            print(f"✅ 成功: {result}")
            return result
        except APIError as e:
            print(f"⚠️ 第 {attempt} 次尝试失败: {e}")
            if attempt == max_retries:
                print("❌ 达到最大重试次数，抛出最终异常")
                raise   # 重新抛出，让上层处理
            # 模拟退避等待（面试常问）
            import time
            time.sleep(1 * attempt)  # 1秒, 2秒, 3秒...

if __name__ == "__main__":
    try:
        process_with_retry("你好，AI")
    except APIError as e:
        print(f" 程序最终捕获: {e}")