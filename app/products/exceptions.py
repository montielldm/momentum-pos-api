from fastapi import HTTPException, status

def ProductNotFound():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="PRODUCT_NOT_FOUND",
    )
def ProductsNotFound():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="PRODUCTS_NOT_FOUND",
    )