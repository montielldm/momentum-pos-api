from providers.database import ConnectDatabase
from sqlalchemy.exc import PendingRollbackError
from app.users.services import (
    get_user_by_document_service,
    get_user_by_id_service
)
from app.auth.utils import (
    verify_password,
    hash_password
)
from app.users.exceptions import UserNotFound

session = ConnectDatabase.getInstance().db

def authenticate_user_service(document: str, password: str):
    try:
        user = get_user_by_document_service(document)
        if not user:
            pass
        else:
            if not verify_password(password, user.password):
                return None
            return user.id
    except PendingRollbackError as e:
            print("error: ", e)
            session.rollback()

def reset_password_service(user_id: str, new_password: str):
    try:
        user = get_user_by_id_service(user_id)
        if not user:
            UserNotFound()
        else:
            hashed_password = hash_password(new_password)
            user.password = hashed_password
            session.commit()
            session.refresh(user)
            return user
    except PendingRollbackError as e:
        print("error: ", e)
        session.rollback()
