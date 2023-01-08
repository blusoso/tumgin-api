from sqlalchemy import Column, String, JSON, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .....database import Base


class DietType(Base):
    __tablename__ = 'diet_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    emoji = Column(String, nullable=True)
    description = Column(String, nullable=True)
    foods_allowed = Column(JSON, nullable=True)
    foods_restricted = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=True, server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        nullable=True, onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    user_diet_type = relationship(
        'UserDietType', back_populates='diet_type')