from app.users.services import get_user_by_id_service
from typing import List
from app.tickets.schema import Item, ConfirmSale
from app.tickets.models import TicketSale
from sqlalchemy import select
from providers.database import ConnectDatabase
from app.activities.models import Ticket, Activity, TypeEnum, StatusTicket
from sqlalchemy.exc import SQLAlchemyError
from app.customers.models import Customer
from fastapi import HTTPException
from app.users.models import User
from app.products.models import Product
from app.products.exceptions import ProductNotFound
from app.tickets.exceptions import (
    InsufficientStock,
    TicketNotFound
)
from app.tickets.utils import generate_ticket_number
from uuid import UUID

session = ConnectDatabase.getInstance().db

def get_all_tickets_service():
    try:
        stmt = select(Ticket)
        results = session.scalars(stmt).all()
        return results
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        raise e

def get_ticket_by_id_service(id: str):
    try:
        stmt = session.get(Ticket, id)
        if not stmt:
            TicketNotFound()
            
        return stmt
    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        raise e

def confirm_ticket_service(data: ConfirmSale, user_id: str):
    try:
        ticket_number = generate_ticket_number()
        
        customer: Customer | None = None
        if not data.customer:
            customer = session.query(Customer).filter_by(identification="0000000000").first()
        else:
            customer = session.get(Customer, data.customer)

        ticket = Ticket(
            ticket_number=ticket_number,
            payment_method=data.payment_method,
            quantity=len(data.items),
            discount=data.discount,
            subtotal=data.subtotal,
            total=data.total,
            customer_id=customer.id,
            user_id=UUID(user_id),
            status=StatusTicket.PAID
        )
        session.add(ticket)
        session.commit()
        session.refresh(ticket)

        activities = []

        for item in data.items:
            product = session.get(Product, item.product)

            if not product:
                ProductNotFound()
            
            new_stock = product.current_quantity - item.quantity
            if new_stock < 0:
                InsufficientStock()
             
            activity = Activity(
                quantity=item.quantity,
                stock_before=product.current_quantity,
                stock_after=new_stock,
                type=TypeEnum.SALE,
                note="",
                discount=int(item.discount),
                subtotal=item.subtotal,
                total=item.subtotal,
                ticket_number=ticket.ticket_number,
                user_id=user_id,
                product_id=product.id,
            )
            product.current_quantity = new_stock
            activities.append(activity)

        session.add_all(activities)
        session.commit()
        
        session.refresh(ticket)

        return ticket

    except (SQLAlchemyError, ValueError) as e:
        session.rollback()
        raise e

def generate_ticket_sale_service(
        user_id: str,
        ticket_id: str,
        cash: float,
        due: float,
        items: List[Item]
    ):
    user = get_user_by_id_service(user_id)
    ticket = TicketSale(
        products=items,
        ticket_id=ticket_id,
        company=user.company.company_name,
        nit=user.company.tax_identification,
        cash=cash,
        due=due
    )
    ticket.add_page()
    ticket.add_items()
    ticket.add_info_cash()
    ticket.add_company_info()
    ticket.output(f"ticket-{ticket_id}.pdf")
    return f"ticket-{ticket_id}.pdf"