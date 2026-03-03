"""
数据访问层Repositories
"""
from app.repositories.base_repository import BaseRepository
from app.repositories.user_repository import UserRepository
from app.repositories.clothing_repository import ClothingRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.message_repository import MessageRepository

__all__ = [
    'BaseRepository',
    'UserRepository',
    'ClothingRepository',
    'OrderRepository',
    'MessageRepository',
]
