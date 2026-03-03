"""
衣物相关API
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.base import Response, PageResponse
from app.schemas.clothing import (
    ClothingCreate, ClothingUpdate, ClothingListQuery,
    ClothingResponse, ClothingDetailResponse
)
from app.services.clothing_service import ClothingService
from app.core.deps import get_current_user


router = APIRouter()


@router.get("/", response_model=Response[PageResponse], summary="获取衣物列表")
async def list_clothings(
    category: Optional[str] = Query(None, description="分类筛选"),
    size: Optional[str] = Query(None, description="尺码筛选"),
    brand: Optional[str] = Query(None, description="品牌筛选"),
    min_price: Optional[float] = Query(None, description="最低价格"),
    max_price: Optional[float] = Query(None, description="最高价格"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    sort_by: Optional[str] = Query(None, description="排序字段"),
    sort_order: str = Query("desc", description="排序顺序"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取衣物列表,支持筛选和搜索

    - **category**: 分类筛选
    - **size**: 尺码筛选
    - **brand**: 品牌筛选
    - **min_price**: 最低价格
    - **max_price**: 最高价格
    - **keyword**: 关键词搜索
    - **page**: 页码
    - **page_size**: 每页数量
    - **sort_by**: 排序字段(created_at/price/rating/rent_count)
    - **sort_order**: 排序顺序(asc/desc)
    """
    clothing_service = ClothingService(db)

    query = ClothingListQuery(
        category=category,
        size=size,
        brand=brand,
        min_price=min_price,
        max_price=max_price,
        keyword=keyword,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order
    )

    result = await clothing_service.list_clothings(query)
    return Response(data=PageResponse(**result))


@router.get("/popular", response_model=Response[list], summary="获取热门衣物")
async def get_popular_clothings(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取热门衣物

    - **limit**: 返回数量
    """
    clothing_service = ClothingService(db)
    clothings = await clothing_service.get_popular_clothings(limit)
    return Response(data=clothings)


@router.get("/latest", response_model=Response[list], summary="获取最新衣物")
async def get_latest_clothings(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取最新衣物

    - **limit**: 返回数量
    """
    clothing_service = ClothingService(db)
    clothings = await clothing_service.get_latest_clothings(limit)
    return Response(data=clothings)


@router.get("/{clothing_id}", response_model=Response[ClothingDetailResponse], summary="获取衣物详情")
async def get_clothing_detail(
    clothing_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    获取衣物详情

    - **clothing_id**: 衣物ID
    """
    clothing_service = ClothingService(db)
    detail = await clothing_service.get_clothing_detail(clothing_id)

    if not detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="衣物不存在"
        )

    return Response(data=ClothingDetailResponse(**detail))


@router.post("/", response_model=Response[ClothingResponse], summary="发布衣物")
async def create_clothing(
    data: ClothingCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    发布衣物

    - **name**: 衣物名称
    - **brand**: 品牌
    - **category**: 分类
    - **size**: 尺码
    - **condition**: 新旧程度
    - **description**: 描述
    - **images**: 图片URL列表(3-5张)
    - **daily_rent**: 日租金
    - **deposit**: 押金
    - **min_rent_days**: 最短租期
    - **max_rent_days**: 最长租期
    - **require_wash**: 是否需要清洗
    - **delivery_type**: 配送方式
    - **delivery_fee**: 运费
    """
    clothing_service = ClothingService(db)

    try:
        clothing = await clothing_service.create_clothing(current_user.id, data)
        return Response(data=ClothingResponse.model_validate(clothing))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{clothing_id}", response_model=Response[ClothingResponse], summary="编辑衣物")
async def update_clothing(
    clothing_id: int,
    data: ClothingUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    编辑衣物信息

    - **clothing_id**: 衣物ID
    - 其他字段同发布衣物
    """
    clothing_service = ClothingService(db)

    try:
        clothing = await clothing_service.update_clothing(current_user.id, clothing_id, data)
        return Response(data=ClothingResponse.model_validate(clothing))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{clothing_id}", response_model=Response, summary="删除衣物")
async def delete_clothing(
    clothing_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除衣物(下架)

    - **clothing_id**: 衣物ID
    """
    clothing_service = ClothingService(db)

    try:
        await clothing_service.delete_clothing(current_user.id, clothing_id)
        return Response(data={"message": "删除成功"})
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{clothing_id}/favorite", response_model=Response, summary="收藏衣物")
async def favorite_clothing(
    clothing_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    收藏衣物

    - **clothing_id**: 衣物ID
    """
    clothing_service = ClothingService(db)
    await clothing_service.favorite_clothing(current_user.id, clothing_id)
    return Response(data={"message": "收藏成功"})


@router.delete("/{clothing_id}/favorite", response_model=Response, summary="取消收藏")
async def unfavorite_clothing(
    clothing_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    取消收藏衣物

    - **clothing_id**: 衣物ID
    """
    clothing_service = ClothingService(db)
    await clothing_service.unfavorite_clothing(current_user.id, clothing_id)
    return Response(data={"message": "取消收藏成功"})
