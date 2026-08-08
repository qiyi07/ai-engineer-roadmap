from sqlmodel import Session, select
from src.models.db_models import Message, User
from src.repositories.message_repo import engine

with Session(engine) as session:
    # 查询最新 3 条消息
    msgs = session.exec(select(Message).order_by(Message.id.desc()).limit(3)).all()
    for m in msgs:
        print(f"ID: {m.id}, User: {m.user_id}, Message: {m.message[:30]}, Reply: {m.reply[:30]}")
    
    # 查询用户
    users = session.exec(select(User)).all()
    for u in users:
        print(f"User: {u.username}, Email: {u.email}, Created: {u.created_at}")