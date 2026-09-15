from fastapi import APIRouter, HTTPException, Depends, Path

from app.schemas.product import(
    ProductCreate,
    ProductUpdate,
    ProductPatch,
    ProductResponse,
    DeleteResponse
)

from app.services.product_service import product_service

from sqlalchemy.orm import Session
from app.database.dependencies import get_db

from app.database.models import Product


router = APIRouter(
    prefix="/products",
    tags=["products"]
)



# Function to get the product by it's id
def get_existing_product(
    product_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    product = product_service.get_product_by_id(
        db,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product





# Endpoints
# Endpoint to create a product
@router.post(
    "/",
    response_model=ProductResponse,
    status_code=201
)
def create_product(
    product: ProductCreate,
    db: Session =  Depends(get_db)
):
    return product_service.create_product(
        db,
        product
    )


# Endpoint to get all products
@router.get(
    "/",
    response_model=list[ProductResponse]
)
def get_products(
    name: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    db: Session = Depends(get_db)
):
    return product_service.get_products(
        db,
        name,
        min_price,
        max_price
    )



# Endpoint to get a product by it's id
@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product: Product = Depends(get_existing_product)
):
    return product


# Endpoint to update product with PUT
@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    updated_product: ProductUpdate,
    product: Product = Depends(get_existing_product),
    db: Session = Depends(get_db)
):
    return product_service.update_product(
        db,
        updated_product,
        product
    )



# Endpoint to update product with PATCH
@router.patch(
    "/{product_id}",
    response_model=ProductResponse
)
def patch_product(
    patched_product: ProductPatch,
    product: Product = Depends(get_existing_product),
    db: Session = Depends(get_db)
):
    return product_service.patch_product(
        db,
        patched_product,
        product
    )



# Endpoint to delete product from the products list
@router.delete(
    "/{product_id}",
    response_model=DeleteResponse
)
def delete_product(
    product: Product = Depends(get_existing_product),
    db: Session = Depends(get_db)
):
    return product_service.delete_product(
        db,
        product
    )



