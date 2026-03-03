"""
衣物数据模型
"""
from sqlalchemy import Column, BigInteger, String, SmallInteger, Text, DECIMAL, Boolean, DateTime, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Clothing(BaseModel):
    """衣物表"""
    __tablename__ = "clothings"

    # 所属关系
    owner_id = Column(BigInteger, nullable=False, comment="出租方ID")

    # 基本信息
    name = Column(String(100), nullable=False, comment="衣物名称")
    brand = Column(String(50), nullable=True, comment="品牌")
    category = Column(String(50), nullable=False, comment="分类")
    size = Column(String(10), nullable=False, comment="尺码 XS/S/M/L/XL/XXL")
    condition = Column(String(20), nullable=False, comment="新旧程度")

    # 描述
    description = Column(Text, nullable=True, comment="描述")

    # 图片(JSON格式)
    images = Column(Text, nullable=False, comment="图片URL数组JSON")

    # 价格
    daily_rent = Column(DECIMAL(10, 2), nullable=False, comment="日租金")
    deposit = Column(DECIMAL(10, 2), nullable=False, comment="押金")

    # 租赁规则
    min_rent_days = Column(SmallInteger, default=1, comment="最短租期")
    max_rent_days = Column(SmallInteger, default=7, comment="最长租期")
    require_wash = Column(Boolean, default=True, comment="是否需要清洗")

    # 配送
    delivery_type = Column(SmallInteger, default=1, comment="配送方式 1快递到付 2顺丰包邮 3自提")
    delivery_fee = Column(DECIMAL(10, 2), default=0, comment="运费")

    # 状态
    status = Column(SmallInteger, default=1, comment="状态 1可租 2租赁中 3已下架")

    # 统计信息
    rent_count = Column(BigInteger, default=0, comment="租赁次数")
    total_revenue = Column(DECIMAL(10, 2), default=0, comment="总收益")

    # 评分
    rating_avg = Column(DECIMAL(3, 2), nullable=True, comment="平均评分")
    rating_count = Column(BigInteger, default=0, comment="评分数量")

    # 关联关系
    owner = relationship("User", backref="clothings")

    # 索引
    __table_args__ = (
        Index('idx_owner', 'owner_id'),
        Index('idx_category', 'category'),
        Index('idx_size', 'size'),
        Index('idx_status', 'status'),
        Index('idx_price', 'daily_rent'),
        Index('idx_created', 'created_at'),
    )
