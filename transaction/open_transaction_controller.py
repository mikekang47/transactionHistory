from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from transaction import transaction_application

router = APIRouter(
    prefix="/opentranscations",
)


@router.get("/{transaction_id}", status_code=status.HTTP_200_OK)
def get_transaction_by_id(transaction_id: int, db: Session = Depends(get_db)):
    transaction = transaction_application.get_open_transaction(db, transaction_id)
    return transaction.detail
