from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler, Limiter
from slowapi.errors import RateLimitExceeded
from src import api
from src.api.rate_limiter import limiter
from src.core.config import settings
from src.core.exceptions import EntityNotFoundException
from src.core.logging import configure_logging
from src.db import init_db


@asynccontextmanager
async def lifespan(application: FastAPI):  # noqa
    configure_logging()
    await init_db.init()
    yield


tags_metadata = [
    {
        "name": "Authentication",
        "description": "Get authentication token",
    },
    {
        "name": "Users",
        "description": "User registration and management",
    },
]

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Fast and reliable URL shortener powered by FastAPI and MongoDB.",
    # Set current documentation specs to v1
    openapi_url=f"/api/{settings.API_V1_STR}/openapi.json",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add the router responsible for all /api/ endpoint requests
app.include_router(api.router)
# Include redirection router in the main app

# Set all CORS enabled origins
if settings.CORS_ORIGINS:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        response = await call_next(request)
    except EntityNotFoundException as exc:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND, content={"detail": exc.message}
        )
    return response
