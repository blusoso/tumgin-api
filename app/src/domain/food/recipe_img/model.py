from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ....database import Base


class RecipeImage(Base):
    __tablename__ = 'recipe_images'

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    image_id = Column(Integer, ForeignKey('images.id'))
    type = Column(String, default='general')
    created_at = Column(DateTime(timezone=True),
                        nullable=True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    recipe = relationship('Recipe', back_populates='recipe_images')
    image = relationship(
        'Image', back_populates='recipe_images')
