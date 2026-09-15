from app.schemas.user import (
    UserCreate
)

from sqlalchemy.orm import Session

from app.database.models import User
from app.repositories.user_repository import UserRepository
from app.exceptions.user_exceptions import DuplicateEmailError

class UserService:

    def __init__(self):
        self.repository = UserRepository()

    def create_user(
        self,
        user: UserCreate,
        db: Session
    ):
        existing_user = self.repository.get_user_by_email(
            db,
            user.email
        )

        if existing_user:
            raise DuplicateEmailError(
                "Email already registered"
            )

        new_user = User(
            name=user.name,
            email=user.email
        )
            
        return self.repository.create_user(
            db,
            new_user
        )



    def get_users(
        self,
        db: Session
    ):
        return self.repository.get_all_users(db)



    def get_user_by_id(
        self,
        user_id: int,
        db: Session
    ):
        return self.repository.get_user_by_id(
            db,
            user_id
        )



user_service = UserService()