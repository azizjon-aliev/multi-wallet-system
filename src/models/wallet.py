from enum import StrEnum

from beanie import Document, PydanticObjectId
from pydantic import Field


class Currency(StrEnum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


class Wallet(Document):
    user_id: PydanticObjectId
    currency: Currency
    balance: float = Field(default=0.0)

    class Settings:
        name = "wallets"
