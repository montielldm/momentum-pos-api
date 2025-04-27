from fastapi import APIRouter, Depends
from sqlalchemy.util.typing import Annotated
from app.tables.serializers import table_serializer, tables_serializer
from providers.database import get_session
from app.tables.services import (
    get_all_tables_service,
    create_table_service,
    save_position_service
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.auth.utils import get_current_user
from app.tables.exceptions import (
    TablesNotFound
)
from app.tables.schemas import TableRegister, SavePositions

tables = APIRouter(
    prefix="/tables",
    tags=["Tables"]
)

SessionDep = Annotated[Session, Depends(get_session)]
UserDep = Annotated[str, Depends(get_current_user)]

@tables.get("/")
def get_all_tables(session: SessionDep, user_id: UserDep):
    try:
        tables = get_all_tables_service(session, user_id)
        return tables_serializer(tables)
    except SQLAlchemyError as e:
        TablesNotFound(e)

@tables.post("/")
def create_table(session: SessionDep, table: TableRegister, user_id: UserDep):
    try:
        table = create_table_service(session, table, user_id)
        return table_serializer(table)
    except SQLAlchemyError as e:
        TablesNotFound(e)

@tables.post("/save-positions")
def save_positions(session: SessionDep, save_positions: SavePositions, user_id: UserDep):
    try:
        table = save_position_service(session, save_positions, user_id)
        return table_serializer(table)
    except SQLAlchemyError as e:
        TablesNotFound(e)
