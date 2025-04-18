import uuid
from datetime import datetime
from providers.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Enum as SqlALchemyEnum, DateTime, Text, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from typing import List
from app.products.models import Product
from app.customers.models import Customer

class TypeEnum(str, Enum):
    SALE = "SALE"
    PURCHASE = "PURCHASE"
    ADJUSTMENT = "ADJUSTMENT"
    REFUND = "REFUND"

class StatusTicket(str, Enum):
    OPEN = "OPEN"
    PAID = "PAID"
    CANCELLED = "CANCELLED"



class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    quantity: Mapped[int] = mapped_column(Integer, nullable=True)
    stock_before: Mapped[int] = mapped_column(Integer, nullable=True)
    stock_after: Mapped[int] = mapped_column(Integer, nullable=True)
    type: Mapped[str] = mapped_column(SqlALchemyEnum(TypeEnum), nullable=False)
    note: Mapped[str] = mapped_column(Text, nullable=True)
    discount: Mapped[float] = mapped_column(Float, nullable=True)
    subtotal: Mapped[float] = mapped_column(Float, nullable=True)
    total: Mapped[float] = mapped_column(Float, nullable=True)

    ticket_number: Mapped[str] = mapped_column(ForeignKey("tickets.ticket_number"))
    ticket: Mapped["Ticket"] = relationship(back_populates="activities")
    
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="activities")

    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))
    product: Mapped["Product"] = relationship("Product", back_populates="activities")


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    ticket_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    payment_method: Mapped[str] = mapped_column(String(60), nullable=False)
    status: Mapped[str] = mapped_column(SqlALchemyEnum(StatusTicket), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=True)
    discount: Mapped[int] = mapped_column(Integer, nullable=True)
    subtotal: Mapped[float] = mapped_column(Float, nullable=True)
    total: Mapped[float] = mapped_column(Float, nullable=True)

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="tickets")

    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"))
    customer: Mapped["Customer"] = relationship("Customer", back_populates="tickets")

    activities: Mapped[List["Activity"]] = relationship(back_populates="ticket")
    