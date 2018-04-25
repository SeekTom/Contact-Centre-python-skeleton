# encoding: utf-8
from flask import Flask, request, Response, render_template, jsonify
from twilio.rest import Client
from twilio.jwt.taskrouter.capabilities import WorkerCapabilityToken
from twilio.twiml.voice_response import VoiceResponse, Conference, Enqueue, Dial
from twilio.twiml.messaging_response import Message, MessagingResponse
from twilio.jwt.client import ClientCapabilityToken
import os

app = Flask(__name__, static_folder='app/static')

# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = os.environ.get("TWILIO_ACME_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_ACME_AUTH_TOKEN")
workspace_sid = os.environ.get("TWILIO_ACME_ALT_WORKSPACE_SID") # workspace
workflow_support_sid = os.environ.get("TWILIO_ACME_ALT_SUPPORT_WORKFLOW_SID")  # support workflow
workflow_sales_sid = os.environ.get("TWILIO_ACME_ALT_SALES_WORKFLOW_SID")  # sales workflow
workflow_billing_sid = os.environ.get("TWILIO_ACME_ALT_BILLING_WORKFLOW_SID")  # billing workflow
workflow_mngr_sid = os.environ.get("TWILIO_ACME_ALT_MANAGER_WORKFLOW_SID") # manager escalation workflow
twiml_app = os.environ.get("TWILIO_ACME_TWIML_APP_SID") # Twilio client application SID
caller_id = os.environ.get("TWILIO_ACME_CALLER_ID") # Contact Center's phone number to be used in outbound communication

client = Client(account_sid, auth_token)


# Private functions

# Main browser entry point - renders index page

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')

@app.route("/incoming_call", methods=['GET', 'POST'])
def incoming_call():
    # Mission: Create TwiML that generates an IVR for the customer
    # Success criteria: Customer must be able to choose a department (sales/support/billing)
    # Docs: https://www.twilio.com/docs/voice/twiml/gather

    resp = VoiceResponse()
    with resp.gather(num_digits="1", action="/enqueue_call", timeout=10) as g:
       g.say("For sales press one, for support press two, for billing press three", language="en")

    return Response(str(resp), mimetype='text/xml')

@app.route("/enqueue_call", methods=["GET", "POST"])
def enqueue_call():

    # Mission: Create TwiML that generates a Task  with attributes of the selected_product they chose
    # Success criteria: Task must be created with attributes and correct workflow for the specified product
    # Docs: https://www.twilio.com/docs/taskrouter/twiml-queue-calls

    if 'Digits' in request.values:
        choice = int(request.values['Digits'])
        switcher = {
            1: os.environ.get('TWILIO_ACME_ALT_SALES_WORKFLOW_SID'),
            2: os.environ.get('TWILIO_ACME_ALT_SUPPORT_WORKFLOW_SID'),
            3: os.environ.get('TWILIO_ACME_ALT_BILLING_WORKFLOW_SID')
        }

        dept = {
            1: "sales",
            2: "support",
            3: "billing"

        }
        resp = VoiceResponse()
        resp.say('Thank you, connecting you now')
        with resp.enqueue(workflow_sid=switcher[choice]) as e:
            e.task('{"selected_product" : "' + dept[choice] + '"}')

        return Response(str(resp), mimetype='text/xml')
    else:
        resp = VoiceResponse()
        resp.say("no digits detected") #tell user something is amiss
        resp.redirect("/incoming_call")  #redirect back to initial step
    return Response(str(resp), mimetype='text/xml')


 # Place customer on hold

@app.route("/callmute", methods=['GET', 'POST'])
def unmuteCall():

    # Use the Participants API to enable muting of the customer call
    #docs https://www.twilio.com/docs/voice/api/conference-participant
    # request parameters sent to this endpoint from the agent desktop are
    #'conference' - the conference SID
    #'participant' - the customers call SID
    #'muted' - the desired muted status

    participant = client \
        .conferences(request.values.get('conference')) \
        .participants(request.values.get('participant')) \
        .update(hold=request.values.get('muted'))

    resp = VoiceResponse
    return Response(str(resp), mimetype='text/xml')

# Call Transfer

@app.route("/callTransfer", methods=['GET', 'POST'])
def transferCall():

    # Endpoint: transfer call

    #########################################################
    # Mission: Create the call transfer functionality by creating a new task via the API for the manager escalation
    #########################################################
    # Make sure you have created the Manager worker, workflow and taskqueue!
    # Make sure to mute the customer prior to the transfer via the participants API!
    #
    # Include the following task attributes
    # 'selected_product' - set this to be the manager skill
    # 'conference' - the customer conference SID
    # 'customer' - the customers call SID
    # 'customer_taskSid' - the customer task SID

    #########################################################
    # Request values sent to this endpoint from agent desktop:
    #########################################################
    #  tasksid, conference SID
    # 'taskSid' - the customer Task Sid
    # 'conference' - the current customer conference SID
    # 'participant' the customers call SID

    ##########################################################
    #Docs:
    #########################################################
    # Create task via API https://www.twilio.com/docs/taskrouter/api/tasks#action-create
    # Partipants API https://www.twilio.com/docs/voice/api/conference-participant
    # Warm Call transfer https://www.twilio.com/docs/taskrouter/contact-center-blueprint/call-control-concepts#warm-transfer

    participant = client \
        .conferences(request.values.get('conference')) \
        .participants(request.values.get('participant')) \
        .update(hold=True)

    task = client.taskrouter.workspaces(workspace_sid).tasks \
        .create(workflow_sid=workflow_mngr_sid, task_channel="voice",
                attributes='{'
                           '"selected_product":"manager",'
                           '"conference":"' + request.values.get('conference') + '", '
                           '"customer":"' + request.values.get('participant') + '", '
                           '"customer_taskSid":"' + request.values.get('taskSid') + '"}')

    resp = VoiceResponse
    return Response(str(resp), mimetype='text/xml')

# TwiML route to direct manager into conference with Customer

@app.route("/transferTwiml", methods=['GET', 'POST'])
def transferToManager():

    # Mission: Create TwiML that dials the customer conference
    # Docs: https://www.twilio.com/docs/voice/twiml/conference
    # Request parameters sent to this endpoint from the agent desktop
    # 'TaskSid' - the customer TaskSid

    response = VoiceResponse()
    dial = Dial()
    dial.conference(request.values.get('TaskSid'))
    response.append(dial)

    return Response(str(response), mimetype='text/xml')







###################### Agent views_do_not_change_things_will_break! ######################

# List of all agents (voice) together with their availability

@app.route("/agent_list", methods=['GET', 'POST'])
def generate_agent_list_view():
    # Create arrays of workers and share that with the template so that workers can be queried on the client side

    # get workers with enabled voice-channel
    voice_workers = client.taskrouter.workspaces(workspace_sid) \
        .workers.list(target_workers_expression="worker.channel.voice.configured_capacity > 0")

    return render_template('agent_list.html', voice_workers=voice_workers)


# Renders individual agent's voice desktop

@app.route("/agents", methods=['GET'])
def generate_view(charset='utf-8'):
    #This route generates
    #worker token
    #Client capability token

     #Create dictionary with activity SIDs
    activity = {}
    activities = client.taskrouter.workspaces(workspace_sid).activities.list()
    for a in activities:
        activity[a.friendly_name] = a.sid

    worker_sid = request.args.get('WorkerSid')  # TaskRouter Worker Token
    worker_capability = WorkerCapabilityToken(
        account_sid=account_sid,
        auth_token=auth_token,
        workspace_sid=workspace_sid,
        worker_sid=worker_sid
    )  # generate worker capability token

    worker_capability.allow_update_activities()  # allow agent to update their activity status e.g. go offline
    worker_capability.allow_update_reservations()  # allow agents to update reservations e.g. accept/reject
    worker_token = worker_capability.to_jwt(ttl=28800)

    capability = ClientCapabilityToken(account_sid, auth_token)  # agent Twilio Client capability token
    capability.allow_client_outgoing(twiml_app)
    capability.allow_client_incoming(worker_sid)

    client_token = capability.to_jwt()

    # render client/worker tokens to the agent desktop so that they can be queried on the client side
    return render_template('agent_desktop.html', token=client_token.decode("utf-8"),
                           worker_token=worker_token.decode("utf-8"),
                           client_=worker_sid, activity=activity,
                           caller_id=caller_id)




if __name__ == "__main__":
    app.run(debug=True)
