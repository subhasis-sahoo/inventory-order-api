from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database.models import Order, OrderItem


class OrderRepository:

    def create_order(
        self,
        db: Session,
        order: Order,
        order_items: list[OrderItem]
    ):
        try:
            db.add(order)

            db.flush()

            for item in order_items:
                item.order_id = order.id
                db.add(item)

            db.commit()

            db.refresh(order)

            return order

        except Exception:
            db.rollback()
            raise


    def get_order_by_id(
    self,
    db: Session,
    order_id: int
    ):
        return db.scalar(
            select(Order).where(
                Order.id == order_id
            )
        )


    def get_orders_by_user_id(
        self,
        db: Session,
        user_id: int
    ):
        return db.scalars(
            select(Order).where(
                Order.user_id == user_id
            )
        ).all()