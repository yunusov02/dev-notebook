


from datetime import datetime
import uuid

from pydantic import BaseModel, Field, field_validator


class UserCreateModel(BaseModel):
    first_name: str =Field(max_length=25)
    last_name:  str =Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str  = Field(min_length=6)

    @field_validator("password")
    @classmethod
    def password_fits_bcrypt(cls, value: str) -> str:
        # bcrypt only accepts passwords up to 72 bytes
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 bytes long")
        return value


class UserModel(BaseModel):
    """Public view of a user — never exposes the password hash."""
    uid: uuid.UUID
    username: str
    email: str
    first_name: str | None
    last_name: str | None
    role: str
    is_verified: bool
    created_at: datetime


class UserLoginModel(BaseModel):

    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
