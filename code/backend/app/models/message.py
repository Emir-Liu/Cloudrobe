"""
消息数据模型
"""
from sqlalchemy import Column, BigInteger, SmallInteger, String, Text, ForeignKey, Boolean, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Message(BaseModel):
    """消息表"""
    __tablename__ = "messages"

    # 接收用户
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, comment="接收用户ID")

    # 消息类型 1订单通知 2系统通知 3互动消息
    type = Column(SmallInteger, nullable=False, comment="消息类型")

    # 消息内容
    title = Column(String(100), nullable=False, comment="消息标题")
    content = Column(Text, nullable=True, comment="消息内容")

    # 附加数据(JSON格式)
    data = Column(Text, nullable=True, comment="附加数据JSON")

    # 状态
    is_read = Column(Boolean, default=False, comment="是否已读")

    # 关联关系
    user = relationship("User", backref="messages")

    # 索引
    __table_args__ = (
        Index('idx_user', 'user_id'),
        Index('idx_read', 'is_read'),
        Index('idx_type', 'type'),
        Index('idx_created', 'created_at'),
    )
