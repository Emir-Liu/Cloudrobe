"""
用户服务
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.message_repository import MessageRepository
from app.models.message import Message


class UserService:
    """用户服务"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(User, session)
        self.message_repo = MessageRepository(Message, session)

    async def get_user(self, user_id: int) -> Optional[User]:
        """
        获取用户信息

        Args:
            user_id: 用户ID

        Returns:
            用户实例或None
        """
        return await self.user_repo.get_by_id(user_id)

    async def update_user_profile(
        self,
        user_id: int,
        nickname: Optional[str] = None,
        avatar: Optional[str] = None,
        gender: Optional[int] = None,
        height: Optional[int] = None,
        weight: Optional[int] = None,
        bio: Optional[str] = None,
        size_preferences: Optional[str] = None
    ) -> Optional[User]:
        """
        更新用户资料

        Args:
            user_id: 用户ID
            nickname: 昵称
            avatar: 头像
            gender: 性别
            height: 身高
            weight: 体重
            bio: 个人简介
            size_preferences: 尺码偏好

        Returns:
            更新后的用户实例
        """
        return await self.user_repo.update_user(
            user_id,
            nickname=nickname,
            avatar=avatar,
            gender=gender,
            height=height,
            weight=weight,
            bio=bio,
            size_preferences=size_preferences
        )

    async def verify_real_name(
        self,
        user_id: int,
        id_card_name: str,
        id_card_number: str,
        id_card_front: str,
        id_card_back: str
    ) -> Optional[User]:
        """
        实名认证

        Args:
            user_id: 用户ID
            id_card_name: 身份证姓名
            id_card_number: 身份证号
            id_card_front: 身份证正面URL
            id_card_back: 身份证背面URL

        Returns:
            更新后的用户实例

        Raises:
            ValueError: 用户已认证或参数错误
        """
        # 检查是否已认证
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")

        if user.is_verified:
            raise ValueError("用户已实名认证")

        # 更新实名信息
        verified_user = await self.user_repo.verify_user(
            user_id,
            id_card_name,
            id_card_number,
            id_card_front,
            id_card_back
        )

        # 发送系统通知
        await self.message_repo.send_system_notification(
            user_id=user_id,
            title="实名认证成功",
            content="恭喜您完成实名认证,现在可以发布衣物啦!"
        )

        return verified_user

    async def get_credit_info(self, user_id: int) -> dict:
        """
        获取信用信息

        Args:
            user_id: 用户ID

        Returns:
            信用信息字典
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return {}

        return {
            "credit_score": user.credit_score,
            "credit_level": user.credit_level or "普通",
        }

    async def update_credit_score(
        self,
        user_id: int,
        delta: int,
        reason: str
    ) -> Optional[User]:
        """
        更新信用积分

        Args:
            user_id: 用户ID
            delta: 积分变化量
            reason: 变更原因

        Returns:
            更新后的用户实例
        """
        user = await self.user_repo.update_credit_score(user_id, delta)

        # 发送通知
        if user:
            title = "信用积分变更" if delta > 0 else "信用积分扣除"
            content = f"{reason},积分{'+' if delta > 0 else ''}{delta}"
            await self.message_repo.send_system_notification(
                user_id=user_id,
                title=title,
                content=content
            )

        return user

    async def get_balance(self, user_id: int) -> dict:
        """
        获取余额信息

        Args:
            user_id: 用户ID

        Returns:
            余额信息字典
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return {}

        return {
            "balance": float(user.balance),
        }

    async def recharge(
        self,
        user_id: int,
        amount: float,
        description: str = "余额充值"
    ) -> Optional[User]:
        """
        余额充值

        Args:
            user_id: 用户ID
            amount: 充值金额
            description: 描述

        Returns:
            更新后的用户实例
        """
        if amount <= 0:
            raise ValueError("充值金额必须大于0")

        user = await self.user_repo.update_balance(user_id, amount)

        # TODO: 创建交易记录

        return user

    async def withdraw(
        self,
        user_id: int,
        amount: float,
        description: str = "余额提现"
    ) -> Optional[User]:
        """
        余额提现

        Args:
            user_id: 用户ID
            amount: 提现金额
            description: 描述

        Returns:
            更新后的用户实例
        """
        if amount <= 0:
            raise ValueError("提现金额必须大于0")

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("用户不存在")

        if float(user.balance) < amount:
            raise ValueError("余额不足")

        updated_user = await self.user_repo.update_balance(user_id, -amount)

        # TODO: 创建交易记录

        return updated_user
