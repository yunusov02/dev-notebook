from beyond_crud.auth.models import User
from beyond_crud.db.main import get_session
from beyond_crud.db.redis import token_in_blocklist
from fastapi import Request
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import status
from fastapi.exceptions import HTTPException
from beyond_crud.auth.utils import decode_token
from sqlalchemy.ext.asyncio import AsyncSession

from beyond_crud.auth.service import UserService

user_service = UserService()
class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error: bool = True):
        
        super().__init__(auto_error=auto_error)
        
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        token = credentials.credentials
        
        if not await self.valid_token(token):
            
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired",
                    "resolution": "Please get a new token"
                }
            )
            
        return token
    
    
    async def valid_token(self, token: str) -> bool:
        
        token_data = decode_token(token)

        if token_data is None:
            return False
        
        if await token_in_blocklist(token_data.get('jti')):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired",
                    "resolution": "Please get a new token"
                }
            )

        self.verify_token_data(token_data)
        
        return True
    
    
    def verify_token_data(self, token_data: dict):
        
        raise NotImplementedError("Please override this method")



class AccessTokenBearer(TokenBearer):
    
    def verify_token_data(self, token_data: dict):
        
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired",
                    "resolution": "Please get a new token"
                }
            )


class RefreshTokenBearer(TokenBearer):
    
    def verify_token_data(self, token_data: dict):
        
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired",
                    "resolution": "Please get a new token"
                }
            )





async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
):
    
    user_email = token_details['user']['email'] 
    
    return await user_service.get_user_by_email(user_email, session)



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

