from datetime import datetime
from decimal import Decimal
from typing import List

from beanie import PydanticObjectId
from fastapi import HTTPException

from src.core.exceptions import EntityNotFoundException
from src.models import Transaction, User, Wallet
from src.models.transaction import TransactionType
from src.schemas.transaction import TransactionCreate
from src.utils.exchange_rate import convert_currency


def transaction_not_found(transaction_id: PydanticObjectId) -> HTTPException:
    raise EntityNotFoundException(f"Transaction with id {transaction_id} not found")


class TransactionService:
    async def get_all(self, user: User) -> List[Transaction]:
        wallets = await Wallet.find({"user_id": user.id}).to_list()

        if not wallets:
            return []

        wallet_ids = [wallet.id for wallet in wallets]

        transactions = await Transaction.find(
            {
                "wallet_id": {"$in": wallet_ids}
            }
        ).to_list()

        return transactions

    async def create(self, transaction: TransactionCreate, user: User) -> Transaction:
        wallet = await Wallet.get(transaction.wallet_id)
        if not wallet:
            raise HTTPException(status_code=422, detail="Wallet not found")

        if wallet.currency != transaction.currency:
            transaction_amount_in_wallet_currency = await convert_currency(
                transaction.amount, transaction.currency, wallet.currency
            )
        else:
            transaction_amount_in_wallet_currency = transaction.amount

        if transaction.type == TransactionType.DEPOSIT:
            wallet.balance += transaction_amount_in_wallet_currency
        elif transaction.type == TransactionType.WITHDRAW:
            if wallet.balance < transaction_amount_in_wallet_currency:
                raise HTTPException(status_code=400, detail="Insufficient funds")
            wallet.balance -= transaction_amount_in_wallet_currency

        transaction_doc = Transaction(**transaction.dict())
        await transaction_doc.insert()
        await wallet.save()
        return transaction_doc
