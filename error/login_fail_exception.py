from fastapi import HTTPException
from starlette import status


class LoginFailException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Incorrect email or password",
                         headers={"WWW-Authenticate": "Bearer"}, )
