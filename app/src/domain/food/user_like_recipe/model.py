from sqlalchemy import Column,  DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ....database import Base


class UserLikeRecipe(Base):
    __tablename__ = 'user_like_recipes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    created_at = Column(DateTime(timezone=True),
                        nullable=True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship('User', back_populates='user_like_recipes')
    recipe = relationship('Recipe', back_populates='user_like_recipes')
