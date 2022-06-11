import os
from twilio.rest import Client
from ayurvita.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_VERIFICATION_SID


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def otp_verify(phone_number):
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    verification = TWILIO_VERIFICATION_SID
    client = Client(account_sid, auth_token)
    client.verify.services(verification).verifications.create(
        to='+91' + phone_number, channel='sms')


def verify(phone_number,otp):
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    verification = TWILIO_VERIFICATION_SID
    client = Client(account_sid, auth_token, verification)
    verification_check = client.verify \
        .services(verification) \
        .verification_checks \
        .create(to='+91'+phone_number, code=otp)
    
    if verification_check.status == 'approved':
        return True
    else:

        return False
