from fastapi import HTTPException
from starlette import status


class LowerMoneyException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="money must be greater than 0")


class EmptyDetailException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="detail must not be empty")


class EmptyFieldException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="user information field must not be empty")


class PasswordNotMatchException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="password not match")
