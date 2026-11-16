

import uuid

from beyond_crud.books.models import Book
from beyond_crud.books.schemas import BookCreateModel, BookUpdateModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import desc, select

class BookService:
    
    async def get_all_books(self, session: AsyncSession):
        
        st = select(Book).order_by(desc(Book.created_at))
        
        result = await session.execute(st)
        
        return result.scalars().all()
    
    
    async def get_book(self, book_uid: uuid.UUID, session: AsyncSession):
        
        st = select(Book).where(Book.uid == book_uid)
        
        result = await session.execute(st)
        
        return result.scalars().first()
    
    
    async def create_book(self, book: BookCreateModel, session: AsyncSession):
        
        book_data_dict = book.model_dump()
        
        book = Book(**book_data_dict)
        
        session.add(book)
        
        await session.commit()
        
        await session.refresh(book)
        
        return book
    
    
    async def update_book(self, book_uid: uuid.UUID, book_update: BookUpdateModel, session: AsyncSession):
        
        book = await self.get_book(book_uid, session)
        
        book_data_dict = book_update.model_dump()
        
        for key, value in book_data_dict.items():
            setattr(book, key, value)
        
        await session.commit()
        
        return book
    
    
    async def delete_book(self, book_uid: uuid.UUID, session: AsyncSession):
        
        book = await self.get_book(book_uid, session)
        
        await session.delete(book)
        
        await session.commit()
        

