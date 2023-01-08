from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from session import session_application, session_schema
from user import user_application

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/session/login")

router = APIRouter(
    prefix="/session",
)


@router.post("/login", response_model=session_schema.Token)
def login(login_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    # check user and password
    user = user_application.get_user(db, email=login_data.username)
    session_application.verify_password(user, login_data.password)

    return session_application.create_session(db, user.email)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(token: str = Depends(oauth2_scheme),
           db: Session = Depends(get_db)):
    session_application.delete_session(db, token)
