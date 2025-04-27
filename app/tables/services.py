from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.tables.models import RestaurantTable
from app.tables.schemas import SavePositions, TableRegister
from app.users.services import get_user_by_id_service
from app.tables.exceptions import TableNotFound

def get_all_tables_service(session: Session, user_id: str):
    user = get_user_by_id_service(user_id)

    stmt = select(RestaurantTable).where(RestaurantTable.headquarter == user.headquarter)
    results = session.scalars(stmt).all()

    return results

def create_table_service(session: Session, table:TableRegister, user_id: str):
    user = get_user_by_id_service(user_id)

    stmt = select(func.count(RestaurantTable.id))
    result = session.scalar(stmt)

    table = RestaurantTable(
        number=result + 1 if result else 1,
        headquarter_id=user.headquarter_id,
        seats=table.seats
    )

    session.add(table)
    session.commit()
    session.refresh(table)

    return table

def save_position_service(session:Session, save_position:SavePositions, user_id):
    table = session.get(RestaurantTable, save_position.table_id)
    if table is None:
        TableNotFound()
    else:
        table.position_y = save_position.position_y
        table.position_x = save_position.position_x

        session.add(table)
        session.commit()
        session.refresh(table)

        return table
