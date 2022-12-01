from sqlalchemy import Column, String, Float, Boolean, DateTime, Integer, Text
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from ....database import Base


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    minutes = Column(Integer, nullable=True)
    serve = Column(Integer, default=1, nullable=True)
    description = Column(Text, nullable=True)
    steps = Column(ARRAY(String), nullable=True)
    n_ingredients = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        nullable=True, onupdate=func.now())

    recipe_tags = relationship('RecipeTag', back_populates='recipe')
    recipe_ingredients = relationship(
        'RecipeIngredient', back_populates='recipe')
