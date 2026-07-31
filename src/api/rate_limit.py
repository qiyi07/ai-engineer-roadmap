from slowapi import Limiter
from slowapi.util import get_remote_address

# 创建限流器实例，默认全局限流 100 次/分钟
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])