from sqlalchemy import select
from app.activities.models import Ticket
from providers.database import ConnectDatabase
from sqlalchemy.exc import PendingRollbackError

session = ConnectDatabase.getInstance().db

def get_all_tickets_service():
    try:
        stmt = select(Ticket)
        results = session.scalars(stmt).all()
        return results
    except PendingRollbackError as e:
        print("error: ", e)
        session.rollback()