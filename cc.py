# Create workspace
# List activities
# Create extra activity
# Create taskqueues
# Create workflow
# Create workers with contact_uri
# Create tasks

from twilio.rest import Client
import json
import os

account_sid = os.environ.get("TWILIO_ACME_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_ACME_AUTH_TOKEN")

client = Client(account_sid, auth_token)

workspace_sid = 'WS0f2b388d844b4c7d57b6bb4e5631c43f'

offline_activity_sid ='WA1499518d2d300aa80ebe9c4e3783998a'
busy_activity_sid ='WAe634c0eae1a829f1544d8ccb52c712fe'
reserved_activity_sid ='WA7351bd65aa312c223f81ead35055b74d'
wrap_activity_sid ='WA0dabb19c8036a34ac28cb776f2c56174'

support_taskqueue_sid ='WQ21258a3d1aed284ea639223ad590db59'
sales_taskqueue_sid ='WQ85450933979fd66d615c1ddcc69b9da8'
marketing_taskqueue_sid ='WQ251c9de4f94cba1566c8a5e6384f749a'
manager_taskqueue_sid='WQ0742dd703d093f5ca8f65b547eb93ef1'

workflow_sid ='WW2fdf7db2899a1041f46905f25067f9fc'

task = client.taskrouter.workspaces(workspace_sid).tasks.create(
	workflow_sid=workflow_sid,
	attributes='{"selected_product":"support"}'

)


print(task.assignment_status, task.attributes)
# worker = client.taskrouter.workspaces(workspace_sid).workers.create(
# 	friendly_name='Suzanna',
# 	activity_sid=offline_activity_sid,
# 	attributes='{"skills": "manager"}'
# )

# workers = client.taskrouter.workspaces(workspace_sid).workers.list()

# for wk in workers:
# 	print(wk.sid, wk.friendly_name, wk.attributes)
# config = {
#     'task_routing': {
#         'filters': [
#             {
#                 'friendly_name': 'marketing filter',
#                 'expression': "selected_product =='marketing'",
#                 'targets': [{'queue': marketing_taskqueue_sid}]
#             },
#             {
#                 'friendly_name': 'support filter',
#                 'expression': "selected_product =='support'",
#                 'targets': [{'queue': support_taskqueue_sid}]
#             },
#             {
#                 'friendly_name': 'sales filter',
#                 'expression': "selected_product =='sales'",
#                 'targets': [{'queue': sales_taskqueue_sid}]
#             },
#             {
#                 'friendly_name': 'manager filter',
#                 'expression': "selected_product =='manager'",
#                 'targets': [{'queue': manager_taskqueue_sid}]
#             },
 
#         ],
#         'default_filter': {
#             'queue': support_taskqueue_sid
#         }
#     }
# }

# workflow = client.taskrouter.workspaces(workspace_sid).workflows.create(
# 	friendly_name='sales support marketing manager workflow',
# 	configuration=json.dumps(config)
# )

# print(workflow.sid)
# taskqueue = client.taskrouter.workspaces(workspace_sid).task_queues.create(
# 	friendly_name='manager',
# 	reservation_activity_sid =reserved_activity_sid,
# 	assignment_activity_sid=busy_activity_sid,
# 	target_workers='skills HAS "manager"'

# )

# taskqueues = client.taskrouter.workspaces(workspace_sid).task_queues.list()

# for tq in taskqueues:
# 	print(tq.sid, tq.friendly_name)



# wrap_up = client.taskrouter.workspaces(workspace_sid).activities.create(
# 	friendly_name='WrapUp',
# 	available=False
# )

# activities = client.taskrouter.workspaces(workspace_sid).activities.list()

# for act in activities:
# 	print(act.friendly_name, act.sid)
# workspace = client.taskrouter.workspaces.create(
# 	friendly_name='September class'
# )

# print(workspace.sid)