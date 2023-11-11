# twilio_utils.py
from twilio.rest import Client
from django.conf import settings
import re

def send_sms_verification_code(phone_number, verification_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verified_number = verify_and_format_phone_number(phone_number)
    if verified_number is None:
        return None

    message = client.messages.create(
        to=verified_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=f'Your verification code is: {verification_code}'
    )

    verification = client.verify.v2.services('VA36d4aa1165435adfff4d5bd2f9b42b5f').verifications.create(to=verified_number, channel="sms")
    print(verification.status)
    otp_code = input("Please enter the OTP:")

    verification_check = client.verify.v2.services('VA36d4aa1165435adfff4d5bd2f9b42b5f').verification_checks.create(to=verified_number, code=otp_code)
    print(verification_check.status)

    return message.sid


def verify_and_format_phone_number(phone_number):
    # Regular expression pattern for a valid phone number without '+1'
    pattern = re.compile(r'^\d{10}$')

    # Check if the phone number matches the pattern
    if re.match(pattern, phone_number):
        # If the phone number doesn't start with '+1', add it
        print("Valid phone number")
        if not phone_number.startswith('+1'):
            print("Adding +1 to phone number")
            phone_number = '+1' + phone_number
            print(phone_number)
            return phone_number

        return phone_number
    else:
        return None