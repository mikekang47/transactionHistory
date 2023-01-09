from fastapi import APIRouter

from app.api.api_v1.endpoints import open_transactions
from app.api.api_v1.endpoints import users, transactions

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(open_transactions.router, prefix="/open_transactions", tags=["open_transactions"])

