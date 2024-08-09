from beanie import Document
from src.models.wallet import Currency


class ExchangeRate(Document):
    from_currency: Currency
    to_currency: Currency
    rate: float
    commission: float

    class Settings:
        collection = "exchange_rates"
