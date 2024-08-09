from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from src.api.v1.deps import get_current_active_user, get_wallet_service
from src.models import User
from src.models.wallet import Wallet
from src.schemas.wallet import WalletCreate, WalletUpdate
from http import HTTPStatus

from src.services.wallet import WalletService

router = APIRouter()


@router.get("/")
async def get_wallet(
    service: WalletService = Depends(get_wallet_service),
    user: User = Depends(get_current_active_user),
) -> list[Wallet]:
    return await service.get_all(user)


@router.get("/{wallet_id}")
async def get_wallet_by_id(
    wallet_id: PydanticObjectId,
    user: User = Depends(get_current_active_user),
    service: WalletService = Depends(get_wallet_service),
) -> Wallet:
    return await service.get_by_id(wallet_id=wallet_id, user=user)


@router.post("/", response_model=Wallet)
async def create_wallet(
    wallet: WalletCreate,
    user=Depends(get_current_active_user),
    service: WalletService = Depends(get_wallet_service),
) -> Wallet:
    return await service.create(wallet=wallet, user=user)


@router.patch("/{wallet_id}", response_model=Wallet)
async def update_wallet(
    wallet_id: PydanticObjectId,
    wallet: WalletUpdate,
    user: User = Depends(get_current_active_user),
    service: WalletService = Depends(get_wallet_service),
) -> Wallet:
    return await service.update(wallet_id=wallet_id, wallet=wallet, user=user)


@router.delete("/{wallet_id}", responses={HTTPStatus.NO_CONTENT: {}})
async def delete_wallet(
    wallet_id: PydanticObjectId,
    user: User = Depends(get_current_active_user),
    service: WalletService = Depends(get_wallet_service),
):
    return await service.delete(wallet_id=wallet_id, user=user)
