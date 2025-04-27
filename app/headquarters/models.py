from providers.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Enum as SqlAlchemyEnum, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from typing import List
import uuid
from datetime import datetime
from app.tables.models import RestaurantTable

class StatusHeadquarters(str, Enum):
    ACTIVE = "ACTIVE"
    CLOSE = "CLOSE"

class Headquarter(Base):
    __tablename__ = "headquarters"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(String(500), nullable=False)
    phone: Mapped[str] = mapped_column(String(60), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(SqlAlchemyEnum(StatusHeadquarters), nullable=False)

    users: Mapped[List["User"]] = relationship("User", back_populates="headquarter")
    tables: Mapped[List["RestaurantTable"]] = relationship("RestaurantTable", back_populates="headquarter")

    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"))
    company: Mapped["Company"] = relationship("Company", back_populates="headquarters")
