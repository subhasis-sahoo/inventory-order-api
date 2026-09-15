from fastapi import APIRouter, HTTPException, Depends, Path

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.order_service import order_service

from app.schemas.order import (
    OrderCreate,
    OrderResponse
)

from app.exceptions.order_exceptions import (
    UserNotFoundError,
    ProductNotFoundError,
    InsufficientStockError
)


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)



@router.post(
    "/",
    response_model=OrderResponse,
    status_code=201
)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    try:
        return order_service.create_order(
            db,
            order_data
        )

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except ProductNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except InsufficientStockError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order_by_id(
    order_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    order = order_service.get_order_by_id(
        db,
        order_id
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order




