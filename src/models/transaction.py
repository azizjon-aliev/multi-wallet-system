from beanie import Document, PydanticObjectId
from pydantic import Field

from src.models.wallet import Currency


class Transaction(Document):
    debit: PydanticObjectId
    credit: PydanticObjectId
    amount: float = Field(default=0.0)
    converted_amount: float = Field(default=0.0)
    currency: Currency
    rate: float = Field(default=1.0)
    commission: float = Field(default=3.0)
    description: str = Field(default="")
    created_by: PydanticObjectId

    class Settings:
        name = "transactions"
