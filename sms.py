from twilio.rest import Client
from datetime import datetime
import os

account_sid = os.environ.get("TWILIO_ACME_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_ACME_AUTH_TOKEN")
callerID = os.environ.get("TWILIO_ACME_CALLERID")

client = Client(account_sid, auth_token)

sms = client.messages.create(
	from_='MG879c5b15284572733cdee42a5ed08fac',
	to ='+61457314916',
	body ='sent using messaging service!'
)

print(sms.sid, sms.body)