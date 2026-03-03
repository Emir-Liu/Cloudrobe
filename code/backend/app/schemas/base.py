"""
基础Schema
"""
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar('T')


class Response(BaseModel, Generic[T]):
    """通用响应模型"""
    code: int = Field(default=0, description="状态码 0表示成功")
    message: str = Field(default="success", description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")


class PageResponse(BaseModel, Generic[T]):
    """分页响应模型"""
    items: list[T] = Field(default=[], description="数据列表")
    total: int = Field(default=0, description="总数")
    page: int = Field(default=1, description="当前页码")
    page_size: int = Field(default=20, description="每页数量")


class ErrorDetail(BaseModel):
    """错误详情"""
    field: str = Field(description="字段名")
    message: str = Field(description="错误消息")


class ErrorResponse(BaseModel):
    """错误响应模型"""
    code: int = Field(description="错误码")
    message: str = Field(description="错误消息")
    errors: Optional[list[ErrorDetail]] = Field(default=None, description="错误详情列表")
