from sqlalchemy.orm import Session

from app.database.models import Order, OrderItem
from app.schemas.order import OrderCreate
from app.repositories.order_repository import OrderRepository
from app.repositories.user_repository import UserRepository
from app.repositories.product_repository import ProductRepository

from app.exceptions.order_exceptions import (
    UserNotFoundError,
    ProductNotFoundError,
    InsufficientStockError
)


class OrderService:

    def __init__(self):
        self.order_repository = OrderRepository()
        self.user_repository = UserRepository()
        self.product_repository = ProductRepository()

    def create_order(
        self,
        db: Session,
        order_data: OrderCreate
    ):
        try:
            # Step-1: Check whether user exists 
            user = self.user_repository.get_user_by_id(
                db,
                order_data.user_id
            )

            if user is None:
                raise UserNotFoundError("User not found")


            # Step-2: Create empty list for OrderItem objects
            order_items = []

            # Step-3: Keep track of total order amount
            total_amount = 0

            # Step-4: Process every item in order
            for item in order_data.items:

                # Find product
                product = self.product_repository.get_product_by_id(
                    db,
                    item.product_id
                )

                if product is None:
                    raise ProductNotFoundError(
                        f"Product {item.product_id} not found"
                    )

                # Check stock
                if product.stock < item.quantity:
                    raise InsufficientStockError(
                        f"Insufficient stock for product {product.id}"
                    )

                # Get price from database
                item_total = product.price * item.quantity

                # Add to total order amount
                total_amount = total_amount + item_total

                # Reduce stock
                product.stock = product.stock - item.quantity

                # Create OrderItem
                order_item = OrderItem(
                    product_id=product.id,
                    quantity=item.quantity,
                    price=product.price
                )

                order_items.append(order_item)


            # Step-5: Create Order
            order = Order(
                user_id=user.id,
                total_amount=total_amount
            )

            # Step-6: Save everything through repository
            return self.order_repository.create_order(
                db,
                order,
                order_items
            )

        except Exception:
            db.rollback()
            raise


    def get_order_by_id(
        self,
        db: Session,
        order_id: int
    ):
        return self.order_repository.get_order_by_id(
            db,
            order_id
        )


    def get_orders_by_user_id(
        self,
        user_id: int,
        db: Session
    ):
        user = self.user_repository.get_user_by_id(
            db,
            user_id
        )

        if user is None:
            raise UserNotFoundError("User not found")

        return self.order_repository.get_orders_by_user_id(
            db,
            user_id
        )



order_service = OrderService()