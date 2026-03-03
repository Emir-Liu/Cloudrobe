"""
用户相关Schema
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class UserBase(BaseModel):
    """用户基础模型"""
    nickname: Optional[str] = Field(None, description="昵称", max_length=50)
    avatar: Optional[str] = Field(None, description="头像URL", max_length=500)
    gender: Optional[int] = Field(0, description="性别 0未知 1男 2女", ge=0, le=2)
    height: Optional[int] = Field(None, description="身高cm", ge=100, le=250)
    weight: Optional[int] = Field(None, description="体重kg", ge=30, le=200)
    bio: Optional[str] = Field(None, description="个人简介")


class UserCreate(UserBase):
    """用户创建模型"""
    phone: Optional[str] = Field(None, description="手机号", pattern=r'^1[3-9]\d{9}$')
    openid: Optional[str] = Field(None, description="微信openid", max_length=128)
    unionid: Optional[str] = Field(None, description="微信unionid", max_length=128)


class UserUpdate(UserBase):
    """用户更新模型"""
    size_preferences: Optional[str] = Field(None, description="尺码偏好JSON")


class UserVerify(BaseModel):
    """实名认证模型"""
    id_card_name: str = Field(..., description="身份证姓名", max_length=50)
    id_card_number: str = Field(..., description="身份证号")
    id_card_front: str = Field(..., description="身份证正面URL", max_length=500)
    id_card_back: str = Field(..., description="身份证背面URL", max_length=500)


class UserResponse(UserBase):
    """用户响应模型"""
    id: int = Field(..., description="用户ID")
    phone: Optional[str] = Field(None, description="手机号(脱敏)")
    credit_score: int = Field(default=0, description="信用积分")
    credit_level: Optional[str] = Field(None, description="信用等级")
    balance: float = Field(default=0.0, description="余额")
    is_verified: bool = Field(default=False, description="是否实名认证")
    status: int = Field(default=1, description="状态")
    created_at: datetime = Field(..., description="创建时间")

    @field_validator('phone')
    @classmethod
    def mask_phone(cls, v: Optional[str]) -> Optional[str]:
        """手机号脱敏"""
        if v and len(v) == 11:
            return v[:3] + '****' + v[7:]
        return v


class UserLogin(BaseModel):
    """用户登录模型"""
    phone: str = Field(..., description="手机号", pattern=r'^1[3-9]\d{9}$')
    code: str = Field(..., description="验证码", pattern=r'^\d{6}$')


class UserWechatLogin(BaseModel):
    """微信登录模型"""
    code: str = Field(..., description="微信登录code")


class SendSmsRequest(BaseModel):
    """发送短信请求"""
    phone: str = Field(..., description="手机号", pattern=r'^1[3-9]\d{9}$')
