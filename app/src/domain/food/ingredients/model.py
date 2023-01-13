from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ....database import Base


class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String)
    emoji = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    is_allergy = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    recipe_ingredients = relationship(
        'RecipeIngredient', back_populates='ingredient')
    user_allergy = relationship(
        'UserAllergy', back_populates='ingredient')
