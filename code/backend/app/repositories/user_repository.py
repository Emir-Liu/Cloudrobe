"""
用户Repository
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """用户Repository"""

    async def get_by_phone(self, phone: str) -> Optional[User]:
        """根据手机号获取用户"""
        return await self.get_by_field('phone', phone)

    async def get_by_openid(self, openid: str) -> Optional[User]:
        """根据微信openid获取用户"""
        return await self.get_by_field('openid', openid)

    async def create_user(
        self,
        phone: Optional[str] = None,
        openid: Optional[str] = None,
        unionid: Optional[str] = None,
        nickname: Optional[str] = None,
        avatar: Optional[str] = None,
        **kwargs
    ) -> User:
        """
        创建用户

        Args:
            phone: 手机号
            openid: 微信openid
            unionid: 微信unionid
            nickname: 昵称
            avatar: 头像
            **kwargs: 其他字段

        Returns:
            用户实例
        """
        return await self.create(
            phone=phone,
            openid=openid,
            unionid=unionid,
            nickname=nickname,
            avatar=avatar,
            **kwargs
        )

    async def update_user(
        self,
        user_id: int,
        nickname: Optional[str] = None,
        avatar: Optional[str] = None,
        gender: Optional[int] = None,
        height: Optional[int] = None,
        weight: Optional[int] = None,
        bio: Optional[str] = None,
        size_preferences: Optional[str] = None,
        **kwargs
    ) -> Optional[User]:
        """
        更新用户信息

        Args:
            user_id: 用户ID
            nickname: 昵称
            avatar: 头像
            gender: 性别
            height: 身高
            weight: 体重
            bio: 个人简介
            size_preferences: 尺码偏好
            **kwargs: 其他字段

        Returns:
            更新后的用户实例
        """
        return await self.update(
            user_id,
            nickname=nickname,
            avatar=avatar,
            gender=gender,
            height=height,
            weight=weight,
            bio=bio,
            size_preferences=size_preferences,
            **kwargs
        )

    async def verify_user(
        self,
        user_id: int,
        id_card_name: str,
        id_card_number: str,
        id_card_front: str,
        id_card_back: str
    ) -> Optional[User]:
        """
        用户实名认证

        Args:
            user_id: 用户ID
            id_card_name: 身份证姓名
            id_card_number: 身份证号
            id_card_front: 身份证正面
            id_card_back: 身份证背面

        Returns:
            更新后的用户实例
        """
        return await self.update(
            user_id,
            id_card_name=id_card_name,
            id_card_number=id_card_number,
            id_card_front=id_card_front,
            id_card_back=id_card_back,
            is_verified=True
        )

    async def update_credit_score(self, user_id: int, delta: int) -> Optional[User]:
        """
        更新信用积分

        Args:
            user_id: 用户ID
            delta: 积分变化量

        Returns:
            更新后的用户实例
        """
        user = await self.get_by_id(user_id)
        if user:
            new_score = user.credit_score + delta
            new_score = max(0, new_score)  # 积分不能为负

            # 计算信用等级
            credit_level = self._calculate_credit_level(new_score)

            return await self.update(
                user_id,
                credit_score=new_score,
                credit_level=credit_level
            )
        return None

    @staticmethod
    def _calculate_credit_level(score: int) -> str:
        """根据积分计算信用等级"""
        if score >= 100:
            return "信用之星"
        elif score >= 80:
            return "优秀"
        elif score >= 60:
            return "良好"
        else:
            return "普通"

    async def update_balance(self, user_id: int, amount: float) -> Optional[User]:
        """
        更新用户余额

        Args:
            user_id: 用户ID
            amount: 变化金额

        Returns:
            更新后的用户实例
        """
        user = await self.get_by_id(user_id)
        if user:
            new_balance = float(user.balance) + amount
            new_balance = max(0, new_balance)  # 余额不能为负
            return await self.update(user_id, balance=new_balance)
        return None

    async def get_users_by_status(self, status: int) -> List[User]:
        """根据状态获取用户列表"""
        return await self.get_multi(filters={'status': status})
