from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

def TablesNotFound(e:SQLAlchemyError):
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Errors in obtaining tables {str(e)}")

def TableNotFound():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table Not Found")
