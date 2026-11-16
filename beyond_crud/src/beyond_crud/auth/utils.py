from datetime import datetime, timedelta
import logging
import uuid

import jwt
from passlib.context import CryptContext
from beyond_crud.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)




def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    
    payload = {
        "user": user_data,
        "refresh": refresh,
        "exp": datetime.now() + (expiry if expiry is not None else timedelta(minutes=60)),
        "jti": str(uuid.uuid4())
    }
    
    token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token

def decode_token(token: str) -> dict:
    
    try:
        payload = jwt.decode(
            token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        return payload
    
    except jwt.PyJWTError as jwterror:
        logging.exeption(jwterror)
        return None
    
    except Exception as e:
        logging.exception(e)
        return None
    

