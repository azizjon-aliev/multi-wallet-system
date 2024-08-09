from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from src.models.wallet import Currency


class TransactionBase(BaseModel):
    debit: PydanticObjectId
    credit: PydanticObjectId
    amount: float = Field(default=0.0)
    currency: Currency
    rate: float = Field(default=1.0)
    description: str = Field(default="")


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    debit: Optional[PydanticObjectId] = None
    credit: Optional[PydanticObjectId] = None
    amount: Optional[float] = None
    currency: Optional[Currency] = None
    rate: Optional[float] = None
    description: Optional[str] = None
