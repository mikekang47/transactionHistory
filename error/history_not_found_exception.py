from fastapi import HTTPException


class NotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="History not found")
