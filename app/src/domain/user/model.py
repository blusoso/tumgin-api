from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ...database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True, unique=True)
    password_hash = Column(String(120), nullable=True)
    email = Column(String, unique=True)
    gender = Column(Integer)
    profile_img = Column(String, nullable=True)
    login_with = Column(String, default='site', nullable=True)
    is_active = Column(Boolean, default=True)
    is_consent = Column(Boolean, default=True)
    role = Column(String, default='user', nullable=False)
    created_at = Column(DateTime(timezone=True),
                        nullable=True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        nullable=True, onupdate=func.now())

    access_token = relationship(
        'AccessToken', back_populates='user')
    refresh_token = relationship(
        'RefreshToken', back_populates='user')