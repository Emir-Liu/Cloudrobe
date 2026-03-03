"""
衣物服务
"""
from typing import Optional, List
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.clothing import Clothing
from app.models.user import User
from app.models.favorite import Favorite
from app.repositories.clothing_repository import ClothingRepository
from app.repositories.user_repository import UserRepository
from app.repositories.base_repository import BaseRepository
from app.schemas.clothing import ClothingCreate, ClothingUpdate, ClothingListQuery


class ClothingService:
    """衣物服务"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.clothing_repo = ClothingRepository(Clothing, session)
        self.user_repo = UserRepository(User, session)
        self.favorite_repo = BaseRepository(Favorite, session)

    async def get_clothing(self, clothing_id: int) -> Optional[Clothing]:
        """
        获取衣物详情

        Args:
            clothing_id: 衣物ID

        Returns:
            衣物实例或None
        """
        return await self.clothing_repo.get_by_id(clothing_id)

    async def get_clothing_detail(self, clothing_id: int) -> Optional[dict]:
        """
        获取衣物详情(包含出租方信息)

        Args:
            clothing_id: 衣物ID

        Returns:
            衣物详情字典
        """
        clothing = await self.clothing_repo.get_by_id(clothing_id)
        if not clothing:
            return None

        # 获取出租方信息
        owner = await self.user_repo.get_by_id(clothing.owner_id)

        return {
            "id": clothing.id,
            "name": clothing.name,
            "brand": clothing.brand,
            "category": clothing.category,
            "size": clothing.size,
            "condition": clothing.condition,
            "description": clothing.description,
            "images": json.loads(clothing.images) if clothing.images else [],
            "daily_rent": float(clothing.daily_rent),
            "deposit": float(clothing.deposit),
            "min_rent_days": clothing.min_rent_days,
            "max_rent_days": clothing.max_rent_days,
            "require_wash": clothing.require_wash,
            "delivery_type": clothing.delivery_type,
            "delivery_fee": float(clothing.delivery_fee),
            "status": clothing.status,
            "rent_count": clothing.rent_count,
            "total_revenue": float(clothing.total_revenue),
            "rating_avg": float(clothing.rating_avg) if clothing.rating_avg else None,
            "rating_count": clothing.rating_count,
            "created_at": clothing.created_at.isoformat(),
            "owner": {
                "id": owner.id,
                "nickname": owner.nickname,
                "avatar": owner.avatar,
                "credit_level": owner.credit_level,
            } if owner else None
        }

    async def list_clothings(
        self,
        query: ClothingListQuery
    ) -> dict:
        """
        获取衣物列表

        Args:
            query: 查询参数

        Returns:
            分页结果字典
        """
        # 计算分页
        skip = (query.page - 1) * query.page_size

        # 获取列表
        clothings = await self.clothing_repo.get_multi(
            skip=skip,
            limit=query.page_size,
            order_by=query.sort_by or 'created_at',
            order_direction=query.sort_order
        )

        # 获取总数
        total = await self.clothing_repo.count()

        # 转换为响应格式
        items = []
        for clothing in clothings:
            items.append({
                "id": clothing.id,
                "name": clothing.name,
                "brand": clothing.brand,
                "category": clothing.category,
                "size": clothing.size,
                "images": json.loads(clothing.images) if clothing.images else [],
                "daily_rent": float(clothing.daily_rent),
                "deposit": float(clothing.deposit),
                "status": clothing.status,
                "rent_count": clothing.rent_count,
                "rating_avg": float(clothing.rating_avg) if clothing.rating_avg else None,
                "rating_count": clothing.rating_count,
                "created_at": clothing.created_at.isoformat(),
            })

        return {
            "items": items,
            "total": total,
            "page": query.page,
            "page_size": query.page_size
        }

    async def create_clothing(
        self,
        user_id: int,
        data: ClothingCreate
    ) -> Clothing:
        """
        发布衣物

        Args:
            user_id: 用户ID
            data: 衣物数据

        Returns:
            创建的衣物实例

        Raises:
            ValueError: 用户未实名认证
        """
        # 检查用户是否已实名认证
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_verified:
            raise ValueError("请先完成实名认证")

        # 创建衣物
        clothing = await self.clothing_repo.create_clothing(
            owner_id=user_id,
            name=data.name,
            brand=data.brand,
            category=data.category,
            size=data.size,
            condition=data.condition,
            description=data.description,
            images=data.images,
            daily_rent=data.daily_rent,
            deposit=data.deposit,
            min_rent_days=data.min_rent_days,
            max_rent_days=data.max_rent_days,
            require_wash=data.require_wash,
            delivery_type=data.delivery_type,
            delivery_fee=data.delivery_fee
        )

        return clothing

    async def update_clothing(
        self,
        user_id: int,
        clothing_id: int,
        data: ClothingUpdate
    ) -> Optional[Clothing]:
        """
        更新衣物信息

        Args:
            user_id: 用户ID
            clothing_id: 衣物ID
            data: 更新数据

        Returns:
            更新后的衣物实例

        Raises:
            ValueError: 无权限
        """
        # 检查权限
        clothing = await self.clothing_repo.get_by_id(clothing_id)
        if not clothing:
            raise ValueError("衣物不存在")

        if clothing.owner_id != user_id:
            raise ValueError("无权限操作")

        # 更新衣物
        return await self.clothing_repo.update_clothing(
            clothing_id,
            **data.model_dump(exclude_unset=True)
        )

    async def delete_clothing(
        self,
        user_id: int,
        clothing_id: int
    ) -> bool:
        """
        删除衣物(下架)

        Args:
            user_id: 用户ID
            clothing_id: 衣物ID

        Returns:
            是否删除成功

        Raises:
            ValueError: 无权限
        """
        # 检查权限
        clothing = await self.clothing_repo.get_by_id(clothing_id)
        if not clothing:
            raise ValueError("衣物不存在")

        if clothing.owner_id != user_id:
            raise ValueError("无权限操作")

        # 下架衣物
        return await self.clothing_repo.update_status(clothing_id, 3) is not None

    async def favorite_clothing(
        self,
        user_id: int,
        clothing_id: int
    ) -> bool:
        """
        收藏衣物

        Args:
            user_id: 用户ID
            clothing_id: 衣物ID

        Returns:
            是否收藏成功
        """
        # 检查是否已收藏
        existing = await self.favorite_repo.get_by_field('user_id', user_id)
        # TODO: 检查是否已收藏

        # 创建收藏
        await self.favorite_repo.create(
            user_id=user_id,
            clothing_id=clothing_id
        )

        return True

    async def unfavorite_clothing(
        self,
        user_id: int,
        clothing_id: int
    ) -> bool:
        """
        取消收藏

        Args:
            user_id: 用户ID
            clothing_id: 衣物ID

        Returns:
            是否取消成功
        """
        # TODO: 删除收藏记录
        return True

    async def get_popular_clothings(self, limit: int = 10) -> List[dict]:
        """
        获取热门衣物

        Args:
            limit: 返回数量

        Returns:
            衣物列表
        """
        clothings = await self.clothing_repo.get_popular_clothings(limit)

        result = []
        for clothing in clothings:
            result.append({
                "id": clothing.id,
                "name": clothing.name,
                "images": json.loads(clothing.images) if clothing.images else [],
                "daily_rent": float(clothing.daily_rent),
                "rent_count": clothing.rent_count,
                "rating_avg": float(clothing.rating_avg) if clothing.rating_avg else None,
            })

        return result

    async def get_latest_clothings(self, limit: int = 10) -> List[dict]:
        """
        获取最新衣物

        Args:
            limit: 返回数量

        Returns:
            衣物列表
        """
        clothings = await self.clothing_repo.get_latest_clothings(limit)

        result = []
        for clothing in clothings:
            result.append({
                "id": clothing.id,
                "name": clothing.name,
                "images": json.loads(clothing.images) if clothing.images else [],
                "daily_rent": float(clothing.daily_rent),
                "created_at": clothing.created_at.isoformat(),
            })

        return result
