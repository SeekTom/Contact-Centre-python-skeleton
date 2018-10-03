from twilio.rest import Client
import os

account_sid = os.environ.get("TWILIO_ACME_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_ACME_AUTH_TOKEN")
callerID = '+14152002423'

#TwiML Bin
#https://handler.twilio.com/twiml/EHb5858982b633ee1651420127db2d2b77'
#https://api.twilio.com/Cowbell.mp3

client = Client(account_sid, auth_token)

