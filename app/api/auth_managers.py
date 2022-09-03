
from app.models.loginattempt import LoginAttempt

from datetime import datetime
class OtpLoginManager:

    def verify_otp(self, session, identifier, code):
        """ Verifies OTP for a single login attempt """
        attempt = session.query(LoginAttempt).filter_by(identifier=identifier, otp =code).first()
        print("Attempt otp is correct", attempt)
        print("Attempt otp is correct 2",attempt.is_within_time_thresoled()  )
        conditions = [
            attempt,
            attempt.is_within_time_thresoled(),
        ]
        if not all(conditions):
            return False
        return True



