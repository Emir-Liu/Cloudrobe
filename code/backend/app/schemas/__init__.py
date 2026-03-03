"""
Pydantic Schemas
"""
from app.schemas.base import Response, PageResponse, ErrorDetail, ErrorResponse
from app.schemas.user import (
    UserBase, UserCreate, UserUpdate, UserVerify, UserResponse,
    UserLogin, UserWechatLogin, SendSmsRequest
)
from app.schemas.clothing import (
    ClothingBase, ClothingCreate, ClothingUpdate, ClothingListQuery,
    ClothingResponse, ClothingDetailResponse
)
from app.schemas.order import (
    OrderBase, OrderCreate, OrderUpdate, OrderListQuery,
    OrderResponse, OrderDetailResponse, OrderRatingCreate, OrderDisputeCreate
)
from app.schemas.message import MessageResponse, MessageListQuery

__all__ = [
    # Base
    'Response', 'PageResponse', 'ErrorDetail', 'ErrorResponse',
    # User
    'UserBase', 'UserCreate', 'UserUpdate', 'UserVerify', 'UserResponse',
    'UserLogin', 'UserWechatLogin', 'SendSmsRequest',
    # Clothing
    'ClothingBase', 'ClothingCreate', 'ClothingUpdate', 'ClothingListQuery',
    'ClothingResponse', 'ClothingDetailResponse',
    # Order
    'OrderBase', 'OrderCreate', 'OrderUpdate', 'OrderListQuery',
    'OrderResponse', 'OrderDetailResponse', 'OrderRatingCreate', 'OrderDisputeCreate',
    # Message
    'MessageResponse', 'MessageListQuery',
]
