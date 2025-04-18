from fastapi import APIRouter, Depends
from app.products.services import (
    get_product_by_barcode_service,
    get_all_products_service
)
from app.products.exceptions import (
    ProductNotFound,
    ProductsNotFound
)
from app.products.serializers import (
    product_serializer,
    products_serializer
)
from app.auth.utils import get_current_user


products = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@products.get("/")
def get_all_products(user_id: str = Depends(get_current_user)):
    products = get_all_products_service()
    if not products:
        ProductsNotFound()
    else:
        return products_serializer(products)

@products.get("/barcode/{barcode}")
def get_product_by_id(barcode: str, user_id: str = Depends(get_current_user)):
    product = get_product_by_barcode_service(barcode)
    if not product:
        ProductNotFound()
    else:
        return product_serializer(product)
