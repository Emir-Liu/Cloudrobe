"""
消息相关Schema
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    """消息响应模型"""
    id: int = Field(..., description="消息ID")
    user_id: int = Field(..., description="用户ID")
    type: int = Field(..., description="消息类型")
    title: str = Field(..., description="消息标题")
    content: Optional[str] = Field(None, description="消息内容")
    data: Optional[str] = Field(None, description="附加数据JSON")
    is_read: bool = Field(default=False, description="是否已读")
    created_at: datetime = Field(..., description="创建时间")


class MessageListQuery(BaseModel):
    """消息列表查询模型"""
    type: Optional[int] = Field(None, description="消息类型筛选")
    is_read: Optional[bool] = Field(None, description="是否已读筛选")
    page: int = Field(default=1, description="页码", ge=1)
    page_size: int = Field(default=20, description="每页数量", ge=1, le=100)
