from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from database import Base
from models import BaseMixin


class History(Base, BaseMixin):
    __tablename__ = 'histories'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    detail = Column(String(255), nullable=True, default='')
    money = Column(Integer, nullable=False, default=0)
    user = relationship('User', backref=backref('histories', order_by=id))

    def updateHistory(self, detail, money):
        self.detail = detail
        self.money = money
