from fastapi import APIRouter

from src.api.v1.endpoints import auth, urls, users
from src.core.config import settings

router = APIRouter(prefix=f"/{settings.API_V1_STR}")
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(urls.router, prefix="/urls", tags=["URLs"])
