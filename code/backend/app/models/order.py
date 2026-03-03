"""
订单数据模型
"""
from datetime import date
from sqlalchemy import Column, BigInteger, String, SmallInteger, Text, DECIMAL, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Order(BaseModel):
    """订单表"""
    __tablename__ = "orders"

    # 订单号
    order_no = Column(String(32), nullable=False, unique=True, comment="订单号")

    # 关联关系
    clothing_id = Column(BigInteger, ForeignKey('clothings.id'), nullable=False, comment="衣物ID")
    renter_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, comment="租赁方ID")
    owner_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, comment="出租方ID")

    # 租赁信息
    start_date = Column(DateTime, nullable=False, comment="开始日期")
    end_date = Column(DateTime, nullable=False, comment="结束日期")
    rent_days = Column(SmallInteger, nullable=False, comment="租赁天数")

    # 金额
    daily_rent = Column(DECIMAL(10, 2), nullable=False, comment="日租金")
    rent_amount = Column(DECIMAL(10, 2), nullable=False, comment="租金总额")
    deposit = Column(DECIMAL(10, 2), nullable=False, comment="押金")
    delivery_fee = Column(DECIMAL(10, 2), default=0, comment="运费")
    total_amount = Column(DECIMAL(10, 2), nullable=False, comment="订单总额")

    # 订单状态流转
    # 1待确认 2待发货 3待收货 4租赁中 5待归还 6已完成 7已取消 8售后中
    status = Column(SmallInteger, nullable=False, comment="订单状态")

    # 时间节点
    confirm_time = Column(DateTime, nullable=True, comment="确认时间")
    ship_time = Column(DateTime, nullable=True, comment="发货时间")
    receive_time = Column(DateTime, nullable=True, comment="收货时间")
    return_time = Column(DateTime, nullable=True, comment="归还时间")
    complete_time = Column(DateTime, nullable=True, comment="完成时间")
    cancel_time = Column(DateTime, nullable=True, comment="取消时间")

    # 物流信息
    express_company = Column(String(50), nullable=True, comment="快递公司")
    express_no = Column(String(50), nullable=True, comment="快递单号")

    # 租赁方评价
    renter_rating = Column(SmallInteger, nullable=True, comment="租赁方评分")
    renter_comment = Column(Text, nullable=True, comment="租赁方评价")
    renter_images = Column(Text, nullable=True, comment="租赁方评价图片JSON")

    # 出租方评价
    owner_rating = Column(SmallInteger, nullable=True, comment="出租方评分")
    owner_comment = Column(Text, nullable=True, comment="出租方评价")
    owner_images = Column(Text, nullable=True, comment="出租方评价图片JSON")

    # 售后
    dispute_reason = Column(String(100), nullable=True, comment="争议原因")
    dispute_desc = Column(Text, nullable=True, comment="争议描述")
    dispute_images = Column(Text, nullable=True, comment="争议图片JSON")
    # 0无争议 1处理中 2已解决
    dispute_status = Column(SmallInteger, default=0, comment="争议状态")
    dispute_result = Column(Text, nullable=True, comment="争议结果")
    deposit_refund = Column(DECIMAL(10, 2), nullable=True, comment="实际退还押金")

    # 关联关系
    clothing = relationship("Clothing", backref="orders")
    renter = relationship("User", foreign_keys=[renter_id], backref="rent_orders")
    owner = relationship("User", foreign_keys=[owner_id], backref="owner_orders")

    # 索引
    __table_args__ = (
        Index('idx_order_no', 'order_no'),
        Index('idx_renter', 'renter_id'),
        Index('idx_owner', 'owner_id'),
        Index('idx_clothing', 'clothing_id'),
        Index('idx_status', 'status'),
        Index('idx_created', 'created_at'),
        Index('idx_renter_status', 'renter_id', 'status'),
    )
