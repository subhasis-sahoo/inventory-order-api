from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import User


class UserRepository:

    def create_user(
        self,
        db: Session,
        user: User
    ):
        try:
            db.add(user)
            db.commit()
            db.refresh(user)

            return user

        except Exception:
            db.rollback()
            raise


    def get_all_users(
        self,
        db: Session
    ):
        return db.scalars(
            select(User)
        ).all()


    def get_user_by_id(
        self,
        db: Session,
        user_id: int
    ):
        return db.scalar(
            select(User).where(
                User.id == user_id
            )
        )


    def get_user_by_email(
        self,
        db: Session,
        email: str
    ):
        return db.scalar(
            select(User).where(
                User.email == email
            )
        )