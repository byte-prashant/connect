from sqlalchemy import Boolean, Column, Integer, String
from app.api.utils import get_hashed_password
from sqlalchemy.event import listen
from app.db.database import Base
import pyotp

def make_totp_secret():
    """ Function for generating a secret for TOTP algorithm """
    return pyotp.random_base32()

def hash_user_password(mapper, context, target):
    """ SQLAlchemy event hook for hashing raw passwords """
    target.hash_password()

class User(Base):
    __tablename__ = "users"
    name = Column(String, nullable=True)
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True)
    email = Column(String, nullable=True)
    otp_secret = Column(String, default=make_totp_secret)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_mobile_authenticated = Column(Boolean, default=False)

    def hash_password(self):
        """ Stores hashed password into DB instead of the raw one """
        self.hashed_password = get_hashed_password(self.hashed_password)

listen(User, "before_insert", hash_user_password)

