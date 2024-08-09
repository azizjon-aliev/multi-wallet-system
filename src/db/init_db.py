from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import settings
from src.core.security import get_password_hash
from src.models import User, gather_documents
from src.models.exchange_rate import ExchangeRate
from src.models.wallet import Currency


async def init() -> None:
    client = AsyncIOMotorClient(str(settings.MONGODB_URI))
    await init_beanie(
        database=getattr(client, settings.MONGODB_DB_NAME),
        document_models=gather_documents(),  # type: ignore[arg-type]
    )
    if not await User.get_by_username(username=settings.FIRST_SUPERUSER):
        await User(
            username=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
            base_currency=settings.BASE_CURRENCY,
        ).insert()

    # init exchange rates
    if not await ExchangeRate.find_all().to_list():
        usd_to_eur = ExchangeRate(
            from_currency=Currency.USD,
            to_currency=Currency.EUR,
            rate=0.9,
            commission=0.03
        )
        eur_to_usd = ExchangeRate(
            from_currency=Currency.EUR,
            to_currency=Currency.USD,
            rate=1.1,
            commission=0.03
        )
        usd_to_gbp = ExchangeRate(
            from_currency=Currency.USD,
            to_currency=Currency.GBP,
            rate=0.75,
            commission=0.03
        )
        gbp_to_usd = ExchangeRate(
            from_currency=Currency.GBP,
            to_currency=Currency.USD,
            rate=1.33,
            commission=0.03
        )
        eur_to_gbp = ExchangeRate(
            from_currency=Currency.EUR,
            to_currency=Currency.GBP,
            rate=0.83,
            commission=0.03
        )
        gbp_to_eur = ExchangeRate(
            from_currency=Currency.GBP,
            to_currency=Currency.EUR,
            rate=1.21,
            commission=0.03
        )
        await usd_to_eur.insert()
        await eur_to_usd.insert()

        await usd_to_gbp.insert()
        await gbp_to_usd.insert()

        await eur_to_gbp.insert()
        await gbp_to_eur.insert()
