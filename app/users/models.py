import uuid
from datetime import datetime
from providers.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Enum as SqlALchemyEnum, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from typing import List
from app.activities.models import Activity, Ticket

class StatusType(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class DocumentType(str, Enum):
    RC = "RC"
    TI = "TI"
    CC = "CC"
    TE = "TE"
    CE = "CE"

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    lastname: Mapped[str] = mapped_column(String(100))
    document_type: Mapped[str] = mapped_column(SqlALchemyEnum(DocumentType), nullable=False)
    document: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    telephone: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    avatar: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(SqlALchemyEnum(StatusType), nullable=False, default=StatusType.ACTIVE)
    password: Mapped[str] = mapped_column(Text, nullable=True)

    headquarter_id: Mapped[str] = mapped_column(ForeignKey("headquarters.id"))
    headquarter: Mapped["Headquarter"] = relationship(back_populates="users")

    activities: Mapped[List["Activity"]] = relationship(back_populates="user")
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="user")
