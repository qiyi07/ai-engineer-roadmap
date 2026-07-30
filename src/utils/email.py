async def send_verification_email(email_to: str, username: str, code: str):
    """开发环境：仅打印到控制台，不真实发送邮件"""
    print(f"📧 验证码发送至: {email_to}")
    print(f"👤 用户: {username}")
    print(f"🔑 验证码: {code}")
    print("⏰ 有效期: 10 分钟")
    # 返回模拟成功，让调用方继续执行
    return {"message": "Code printed to console (dev mode)"}


# 为了兼容 fastapi-mail 的返回结构，保留一个空类（实际没用）
class FastMail:
    pass
