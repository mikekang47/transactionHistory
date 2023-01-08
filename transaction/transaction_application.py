from sqlalchemy.orm import Session

from error import credentials_exception
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
