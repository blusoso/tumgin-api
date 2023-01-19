from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from ....database import Base


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    name_en = Column(String)
    slug = Column(String)
    description = Column(Text, nullable=True)
    thumbnail_img = Column(String, nullable=True)
    difficult_level = Column(Integer)
    calory = Column(Float, nullable=True)
    minute = Column(Integer, nullable=True)
    serving = Column(Integer, default=1, nullable=True)
    protein_gram = Column(Float, nullable=True)
    protein_percent = Column(Float, nullable=True)
    fat_gram = Column(Float, nullable=True)
    fat_percent = Column(Float, nullable=True)
    carb_gram = Column(Float, nullable=True)
    carb_percent = Column(Float, nullable=True)
    is_staff_pick = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship(
        'User', back_populates='recipe')
    recipe_tags = relationship('RecipeTag', back_populates='recipe')
    recipe_ingredients = relationship(
        'RecipeIngredient', back_populates='recipe')
    directions = relationship('Direction', back_populates='recipe')
    user_like_recipes = relationship('UserLikeRecipe', back_populates='recipe')
    reviews = relationship('Review', back_populates='recipe')
    recipe_images = relationship('RecipeImage', back_populates='recipe')
