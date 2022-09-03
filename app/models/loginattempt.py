import os
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from app.db.database import Base


class LoginAttempt(Base):
    """ Describes a single registration attempt with an identifier """
    __tablename__ = "loginattempt"
    id = Column(Integer, primary_key=True)
    identifier = Column(String, nullable=False, unique=True, index=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    otp = Column(String, nullable=False)

    def is_within_time_thresoled(self) -> bool:
        return (
            datetime.utcnow() - self.updated
        ).seconds < int(os.environ['AUTH_OTP_THRESHOLD_SECONDS'])

