from typing import Optional
from pydantic import BaseModel, Field
from src.models.wallet import Currency


class WalletBase(BaseModel):
    currency: Currency
    balance: float = Field(default=0.0)


class WalletCreate(WalletBase):
    pass


class WalletUpdate(BaseModel):
    currency: Optional[Currency] = None
    balance: Optional[float] = None


class WalletDepositRequest(BaseModel):
    amount: float
    currency: Currency
