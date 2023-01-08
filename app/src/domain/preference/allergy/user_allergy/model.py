from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .....database import Base


class UserAllergy(Base):
    __tablename__ = 'user_allergies'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))
    created_at = Column(DateTime(timezone=True),
                        nullable=True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship(
        'User', back_populates='user_allergy')
    ingredient = relationship(
        'Ingredient', back_populates='user_allergy')