"""
订单相关API
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.base import Response, PageResponse
from app.schemas.order import (
    OrderCreate, OrderListQuery,
    OrderResponse, OrderDetailResponse,
    OrderRatingCreate, OrderDisputeCreate
)
from app.services.order_service import OrderService
from app.core.deps import get_current_user


router = APIRouter()


@router.post("/", response_model=Response[OrderResponse], summary="创建订单")
async def create_order(
    data: OrderCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建订单

    - **clothing_id**: 衣物ID
    - **start_date**: 开始日期
    - **end_date**: 结束日期
    """
    order_service = OrderService(db)

    try:
        order = await order_service.create_order(current_user.id, data)
        return Response(data=OrderResponse.model_validate(order))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=Response[PageResponse], summary="获取订单列表")
async def list_orders(
    as_owner: Optional[bool] = Query(False, description="是否作为出租方查看"),
    status: Optional[int] = Query(None, description="订单状态筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取订单列表

    - **as_owner**: 是否作为出租方查看
    - **status**: 订单状态筛选
    - **page**: 页码
    - **page_size**: 每页数量
    """
    order_service = OrderService(db)
    result = await order_service.list_orders(
        current_user.id,
        as_owner=as_owner,
        status=status,
        page=page,
        page_size=page_size
    )
    return Response(data=PageResponse(**result))


@router.get("/{order_id}", response_model=Response[OrderDetailResponse], summary="获取订单详情")
async def get_order_detail(
    order_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取订单详情

    - **order_id**: 订单ID
    """
    order_service = OrderService(db)

    try:
        order = await order_service.get_order(order_id, current_user.id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="订单不存在"
            )
        return Response(data=OrderDetailResponse.model_validate(order))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{order_id}/confirm", response_model=Response[OrderResponse], summary="确认订单")
async def confirm_order(
    order_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    确认订单(出租方操作)

    - **order_id**: 订单ID
    """
    order_service = OrderService(db)

    try:
        order = await order_service.confirm_order(order_id, current_user.id)
        return Response(data=OrderResponse.model_validate(order))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{order_id}/ship", response_model=Response[OrderResponse], summary="发货")
async def ship_order(
    order_id: int,
    express_company: str = Query(..., description="快递公司"),
    express_no: str = Query(..., description="快递单号"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    发货(出租方操作)

    - **order_id**: 订单ID
    - **express_company**: 快递公司
    - **express_no**: 快递单号
    """
    order_service = OrderService(db)

    try:
        order = await order_service.ship_order(
            order_id,
            current_user.id,
            express_company,
            express_no
        )
        return Response(data=OrderResponse.model_validate(order))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{order_id}/receive", response_model=Response[OrderResponse], summary="确认收货")
async def receive_order(
    order_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    确认收货(租赁方操作)

    - **order_id**: 订单ID
    """
    order_service = OrderService(db)

    try:
        order = await order_service.receive_order(order_id, current_user.id)
        return Response(data=OrderResponse.model_validate(order))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{order_id}/return", response_model=Response[OrderResponse], summary="申请归还")
async def return_order(
    order_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    申请归还(租赁方操作)

    - **order_id**: 订单ID
    """
    order_service = OrderService(db)

    try:
        order = await order_service.return_order(order_id, current_user.id)
        return Response(data=OrderResponse.model_validate(order))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{order_id}/complete", response_model=Response[OrderResponse], summary="完成订单")
async def complete_order(
    order_id: int,
    deposit_refund: Optional[float] = Query(None, description="实际退还押金"),
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    完成订单(出租方操作)

    - **order_id**: 订单ID
    - **deposit_refund**: 实际退还押金
    """
    order_service = OrderService(db)

    try:
        order = await order_service.complete_order(
            order_id,
            current_user.id,
            deposit_refund
        )
        return Response(data=OrderResponse.model_validate(order))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{order_id}/cancel", response_model=Response[OrderResponse], summary="取消订单")
async def cancel_order(
    order_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    取消订单

    - **order_id**: 订单ID
    """
    order_service = OrderService(db)

    try:
        order = await order_service.cancel_order(order_id, current_user.id)
        return Response(data=OrderResponse.model_validate(order))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{order_id}/rating", response_model=Response[OrderResponse], summary="评价订单")
async def rate_order(
    order_id: int,
    data: OrderRatingCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    评价订单

    - **order_id**: 订单ID
    - **rating**: 评分 1-5
    - **comment**: 评价内容
    - **images**: 评价图片
    """
    order_service = OrderService(db)

    try:
        order = await order_service.rate_order(order_id, current_user.id, data)
        return Response(data=OrderResponse.model_validate(order))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{order_id}/dispute", response_model=Response[OrderResponse], summary="创建售后争议")
async def create_dispute(
    order_id: int,
    data: OrderDisputeCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    创建售后争议

    - **order_id**: 订单ID
    - **reason**: 争议原因
    - **description**: 争议描述
    - **images**: 争议图片
    """
    order_service = OrderService(db)

    try:
        order = await order_service.create_dispute(order_id, current_user.id, data)
        return Response(data=OrderResponse.model_validate(order))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
