
from datetime import datetime, timedelta

from beyond_crud.db.redis import add_jti_to_blocklist
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from beyond_crud.auth.models import User
from beyond_crud.auth.schemas import UserCreateModel, UserLoginModel, UserModel
from beyond_crud.auth.service import UserService
from beyond_crud.db.main import get_session
from beyond_crud.auth.utils import create_access_token, verify_password
from beyond_crud.auth.dependencies import AccessTokenBearer, RefreshTokenBearer, get_current_user

auth_router = APIRouter()

user_service = UserService()

@auth_router.post(
    "/signup",
    response_model=UserModel,
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
    "/login",
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

    # Only JSON-serializable, non-sensitive data goes into the token
    token_user_data = {
        "email": user.email,
        "user_uid": str(user.uid),
        "role": user.role,
    }

    access_token = create_access_token(token_user_data, refresh=False)
    refresh_token = create_access_token(token_user_data, refresh=True, expiry=timedelta(days=30))

    return JSONResponse(content={"access_token": access_token, "refresh_token": refresh_token})




@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):

    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) < datetime.now():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": "This token is invalid or expired",
                "resolution": "Please get a new token"
            }
        )

    new_access_token = create_access_token(token_details["user"])

    return JSONResponse(content={"access_token": new_access_token})


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):

    jti = token_details.get('jti')

    await add_jti_to_blocklist(jti)

    return JSONResponse(content={"message": "Successfully logged out"}, status_code=status.HTTP_200_OK)





@auth_router.get("/me", response_model=UserModel)
async def get_me(
    user: User = Depends(get_current_user),
):
    return user

