

import redis.asyncio as aioredis

from beyond_crud.settings import settings


JWT_EXPIRY = 3600

token_blocklist = aioredis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0
)


async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="", ex=JWT_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    return await token_blocklist.exists(jti) > 0
