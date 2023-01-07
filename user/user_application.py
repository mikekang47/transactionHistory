from passlib.context import CryptContext
from sqlalchemy.orm import Session

from error import user_not_found_exception, user_exists_exception
from user.user_model import User
from user.user_schema import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    exists_user = __get_existing_user(db, user_create)
    if exists_user is not None:
        raise user_exists_exception.UserExistsException()

    user = User(nick_name=user_create.nick_name,
                email=user_create.email,
                password=pwd_context.hash(user_create.password))

    db.add(user)
    db.commit()
    return user


def __get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.nick_name == user_create.nick_name) |
        (User.email == user_create.email)
    ).first()


def get_user(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise user_not_found_exception.UserNotFoundException()
    return user
