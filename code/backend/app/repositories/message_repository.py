"""
消息Repository
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message
from app.repositories.base_repository import BaseRepository


class MessageRepository(BaseRepository[Message]):
    """消息Repository"""

    async def get_user_messages(
        self,
        user_id: int,
        message_type: Optional[int] = None,
        is_read: Optional[bool] = None,
        **kwargs
    ) -> List[Message]:
        """
        获取用户消息列表

        Args:
            user_id: 用户ID
            message_type: 消息类型
            is_read: 是否已读
            **kwargs: 其他参数

        Returns:
            消息列表
        """
        filters = {'user_id': user_id}
        if message_type is not None:
            filters['type'] = message_type
        if is_read is not None:
            filters['is_read'] = is_read

        return await self.get_multi(
            filters=filters,
            order_by='created_at',
            order_direction='desc',
            **kwargs
        )

    async def create_message(
        self,
        user_id: int,
        message_type: int,
        title: str,
        content: Optional[str] = None,
        data: Optional[str] = None,
        **kwargs
    ) -> Message:
        """
        创建消息

        Args:
            user_id: 用户ID
            message_type: 消息类型
            title: 消息标题
            content: 消息内容
            data: 附加数据
            **kwargs: 其他字段

        Returns:
            消息实例
        """
        return await self.create(
            user_id=user_id,
            type=message_type,
            title=title,
            content=content,
            data=data,
            is_read=False,
            **kwargs
        )

    async def mark_as_read(self, message_id: int) -> Optional[Message]:
        """
        标记消息为已读

        Args:
            message_id: 消息ID

        Returns:
            更新后的消息实例
        """
        return await self.update(message_id, is_read=True)

    async def mark_all_as_read(self, user_id: int) -> int:
        """
        标记用户所有消息为已读

        Args:
            user_id: 用户ID

        Returns:
            更新的消息数
        """
        from sqlalchemy import update

        result = await self.session.execute(
            update(Message)
            .where(Message.user_id == user_id, Message.is_read == False)
            .values(is_read=True)
        )
        await self.session.flush()
        return result.rowcount

    async def count_unread(self, user_id: int) -> int:
        """
        统计未读消息数

        Args:
            user_id: 用户ID

        Returns:
            未读消息数
        """
        return await self.count(
            filters={'user_id': user_id, 'is_read': False}
        )

    async def send_order_notification(
        self,
        user_id: int,
        title: str,
        content: str,
        order_id: int,
        **kwargs
    ) -> Message:
        """
        发送订单通知

        Args:
            user_id: 用户ID
            title: 标题
            content: 内容
            order_id: 订单ID
            **kwargs: 其他字段

        Returns:
            消息实例
        """
        import json

        data = json.dumps({'order_id': order_id}) if order_id else None

        return await self.create_message(
            user_id=user_id,
            message_type=1,  # 订单通知
            title=title,
            content=content,
            data=data,
            **kwargs
        )

    async def send_system_notification(
        self,
        user_id: int,
        title: str,
        content: str,
        **kwargs
    ) -> Message:
        """
        发送系统通知

        Args:
            user_id: 用户ID
            title: 标题
            content: 内容
            **kwargs: 其他字段

        Returns:
            消息实例
        """
        return await self.create_message(
            user_id=user_id,
            message_type=2,  # 系统通知
            title=title,
            content=content,
            **kwargs
        )
