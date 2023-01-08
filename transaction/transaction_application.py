from sqlalchemy.orm import Session

from error import credentials_exception, history_not_found_exception
from transaction import transaction_schema
from transaction.transaction_model import History
from user.user_model import User


def get_transactions(db: Session, user_id: int):
    return db.query(History).outerjoin(User, User.id == History.user_id) \
        .filter(User.id == user_id).all()


def get_transaction(db: Session, transaction_id: int, current_user_id: int):
    history = __find_history(db, transaction_id)

    __verify_history_writer(current_user_id, history)

    return history


def create_transaction(db: Session, transaction_request: transaction_schema.HistoryRequest, current_user_id: int):
    history = History(detail=transaction_request.detail, money=transaction_request.money,
                      user_id=current_user_id)
    db.add(history)
    db.commit()
    return history


def update_transaction(db: Session, transaction_id: int, transaction_request: transaction_schema.HistoryRequest,
                       current_user_id: int):
    history = __find_history(db, transaction_id)

    __verify_history_writer(current_user_id, history)

    history.updateHistory(transaction_request.detail, transaction_request.money)

    db.commit()

    return history


def delete_transaction(db, transaction_id, current_user_id):
    history = __find_history(db, transaction_id)

    __verify_history_writer(current_user_id, history)

    history.deleteHistory()
    db.commit()


def __find_history(db, transaction_id):
    history = db.query(History).filter(History.id == transaction_id).first()
    if history is None:
        raise history_not_found_exception.NotFoundException()
    return history


def __verify_history_writer(current_user_id, history):
    if history.user_id != current_user_id:
        raise credentials_exception.ForbiddenException()
