

from datetime import datetime
import uuid

from sqlmodel import Column, Field, SQLModel
from sqlalchemy.dialects import postgresql as pg

class User(SQLModel, table=True):

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4
        )
    )
    username: str
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    
    role: str = Field(
        sa_column=Column(
            pg.VARCHAR,
            nullable=False,
            default="user"
        )
    )
    
    is_verified: bool = False
    email: str
    password_hash: str
    
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=datetime.now
        )
    )
    
    
    def __repr__(self):
        return f"User(username={self.username})"
    