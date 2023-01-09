from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.models.transaction import History
from app.models.user import User
from app.schemas.transaction import HistoryCreate


class CRUDTransaction:
    def get_transactions(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> List[History]:
        return db.query(History).outerjoin(User, User.id == History.user_id) \
            .filter(History.user_id == user_id) \
            .filter(History.is_deleted == False) \
            .offset(skip) \
            .limit(limit) \
            .all()

    def get_transaction(self, db: Session, *, transaction_id: int, user_id: int) -> History:
        history = self.__find_history(db, transaction_id=transaction_id)

        self.__verify_history_writer(user_id=user_id, history=history)

        return history

    def get_open_transaction(self, db, *, transaction_id):
        return self.__find_history(db, transaction_id=transaction_id)

    def create_transaction(self, db: Session, *, transaction_request: HistoryCreate,
                           user_id: int) -> History:
        history = History(detail=transaction_request.detail, money=transaction_request.money,
                          user_id=user_id)
        db.add(history)
        db.commit()
        return history

    def update_transaction(self, db: Session, *, transaction_id: int, transaction_request: HistoryCreate,
                           user_id: int):
        history = self.__find_history(db, transaction_id=transaction_id)

        self.__verify_history_writer(user_id=user_id, history=history)

        history.updateHistory(transaction_request.detail, transaction_request.money)

        db.commit()

        return history

    def delete_transaction(self, db: Session, *, transaction_id: int, user_id: int):
        history = self.__find_history(db, transaction_id=transaction_id)

        self.__verify_history_writer(user_id=user_id, history=history)

        history.deleteHistory()

        db.commit()

    def __find_history(self, db, *, transaction_id):
        history = db.query(History) \
            .filter(History.id == transaction_id) \
            .filter(History.is_deleted == False).first()
        if history is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="History not found")
        return history

    def __verify_history_writer(self, *, user_id, history):
        if history.user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You do not have permission to access this resource")


transaction = CRUDTransaction()
