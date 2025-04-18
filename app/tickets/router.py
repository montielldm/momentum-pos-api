from fastapi import APIRouter, Depends
from app.auth.utils import get_current_user
from app.tickets.schema import Item, ConfirmSale
from typing import List
from app.tickets.services import (
    get_all_tickets_service,
    confirm_ticket_service,
    get_ticket_by_id_service
)
from app.tickets.serializers import (
    tickets_serializer,
    ticket_serializer,
    ticket_to_details_serializer
)


tickets = APIRouter(prefix="/tickets", tags=["Tickets"])

@tickets.get("")
def get_all_tickets(user_id: str = Depends(get_current_user)):
    results = get_all_tickets_service()
    return tickets_serializer(results)

@tickets.get("/{id}")
def get_ticket_by_id(id: str, user_id: str = Depends(get_current_user)):
    result = get_ticket_by_id_service(id)
    return ticket_to_details_serializer(result)

@tickets.post("/confirm-ticket")
def confirm_ticket(data: ConfirmSale, user_id: str = Depends(get_current_user)):
    ticket = confirm_ticket_service(data, user_id)
    return ticket