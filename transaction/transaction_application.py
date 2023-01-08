from sqlalchemy.orm import Session

from transaction.transaction_model import History
from user.user_model import User


def get_transactions(db: Session, user_id: int):
    return db.query(History).outerjoin(User, User.id == History.user_id) \
        .filter(User.id == user_id).all()


def get_transaction(db: Session, transaction_id: int):
    return db.query(History).filter(History.id == transaction_id).first()
