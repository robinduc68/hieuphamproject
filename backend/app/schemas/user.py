from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class UserRegister(BaseModel):
    email:     EmailStr
    full_name: Optional[str] = None
    password:  str
    phone:     Optional[str] = None

class UserLogin(BaseModel):
    email:    EmailStr
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone:     Optional[str] = None
    address:   Optional[str] = None

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:        int
    email:     str
    full_name: Optional[str] = None
    phone:     Optional[str] = None
    address:   Optional[str] = None
    is_active: bool
    is_admin:  bool
    created_at: datetime

class TokenOut(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    user:         UserOut
