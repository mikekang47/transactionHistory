from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas import UserCreate
from error import user_exception

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CRUDUser(CRUDBase[User, UserCreate]):
    def create_user(self, db: Session, *, user_create: UserCreate):
        exists_user = self.__get_existing_user(db, user_create=user_create)
        if exists_user is not None:
            raise user_exception.UserExistsException()

        source = User(nick_name=user_create.nick_name,
                      email=user_create.email,
                      password=pwd_context.hash(user_create.password))

        db.add(source)
        db.commit()
        return source

    def __get_existing_user(self, db: Session, *, user_create: UserCreate):
        return db.query(User).filter(
            (User.nick_name == user_create.nick_name) |
            (User.email == user_create.email)
        ).first()

    def get_user_by_email(self, db: Session, *, email: str) -> User:
        source = db.query(User).filter(User.email == email).first()
        if source is None:
            raise user_exception.UserNotFoundException()
        return source


user = CRUDUser(User)
