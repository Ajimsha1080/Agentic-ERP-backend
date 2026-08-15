"""Authentication routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta

from packages.database import get_db
from packages.config import get_settings
from packages.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
    get_current_user,
)
from packages.models import User, UserRole, UserRoleAssignment
from ..schemas.user import UserLogin, Token, TokenRefresh, UserCreate, UserResponse, UserCreateResponse

settings = get_settings()

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user.

    Args:
        user_data: User creation data
        db: Database session

    Returns:
        UserCreateResponse: Created user with token

    Raises:
        HTTPException: If email already exists or registration fails
    """
    # Check if user already exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Hash password
    password_hash = get_password_hash(user_data.password)

    # Create user
    user = User(
        email=user_data.email,
        password_hash=password_hash,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        organization_id=user_data.organization_id,
        is_verified=False,
        status="pending",
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Generate tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "id": user.id,
        "user": user
    }


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login user.

    Args:
        login_data: Login credentials
        db: Database session

    Returns:
        Token: Access and refresh tokens

    Raises:
        HTTPException: If credentials are invalid
    """
    # Get user
    result = await db.execute(
        select(User).where(User.email == login_data.email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Generate tokens
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.jwt_access_token_expire_minutes)
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=settings.jwt_refresh_token_expire_days)
    )

    # Update last login
    user.last_login_at = datetime.utcnow()
    await db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.jwt_access_token_expire_minutes * 60
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: TokenRefresh,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token.

    Args:
        refresh_data: Refresh token
        db: Database session

    Returns:
        Token: New access and refresh tokens

    Raises:
        HTTPException: If refresh token is invalid
    """
    # TODO: Implement token validation and refresh logic
    # This requires a proper token validator

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Refresh token functionality not yet implemented"
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information.

    Args:
        current_user: Current authenticated user

    Returns:
        UserResponse: User information

    Raises:
        HTTPException: If user not found
    """
    return current_user


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """Logout current user.

    Args:
        current_user: Current authenticated user

    Returns:
        dict: Success message
    """
    # TODO: Invalidate tokens, store logout events
    return {"message": "Successfully logged out"}


@router.post("/verify")
async def verify_user(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Verify user account.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        dict: Verification result
    """
    # TODO: Implement user verification logic
    # This would typically require a verification token sent via email

    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User verification not yet implemented"
    )
