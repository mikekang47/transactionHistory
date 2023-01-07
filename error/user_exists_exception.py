from fastapi import HTTPException
from starlette import status


class UserExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT,
                         detail="User already exists")
