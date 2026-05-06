from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.schemas import UserCreate
from app.auth import hash_password, verify_password


def create_user(db: Session, user_data: UserCreate) -> User:
    if db.query(User).filter(User.username == user_data.username).first():
        return None

    hashed = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed,
        role=user_data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user