"""
衣物Repository
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, or_
from app.models.clothing import Clothing
from app.repositories.base_repository import BaseRepository


class ClothingRepository(BaseRepository[Clothing]):
    """衣物Repository"""

    async def get_clothings_by_owner(self, owner_id: int, **kwargs) -> List[Clothing]:
        """获取出租方的衣物列表"""
        return await self.get_multi(filters={'owner_id': owner_id, **kwargs})

    async def get_clothings_by_category(self, category: str, **kwargs) -> List[Clothing]:
        """根据分类获取衣物列表"""
        return await self.get_multi(filters={'category': category, **kwargs})

    async def get_clothings_by_size(self, size: str, **kwargs) -> List[Clothing]:
        """根据尺码获取衣物列表"""
        return await self.get_multi(filters={'size': size, **kwargs})

    async def search_clothings(
        self,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        size: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        **kwargs
    ) -> List[Clothing]:
        """
        搜索衣物

        Args:
            keyword: 关键词
            category: 分类
            size: 尺码
            min_price: 最低价格
            max_price: 最高价格
            **kwargs: 其他参数

        Returns:
            衣物列表
        """
        filters = {}

        # 基础过滤
        if category:
            filters['category'] = category
        if size:
            filters['size'] = size
        if 'status' not in filters:
            filters['status'] = 1  # 默认只显示可租赁的

        # 价格范围过滤
        # 注意: 这里简化处理,实际应该在Service层处理

        # 调用父类方法获取列表
        clothings = await self.get_multi(filters=filters, **kwargs)

        # 关键词搜索(需要在Service层实现全文搜索)
        # 这里暂时返回所有结果,后续优化

        return clothings

    async def create_clothing(
        self,
        owner_id: int,
        name: str,
        images: list,
        daily_rent: float,
        deposit: float,
        **kwargs
    ) -> Clothing:
        """
        创建衣物

        Args:
            owner_id: 出租方ID
            name: 衣物名称
            images: 图片列表
            daily_rent: 日租金
            deposit: 押金
            **kwargs: 其他字段

        Returns:
            衣物实例
        """
        import json

        return await self.create(
            owner_id=owner_id,
            name=name,
            images=json.dumps(images),
            daily_rent=daily_rent,
            deposit=deposit,
            **kwargs
        )

    async def update_clothing(
        self,
        clothing_id: int,
        **kwargs
    ) -> Optional[Clothing]:
        """
        更新衣物信息

        Args:
            clothing_id: 衣物ID
            **kwargs: 更新的字段

        Returns:
            更新后的衣物实例
        """
        import json

        # 处理图片列表
        if 'images' in kwargs and kwargs['images'] is not None:
            kwargs['images'] = json.dumps(kwargs['images'])

        return await self.update(clothing_id, **kwargs)

    async def update_rent_count(self, clothing_id: int) -> Optional[Clothing]:
        """
        增加租赁次数

        Args:
            clothing_id: 衣物ID

        Returns:
            更新后的衣物实例
        """
        clothing = await self.get_by_id(clothing_id)
        if clothing:
            return await self.update(
                clothing_id,
                rent_count=clothing.rent_count + 1
            )
        return None

    async def update_rating(
        self,
        clothing_id: int,
        new_rating: int
    ) -> Optional[Clothing]:
        """
        更新衣物评分

        Args:
            clothing_id: 衣物ID
            new_rating: 新评分(1-5)

        Returns:
            更新后的衣物实例
        """
        clothing = await self.get_by_id(clothing_id)
        if clothing:
            total_score = (clothing.rating_avg or 0) * clothing.rating_count + new_rating
            new_count = clothing.rating_count + 1
            new_avg = total_score / new_count

            return await self.update(
                clothing_id,
                rating_avg=round(new_avg, 2),
                rating_count=new_count
            )
        return None

    async def update_status(
        self,
        clothing_id: int,
        status: int
    ) -> Optional[Clothing]:
        """
        更新衣物状态

        Args:
            clothing_id: 衣物ID
            status: 状态 1可租 2租赁中 3已下架

        Returns:
            更新后的衣物实例
        """
        return await self.update(clothing_id, status=status)

    async def get_popular_clothings(self, limit: int = 10) -> List[Clothing]:
        """
        获取热门衣物

        Args:
            limit: 返回数量

        Returns:
            衣物列表
        """
        return await self.get_multi(
            limit=limit,
            filters={'status': 1},
            order_by='rent_count',
            order_direction='desc'
        )

    async def get_latest_clothings(self, limit: int = 10) -> List[Clothing]:
        """
        获取最新衣物

        Args:
            limit: 返回数量

        Returns:
            衣物列表
        """
        return await self.get_multi(
            limit=limit,
            filters={'status': 1},
            order_by='created_at',
            order_direction='desc'
        )
