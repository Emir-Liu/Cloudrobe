"""
API v1路由
"""
from fastapi import APIRouter
from app.api.v1 import auth, users, clothings, orders


router = APIRouter()

# 注册子路由
router.include_router(auth.router, prefix="/auth", tags=["认证"])
router.include_router(users.router, prefix="/users", tags=["用户"])
router.include_router(clothings.router, prefix="/clothings", tags=["衣物"])
router.include_router(orders.router, prefix="/orders", tags=["订单"])
