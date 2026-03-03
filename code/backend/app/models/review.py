"""
评价数据模型
"""
from sqlalchemy import Column, BigInteger, SmallInteger, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Review(BaseModel):
    """评价表"""
    __tablename__ = "reviews"

    # 关联关系
    order_id = Column(BigInteger, ForeignKey('orders.id'), nullable=False, comment="订单ID")
    reviewer_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, comment="评价人ID")
    target_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, comment="被评价人ID")

    # 评价类型 1租赁方评价出租方 2出租方评价租赁方
    type = Column(SmallInteger, nullable=False, comment="评价类型")

    # 评分 1-5
    rating = Column(SmallInteger, nullable=False, comment="评分")
    comment = Column(Text, nullable=True, comment="评价内容")
    images = Column(Text, nullable=True, comment="评价图片JSON")

    # 关联关系
    order = relationship("Order", backref="reviews")
    reviewer = relationship("User", foreign_keys=[reviewer_id], backref="given_reviews")
    target = relationship("User", foreign_keys=[target_id], backref="received_reviews")

    # 索引
    __table_args__ = (
        Index('idx_reviewer', 'reviewer_id'),
        Index('idx_target', 'target_id'),
        Index('idx_order', 'order_id'),
    )
