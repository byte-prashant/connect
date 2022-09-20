from  app.schema.request import CreateRequestSchema
from app.models.requests import Request


class CRUDRequest:

    def create(self, db, *, request:CreateRequestSchema):
        db_req = Request(reference_no=request.reference_no, req_type_id=request.request_type, user_id=request.user_id,
                         lat=request.lat, long=request.long, is_active=True)
        db.add(db_req)
        db.commit()
        db.refresh(db_req)
        return db_req


