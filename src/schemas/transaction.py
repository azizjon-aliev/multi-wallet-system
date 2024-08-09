from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel

from src.models.transaction import TransactionType
from src.models.wallet import Currency


class TransactionBase(BaseModel):
    wallet_id: PydanticObjectId
    type: TransactionType
    amount: float
    currency: Currency
    timestamp: datetime


class TransactionCreate(TransactionBase):
    pass
