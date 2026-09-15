
from app.schemas.product import(
    ProductCreate,
    ProductUpdate,
    ProductPatch
)

from sqlalchemy.orm import Session
from app.database.models import Product

from app.repositories.product_repository import ProductRepository


class ProductService:

    def __init__(self):
        self.repository = ProductRepository()


    def create_product(
        self,
        db: Session,
        product: ProductCreate
    ):
        new_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            stock=product.stock
        )

        return self.repository.create_product(
            db,
            new_product
        )



    def get_products(
        self,
        db: Session,
        name=None,
        min_price=None,
        max_price=None
    ):
        return self.repository.get_all_products(
            db,
            name,
            min_price,
            max_price
        )



    def get_product_by_id(
        self,
        db: Session,
        product_id: int
    ):
        return self.repository.get_product_by_id(
            db,
            product_id
        )



    def update_product(
        self,
        db: Session,
        updated_product: ProductUpdate,
        product: Product
    ):
        product.name = updated_product.name
        product.description = updated_product.description
        product.price = updated_product.price
        product.stock = updated_product.stock

        return self.repository.update(
            db,
            product
        )


    def patch_product(
        self,
        db: Session,
        patched_product: ProductPatch,
        product: Product
    ):
        updates = patched_product.model_dump(
            exclude_unset=True
        )

        for field, value in updates.items():
            setattr(product, field, value)

        return self.repository.patch(
            db,
            product
        )


    def delete_product(
        self,
        db: Session,
        product: Product
    ):
        return self.repository.delete(
            db,
            product
        )
    



product_service = ProductService()