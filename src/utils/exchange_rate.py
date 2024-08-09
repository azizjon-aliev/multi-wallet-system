from fastapi import HTTPException

from src.models.exchange_rate import ExchangeRate


async def convert_currency(
    amount: float, from_currency: str, to_currency: str
) -> float:
    if from_currency == to_currency:
        return amount

    exchange_rate_doc = await ExchangeRate.find_one(
        ExchangeRate.from_currency == from_currency,
        ExchangeRate.to_currency == to_currency
    )
    if not exchange_rate_doc:
        raise HTTPException(status_code=404, detail="Exchange rate not found")

    rate = exchange_rate_doc.rate
    commission = exchange_rate_doc.commission
    return amount * rate * (1 - commission)
