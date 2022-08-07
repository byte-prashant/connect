from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class User(Base):
    __tablename__ = "users"
    name = Column(String, nullable=True)
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True)
    email = Column(String, nullable=True)
    # request = relationship("Request", back_populates="seeker")
    # assisance = relationship("Request", back_populates="saint")
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

