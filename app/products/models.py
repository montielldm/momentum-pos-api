import uuid
from datetime import datetime
from providers.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Enum as SqlALchemyEnum, DateTime, Text, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from typing import List
from app.companies.models import Company

class StatusType(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    barcode: Mapped[str] = mapped_column(String(12), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    current_quantity: Mapped[int] = mapped_column(Integer, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    selling_price: Mapped[float] = mapped_column(Float, nullable=True)
    unit_measure: Mapped[str] = mapped_column(String(100), nullable=True)
    fixed_discount: Mapped[int] = mapped_column(Integer, nullable=True)
    percentage_discount: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(SqlALchemyEnum(StatusType), nullable=False, default=StatusType.ACTIVE)

    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"))
    company: Mapped["Company"] = relationship("Company", back_populates="products")

    category_id: Mapped[str] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="products")

    activities: Mapped[List["Activity"]] = relationship("Activity", back_populates="product")
