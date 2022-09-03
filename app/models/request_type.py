from sqlalchemy import Boolean, Column, Integer, String

from app.db.database import Base


class RequestType(Base):
    __tablename__ = "request_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)


