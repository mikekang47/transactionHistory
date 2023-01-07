from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import jwt_config
from models import User
from user.user_schema import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    data = {
        "exp": datetime.utcnow() + timedelta(hours=9) + timedelta(minutes=jwt_config.getRefreshTokenExpireMinutes()),
    }
    refresh_token = jwt.encode(data, jwt_config.getSecretKey(), algorithm=jwt_config.getAlgorithm())
    print(data["exp"])
    user = User(nick_name=user_create.nick_name,
                email=user_create.email,
                password=pwd_context.hash(user_create.password),
                refresh_token=refresh_token)

    db.add(user)
    db.commit()
    return user


def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.nick_name == user_create.nick_name) |
        (User.email == user_create.email)
    ).first()


def get_user(db: Session, username: str):
    return db.query(User).filter(User.email == username).first()
