from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    SUPPLIER = "supplier"
    FORWARDER = "forwarder"
    BUYER = "buyer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=2)
    company_name: Optional[str] = None
    phone: str = Field(..., regex=r'^\+?[1-9]\d{1,14}$')
    role: UserRole
    gstin: Optional[str] = None
    country: str = Field(default="IN", max_length=2)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    company_name: Optional[str]
    phone: str
    role: UserRole
    gstin: Optional[str]
    country: str
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse

class TokenPayload(BaseModel):
    sub: str
    role: str
    exp: datetime
