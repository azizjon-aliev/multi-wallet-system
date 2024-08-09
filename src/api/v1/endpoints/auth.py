from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from src import schemas
from src.core import security
from src.core.config import settings
from src.models import User

router = APIRouter(
    responses={
        401: {
            "description": "Unauthorized, invalid credentials or access token",
        },
    },
)


@router.post(
    "/access-token",
    response_model=schemas.AuthToken,
    description="Retrieve an access token for the given username and password.",
)
async def generate_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> JSONResponse:
    """Get an access token for future requests."""
    user = await User.authenticate(
        username=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    expires_in = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return JSONResponse(
        content={
            "access_token": security.create_access_token(
                user.id,
                expires_delta=expires_in,
            ),
            "token_type": "bearer",
        },
    )


# @cbv(router)
# class BasicUserViews:
#     user: User = Depends(get_current_active_user)
#
#     @router.post(
#         "/api-key",
#         response_model=schemas.User,
#         status_code=status.HTTP_201_CREATED,
#     )
#     async def generate_new_api_key(self) -> User:
#         """Create a new API key for current user."""
#         self.user.api_key = create_api_key()
#         await self.user.save_changes()
#         return self.user
