from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from src.api.rate_limiter import limiter
from src.api.v1.deps import (
    get_current_active_user,
    get_transaction_service,
)
from src.models import Transaction, User
from src.models.wallet import Wallet
from src.schemas.transaction import TransactionCreate, TransactionUpdate
from http import HTTPStatus
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


@router.get("/{transaction_id}")
async def get_by_id(
    transaction_id: PydanticObjectId,
    user: User = Depends(get_current_active_user),
    service: TransactionService = Depends(get_transaction_service),
) -> Transaction:
    return await service.get_by_id(transaction_id=transaction_id, user=user)


@router.post("/", response_model=Wallet)
async def create(
    transaction: TransactionCreate,
    user=Depends(get_current_active_user),
    service: TransactionService = Depends(get_transaction_service),
) -> Transaction:
    return await service.create(transaction=transaction, user=user)


@router.patch("/{transaction_id}")
async def update(
    transaction_id: PydanticObjectId,
    transaction: TransactionUpdate,
    user: User = Depends(get_current_active_user),
    service: TransactionService = Depends(get_transaction_service),
) -> Transaction:
    return await service.update(
        transaction_id=transaction_id,
        transaction_update=transaction,
        user=user,
    )


@router.delete("/{transaction_id}", responses={HTTPStatus.NO_CONTENT: {}})
async def delete(
    transaction_id: PydanticObjectId,
    user: User = Depends(get_current_active_user),
    service: TransactionService = Depends(get_transaction_service),
):
    return await service.delete(transaction_id=transaction_id, user=user)
