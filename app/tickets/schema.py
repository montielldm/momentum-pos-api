from pydantic import BaseModel
from typing import List, Optional

class Item(BaseModel):
    id: str
    product: str
    quantity: int
    discount: float
    subtotal: float

class ConfirmSale(BaseModel):
    payment_method: str
    customer: Optional[str] = None
    subtotal: float
    total: float
    discount: float
    items: List[Item]