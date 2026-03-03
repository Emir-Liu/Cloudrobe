"""
收藏数据模型
"""
from sqlalchemy import Column, BigInteger, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Favorite(BaseModel):
    """收藏表"""
    __tablename__ = "favorites"

    # 关联关系
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, comment="用户ID")
    clothing_id = Column(BigInteger, ForeignKey('clothings.id'), nullable=False, comment="衣物ID")

    # 关联关系
    user = relationship("User", backref="favorites")
    clothing = relationship("Clothing", backref="favorited_by")

    # 唯一约束和索引
    __table_args__ = (
        UniqueConstraint('user_id', 'clothing_id', name='uk_user_clothing'),
        Index('idx_user', 'user_id'),
        Index('idx_clothing', 'clothing_id'),
    )
