from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from database import Base


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.utc_timestamp())
    updated_at = Column(DateTime,
                        nullable=False,
                        default=func.utc_timestamp(),
                        onupdate=func.utc_timestamp())


class Histroy(Base, BaseMixin):
    __tablename__ = 'histories'
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    discription = Column(String(255))
    money = Column(Integer, nullable=False)
    real_transaction_date = Column(DateTime, nullable=False)
    current_user = relationship('User', backref='histories')
