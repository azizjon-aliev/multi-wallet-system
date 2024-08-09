from typing import List

from beanie import PydanticObjectId
from fastapi import HTTPException

from src.core.exceptions import EntityNotFoundException
from src.models import User, Wallet
from src.schemas.wallet import WalletCreate, WalletUpdate


def wallet_not_found(wallet_id: PydanticObjectId) -> HTTPException:
    raise EntityNotFoundException(f"Wallet with id {wallet_id} not found")


class WalletService:
    async def get_all(self, user: User) -> List[Wallet]:
        return await Wallet.find(Wallet.user_id == user.id).to_list()

    async def get_by_id(self, wallet_id: PydanticObjectId, user: User) -> Wallet:
        wallet = await Wallet.find_one(
            Wallet.id == wallet_id, Wallet.user_id == user.id
        )
        if not wallet:
            wallet_not_found(wallet_id=wallet_id)
        return wallet

    async def create(self, wallet: WalletCreate, user: User) -> Wallet:
        return await Wallet(
            **wallet.dict(),
            user_id=user.id,
        ).insert()

    async def update(
        self, wallet_id: PydanticObjectId, wallet: WalletUpdate, user: User
    ):
        wallet_obj = await Wallet.find_one(
            Wallet.id == wallet_id, Wallet.user_id == user.id
        )
        if not wallet_obj:
            wallet_not_found(wallet_id)

        update_data = wallet.dict(exclude_unset=True)
        await wallet_obj.set(update_data)
        return wallet_obj

    async def delete(self, wallet_id: PydanticObjectId, user: User):
        wallet = await Wallet.find_one(
            Wallet.id == wallet_id, Wallet.user_id == user.id
        )
        if not wallet:
            wallet_not_found(wallet_id)
        await wallet.delete()
