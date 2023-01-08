from sqlalchemy.orm import Session

from error import credentials_exception
from transaction import transaction_schema
from transaction.transaction_model import History
from user.user_model import User


def get_transactions(db: Session, user_id: int):
    return db.query(History).outerjoin(User, User.id == History.user_id) \
        .filter(User.id == user_id).all()


def get_transaction(db: Session, transaction_id: int, current_user_id: int):
    history = db.query(History).filter(History.id == transaction_id).first()
    if history.user_id != current_user_id:
        raise credentials_exception.ForbiddenException()
    return history


def create_transaction(db: Session, transaction_request: transaction_schema.HistoryRequest, current_user_id: int):
    history = History(detail=transaction_request.detail, money=transaction_request.money,
                      user_id=current_user_id)
    db.add(history)
    db.commit()
    return history


def update_transaction(db: Session, transaction_id: int, transaction_request: transaction_schema.HistoryRequest,
                       current_user_id: int):
    history = db.query(History).filter(History.id == transaction_id).first()
    if history.user_id != current_user_id:
        raise credentials_exception.ForbiddenException()

    history.updateHistory(transaction_request.detail, transaction_request.money)

    db.commit()

    return history


def delete_transaction(db, transaction_id, current_user_id):
    history = db.query(History).filter(History.id == transaction_id).first()
    if history.user_id != current_user_id:
        raise credentials_exception.ForbiddenException()
    db.query(History).filter(History.id == transaction_id).delete()
    db.commit()
