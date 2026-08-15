# app/schemas/user.py
"""
ARGUS User Schemas
==================
Pydantic models for user-related API operations.
"""

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email:    EmailStr
    password: str
    role:     str = "readonly"

class UserResponse(BaseModel):
    id:       int
    username: str
    email:    str
    role:     str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    username:     str
    role:         str

class LoginRequest(BaseModel):
    username: str
    password: str