from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from pydantic import EmailStr

from src import schemas
from src.api.v1.deps import get_current_active_superuser, get_current_active_user
from src.core.security import get_password_hash
from src.models import User
from src.utils import paginate
from src.utils.types import PaginationDict

router = APIRouter()


def user_not_found_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="The user with this username does not exist",
    )


@router.get("/me")
def get_current_user(user: User = Depends(get_current_active_user)) -> User:
    """Get current active user details."""
    return user


@router.patch("/me", response_model=schemas.User)
async def update_current_user(
    password: Optional[str] = Body(None),
    email: Optional[EmailStr] = Body(None),
    user: User = Depends(get_current_active_user),
) -> User:
    """Update current user using provided data."""
    if password is not None:
        user.hashed_password = get_password_hash(password)
    if email is not None:
        user.email = email
    await user.save_changes()
    return user


@router.get("/", response_model=schemas.Paginated[schemas.User])
async def get_users(
    paging: schemas.PaginationParams = Depends(),
    sorting: schemas.SortingParams = Depends(),
    superuser: User = Depends(get_current_active_superuser),
) -> "PaginationDict":
    return await paginate(User, paging, sorting)


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: schemas.UserCreate) -> User:
    """Create new user in the database."""
    user = await User.get_by_username(username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user associated with this username already exists",
        )
    data = user_in.dict()
    data["hashed_password"] = get_password_hash(data.pop("password"))
    return await User(**data).insert()


@router.get("/{username}", response_model=schemas.User)
async def get_user_by_username(username: str) -> User:
    """Get a specific user by username."""
    user = await User.get_by_username(username=username)
    if not user:
        raise user_not_found_error()
    return user


@router.patch("/{username}", response_model=schemas.User)
async def update_user_by_username(
    username: str,
    user_in: schemas.UserUpdate,
) -> User:
    """Update a specific user by username."""
    user = await User.get_by_username(username=username)
    if not user:
        raise user_not_found_error()
    update_data = user_in.dict(exclude_unset=True)
    await user.set(update_data)
    return user
