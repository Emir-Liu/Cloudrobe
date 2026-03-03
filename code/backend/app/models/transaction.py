"""
交易记录数据模型
"""
from sqlalchemy import Column, BigInteger, SmallInteger, String, DECIMAL, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Transaction(BaseModel):
    """交易记录表"""
    __tablename__ = "transactions"

    # 关联关系
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, comment="用户ID")
    order_id = Column(BigInteger, ForeignKey('orders.id'), nullable=True, comment="订单ID")

    # 交易类型 1租金 2押金 3退款 4提现
    type = Column(SmallInteger, nullable=False, comment="交易类型")

    # 金额
    amount = Column(DECIMAL(10, 2), nullable=False, comment="金额")
    balance_before = Column(DECIMAL(10, 2), nullable=True, comment="操作前余额")
    balance_after = Column(DECIMAL(10, 2), nullable=True, comment="操作后余额")

    # 描述
    description = Column(String(200), nullable=True, comment="描述")

    # 关联关系
    user = relationship("User", backref="transactions")
    order = relationship("Order", backref="transactions")

    # 索引
    __table_args__ = (
        Index('idx_user', 'user_id'),
        Index('idx_order', 'order_id'),
        Index('idx_type', 'type'),
        Index('idx_created', 'created_at'),
    )
