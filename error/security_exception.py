from fastapi import HTTPException
from starlette import status


class CredentialException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Could not validate credentials",
                         headers={"WWW-Authenticate": "Bearer"})


class TokenTimeOutException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Token time out",
                         headers={"WWW-Authenticate": "Bearer"})


class ForbiddenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN,
                         detail="You do not have permission to access this resource")


class TokenInvalidException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Token invalid",
                         headers={"WWW-Authenticate": "Bearer"})


class UnknownHeaderException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED,
                         detail="Unknown Header")
