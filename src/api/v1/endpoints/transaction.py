from fastapi import APIRouter, Depends

from src.api.rate_limiter import limiter
from src.api.v1.deps import (
    get_current_active_user,
    get_transaction_service,
)
from src.models import Transaction, User
from src.schemas.transaction import TransactionCreate
from fastapi.requests import Request
from src.services.transaction import TransactionService

router = APIRouter()


@router.get("/")
@limiter.limit("100/minute")
async def get_all(
    request: Request,
    service: TransactionService = Depends(get_transaction_service),
    user: User = Depends(get_current_active_user),
) -> list[Transaction]:
    print(request)
    return await service.get_all(user)


@router.post("/")
async def create(
    transaction: TransactionCreate,
    user=Depends(get_current_active_user),
    service: TransactionService = Depends(get_transaction_service),
) -> Transaction:
    return await service.create(transaction=transaction, user=user)
