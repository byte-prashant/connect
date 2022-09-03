
from app.models.loginattempt import LoginAttempt
from  app.schema.loginattempt import LoginAttemptSchema, UpdateLoginAttemptSchema
from datetime import datetime

class CRUDLoginAttempt:

    def create(self, db, *, login: LoginAttemptSchema) -> LoginAttempt:
        obj = LoginAttempt(identifier=login.identifier, otp=login.otp)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db, *, login: LoginAttemptSchema) -> UpdateLoginAttemptSchema:
        is_updated = db.query(LoginAttempt).filter(LoginAttempt.identifier == login.identifier).update({
            LoginAttempt.otp: login.otp
        }, synchronize_session=False)

        db.flush()
        db.commit()
        if is_updated:
            obj = db.query(LoginAttempt).filter(
                LoginAttempt.identifier == login.identifier).one()

            return UpdateLoginAttemptSchema(identifier=obj.identifier, otp=obj.otp,  msg="Updated successfully")
        else:
            return UpdateLoginAttemptSchema(msg="This username does not exists")

