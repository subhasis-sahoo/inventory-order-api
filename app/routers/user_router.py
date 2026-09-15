from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse
from app.schemas.order import OrderResponse

from app.services.user_service import user_service
from app.services.order_service import order_service

from app.database.dependencies import get_db
from app.database.models import User

from app.exceptions.user_exceptions import DuplicateEmailError
from app.exceptions.order_exceptions import UserNotFoundError





router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Function to get the product by it's id
def get_existing_user(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    user = user_service.get_user_by_id(
        user_id, db
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=201
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return user_service.create_user(
            user,
            db
        )

    except DuplicateEmailError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )



@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_all_users(
    db: Session = Depends(get_db)
):
    return user_service.get_users(db)




@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user_by_id(
    user: User = Depends(get_existing_user)
):
    return user




@router.get(
    "/{user_id}/orders",
    response_model=list[OrderResponse]
)
def get_orders_by_user_id(
    user_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    try:
        return order_service.get_orders_by_user_id(
            user_id,
            db
        )

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
