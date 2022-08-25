from twilio.rest import Client
import os
def send_sms(body,to):

    print("you are inside celery msg function")
    account_sid = os.environ['TWILIO_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        messaging_service_sid='MG2190d9dde227cc4ab4902b056c7612be',
        body= str(body),
        to=to
    )
    return str(message)