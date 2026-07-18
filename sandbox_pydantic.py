from pydantic import BaseModel, EmailStr,Field
from typing import Optional
from datetime import datetime
class UserProfile(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    age: Optional[int] = Field(None, ge=18, le=120)
    created_at: datetime = Field(default_factory=datetime.now)
if __name__ == "__main__":
    # 1. 正常数据
    user1 = UserProfile(id=1, username="alice_123", email="alice@test.com", age=25)
    print(user1.model_dump())          # 转成字典
    print(user1.model_dump_json())     # 转成 JSON 字符串

    # 2. 异常数据（触发校验错误）
    try:
        bad_user = UserProfile(id=2, username="a", email="not_an_email", age=150)
    except Exception as e:
        print(f"校验拦截: {e}")