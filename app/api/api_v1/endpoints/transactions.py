import socket
from typing import Any, List, Optional

import pyperclip
import pyshorteners
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app import crud, models
from app.api.api_v1.deps import get_current_user_authorizer
from app.api.api_v1.deps import get_db
from app.models.user import User
from app.schemas.transaction import HistoryResponse, HistoryCreate, HistoryUpdate

router = APIRouter()


@router.get("/", response_model=List[HistoryResponse])
def read_transactions(
        *,
        db: Session = Depends(get_db),
        skip: Optional[int] = 0,
        limit: Optional[int] = 100,
        current_user: User = Depends(get_current_user_authorizer())
) -> Any:
    transactions = crud.transaction.get_transactions(db, user_id=current_user.id, skip=skip, limit=limit)
    return list(
        map(lambda t: HistoryResponse(id=t.id, detail=t.detail,
                                      money=t.money,
                                      created_at=t.created_at,
                                      updated_at=t.updated_at), transactions))


@router.get("/{transaction_id}", response_model=HistoryResponse)
def read_transaction(
        *,
        db: Session = Depends(get_db),
        transaction_id: int,
        current_user: models.User = Depends(get_current_user_authorizer())
) -> Any:
    transaction = crud.transaction.get_transaction(db, transaction_id=transaction_id, user_id=current_user.id)
    return HistoryResponse(id=transaction.id, detail=transaction.detail, money=transaction.money,
                           created_at=transaction.created_at,
                           updated_at=transaction.updated_at)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=HistoryResponse)
def create_transaction(
        *,
        db: Session = Depends(get_db),
        transaction_request: HistoryCreate,
        current_user: models.User = Depends(get_current_user_authorizer())
) -> Any:
    transaction = crud.transaction.create_transaction(db=db,
                                                      transaction_request=transaction_request,
                                                      user_id=current_user.id)
    return HistoryResponse(id=transaction.id, detail=transaction.detail, money=transaction.money,
                           created_at=transaction.created_at,
                           updated_at=transaction.updated_at)


@router.put("/{transaction_id}", status_code=status.HTTP_200_OK, response_model=HistoryResponse)
def update(
        *,
        db: Session = Depends(get_db),
        transaction_id: int,
        transaction_request: HistoryUpdate,
        current_user: models.User = Depends(get_current_user_authorizer())
) -> Any:
    transaction = crud.transaction.update_transaction(db=db, transaction_id=transaction_id,
                                                      transaction_request=transaction_request,
                                                      user_id=current_user.id)
    return HistoryResponse(id=transaction.id, detail=transaction.detail, money=transaction.money,
                           created_at=transaction.created_at,
                           updated_at=transaction.updated_at)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
        *,
        db: Session = Depends(get_db),
        transaction_id: int,
        current_user: models.User = Depends(get_current_user_authorizer())
) -> Any:
    crud.transaction.delete_transaction(db, transaction_id=transaction_id, user_id=current_user.id)


@router.get("/shortcut/{transaction_id}", status_code=status.HTTP_200_OK)
def shortcut_transaction(
        *,
        db: Session = Depends(get_db),
        transaction_id: int,
        current_user: models.User = Depends(get_current_user_authorizer())
) -> Any:
    crud.transaction.get_transaction(db, transaction_id=transaction_id, user_id=current_user.id)

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    url = f"https://{ip_address}:80/opentransactions/{transaction_id}"
    s = pyshorteners.Shortener(timeout=60 * 10).tinyurl.short(url)
    return {"message": f"Shortcut url: {s}"}


@router.get("/copy/{transaction_id}", status_code=status.HTTP_200_OK)
def copy_transaction(transaction_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user_authorizer())):
    transaction = crud.transaction.get_transaction(db, transaction_id=transaction_id, user_id=current_user.id)
    pyperclip.copy(transaction.detail)
    return {"message": "Copy transaction detail to clipboard"}
