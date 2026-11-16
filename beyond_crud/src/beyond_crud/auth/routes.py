
from datetime import timedelta

from beyond_crud.auth.models import User
from beyond_crud.auth.schemas import UserCreateModel, UserLoginModel
from beyond_crud.auth.service import UserService
from beyond_crud.db.main import get_session
from beyond_crud.auth.utils import create_access_token, verify_password
from fastapi import APIRouter, HTTPException
from fastapi import status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession


auth_router = APIRouter()

user_service = UserService()

@auth_router.post(
    "/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session)
):
    
    email = user_data.email
    
    user_exists = await user_service.check_user_exists(email, session)
    
    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    
    user = await user_service.create_user(user_data, session)
    
    return user




@auth_router.post(
    "login",
    status_code=status.HTTP_200_OK
)
async def login_users(
    user_login_model: UserLoginModel,
    session: AsyncSession = Depends(get_session)
):
    
    email = user_login_model.email
    password = user_login_model.password
    
    user = await user_service.get_user_by_email(email, session)
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    access_token = create_access_token(user.model_dump(), refresh=False)
    refresh_token = create_access_token(user.model_dump(), refresh=True, expiry=timedelta(days=30))
    
    return JSONResponse(content={"access_token": access_token, "refresh_token": refresh_token})
    
    