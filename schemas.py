from pydantic import BaseModel
from typing import List, Optional

# --- Schemas cho License ---
class LicenseBase(BaseModel):
    key: str
    is_active: bool = True

class LicenseCreate(BaseModel):
    owner_id: int

class License(LicenseBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

# --- Schemas cho User ---
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    licenses: List[License] = []

    class Config:
        from_attributes = True

# --- Schemas cho Token (JWT) ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None