"""
订单相关Schema
"""
from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel, Field, field_validator


class OrderBase(BaseModel):
    """订单基础模型"""
    clothing_id: int = Field(..., description="衣物ID")
    start_date: date = Field(..., description="开始日期")
    end_date: date = Field(..., description="结束日期")

    @field_validator('end_date')
    @classmethod
    def validate_dates(cls, v, info):
        """验证日期范围"""
        if 'start_date' in info.data:
            start = info.data['start_date']
            if v <= start:
                raise ValueError('结束日期必须大于开始日期')
            # 计算天数
            days = (v - start).days + 1
            if days > 30:
                raise ValueError('单次租赁最多30天')
        return v


class OrderCreate(OrderBase):
    """订单创建模型"""


class OrderUpdate(BaseModel):
    """订单更新模型"""
    express_company: Optional[str] = Field(None, description="快递公司", max_length=50)
    express_no: Optional[str] = Field(None, description="快递单号", max_length=50)


class OrderListQuery(BaseModel):
    """订单列表查询模型"""
    status: Optional[int] = Field(None, description="订单状态筛选")
    page: int = Field(default=1, description="页码", ge=1)
    page_size: int = Field(default=20, description="每页数量", ge=1, le=100)


class OrderResponse(BaseModel):
    """订单响应模型"""
    id: int = Field(..., description="订单ID")
    order_no: str = Field(..., description="订单号")
    clothing_id: int = Field(..., description="衣物ID")
    renter_id: int = Field(..., description="租赁方ID")
    owner_id: int = Field(..., description="出租方ID")

    # 租赁信息
    start_date: date = Field(..., description="开始日期")
    end_date: date = Field(..., description="结束日期")
    rent_days: int = Field(..., description="租赁天数")

    # 金额
    daily_rent: float = Field(..., description="日租金")
    rent_amount: float = Field(..., description="租金总额")
    deposit: float = Field(..., description="押金")
    delivery_fee: float = Field(..., description="运费")
    total_amount: float = Field(..., description="订单总额")

    # 订单状态
    status: int = Field(..., description="订单状态")

    # 时间节点
    confirm_time: Optional[datetime] = Field(None, description="确认时间")
    ship_time: Optional[datetime] = Field(None, description="发货时间")
    receive_time: Optional[datetime] = Field(None, description="收货时间")
    return_time: Optional[datetime] = Field(None, description="归还时间")
    complete_time: Optional[datetime] = Field(None, description="完成时间")

    # 物流信息
    express_company: Optional[str] = Field(None, description="快递公司")
    express_no: Optional[str] = Field(None, description="快递单号")

    # 评价信息
    renter_rating: Optional[int] = Field(None, description="租赁方评分")
    renter_comment: Optional[str] = Field(None, description="租赁方评价")
    owner_rating: Optional[int] = Field(None, description="出租方评分")
    owner_comment: Optional[str] = Field(None, description="出租方评价")

    # 售后信息
    dispute_status: int = Field(default=0, description="争议状态")
    deposit_refund: Optional[float] = Field(None, description="实际退还押金")

    created_at: datetime = Field(..., description="创建时间")


class OrderDetailResponse(OrderResponse):
    """订单详情响应模型"""
    clothing: Optional[dict] = Field(None, description="衣物信息简略")
    renter: Optional[dict] = Field(None, description="租赁方信息简略")
    owner: Optional[dict] = Field(None, description="出租方信息简略")


class OrderRatingCreate(BaseModel):
    """订单评价创建模型"""
    rating: int = Field(..., description="评分 1-5", ge=1, le=5)
    comment: Optional[str] = Field(None, description="评价内容", max_length=500)
    images: Optional[List[str]] = Field(None, description="评价图片", max_length=9)


class OrderDisputeCreate(BaseModel):
    """订单售后创建模型"""
    reason: str = Field(..., description="争议原因", max_length=100)
    description: str = Field(..., description="争议描述", max_length=500)
    images: Optional[List[str]] = Field(None, description="争议图片", max_length=9)
