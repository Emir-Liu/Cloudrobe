"""
用户相关API
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.base import Response
from app.schemas.user import UserResponse, UserUpdate, UserVerify
from app.services.user_service import UserService
from app.core.deps import get_current_user


router = APIRouter()


@router.get("/me", response_model=Response[UserResponse], summary="获取当前用户信息")
async def get_current_user_info(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前登录用户的详细信息
    """
    return Response(data=UserResponse.model_validate(current_user))


@router.put("/me", response_model=Response[UserResponse], summary="更新用户信息")
async def update_user_info(
    update_data: UserUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    更新当前用户信息

    - **nickname**: 昵称
    - **avatar**: 头像URL
    - **gender**: 性别 0未知 1男 2女
    - **height**: 身高cm
    - **weight**: 体重kg
    - **bio**: 个人简介
    - **size_preferences**: 尺码偏好JSON
    """
    user_service = UserService(db)

    updated_user = await user_service.update_user_profile(
        current_user.id,
        nickname=update_data.nickname,
        avatar=update_data.avatar,
        gender=update_data.gender,
        height=update_data.height,
        weight=update_data.weight,
        bio=update_data.bio,
        size_preferences=update_data.size_preferences
    )

    return Response(data=UserResponse.model_validate(updated_user))


@router.post("/verify", response_model=Response[UserResponse], summary="实名认证")
async def verify_real_name(
    verify_data: UserVerify,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    实名认证

    - **id_card_name**: 身份证姓名
    - **id_card_number**: 身份证号
    - **id_card_front**: 身份证正面URL
    - **id_card_back**: 身份证背面URL
    """
    user_service = UserService(db)

    try:
        verified_user = await user_service.verify_real_name(
            current_user.id,
            verify_data.id_card_name,
            verify_data.id_card_number,
            verify_data.id_card_front,
            verify_data.id_card_back
        )
        return Response(data=UserResponse.model_validate(verified_user))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/credit", response_model=Response[dict], summary="获取信用信息")
async def get_credit_info(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户信用信息
    """
    user_service = UserService(db)
    credit_info = await user_service.get_credit_info(current_user.id)
    return Response(data=credit_info)


@router.get("/balance", response_model=Response[dict], summary="获取余额信息")
async def get_balance_info(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户余额信息
    """
    user_service = UserService(db)
    balance_info = await user_service.get_balance(current_user.id)
    return Response(data=balance_info)
