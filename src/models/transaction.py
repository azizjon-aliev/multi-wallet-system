from datetime import datetime
from enum import StrEnum
from typing import Optional

from beanie import Document, PydanticObjectId
from pydantic import Field

from src.models.wallet import Currency


class TransactionType(StrEnum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class Transaction(Document):
    wallet_id: PydanticObjectId
    type: TransactionType
    amount: float
    currency: Currency
    timestamp: datetime

    class Settings:
        name = "transactions"
