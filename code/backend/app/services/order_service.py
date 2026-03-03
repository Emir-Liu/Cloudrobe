"""
订单服务
"""
from typing import Optional
from datetime import date, datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import Order
from app.models.clothing import Clothing
from app.models.user import User
from app.repositories.order_repository import OrderRepository
from app.repositories.clothing_repository import ClothingRepository
from app.repositories.user_repository import UserRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.order import OrderCreate, OrderRatingCreate, OrderDisputeCreate


class OrderService:
    """订单服务"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repo = OrderRepository(Order, session)
        self.clothing_repo = ClothingRepository(Clothing, session)
        self.user_repo = UserRepository(User, session)
        self.message_repo = MessageRepository.__bases__[0](None, session)

    def _generate_order_no(self) -> str:
        """生成订单号"""
        import time
        timestamp = int(time.time())
        random_str = str(timestamp)[-6:]
        return f"CR{timestamp}{random_str}"

    async def create_order(
        self,
        user_id: int,
        data: OrderCreate
    ) -> Order:
        """
        创建订单

        Args:
            user_id: 用户ID
            data: 订单数据

        Returns:
            创建的订单实例

        Raises:
            ValueError: 参数错误
        """
        # 获取衣物信息
        clothing = await self.clothing_repo.get_by_id(data.clothing_id)
        if not clothing:
            raise ValueError("衣物不存在")

        if clothing.status != 1:
            raise ValueError("衣物当前不可租")

        if clothing.owner_id == user_id:
            raise ValueError("不能租用自己的衣物")

        # 计算租赁天数
        rent_days = (data.end_date - data.start_date).days + 1

        # 验证租赁天数
        if rent_days < clothing.min_rent_days:
            raise ValueError(f"最少租期为{clothing.min_rent_days}天")
        if rent_days > clothing.max_rent_days:
            raise ValueError(f"最长租期为{clothing.max_rent_days}天")

        # 计算费用
        rent_amount = float(clothing.daily_rent) * rent_days
        deposit = float(clothing.deposit)
        delivery_fee = float(clothing.delivery_fee)
        total_amount = rent_amount + deposit + delivery_fee

        # 生成订单号
        order_no = self._generate_order_no()

        # 创建订单
        order = await self.order_repo.create_order(
            order_no=order_no,
            clothing_id=data.clothing_id,
            renter_id=user_id,
            owner_id=clothing.owner_id,
            start_date=data.start_date,
            end_date=data.end_date,
            rent_days=rent_days,
            daily_rent=float(clothing.daily_rent),
            rent_amount=rent_amount,
            deposit=deposit,
            delivery_fee=delivery_fee,
            total_amount=total_amount
        )

        # 发送通知给出租方
        await self.message_repo.send_order_notification(
            user_id=clothing.owner_id,
            title="新租赁订单",
            content=f"您有一笔新订单,请及时确认",
            order_id=order.id
        )

        return order

    async def get_order(self, order_id: int, user_id: int) -> Optional[Order]:
        """
        获取订单详情

        Args:
            order_id: 订单ID
            user_id: 用户ID

        Returns:
            订单实例或None

        Raises:
            ValueError: 无权限
        """
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            return None

        # 检查权限
        if order.renter_id != user_id and order.owner_id != user_id:
            raise ValueError("无权限查看该订单")

        return order

    async def list_orders(
        self,
        user_id: int,
        as_owner: bool = False,
        status: Optional[int] = None,
        page: int = 1,
        page_size: int = 20
    ) -> dict:
        """
        获取订单列表

        Args:
            user_id: 用户ID
            as_owner: 是否作为出租方查看
            status: 订单状态筛选
            page: 页码
            page_size: 每页数量

        Returns:
            分页结果字典
        """
        skip = (page - 1) * page_size

        if as_owner:
            orders = await self.order_repo.get_owner_orders(
                user_id,
                status=status,
                skip=skip,
                limit=page_size,
                order_by='created_at',
                order_direction='desc'
            )
        else:
            orders = await self.order_repo.get_renter_orders(
                user_id,
                status=status,
                skip=skip,
                limit=page_size,
                order_by='created_at',
                order_direction='desc'
            )

        # 计算总数
        filters = {'owner_id' if as_owner else 'renter_id': user_id}
        if status is not None:
            filters['status'] = status
        total = await self.order_repo.count(filters=filters)

        return {
            "items": orders,
            "total": total,
            "page": page,
            "page_size": page_size
        }

    async def confirm_order(
        self,
        order_id: int,
        owner_id: int
    ) -> Optional[Order]:
        """
        确认订单(出租方)

        Args:
            order_id: 订单ID
            owner_id: 出租方ID

        Returns:
            更新后的订单实例

        Raises:
            ValueError: 无权限或状态错误
        """
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("订单不存在")

        if order.owner_id != owner_id:
            raise ValueError("无权限操作")

        if order.status != 1:
            raise ValueError("订单状态不正确")

        # 更新订单状态
        updated_order = await self.order_repo.confirm_order(order_id)

        # 更新衣物状态
        await self.clothing_repo.update_status(order.clothing_id, 2)

        # 发送通知
        await self.message_repo.send_order_notification(
            user_id=order.renter_id,
            title="订单已确认",
            content="出租方已确认您的订单",
            order_id=order_id
        )

        return updated_order

    async def ship_order(
        self,
        order_id: int,
        owner_id: int,
        express_company: str,
        express_no: str
    ) -> Optional[Order]:
        """
        发货(出租方)

        Args:
            order_id: 订单ID
            owner_id: 出租方ID
            express_company: 快递公司
            express_no: 快递单号

        Returns:
            更新后的订单实例

        Raises:
            ValueError: 无权限或状态错误
        """
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("订单不存在")

        if order.owner_id != owner_id:
            raise ValueError("无权限操作")

        if order.status != 2:
            raise ValueError("订单状态不正确")

        # 更新订单状态
        updated_order = await self.order_repo.ship_order(
            order_id,
            express_company,
            express_no
        )

        # 发送通知
        await self.message_repo.send_order_notification(
            user_id=order.renter_id,
            title="订单已发货",
            content=f"快递: {express_company}, 单号: {express_no}",
            order_id=order_id
        )

        return updated_order

    async def receive_order(
        self,
        order_id: int,
        renter_id: int
    ) -> Optional[Order]:
        """
        确认收货(租赁方)

        Args:
            order_id: 订单ID
            renter_id: 租赁方ID

        Returns:
            更新后的订单实例

        Raises:
            ValueError: 无权限或状态错误
        """
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("订单不存在")

        if order.renter_id != renter_id:
            raise ValueError("无权限操作")

        if order.status != 3:
            raise ValueError("订单状态不正确")

        # 更新订单状态
        return await self.order_repo.receive_order(order_id)

    async def return_order(
        self,
        order_id: int,
        renter_id: int
    ) -> Optional[Order]:
        """
        申请归还(租赁方)

        Args:
            order_id: 订单ID
            renter_id: 租赁方ID

        Returns:
            更新后的订单实例

        Raises:
            ValueError: 无权限或状态错误
        """
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("订单不存在")

        if order.renter_id != renter_id:
            raise ValueError("无权限操作")

        if order.status != 4:
            raise ValueError("订单状态不正确")

        # 更新订单状态
        updated_order = await self.order_repo.return_order(order_id)

        # 发送通知
        await self.message_repo.send_order_notification(
            user_id=order.owner_id,
            title="订单待归还",
            content="租赁方已申请归还,请确认收到",
            order_id=order_id
        )

        return updated_order

    async def complete_order(
        self,
        order_id: int,
        owner_id: int,
        deposit_refund: Optional[float] = None
    ) -> Optional[Order]:
        """
        完成订单(出租方)

        Args:
            order_id: 订单ID
            owner_id: 出租方ID
            deposit_refund: 实际退还押金

        Returns:
            更新后的订单实例

        Raises:
            ValueError: 无权限或状态错误
        """
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("订单不存在")

        if order.owner_id != owner_id:
            raise ValueError("无权限操作")

        if order.status != 5:
            raise ValueError("订单状态不正确")

        # 默认全额退还押金
        if deposit_refund is None:
            deposit_refund = float(order.deposit)

        # 更新订单状态
        updated_order = await self.order_repo.complete_order(order_id)

        # 更新押金
        await self.order_repo.update(order_id, deposit_refund=deposit_refund)

        # 更新衣物状态和统计
        await self.clothing_repo.update_status(order.clothing_id, 1)
        await self.clothing_repo.update_rent_count(order.clothing_id)
        await self.clothing_repo.update_status(order.clothing_id, 1)

        # TODO: 退还押金给租赁方
        # await self.user_repo.update_balance(order.renter_id, deposit_refund)

        # TODO: 增加出租方收益
        # await self.user_repo.update_balance(order.owner_id, order.rent_amount)

        # 更新信用积分
        await self.user_repo.update_credit_score(order.renter_id, 1, "按时归还")
        await self.user_repo.update_credit_score(order.owner_id, 1, "完成交易")

        # 发送通知
        await self.message_repo.send_order_notification(
            user_id=order.renter_id,
            title="订单已完成",
            content=f"押金¥{deposit_refund}已退还",
            order_id=order_id
        )

        return updated_order

    async def cancel_order(
        self,
        order_id: int,
        user_id: int
    ) -> Optional[Order]:
        """
        取消订单

        Args:
            order_id: 订单ID
            user_id: 用户ID

        Returns:
            更新后的订单实例

        Raises:
            ValueError: 无权限或状态错误
        """
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("订单不存在")

        if order.renter_id != user_id and order.owner_id != user_id:
            raise ValueError("无权限操作")

        if order.status not in [1, 2]:
            raise ValueError("该状态下不能取消订单")

        # 更新订单状态
        updated_order = await self.order_repo.cancel_order(order_id)

        # 如果衣物已租赁中,恢复为可租赁
        if order.clothing_id:
            await self.clothing_repo.update_status(order.clothing_id, 1)

        # 发送通知
        await self.message_repo.send_order_notification(
            user_id=order.owner_id if user_id == order.renter_id else order.renter_id,
            title="订单已取消",
            content="订单已取消",
            order_id=order_id
        )

        return updated_order

    async def rate_order(
        self,
        order_id: int,
        user_id: int,
        data: OrderRatingCreate
    ) -> Optional[Order]:
        """
        评价订单

        Args:
            order_id: 订单ID
            user_id: 用户ID
            data: 评价数据

        Returns:
            更新后的订单实例

        Raises:
            ValueError: 无权限或状态错误
        """
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("订单不存在")

        # 判断是租赁方评价还是出租方评价
        if user_id == order.renter_id:
            # 租赁方评价
            if order.renter_rating:
                raise ValueError("已经评价过了")

            updated_order = await self.order_repo.renter_rating(
                order_id,
                data.rating,
                data.comment,
                json.dumps(data.images) if data.images else None
            )
        elif user_id == order.owner_id:
            # 出租方评价
            if order.owner_rating:
                raise ValueError("已经评价过了")

            updated_order = await self.order_repo.owner_rating(
                order_id,
                data.rating,
                data.comment,
                json.dumps(data.images) if data.images else None
            )
        else:
            raise ValueError("无权限操作")

        # 如果双方都评价了,更新衣物评分
        if updated_order.renter_rating and updated_order.owner_rating:
            avg_rating = (updated_order.renter_rating + updated_order.owner_rating) / 2
            await self.clothing_repo.update_rating(order.clothing_id, avg_rating)

        return updated_order

    async def create_dispute(
        self,
        order_id: int,
        user_id: int,
        data: OrderDisputeCreate
    ) -> Optional[Order]:
        """
        创建售后争议

        Args:
            order_id: 订单ID
            user_id: 用户ID
            data: 争议数据

        Returns:
            更新后的订单实例

        Raises:
            ValueError: 无权限
        """
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError("订单不存在")

        if order.renter_id != user_id and order.owner_id != user_id:
            raise ValueError("无权限操作")

        # 创建争议
        updated_order = await self.order_repo.create_dispute(
            order_id,
            data.reason,
            data.description,
            json.dumps(data.images) if data.images else None
        )

        # TODO: 通知客服处理

        return updated_order
