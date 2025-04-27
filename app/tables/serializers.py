from app.tables.models import RestaurantTable
from typing import Sequence

def table_serializer(table: RestaurantTable) -> dict:
    return {
        "id": table.id,
        "created_at": table.created_at,
        "number": table.number,
        "seats": table.seats,
        "status": table.status,
        "orientation": table.orientation,
        "headquarter": table.headquarter.name,
        "position_x": table.position_x,
        "position_y": table.position_y,
    }

def tables_serializer(tables: Sequence[RestaurantTable]) -> list:
    return [table_serializer(table) for table in tables]
