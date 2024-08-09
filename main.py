import uvicorn

from src.core.config import settings


def run_dev_server() -> None:
    """Run the uvicorn server in development environment."""
    uvicorn.run(
        "src.server:app",
        host=settings.UVICORN_HOST,
        port=settings.UVICORN_PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    run_dev_server()
