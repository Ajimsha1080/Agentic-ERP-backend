"""User-related schemas."""

from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime
from uuid import UUID

from .base import UUIDResponse, PaginationParams, PaginatedResponse


class UserCreate(BaseModel):
    """User creation schema.

    Args:
        email: User email
        password: User password
        first_name: First name
        last_name: Last name
        organization_id: Organization ID
        role_id: Role ID (optional)
        workspace_id: Workspace ID (optional)
    """

    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="User password")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    organization_id: UUID = Field(..., description="Organization ID")
    role_id: Optional[UUID] = Field(None, description="Role ID")
    workspace_id: Optional[UUID] = Field(None, description="Workspace ID")
    phone: Optional[str] = Field(None, max_length=50, description="Phone number")
    title: Optional[str] = Field(None, max_length=255, description="Job title")


class UserUpdate(BaseModel):
    """User update schema.

    Args:
        first_name: First name
        last_name: Last name
        avatar_url: Avatar URL
        title: Job title
        phone: Phone number
        location: Location
    """

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)
    title: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None


class UserLogin(BaseModel):
    """User login schema.

    Args:
        email: User email
        password: User password
    """

    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")


class UserResponse(BaseModel):
    """User response schema.

    Args:
        id: User ID
        email: User email
        first_name: First name
        last_name: Last name
        full_name: Full name
        avatar_url: Avatar URL
        title: Job title
        phone: Phone number
        location: Location
        is_verified: Whether user is verified
        is_active: Whether user is active
        created_at: Creation timestamp
    """

    id: UUID
    email: str
    first_name: str
    last_name: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    title: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    is_verified: bool
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreateResponse(UUIDResponse):
    """User creation response.

    Inherits from UUIDResponse.
    """

    user: UserResponse


class Token(BaseModel):
    """Authentication token.

    Args:
        access_token: Access token
        refresh_token: Refresh token
        token_type: Token type
        expires_in: Expiration time in seconds
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefresh(BaseModel):
    """Token refresh schema.

    Args:
        refresh_token: Refresh token
    """

    refresh_token: str


class UserRoleResponse(BaseModel):
    """User role response.

    Args:
        id: Role ID
        name: Role name
        slug: Role slug
        description: Role description
        display_name: Display name
        role_type: Role type
    """

    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    display_name: Optional[str] = None
    role_type: str
