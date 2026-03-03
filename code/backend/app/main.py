"""
云衣橱后端应用主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from app.core.config import settings
from app.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 云衣橱后端服务启动中...")
    logger.info(f"📦 环境: {settings.ENVIRONMENT}")
    logger.info(f"🌐 服务地址: http://{settings.HOST}:{settings.PORT}")
    
    yield
    
    # 关闭时执行
    logger.info("👋 云衣橱后端服务已关闭")


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="云衣橱 - P2P服装租赁共享平台",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"/api/v{settings.API_VERSION.split('.')[0]}/openapi.json"
)


# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 注册路由
app.include_router(api_router, prefix=f"/api/v{settings.API_VERSION.split('.')[0]}")


# 健康检查
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


# 根路径
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用云衣橱API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
