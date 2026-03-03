"""
衣物相关Schema
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class ClothingBase(BaseModel):
    """衣物基础模型"""
    name: str = Field(..., description="衣物名称", max_length=100)
    brand: Optional[str] = Field(None, description="品牌", max_length=50)
    category: str = Field(..., description="分类", max_length=50)
    size: str = Field(..., description="尺码", pattern=r'^(XS|S|M|L|XL|XXL)$')
    condition: str = Field(..., description="新旧程度")
    description: Optional[str] = Field(None, description="描述")
    daily_rent: float = Field(..., description="日租金", gt=0)
    deposit: float = Field(..., description="押金", ge=0)
    min_rent_days: int = Field(default=1, description="最短租期", ge=1)
    max_rent_days: int = Field(default=7, description="最长租期", ge=1)
    require_wash: bool = Field(default=True, description="是否需要清洗")
    delivery_type: int = Field(default=1, description="配送方式 1快递到付 2顺丰包邮 3自提", ge=1, le=3)
    delivery_fee: float = Field(default=0, description="运费", ge=0)

    @field_validator('max_rent_days')
    @classmethod
    def validate_max_days(cls, v, info):
        """验证最长租期"""
        if 'min_rent_days' in info.data and v < info.data['min_rent_days']:
            raise ValueError('最长租期不能小于最短租期')
        return v


class ClothingCreate(ClothingBase):
    """衣物创建模型"""
    images: List[str] = Field(..., description="图片URL列表", min_length=3, max_length=5)

    @field_validator('images')
    @classmethod
    def validate_images(cls, v):
        """验证图片数量"""
        if len(v) < 3 or len(v) > 5:
            raise ValueError('图片数量必须在3-5张之间')
        return v


class ClothingUpdate(BaseModel):
    """衣物更新模型"""
    name: Optional[str] = Field(None, description="衣物名称", max_length=100)
    brand: Optional[str] = Field(None, description="品牌", max_length=50)
    category: Optional[str] = Field(None, description="分类", max_length=50)
    size: Optional[str] = Field(None, description="尺码", pattern=r'^(XS|S|M|L|XL|XXL)$')
    condition: Optional[str] = Field(None, description="新旧程度")
    description: Optional[str] = Field(None, description="描述")
    daily_rent: Optional[float] = Field(None, description="日租金", gt=0)
    deposit: Optional[float] = Field(None, description="押金", ge=0)
    min_rent_days: Optional[int] = Field(None, description="最短租期", ge=1)
    max_rent_days: Optional[int] = Field(None, description="最长租期", ge=1)
    require_wash: Optional[bool] = Field(None, description="是否需要清洗")
    delivery_type: Optional[int] = Field(None, description="配送方式", ge=1, le=3)
    delivery_fee: Optional[float] = Field(None, description="运费", ge=0)
    images: Optional[List[str]] = Field(None, description="图片URL列表")


class ClothingListQuery(BaseModel):
    """衣物列表查询模型"""
    category: Optional[str] = Field(None, description="分类筛选")
    size: Optional[str] = Field(None, description="尺码筛选")
    brand: Optional[str] = Field(None, description="品牌筛选")
    min_price: Optional[float] = Field(None, description="最低价格", ge=0)
    max_price: Optional[float] = Field(None, description="最高价格", ge=0)
    keyword: Optional[str] = Field(None, description="关键词搜索")
    page: int = Field(default=1, description="页码", ge=1)
    page_size: int = Field(default=20, description="每页数量", ge=1, le=100)
    sort_by: Optional[str] = Field(None, description="排序字段 created_at/price/rating/rent_count")
    sort_order: str = Field(default="desc", description="排序顺序 asc/desc")


class ClothingResponse(ClothingBase):
    """衣物响应模型"""
    id: int = Field(..., description="衣物ID")
    owner_id: int = Field(..., description="出租方ID")
    images: List[str] = Field(..., description="图片URL列表")
    status: int = Field(default=1, description="状态")
    rent_count: int = Field(default=0, description="租赁次数")
    total_revenue: float = Field(default=0.0, description="总收益")
    rating_avg: Optional[float] = Field(None, description="平均评分")
    rating_count: int = Field(default=0, description="评分数量")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")


class ClothingDetailResponse(ClothingResponse):
    """衣物详情响应模型"""
    owner: Optional[dict] = Field(None, description="出租方信息简略")
