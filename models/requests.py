from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class Request(Base):
    __tablename__ = "request"

    id = Column(Integer, primary_key=True, index=True)
    req_type_id = Column(Integer, ForeignKey("request_type.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    seeker = relationship("User", back_populates="request")
    request_type = relationship("RequestType", back_populates="request")
    is_active = Column(Boolean, default=True)
    lat = Column(String)
    long = Column(String)

