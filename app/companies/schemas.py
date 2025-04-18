from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    ticket_number: str
    product_id: str
    quantity: int
    discount: int
    subtotal: float
    total: float

class ConfirmSale(BaseModel):
    quantity: int
    discount: int
    subtotal: float
    total: float
    type: str
    cash: float
    due: float
    items: List[Item]