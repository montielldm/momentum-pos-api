from fastapi import HTTPException, status

def InsufficientStock():
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="INSUFFICIENT_STOCK",
    )

def TicketNotFound():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="TICKET_NOT_FOUND",
    )