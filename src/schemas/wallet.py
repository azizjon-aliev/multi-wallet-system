from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from src.models.wallet import Currency


class WalletBase(BaseModel):
    name: str
    currency: Currency
    balance: float = Field(default=0.0)


class WalletCreate(WalletBase):
    pass


class WalletUpdate(BaseModel):
    name: Optional[str] = None
    currency: Optional[Currency] = None
    balance: Optional[float] = None


class WalletDetail(WalletBase):
    id: PydanticObjectId

    class Config:
        from_attributes = True
