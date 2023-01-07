from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from session import session_application, session_schema
from user import user_application
from user.user_application import pwd_context

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/session/login")

router = APIRouter(
    prefix="/session",
)


@router.post("/login", response_model=session_schema.Token)
def login_for_access_token(login_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    # check user and password
    # TODO
    # verfiy랑 create 책임 분리
    user = user_application.get_user(db, login_data.username)
    if not user or not pwd_context.verify(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return session_application.create_session(user.nick_name)
