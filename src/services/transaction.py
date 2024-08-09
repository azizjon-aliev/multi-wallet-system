from typing import List

from beanie import PydanticObjectId
from fastapi import HTTPException

from src.core.exceptions import EntityNotFoundException
from src.models import Transaction, User, Wallet
from src.schemas.transaction import TransactionCreate, TransactionUpdate


def transaction_not_found(transaction_id: PydanticObjectId) -> HTTPException:
    raise EntityNotFoundException(f"Transaction with id {transaction_id} not found")


class TransactionService:
    async def get_all(self, user: User) -> List[Transaction]:
        wallets = await Wallet.find({"user_id": user.id}).to_list()

        if not wallets:
            return []

        wallet_ids = [wallet.id for wallet in wallets]

        transactions = await Transaction.find(
            {"$or": [{"debit": {"$in": wallet_ids}}, {"credit": {"$in": wallet_ids}}]}
        ).to_list()

        return transactions

    async def get_by_id(
        self, transaction_id: PydanticObjectId, user: User
    ) -> Transaction:
        transaction = await Transaction.get(transaction_id)

        if not transaction:
            transaction_not_found(transaction_id)

        if transaction.created_by != user.id:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to update this transaction.",
            )

        return transaction

    async def create(self, transaction: TransactionCreate, user: User) -> Transaction:
        # Проверка наличия кошельков
        debit_wallet = await Wallet.get(transaction.debit)
        credit_wallet = await Wallet.get(transaction.credit)

        if not debit_wallet:
            raise HTTPException(status_code=422, detail="Debit wallet not found.")

        if not credit_wallet:
            raise HTTPException(status_code=422, detail="Credit wallet not found.")

        # Проверка баланса на кошельке-дебет
        if debit_wallet.balance < transaction.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance.")

        # Расчет комиссии
        commission = 0.03 * transaction.amount  # 3% комиссии
        converted_amount = transaction.amount * transaction.rate

        # Создание транзакции
        transaction_doc = Transaction(
            debit=transaction.debit,
            credit=transaction.credit,
            amount=transaction.amount,
            converted_amount=converted_amount,
            currency=transaction.currency,
            rate=transaction.rate,
            commission=commission,
            description=transaction.description,
            created_by=user.id,
        )

        # Сохранение транзакции
        return await transaction_doc.insert()

    async def update(
        self,
        transaction_id: PydanticObjectId,
        transaction_update: TransactionUpdate,
        user: User,
    ):
        # Получение существующей транзакции
        transaction = await Transaction.get(transaction_id)

        if not transaction:
            transaction_not_found(transaction_id)

        if transaction.created_by != user.id:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to update this transaction.",
            )

        if transaction_update.debit and transaction_update.credit:
            # Проверка наличия кошельков и их балансов (только если обновляются
            # debit/credit)
            debit_wallet = await Wallet.get(transaction.debit)
            credit_wallet = await Wallet.get(transaction.credit)

            if not debit_wallet or not credit_wallet:
                raise HTTPException(
                    status_code=422, detail="One or both wallets not found."
                )

            if debit_wallet.balance < transaction_update.amount:
                raise HTTPException(status_code=400, detail="Insufficient balance.")

            # Применение обновлений
        transaction.amount = transaction_update.amount or transaction.amount
        transaction.currency = transaction_update.currency or transaction.currency
        transaction.rate = transaction_update.rate or transaction.rate
        transaction.description = (
            transaction_update.description or transaction.description
        )

        # Сохранение обновленной транзакции
        await transaction.save()

        return transaction

    async def delete(self, transaction_id: PydanticObjectId, user: User):
        transaction = await Transaction.get(transaction_id)

        if not transaction:
            transaction_not_found(transaction_id)

        if transaction.created_by != user.id:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to update this transaction.",
            )

        await transaction.delete()
