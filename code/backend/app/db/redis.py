"""
Redis客户端管理
"""
from typing import AsyncGenerator
from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

from app.core.config import settings

# 创建连接池
pool = ConnectionPool.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True,
    password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
    db=settings.REDIS_DB,
    max_connections=20
)


async def get_redis() -> AsyncGenerator[Redis, None]:
    """
    获取Redis客户端
    用于FastAPI依赖注入
    """
    redis = Redis(connection_pool=pool)
    try:
        yield redis
    finally:
        await redis.close()
