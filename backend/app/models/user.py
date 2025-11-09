"""User model."""
from sqlalchemy import Column, String, Date, Numeric, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .base import Base


class User(Base):
    """User account information."""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    date_of_birth = Column(Date)
    diabetes_type = Column(String(20))  # 'type1', 'type2', 'prediabetes', 'gestational'
    target_glucose_min = Column(Numeric(5, 1), default=70.0)
    target_glucose_max = Column(Numeric(5, 1), default=180.0)
    timezone = Column(String(50), default="UTC")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(email={self.email}, name={self.full_name})>"
