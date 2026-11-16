
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from .models import User
from .utils import generate_password_hash
from .schemas import UserCreateModel


class UserService:
    
    
    async def get_user_by_email(self, email: str, session: AsyncSession):
        
        st = select(User).where(User.email == email)
        
        result = await session.execute(st)
        
        return result.scalars().first()
    
    
    
    async def check_user_exists(self, email: str, session: AsyncSession):
        
        user = await self.get_user_by_email(email, session)
        
        return True if user else False
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        
        user_data_dict = user_data.model_dump()
        
        user = User(**user_data_dict)
        
        user.password_hash = generate_password_hash(user_data.password)
        
        session.add(user)
        
        await session.commit()
        
        await session.refresh(user)
        
        return user