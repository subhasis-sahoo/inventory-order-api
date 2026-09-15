from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=25,
        description="User Name"
    )
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True