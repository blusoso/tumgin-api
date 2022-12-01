from sqlalchemy import Column, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ....database import Base


class RecipeTag(Base):
    __tablename__ = 'recipe_tag'

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    tag_id = Column(Integer, ForeignKey('tags.id'))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        nullable=True, onupdate=func.now())

    recipe = relationship('Recipe', back_populates='recipe_tags')
    tag = relationship('Tag', back_populates='recipe_tags')
