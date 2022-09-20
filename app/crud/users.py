from app.models.user import User
from  app.schema.users import RequestUserSchema


class CRUDUser:

    def create(self, db, *, user: RequestUserSchema) -> User:
        db_user = User(name=user.name, hashed_password=user.password, email=user.email, phone=user.phone,
                       is_active=True)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

