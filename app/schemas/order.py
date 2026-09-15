from datetime import datetime
from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):

    product_id: int = Field(
        gt=0,
        description="Product ID must be greateer than 0"
    )

    quantity: int = Field(
        gt=0,
        description="Quantity must be greateer than 0"
    )



class OrderCreate(BaseModel):

    user_id: int = Field(
        gt=0,
        description="User ID must be greater than 0"
    )

    items: list[OrderItemCreate] = Field(
        min_length=1,
        description="Order must contain at least one item"
    )



class OrderItemResponse(BaseModel):

    id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True



class OrderResponse(BaseModel):

    id: int
    user_id: int
    total_amount: float
    created_at: datetime
    order_items: list[OrderItemResponse]

    class Config:
        from_attributes = True