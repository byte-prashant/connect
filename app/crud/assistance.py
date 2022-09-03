
from app.models.assistance import Assistance
from  app.schema.assistance import AssistanceSchema



class CRUDAssistance:

    def create(self, db, *, assis: AssistanceSchema) -> AssistanceSchema:
        obj = Assistance(request_id=assis.request_id, user_id=assis.user_id, lat=assis.lat, long=assis.long)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db, assist_id=int):
        is_updated = db.query(Assistance).filter(Assistance.id == assist_id).update({
           Assistance.is_approved: True
        }, synchronize_session=False)

        db.flush()
        db.commit()
        if is_updated:
            obj = db.query(Assistance).filter(Assistance.id == assist_id).one()

            return obj
        else:
            return ""

