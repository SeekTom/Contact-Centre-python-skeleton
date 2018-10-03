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

caller_id = '+14152002423' # Contact Center's phone number to be used in outbound communication

workflow_sid = 'WW2fdf7db2899a1041f46905f25067f9fc'
wrap_up ='WA0dabb19c8036a34ac28cb776f2c56174'

client = Client(account_sid, auth_token)

@app.route("/", methods=['GET', 'POST'])
def hello():
    resp = VoiceResponse()
    resp.say(language='en-gb', voice='alice', message='hello world')
    
    return (Response(str(resp), mimetype='text/xml'))

#https://api.twilio.com/Cowbell.mp3

@app.route("/call", methods=['GET', 'POST'])
def calls():
    resp = VoiceResponse()
    resp.say('Hi thanks for calling here is some music')
    resp.play('https://api.twilio.com/Cowbell.mp3')
    

   
    return Response(str(resp), mimetype='text/xml')


# setup a conference endpoint
@app.route("/conference", methods=['GET', 'POST'])
def conference():
    resp = VoiceResponse()
    dial = Dial()
    dial.conference('trainingConference')
    resp.append(dial)
    

    return Response(str(resp), mimetype='text/xml')

@app.route("/group_call", methods=['GET', 'POST'])
def dial_group():
    
    #http://ca951a90.ngrok.io/
    # Create a group call endpoint that calls anyone that has messaged my Twilio number today 

    time = datetime(2018, 9, 11, 0, 0)
    resp = VoiceResponse()

    #list out messages sent to the number sent today (include date_sent and to)
    #top5 = numbers[:5]

    numbers = client.messages.list(
        date_sent=time,
        to= caller_id
    )
    
    top5 = numbers[:5]

    for number in top5:
        client.calls.create(
            from_=caller_id,
            to=number.from_,
            url='http://ca951a90.ngrok.io/conference'
        )
    
   
    return Response(str(resp), mimetype='text/xml')

@app.route("/incoming_call", methods=['GET', 'POST'])
def incoming_call():
    # Mission: Create TwiML that generates an IVR for the customer
    # Success criteria: Customer must be able to choose a department (sales/support/billing)
    # Docs: https://www.twilio.com/docs/voice/twiml/gather

    resp = VoiceResponse()
    gather = Gather(num_digits=1, action="/enqueue_call") 

    gather.say("hi thanks for calling, please select your department")
    gather.say("for support, press one, for sales press two, for marketing press 3")

    resp.append(gather)
    return Response(str(resp), mimetype='text/xml')

@app.route("/enqueue_call", methods=["GET", "POST"])
def enqueue_call():

    # Mission: Create TwiML that generates a Task  with attributes of the selected_product they chose
    # Success criteria: Task must be created with attributes and correct workflow for the specified product
    # Docs: https://www.twilio.com/docs/taskrouter/twiml-queue-calls

    if 'Digits' in request.values:
       
       choice = int(request.values['Digits'])
       resp = VoiceResponse()

       product = {
           1: "support",
           2: "sales",
           3: "marketing"
       }
      
       enqueue = resp.enqueue(workflow_sid=workflow_sid)
       enqueue.task('{"selected_product":"' + product[choice] + '"}')

       #Create the Task via Enqueue verb
       return Response(str(resp), mimetype='text/xml')
    else:
        resp = VoiceResponse()
        resp.say("no digits detected") #tell user something is amiss
        resp.redirect("/incoming_call")  #redirect back to initial step
    return Response(str(resp), mimetype='text/xml')


@app.route("/assignment_callback", methods=['GET', 'POST'])
def acceptTask():
      #Create assignment callback endpoint and associate with workflo
    dequeue = '{"instruction": "dequeue", "from": "' + caller_id +'", "post_work_activity_sid": "'+ wrap_up + '"}'
   
    return Response(dequeue, mimetype='application/json')   

@app.route("/messages", methods=['GET', 'POST'])
def send_docs():

    body = str(request.values['Body']).lower()

    resp = MessagingResponse()

    if body == 'voice':
        resp.message('Hi thanks for taking part in this course! Here is a link to the TwiML we will be talking about in this session: \n\n Dial Verb: https://www.twilio.com/docs/voice/twiml/dial \n\n Conference noun: https://www.twilio.com/docs/voice/twiml/conference ')
    elif body == 'enqueue':
        resp.message('Hi thanks for taking part in this course! Here is a link to the TwiML we will be talking about in this session: \n\n Gather verb: https://www.twilio.com/docs/api/twiml/gather \n\n Enqueue verb: https://www.twilio.com/docs/voice/twiml/enqueue ')

    return Response(str(resp), mimetype='text/xml')
if __name__ == "__main__":
    app.run(debug=True)
