from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.models import Product


class ProductRepository:

    def create_product(
        self,
        db: Session,
        product: Product
    ):
        try:
            db.add(product)
            db.commit()
            db.refresh(product)

            return product

        except Exception:
            db.rollback()
            raise



    def get_all_products(
        self,
        db: Session,
        name=None,
        min_price=None,
        max_price=None
    ):
        query = db.query(Product)

        if name:
            query = query.filter(Product.name.ilike(f"%{name}%"))

        if min_price is not None:
            query = query.filter(Product.price >= min_price)

        if max_price is not None:
            query = query.filter(Product.price <= max_price)

        return query.all()



    def get_product_by_id(
        self,
        db: Session,
        product_id: int
    ):
        return db.scalar(
            select(Product).where(
                Product.id == product_id
            )
        )


    def update(
        self,
        db: Session,
        product: Product
    ):
        try:
            db.commit()
            db.refresh(product)

            return product

        except Exception:
            db.rollback()
            raise



    def patch(
        self,
        db: Session,
        product: Product
    ):
        try: 
            db.commit()
            db.refresh(product)

            return product
        
        except Exception:
            db.rollback()
            raise


    def delete(
        self,
        db: Session,
        product: Product
    ):
        try:
            db.delete(product)
            db.commit()
            return {
                "message": "Product Deleted From The List"
            }
                
        except Exception:
            db.rollback()
            raise