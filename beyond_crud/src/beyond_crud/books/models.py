



from datetime import datetime
from typing import Optional
import uuid

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Field, SQLModel, Column




class Book(SQLModel, table=True):
    
    __tablename__ = "books"
    
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
        ),
        default_factory=uuid.uuid4
    )
    
    
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="user.uid")
    
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=datetime.now
        )
    )
    
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            default=datetime.now,
            onupdate=datetime.now
        )
    )
    
    
    def __repr__(self) -> str:
        return f"Book(uid={self.uid}, title={self.title}, author={self.author})"
    
    
