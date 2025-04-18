import uuid
from datetime import datetime
from providers.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    identification: Mapped[str] = mapped_column(String(60), nullable=True, unique=True)
    type_identification: Mapped[str] = mapped_column(String(60), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(100), nullable=True)

    tickets: Mapped[List["Ticket"]] = relationship(back_populates="customer")
    
