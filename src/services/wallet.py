from datetime import datetime
from typing import List

from beanie import PydanticObjectId
from fastapi import HTTPException

from src.core.exceptions import EntityNotFoundException
from src.models import Transaction, User, Wallet
from src.models.transaction import TransactionType
from src.models.wallet import Currency
from src.schemas.transaction import TransactionCreate
from src.schemas.wallet import WalletCreate, WalletDepositRequest, WalletUpdate
from src.utils.exchange_rate import convert_currency


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

    async def get_total_balance(self, user: User) -> dict:
        wallets = await Wallet.find(Wallet.user_id == user.id).to_list()
        total_balance = 0
        for wallet in wallets:
            if wallet.currency == Currency.USD:
                total_balance += wallet.balance
            elif wallet.currency == Currency.EUR:
                total_balance += await convert_currency(
                    wallet.balance, Currency.EUR, Currency.USD
                )
            elif wallet.currency == Currency.GBP:
                total_balance += await convert_currency(
                    wallet.balance,
                    Currency.GBP,
                    Currency.USD
                )
        return {
            "total_balance": total_balance,
            "currency": Currency.USD
        }

    async def deposit(
        self, wallet_id: PydanticObjectId, data: WalletDepositRequest, user: User
    ) -> Wallet:
        wallet = await Wallet.get(wallet_id)
        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        if wallet.currency != data.currency:
            # Конвертируем сумму в валюту кошелька
            amount = await convert_currency(data.amount, data.currency, wallet.currency)
        else:
            amount = data.amount

        # Пополняем баланс кошелька
        wallet.balance += amount

        # Создаем запись о транзакции
        transaction = TransactionCreate(
            wallet_id=wallet_id,
            type=TransactionType.DEPOSIT,
            amount=amount,
            currency=data.currency,
            timestamp=datetime.utcnow()
        )
        transaction_doc = Transaction(**transaction.dict())
        await transaction_doc.insert()

        # Сохраняем обновленный баланс
        await wallet.save()

        return wallet

    async def get_wallet_transaction(
        self,
        wallet_id: PydanticObjectId,
        user: User,
    ) -> List[Transaction]:
        wallet = await Wallet.find_one(
            Wallet.id == wallet_id, Wallet.user_id == user.id
        )

        if not wallet:
            wallet_not_found(wallet_id)

        transactions = await Transaction.find(
            Transaction.wallet_id == wallet_id
        ).to_list()
        return transactions
