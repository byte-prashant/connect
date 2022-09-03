from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Assistance(Base):
    __tablename__ = "assistance"

    id = Column(Integer, primary_key=True, index=True)
    #request = relationship("Request", back_populates="assistance")
    request_id = Column(Integer, ForeignKey("request.id"))
    user_id = Column(ForeignKey("users.id"))
    #saint = relationship("User", back_populates="assistance")
    is_active = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=False)
    lat = Column(String)
    long = Column(String)

