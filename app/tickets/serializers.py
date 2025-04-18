from app.activities.models import Ticket
from typing import List
from app.customers.serializers import customer_serializer
from app.users.serializers import user_serializer

def ticket_to_details_serializer(ticket: Ticket) -> dict:
    return {
        "id": ticket.id,
        "created_at": ticket.created_at,
        "payment_method": ticket.payment_method,
        "quantity": ticket.quantity,
        "subtotal": ticket.subtotal,
        "user": user_serializer(ticket.user),
        "customer": customer_serializer(ticket.customer),
        "ticket_number": ticket.ticket_number,
        "status": ticket.status,
        "discount": ticket.discount,
        "total": ticket.total,
        "activities": ticket.activities
    }

def ticket_serializer(ticket: Ticket) -> dict:
    return {
        "id": ticket.id,
        "created_at": ticket.created_at,
        "payment_method": ticket.payment_method,
        "quantity": ticket.quantity,
        "subtotal": ticket.subtotal,
        "user": ticket.user.name,
        "customer": ticket.customer.name,
        "ticket_number": ticket.ticket_number,
        "status": ticket.status,
        "discount": ticket.discount,
        "total": ticket.total,
    }

def tickets_serializer(tickets: List[Ticket]) -> list:
    return [ticket_serializer(ticket) for ticket in tickets]