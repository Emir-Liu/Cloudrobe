"""
认证相关API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.base import Response
from app.schemas.user import UserResponse, UserLogin, UserWechatLogin, SendSmsRequest
from app.services.auth_service import AuthService


router = APIRouter()


@router.post("/send-sms", response_model=Response, summary="发送短信验证码")
async def send_sms_code(
    request: SendSmsRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    发送短信验证码

    - **phone**: 手机号
    """
    # TODO: 实现发送短信验证码逻辑
    # auth_service = AuthService(db)
    # await auth_service.send_sms_code(request.phone)

    return Response(data={"message": "验证码已发送(测试环境)"})


@router.post("/register", response_model=Response[UserResponse], summary="手机号注册")
async def register(
    request: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    手机号注册

    - **phone**: 手机号
    - **code**: 验证码
    """
    auth_service = AuthService(db)

    try:
        user, token = await auth_service.register_by_phone(request.phone, request.code)
        return Response(data=UserResponse.model_validate(user))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Response[UserResponse], summary="手机号登录")
async def login(
    request: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    手机号登录

    - **phone**: 手机号
    - **code**: 验证码
    """
    auth_service = AuthService(db)

    try:
        user, token = await auth_service.login_by_phone(request.phone, request.code)
        return Response(data=UserResponse.model_validate(user))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/wechat-login", response_model=Response[UserResponse], summary="微信登录")
async def wechat_login(
    request: UserWechatLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    微信登录

    - **code**: 微信登录code
    """
    auth_service = AuthService(db)

    try:
        user, token = await auth_service.login_by_wechat(request.code)
        return Response(data=UserResponse.model_validate(user))
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
