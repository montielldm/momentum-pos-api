from app.products.models import Product
from typing import List

def product_serializer(product: Product) -> dict:
    return {
        "id": product.id,
        "name": product.name,
        "current_quantity": product.current_quantity,
        "selling_price": product.selling_price,
        "fixed_discount": product.fixed_discount,
        "status": product.status,
        "company": product.company.company_name,
        "description": product.description,
        "created_at": product.created_at,
        "price": product.price,
        "unit_measure": product.unit_measure,
        "percentage_discount": product.percentage_discount,
        "category": product.category.name,
        "barcode": product.barcode
    }

def products_serializer(products: List[Product]) -> list:
    return [product_serializer(product) for product in products]
