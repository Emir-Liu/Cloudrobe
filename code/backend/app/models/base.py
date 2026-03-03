"""
数据库模型基类
"""
from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime
from app.db.session import Base


class BaseModel(Base):
    """模型基类"""
    __abstract__ = True
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键ID")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    def to_dict(self):
        """转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
