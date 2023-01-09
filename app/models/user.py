from sqlalchemy import Column, Integer, String, DateTime

from database import Base
from models import BaseMixin


class User(Base, BaseMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    nick_name = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255))
    expire_time = Column(DateTime)