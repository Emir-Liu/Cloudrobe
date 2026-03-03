"""
基础Repository
提供通用的数据库操作方法
"""
from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from sqlalchemy import select, update, delete, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import BaseModel

ModelType = TypeVar('ModelType', bound=BaseModel)


class BaseRepository(Generic[ModelType]):
    """基础Repository"""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        """
        初始化

        Args:
            model: 模型类
            session: 数据库会话
        """
        self.model = model
        self.session = session

    async def create(self, **kwargs) -> ModelType:
        """
        创建记录

        Args:
            **kwargs: 模型字段值

        Returns:
            创建的模型实例
        """
        db_obj = self.model(**kwargs)
        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        根据ID获取记录

        Args:
            id: 记录ID

        Returns:
            模型实例或None
        """
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_field(self, field_name: str, value: Any) -> Optional[ModelType]:
        """
        根据字段获取记录

        Args:
            field_name: 字段名
            value: 字段值

        Returns:
            模型实例或None
        """
        field = getattr(self.model, field_name)
        result = await self.session.execute(
            select(self.model).where(field == value)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        order_direction: str = "desc"
    ) -> List[ModelType]:
        """
        获取多条记录

        Args:
            skip: 跳过记录数
            limit: 返回记录数
            filters: 过滤条件
            order_by: 排序字段
            order_direction: 排序方向

        Returns:
            模型实例列表
        """
        query = select(self.model)

        # 应用过滤条件
        if filters:
            for field_name, value in filters.items():
                if value is not None:
                    field = getattr(self.model, field_name, None)
                    if field is not None:
                        query = query.where(field == value)

        # 应用排序
        if order_by:
            order_field = getattr(self.model, order_by, None)
            if order_field is not None:
                if order_direction.lower() == "asc":
                    query = query.order_by(order_field.asc())
                else:
                    query = query.order_by(order_field.desc())

        # 应用分页
        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        统计记录数

        Args:
            filters: 过滤条件

        Returns:
            记录数
        """
        query = select(func.count(self.model.id))

        # 应用过滤条件
        if filters:
            for field_name, value in filters.items():
                if value is not None:
                    field = getattr(self.model, field_name, None)
                    if field is not None:
                        query = query.where(field == value)

        result = await self.session.execute(query)
        return result.scalar()

    async def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """
        更新记录

        Args:
            id: 记录ID
            **kwargs: 更新的字段值

        Returns:
            更新后的模型实例或None
        """
        # 排除None值
        update_data = {k: v for k, v in kwargs.items() if v is not None}

        await self.session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
        )
        await self.session.flush()

        return await self.get_by_id(id)

    async def delete(self, id: int) -> bool:
        """
        删除记录

        Args:
            id: 记录ID

        Returns:
            是否删除成功
        """
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.session.flush()
        return result.rowcount > 0

    async def exists(self, id: int) -> bool:
        """
        检查记录是否存在

        Args:
            id: 记录ID

        Returns:
            是否存在
        """
        return await self.get_by_id(id) is not None
