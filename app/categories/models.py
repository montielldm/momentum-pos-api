import uuid
from datetime import datetime
from providers.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Enum as SqlALchemyEnum, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from typing import List

class StatusType(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    status: Mapped[str] = mapped_column(SqlALchemyEnum(StatusType), nullable=False, default=StatusType.ACTIVE)

    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"))
    company: Mapped["Company"] = relationship("Company", back_populates="categories")

    products: Mapped[List["Product"]] = relationship("Product", back_populates="category")
