from sqlalchemy import Column, ForeignKey, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .....database import Base


class UserDietType(Base):
    __tablename__ = 'user_diet_types'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    diet_type_id = Column(Integer, ForeignKey('ingredients.id'))
    created_at = Column(DateTime(timezone=True),
                        nullable=True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship(
        'User', back_populates='user_diet_type')
    diet_type = relationship(
        'DietType', back_populates='user_diet_type')