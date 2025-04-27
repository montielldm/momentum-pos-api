from sqlalchemy.sql.sqltypes import Float
from providers.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SqlAlchemyEnum, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.tables.models import Headquarter  # <- Aquí solo se importa para type hinting

class StatusTable(str, Enum):
    AVAILABLE = "AVAILABLE"
    BOOKED = "BOOKED"
    BUSY = "BUSY"
    OUTOFSERVICE = "OUTOFSERVICE"

class OrientationTable(str, Enum):
    HORIZONTAL = "HORIZONTAL"
    VERTICAL = "VERTICAL"

class RestaurantTable(Base):
    __tablename__ = "tables"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(SqlAlchemyEnum(StatusTable), nullable=False, default=StatusTable.AVAILABLE)
    orientation: Mapped[str] = mapped_column(SqlAlchemyEnum(OrientationTable), nullable=False, default=OrientationTable.HORIZONTAL)

    position_x: Mapped[float] = mapped_column(Float, default=0)
    position_y: Mapped[float] = mapped_column(Float, default=0)

    headquarter_id: Mapped[str] = mapped_column(ForeignKey("headquarters.id"))
    headquarter: Mapped["Headquarter"] = relationship("Headquarter", back_populates="tables")
