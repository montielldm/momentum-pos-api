import uuid
from datetime import datetime
from providers.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Enum as SqlALchemyEnum, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from typing import List
from app.categories.models import Category
from app.products.models import Product

class StatusType(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name: Mapped[str] = mapped_column(String(100), nullable=False)
    tax_identification: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    fiscal_address: Mapped[str] = mapped_column(String(100), nullable=False)
    telephone: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    business_activity: Mapped[str] = mapped_column(String(100), nullable=False)
    tax_regime: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(SqlALchemyEnum(StatusType), nullable=False, default=StatusType.ACTIVE)

    users: Mapped[List["User"]] = relationship("User", back_populates="company")
    categories: Mapped[List["Category"]] = relationship("Category", back_populates="company")
    products: Mapped[List["Product"]] = relationship("Product", back_populates="company")