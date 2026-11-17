from beyond_crud.auth.models import User
from beyond_crud.db.main import get_session
from beyond_crud.db.redis import token_in_blocklist
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import status
from fastapi.exceptions import HTTPException
from beyond_crud.auth.utils import decode_token
from sqlalchemy.ext.asyncio import AsyncSession

from beyond_crud.auth.service import UserService

user_service = UserService()


def invalid_token_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "error": "This token is invalid or expired",
            "resolution": "Please get a new token"
        }
    )


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):

        super().__init__(auto_error=auto_error)


    async def __call__(self, request: Request) -> dict | None:

        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)

        if credentials is None:
            return None

        token_data = decode_token(credentials.credentials)

        if token_data is None:
            raise invalid_token_exception()

        if await token_in_blocklist(token_data['jti']):
            raise invalid_token_exception()

        self.verify_token_data(token_data)

        return token_data


    def verify_token_data(self, token_data: dict):

        raise NotImplementedError("Please override this method")



class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict):

        if token_data['refresh']:
            raise invalid_token_exception()


class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict):

        if not token_data['refresh']:
            raise invalid_token_exception()





async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
) -> User:

    user_email = token_details['user']['email']

    user = await user_service.get_user_by_email(user_email, session)

    if user is None:
        raise invalid_token_exception()

    return user



class RoleChecker:

    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles


    async def __call__(self, current_user: User = Depends(get_current_user)):

        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "You are not authorized to perform this action",
                    "resolution": "Please get a new token"
                }
            )

        return True
