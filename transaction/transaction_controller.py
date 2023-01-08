from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from transaction import transaction_application, transaction_schema
from user.user_controller import get_current_user
from user.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/transactions")

router = APIRouter(
    prefix="/transactions",
)


@router.get("/", response_model=List[transaction_schema.HistoryResponse])
def get_transactions_by_user_id(current_user: User = Depends(get_current_user),
                                db: Session = Depends(get_db)):
    transactions = transaction_application.get_transactions(db, current_user.id)
    return list(
        map(lambda transaction: transaction_schema.HistoryResponse(id=transaction.id, detail=transaction.detail,
                                                                   money=transaction.money,
                                                                   created_at=transaction.created_at,
                                                                   updated_at=transaction.updated_at), transactions))


@router.get("/{transaction_id}", response_model=transaction_schema.HistoryResponse)
def get_transaction_by_id(transaction_id: int, current_user: User = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    transaction = transaction_application.get_transaction(db, transaction_id, current_user.id)
    return transaction_schema.HistoryResponse(id=transaction.id, detail=transaction.detail, money=transaction.money,
                                              created_at=transaction.created_at,
                                              updated_at=transaction.updated_at)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=transaction_schema.HistoryResponse)
def create_transaction(_transaction_request: transaction_schema.HistoryRequest,
                       db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction = transaction_application.create_transaction(db=db,
                                                             transaction_request=_transaction_request,
                                                             current_user_id=current_user.id)
    return transaction_schema.HistoryResponse(id=transaction.id, detail=transaction.detail, money=transaction.money,
                                              created_at=transaction.created_at,
                                              updated_at=transaction.updated_at)


@router.put("/{transaction_id}", status_code=status.HTTP_200_OK, response_model=transaction_schema.HistoryResponse)
def update_transaction(transaction_id: int, _transaction_request: transaction_schema.HistoryRequest,
                       db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transaction = transaction_application.update_transaction(db=db, transaction_id=transaction_id,
                                                             transaction_request=_transaction_request,
                                                             current_user_id=current_user.id)
    return transaction_schema.HistoryResponse(id=transaction.id, detail=transaction.detail, money=transaction.money,
                                              created_at=transaction.created_at,
                                              updated_at=transaction.updated_at)