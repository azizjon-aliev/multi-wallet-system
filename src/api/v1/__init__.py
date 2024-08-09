from fastapi import APIRouter

from src.api.v1.endpoints import auth, urls, users, wallet, transaction
from src.core.config import settings

router = APIRouter(prefix=f"/{settings.API_V1_STR}")
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(wallet.router, prefix="/wallets", tags=["Wallets"])
router.include_router(transaction.router, prefix="/transactions", tags=["Transactions"])
