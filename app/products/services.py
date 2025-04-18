from providers.database import  ConnectDatabase
from app.products.models import Product
from sqlalchemy import select
from app.products.exceptions import ProductNotFound, ProductsNotFound

session = ConnectDatabase.getInstance().db

def get_all_products_service():
    try:
        stmt = select(Product)
        products = session.scalars(stmt).all()
        if not products:
            ProductsNotFound()
        else:
            return products
    except:
        pass

def get_product_by_barcode_service(barcode: str):
    try:
        stmt = select(Product).where(Product.barcode == barcode)
        product = session.scalars(stmt).first()
        if not product:
            ProductNotFound()
        else:
            return product
    except:
        pass
