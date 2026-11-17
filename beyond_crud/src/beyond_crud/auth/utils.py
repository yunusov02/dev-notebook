from datetime import datetime, timedelta, timezone
import logging
import uuid

import bcrypt
import jwt
from beyond_crud.settings import settings


def generate_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        # bcrypt rejects passwords longer than 72 bytes
        return False




def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:

    payload = {
        "user": user_data,
        "refresh": refresh,
        "exp": datetime.now(timezone.utc) + (expiry if expiry is not None else timedelta(minutes=60)),
        "jti": str(uuid.uuid4())
    }

    token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token

def decode_token(token: str) -> dict | None:

    try:
        payload = jwt.decode(
            token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        return payload

    except jwt.PyJWTError as jwterror:
        logging.exception(jwterror)
        return None

    except Exception as e:
        logging.exception(e)
        return None

