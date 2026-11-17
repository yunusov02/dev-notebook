from typing import AsyncGenerator

from sqlmodel import SQLModel, text

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker

from beyond_crud.settings import settings



engine = create_async_engine(settings.get_database_url(), echo=True)

async_session_factory = async_sessionmaker(
    engine, expire_on_commit=False
)

async def init_db():
    
    async with engine.begin() as conn:

        statement = text("select 'Hello world'")
        
        result = await conn.execute(statement)
        
        print(result.all())

        
        from beyond_crud.books.models import Book
        from beyond_crud.auth.models import User
                
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    
    async with async_session_factory() as session:
        yield session
        
        