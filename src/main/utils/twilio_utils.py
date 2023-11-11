# twilio_utils.py
from twilio.rest import Client
from django.conf import settings
import re

def send_sms_verification_code(phone_number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verified_number = verify_and_format_phone_number(phone_number)
    if verified_number is None:
        return None

    try:
        verification = client.verify.v2.services(settings.TWILIO_VERIFY_SID).verifications.create(to=verified_number, channel="sms")
    except Exception as e:
        print(e)
        return "failed"
    
    return verification.status

def check_verification_code(phone_number, verification_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verified_number = verify_and_format_phone_number(phone_number)
    if verified_number is None:
        return None

    try:
        verification_check = client.verify.v2.services(settings.TWILIO_VERIFY_SID).verification_checks.create(to=verified_number, code=verification_code)
    except Exception as e:
        print(e)
        return "failed"

    return verification_check.status



def verify_and_format_phone_number(phone_number):
    # Regular expression pattern for a valid phone number without '+1'
    pattern1 = re.compile(r'^\d{10}$')
    # Regular expression pattern for a valid phone number with '1' in front
    pattern2 = re.compile(r'^1\d{10}$')
    # Regular expression pattern for a valid phone number with '+1' in front
    pattern3 = re.compile(r'^\+1\d{10}$')

    # Check if the phone number matches any of the patterns
    if re.match(pattern1, phone_number):
        # If the phone number doesn't start with '+1', add it
        if not phone_number.startswith('+1'):
            phone_number = '+1' + phone_number
        return phone_number

    elif re.match(pattern2, phone_number):
        # If the phone number doesn't start with '+', add '+'
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        return phone_number

    elif re.match(pattern3, phone_number):
        return phone_number

    else:
        return None