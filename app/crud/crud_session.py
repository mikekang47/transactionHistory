from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import User
from app.schemas.token import Token
from util import jwt_util


class CRUDSession:
    def create_session(self, db: Session, user: User) -> Token:
        tokens = jwt_util.create_tokens(user.email)

        user.refresh_token = tokens.refresh_token.token
        user.expire_time = tokens.refresh_token.expire_date

        db.commit()

        return tokens

    def delete_session(self, db: Session, current_user: User) -> User:
        current_user.expire_time = datetime.utcnow() + timedelta(hours=9)

        db.commit()
        return current_user

    def get_access_token(self, db: Session, current_user: User) -> Token:
        return self.create_session(db, current_user)


session = CRUDSession()
