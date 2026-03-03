"""
认证服务
"""
from typing import Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from app.core.config import settings
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, get_password_hash


class AuthService:
    """认证服务"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(User, session)

    def create_access_token(self, data: dict) -> str:
        """
        创建JWT访问令牌

        Args:
            data: 要编码的数据

        Returns:
            JWT令牌
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def decode_access_token(self, token: str) -> Optional[dict]:
        """
        解码JWT访问令牌

        Args:
            token: JWT令牌

        Returns:
            解码后的数据或None
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError:
            return None

    async def register_by_phone(
        self,
        phone: str,
        code: str,
        nickname: Optional[str] = None
    ) -> Tuple[User, str]:
        """
        手机号注册

        Args:
            phone: 手机号
            code: 验证码
            nickname: 昵称

        Returns:
            用户实例和JWT令牌

        Raises:
            ValueError: 验证码错误或用户已存在
        """
        # TODO: 验证短信验证码
        # if not await self._verify_sms_code(phone, code):
        #     raise ValueError("验证码错误")

        # 检查用户是否已存在
        existing_user = await self.user_repo.get_by_phone(phone)
        if existing_user:
            raise ValueError("该手机号已注册")

        # 创建用户
        user = await self.user_repo.create_user(
            phone=phone,
            nickname=nickname or f"用户{phone[-4:]}",
            status=1
        )

        # 生成JWT令牌
        token = self.create_access_token(data={"sub": str(user.id)})

        # 更新最后登录时间
        await self.user_repo.update(user.id, last_login_at=datetime.now())

        return user, token

    async def login_by_phone(
        self,
        phone: str,
        code: str
    ) -> Tuple[User, str]:
        """
        手机号登录

        Args:
            phone: 手机号
            code: 验证码

        Returns:
            用户实例和JWT令牌

        Raises:
            ValueError: 验证码错误或用户不存在
        """
        # TODO: 验证短信验证码
        # if not await self._verify_sms_code(phone, code):
        #     raise ValueError("验证码错误")

        # 查找用户
        user = await self.user_repo.get_by_phone(phone)
        if not user:
            raise ValueError("用户不存在")

        # 检查用户状态
        if user.status != 1:
            raise ValueError("账号已被冻结")

        # 生成JWT令牌
        token = self.create_access_token(data={"sub": str(user.id)})

        # 更新最后登录时间
        await self.user_repo.update(user.id, last_login_at=datetime.now())

        return user, token

    async def login_by_wechat(
        self,
        code: str
    ) -> Tuple[User, str]:
        """
        微信登录

        Args:
            code: 微信登录code

        Returns:
            用户实例和JWT令牌

        Raises:
            ValueError: 微信登录失败
        """
        # TODO: 调用微信API获取openid和unionid
        # openid, unionid = await self._get_wechat_user_info(code)

        # 暂时使用测试数据
        openid = f"test_openid_{code}"

        # 查找用户
        user = await self.user_repo.get_by_openid(openid)

        if user:
            # 用户已存在,直接登录
            if user.status != 1:
                raise ValueError("账号已被冻结")

            # 生成JWT令牌
            token = self.create_access_token(data={"sub": str(user.id)})

            # 更新最后登录时间
            await self.user_repo.update(user.id, last_login_at=datetime.now())

            return user, token
        else:
            # 新用户,自动注册
            user = await self.user_repo.create_user(
                openid=openid,
                nickname=f"微信用户",
                status=1
            )

            # 生成JWT令牌
            token = self.create_access_token(data={"sub": str(user.id)})

            return user, token

    async def get_current_user(self, token: str) -> Optional[User]:
        """
        获取当前用户

        Args:
            token: JWT令牌

        Returns:
            用户实例或None
        """
        # 解码令牌
        payload = self.decode_access_token(token)
        if not payload:
            return None

        user_id = payload.get("sub")
        if not user_id:
            return None

        # 获取用户
        user = await self.user_repo.get_by_id(int(user_id))
        if not user or user.status != 1:
            return None

        return user

    async def _verify_sms_code(self, phone: str, code: str) -> bool:
        """
        验证短信验证码

        Args:
            phone: 手机号
            code: 验证码

        Returns:
            是否验证成功
        """
        # TODO: 从Redis获取验证码并验证
        # redis_code = await redis_client.get(f"sms_code:{phone}")
        # return redis_code == code
        return True

    async def _get_wechat_user_info(self, code: str) -> Tuple[str, Optional[str]]:
        """
        获取微信用户信息

        Args:
            code: 微信登录code

        Returns:
            openid, unionid
        """
        # TODO: 调用微信API
        # response = await wechat_client.code2session(
        #     appid=settings.WECHAT_APP_ID,
        #     secret=settings.WECHAT_APP_SECRET,
        #     js_code=code
        # )
        # return response['openid'], response.get('unionid')
        return f"test_openid_{code}", None
