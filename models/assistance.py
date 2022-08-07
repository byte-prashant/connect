from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class Assistance(Base):
    __tablename__ = "assistance"

    id = Column(Integer, primary_key=True, index=True)
    request = relationship("Request", back_populates="assistance")
    request_id = Column(Integer, ForeignKey("request.id"))
    user_id = Column(ForeignKey("users.id"), primary_key=True)
    saint = relationship("User", back_populates="assistance")
    is_active = Column(Boolean, default=True)
    seeker_lat = Column(String)
    seeker_lon = Column(String)

