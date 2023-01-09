from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app.api.api_v1.deps import get_db

router = APIRouter()


@router.get("/{transaction_id}", status_code=status.HTTP_200_OK)
def get_transaction_by_id(*, db: Session = Depends(get_db), transaction_id: int) -> str:
    transaction = crud.transaction.get_open_transaction(db, transaction_id)
    return transaction.detail
