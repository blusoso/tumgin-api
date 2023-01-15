from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ....database import Base


class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredient'

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))
    quantity = Column(Float, default=0)
    unit = Column(String)
    is_optional = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    recipe = relationship('Recipe', back_populates='recipe_ingredients')
    ingredient = relationship(
        'Ingredient', back_populates='recipe_ingredients')
