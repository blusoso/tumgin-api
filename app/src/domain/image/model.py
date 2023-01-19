from sqlalchemy import Column, String, Float, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ...database import Base


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    img = Column(String)
    img_format = Column(String, nullable=True)
    img_size = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    recipe_images = relationship('RecipeImage', back_populates='image')
