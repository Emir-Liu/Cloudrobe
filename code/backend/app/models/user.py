"""
用户数据模型
"""
from typing import Optional, List
from sqlalchemy import Column, BigInteger, String, SmallInteger, Text, DECIMAL, Boolean, DateTime, Index
from app.models.base import BaseModel


class User(BaseModel):
    """用户表"""
    __tablename__ = "users"

    # 微信信息
    openid = Column(String(128), nullable=True, unique=True, comment="微信openid")
    unionid = Column(String(128), nullable=True, comment="微信unionid")

    # 基本信息
    phone = Column(String(20), nullable=True, unique=True, comment="手机号")
    nickname = Column(String(50), nullable=True, comment="昵称")
    avatar = Column(String(500), nullable=True, comment="头像URL")
    gender = Column(SmallInteger, default=0, comment="性别 0未知 1男 2女")
    height = Column(SmallInteger, nullable=True, comment="身高cm")
    weight = Column(SmallInteger, nullable=True, comment="体重kg")

    # 尺码偏好(JSON格式)
    size_preferences = Column(Text, nullable=True, comment="尺码偏好JSON")

    # 个人信息
    bio = Column(Text, nullable=True, comment="个人简介")

    # 信用信息
    credit_score = Column(BigInteger, default=0, comment="信用积分")
    credit_level = Column(String(20), nullable=True, comment="信用等级")

    # 财务信息
    balance = Column(DECIMAL(10, 2), default=0, comment="余额")

    # 实名认证
    is_verified = Column(Boolean, default=False, comment="是否实名认证")
    id_card_name = Column(String(50), nullable=True, comment="身份证姓名")
    id_card_number = Column(String(18), nullable=True, comment="身份证号")
    id_card_front = Column(String(500), nullable=True, comment="身份证正面URL")
    id_card_back = Column(String(500), nullable=True, comment="身份证背面URL")

    # 状态
    status = Column(SmallInteger, default=1, comment="状态 1正常 2冻结")

    # 最后登录时间
    last_login_at = Column(DateTime, nullable=True, comment="最后登录时间")

    # 索引
    __table_args__ = (
        Index('idx_phone', 'phone'),
        Index('idx_openid', 'openid'),
        Index('idx_credit_score', 'credit_score'),
        Index('idx_status', 'status'),
    )
