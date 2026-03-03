"""
订单Repository
"""
from typing import Optional, List
from datetime import date, datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_
from app.models.order import Order
from app.repositories.base_repository import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """订单Repository"""

    async def get_by_order_no(self, order_no: str) -> Optional[Order]:
        """根据订单号获取订单"""
        return await self.get_by_field('order_no', order_no)

    async def get_renter_orders(
        self,
        renter_id: int,
        status: Optional[int] = None,
        **kwargs
    ) -> List[Order]:
        """获取租赁方的订单列表"""
        filters = {'renter_id': renter_id}
        if status is not None:
            filters['status'] = status
        return await self.get_multi(filters=filters, **kwargs)

    async def get_owner_orders(
        self,
        owner_id: int,
        status: Optional[int] = None,
        **kwargs
    ) -> List[Order]:
        """获取出租方的订单列表"""
        filters = {'owner_id': owner_id}
        if status is not None:
            filters['status'] = status
        return await self.get_multi(filters=filters, **kwargs)

    async def get_clothing_orders(self, clothing_id: int, **kwargs) -> List[Order]:
        """获取衣物的订单列表"""
        return await self.get_multi(filters={'clothing_id': clothing_id}, **kwargs)

    async def create_order(
        self,
        order_no: str,
        clothing_id: int,
        renter_id: int,
        owner_id: int,
        start_date: date,
        end_date: date,
        rent_days: int,
        daily_rent: float,
        rent_amount: float,
        deposit: float,
        delivery_fee: float,
        total_amount: float,
        **kwargs
    ) -> Order:
        """
        创建订单

        Args:
            order_no: 订单号
            clothing_id: 衣物ID
            renter_id: 租赁方ID
            owner_id: 出租方ID
            start_date: 开始日期
            end_date: 结束日期
            rent_days: 租赁天数
            daily_rent: 日租金
            rent_amount: 租金总额
            deposit: 押金
            delivery_fee: 运费
            total_amount: 订单总额
            **kwargs: 其他字段

        Returns:
            订单实例
        """
        return await self.create(
            order_no=order_no,
            clothing_id=clothing_id,
            renter_id=renter_id,
            owner_id=owner_id,
            start_date=start_date,
            end_date=end_date,
            rent_days=rent_days,
            daily_rent=daily_rent,
            rent_amount=rent_amount,
            deposit=deposit,
            delivery_fee=delivery_fee,
            total_amount=total_amount,
            status=1,  # 待确认
            **kwargs
        )

    async def update_order_status(
        self,
        order_id: int,
        status: int,
        time_field: Optional[str] = None
    ) -> Optional[Order]:
        """
        更新订单状态

        Args:
            order_id: 订单ID
            status: 新状态
            time_field: 时间字段名

        Returns:
            更新后的订单实例
        """
        update_data = {'status': status}

        # 设置时间字段
        if time_field:
            update_data[time_field] = datetime.now()

        return await self.update(order_id, **update_data)

    async def confirm_order(self, order_id: int) -> Optional[Order]:
        """确认订单"""
        return await self.update_order_status(order_id, status=2, time_field='confirm_time')

    async def ship_order(
        self,
        order_id: int,
        express_company: str,
        express_no: str
    ) -> Optional[Order]:
        """
        发货

        Args:
            order_id: 订单ID
            express_company: 快递公司
            express_no: 快递单号

        Returns:
            更新后的订单实例
        """
        return await self.update(
            order_id,
            status=3,
            ship_time=datetime.now(),
            express_company=express_company,
            express_no=express_no
        )

    async def receive_order(self, order_id: int) -> Optional[Order]:
        """确认收货"""
        return await self.update_order_status(order_id, status=4, time_field='receive_time')

    async def return_order(self, order_id: int) -> Optional[Order]:
        """申请归还"""
        return await self.update_order_status(order_id, status=5, time_field='return_time')

    async def complete_order(self, order_id: int) -> Optional[Order]:
        """完成订单"""
        return await self.update_order_status(order_id, status=6, time_field='complete_time')

    async def cancel_order(self, order_id: int) -> Optional[Order]:
        """取消订单"""
        return await self.update_order_status(order_id, status=7, time_field='cancel_time')

    async def renter_rating(
        self,
        order_id: int,
        rating: int,
        comment: Optional[str] = None,
        images: Optional[str] = None
    ) -> Optional[Order]:
        """
        租赁方评价

        Args:
            order_id: 订单ID
            rating: 评分
            comment: 评价内容
            images: 评价图片

        Returns:
            更新后的订单实例
        """
        import json

        images_json = json.dumps(images) if images else None

        return await self.update(
            order_id,
            renter_rating=rating,
            renter_comment=comment,
            renter_images=images_json
        )

    async def owner_rating(
        self,
        order_id: int,
        rating: int,
        comment: Optional[str] = None,
        images: Optional[str] = None
    ) -> Optional[Order]:
        """
        出租方评价

        Args:
            order_id: 订单ID
            rating: 评分
            comment: 评价内容
            images: 评价图片

        Returns:
            更新后的订单实例
        """
        import json

        images_json = json.dumps(images) if images else None

        return await self.update(
            order_id,
            owner_rating=rating,
            owner_comment=comment,
            owner_images=images_json
        )

    async def create_dispute(
        self,
        order_id: int,
        reason: str,
        description: str,
        images: Optional[str] = None
    ) -> Optional[Order]:
        """
        创建售后争议

        Args:
            order_id: 订单ID
            reason: 争议原因
            description: 争议描述
            images: 争议图片

        Returns:
            更新后的订单实例
        """
        import json

        images_json = json.dumps(images) if images else None

        return await self.update(
            order_id,
            status=8,  # 售后中
            dispute_reason=reason,
            dispute_desc=description,
            dispute_images=images_json,
            dispute_status=1  # 处理中
        )

    async def resolve_dispute(
        self,
        order_id: int,
        result: str,
        deposit_refund: Optional[float] = None
    ) -> Optional[Order]:
        """
        解决争议

        Args:
            order_id: 订单ID
            result: 争议结果
            deposit_refund: 实际退还押金

        Returns:
            更新后的订单实例
        """
        return await self.update(
            order_id,
            dispute_status=2,  # 已解决
            dispute_result=result,
            deposit_refund=deposit_refund
        )

    async def count_pending_confirm(self, owner_id: int) -> int:
        """统计待确认订单数"""
        return await self.count(
            filters={'owner_id': owner_id, 'status': 1}
        )

    async def count_pending_ship(self, owner_id: int) -> int:
        """统计待发货订单数"""
        return await self.count(
            filters={'owner_id': owner_id, 'status': 2}
        )
