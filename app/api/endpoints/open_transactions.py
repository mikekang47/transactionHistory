from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from database import get_db

router = APIRouter()


@router.get("/{transaction_id}", status_code=status.HTTP_200_OK)
def get_transaction_by_id(*, db: Session = Depends(get_db), transaction_id: int, ):
    transaction = crud.transaction.get_open_transaction(db, transaction_id=transaction_id)
    return transaction.detail
