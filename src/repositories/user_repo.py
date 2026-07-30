from sqlmodel import Session, select

from src.core.security import get_password_hash, verify_password
from src.models.db_models import User


class UserRepository:
    @staticmethod
    def get_by_username(session: Session, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()

    @staticmethod
    def get_by_email(session: Session, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    @staticmethod
    def create_user(session: Session, username: str, email: str, password: str) -> User:
        hashed = get_password_hash(password)
        user = User(username=username, email=email, hashed_password=hashed)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def authenticate(session: Session, username: str, password: str) -> User | None:
        user = UserRepository.get_by_username(session, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
