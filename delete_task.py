# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'ACa0c7d375ad90e3184d171d6668d406fd'
auth_token = '8dffc208ba28ddcafe7a81ffe3c519ee'
client = Client(account_sid, auth_token)

client.taskrouter.workspaces('WS7244082ec95ed738db257739b2e68ef6') \
                 .tasks('WT474e588c38a3eeab3bc7bb96117059b8') \
                 .delete()