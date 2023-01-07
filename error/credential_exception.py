from fastapi import HTTPException
from starlette import status


class CredentialExcpetion(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Could not validate credentials",
                         headers={"WWW-Authenticate": "Bearer"})


class TokenTimeOutException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Token time out",
                         headers={"WWW-Authenticate": "Bearer"})
