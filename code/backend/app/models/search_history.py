"""
搜索历史数据模型
"""
from sqlalchemy import Column, BigInteger, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class SearchHistory(BaseModel):
    """搜索历史表"""
    __tablename__ = "search_history"

    # 关联关系
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, comment="用户ID")

    # 搜索关键词
    keyword = Column(String(100), nullable=False, comment="搜索关键词")

    # 关联关系
    user = relationship("User", backref="search_history")

    # 索引
    __table_args__ = (
        Index('idx_user', 'user_id'),
        Index('idx_created', 'created_at'),
    )
