#encoding: utf-8
from flask import Flask, request, Response, render_template

from twilio.rest import Client

from twilio.twiml.voice_response import VoiceResponse, Conference, Dial, Say , Gather
from twilio.twiml.messaging_response import Message, MessagingResponse
from datetime import datetime

import os


app = Flask(__name__, static_folder='app/static')

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = os.environ.get("TWILIO_ACME_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_ACME_AUTH_TOKEN")

caller_id = '+447481343625' # Contact Center's phone number to be used in outbound communication

workflow_sid = 'WW3c019f39653f0666d714941d8a449770'
workspace_sid ='WS9fc5bdef8cfa840f1af11889e3d08fd6'
wrap_up ='WA063bbabf2d615e36eeaa1b2b116d5ab7'

client = Client(account_sid, auth_token)


# setup a conference endpoint
@app.route("/conference", methods=['GET', 'POST'])
def conference():
	
	resp = VoiceResponse()

	resp.say('Thanks for joining the conference')

	dial = Dial()
	dial.conference('TrainingConference')
	 
	resp.append(dial)	

	return Response(str(resp), mimetype='text/xml')


@app.route("/group_call", methods=['GET', 'POST'])
def dial_group():
	
	# Create a group call endpoint that calls anyone that has messaged my Twilio number today 

	time = datetime(2018, 5, 30, 0, 0)
	resp = VoiceResponse()

	numbers = client.messages.list(
		date_sent=time,
		to=caller_id,
		)

	for number in numbers:

		call = client.calls.create(
			to = number.from_,
			from_= caller_id,
			url='https://73cae233.ngrok.io/conference'
			)

	return Response(str(resp), mimetype='text/xml')

@app.route("/incoming_call", methods=['GET', 'POST'])
def incoming_call():
    # Mission: Create TwiML that generates an IVR for the customer
    # Success criteria: Customer must be able to choose a department (sales/support/billing)
    # Docs: https://www.twilio.com/docs/voice/twiml/gather

    resp = VoiceResponse()

    gather = Gather(num_digits=1, action='/enqueue_call')
    gather.say('Welcome to Quality clean, thanks for calling')
    gather.say('Please select from the following options')
    gather.say('For support press one, for Sales press two, for marketing press 3')

    resp.append(gather)

    return Response(str(resp), mimetype='text/xml')

@app.route("/enqueue_call", methods=["GET", "POST"])
def enqueue_call():

    # Mission: Create TwiML that generates a Task  with attributes of the selected_product they chose
    # Success criteria: Task must be created with attributes and correct workflow for the specified product
    # Docs: https://www.twilio.com/docs/taskrouter/twiml-queue-calls

    if 'Digits' in request.values:
       
       choice = int(request.values['Digits'])

       department = {
       1: "support",
       2: "sales",
       3: "marketing"

       }

       resp = VoiceResponse()

       enqueue = resp.enqueue(workflow_sid=workflow_sid)
       enqueue.task('{"selected_product":"' + department[choice] + '"}')

       return Response(str(resp), mimetype='text/xml')
    else:
        resp = VoiceResponse()
        resp.say("no digits detected") #tell user something is amiss
        resp.redirect("/incoming_call")  #redirect back to initial step

    return Response(str(resp), mimetype='text/xml')


@app.route("/assignment_callback", methods=['GET', 'POST'])
def acceptTask():

   dequeue = '{"instruction": "dequeue", "from": "' + caller_id +'", "post_work_activity_sid": "'+ wrap_up + '"}'
  
   return Response(dequeue, mimetype='application/json')   

@app.route("/messages", methods=['GET', 'POST'])
def send_docs():

	body = str(request.values['Body']).lower()

	resp = MessagingResponse()

	if body == 'voice':
		resp.message('Hi thanks for taking part in this course! Here is a link to the TwiML we will be talking about today: \n\n Dial Verb: https://www.twilio.com/docs/voice/twiml/dial \n\n Conference noun: https://www.twilio.com/docs/voice/twiml/conference ')
	elif body == 'enqueue':
		resp.message('Hi thanks for taking part in this course! Here is a link to the TwiML we will be talking about today: \n\n Gather verb: https://www.twilio.com/docs/api/twiml/gather \n\n Enqueue verb: https://www.twilio.com/docs/voice/twiml/enqueue ')

	return Response(str(resp), mimetype='text/xml')
if __name__ == "__main__":
    app.run(debug=True)
