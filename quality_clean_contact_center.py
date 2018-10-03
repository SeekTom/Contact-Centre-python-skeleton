from twilio.rest import Client
import os
import json

account_sid = os.environ.get('TWILIO_ACME_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_ACME_AUTH_TOKEN')

client = Client(account_sid, auth_token)

workspace_sid = 'WSa2e82bb8a6c3e7780efc85f946deb9cf'

busy_activity_sid = 'WA57ac3e71a84f5591da3ac587e8e52aa3'
reserved_activity_sid ='WA39499ffbb182cbc6a8629bebc9aabc27'
offline_activity_sid = 'WA72fd3a3a4827ce930fee0c1715286373'
wrapup_activity_sid = 'WA5b4ecac466cf888dbff14d50dae7eed7'

support_taskqueue_sid ='WQ0509ba6199ac30a33aa4773d787abbe6'
sales_taskqueue_sid ='WQecd3d2954d99aec87306342c380b2f58'

workflow_sid = 'WW5f2fd1cdd3ef8a8ce7bcb106e4f3177d'


task = client.taskrouter.workspaces(workspace_sid).tasks.create(
	workflow_sid= workflow_sid,
	attributes='{"selected_product": "support"}'
	)

print(task.sid, task.attributes, task.assignment_status)

# worker_support = client.taskrouter.workspaces(workspace_sid).workers.create(
# 	friendly_name = 'Bob',
# 	activity_sid =offline_activity_sid,
# 	attributes = '{"skills": "support"}'
# )

# worker_sales = client.taskrouter.workspaces(workspace_sid).workers.create(
# 	friendly_name = 'Suzanna',
# 	activity_sid =offline_activity_sid,
# 	attributes = '{"skills": "sales"}'
# )

# workers = client.taskrouter.workspaces(workspace_sid).workers.list()
# for worker in workers:
# 	print(worker.sid, worker.friendly_name, worker.attributes)

# config = {
#     'task_routing': {
#         'filters': [
#               {
#                 'friendly_name': 'support filter',
#                 'expression': "selected_product =='support'",
#                 'targets': [{'queue': support_taskqueue_sid}]
#             },
#             {
#                 'friendly_name': 'sales filter',
#                 'expression': "selected_product =='sales'",
#                 'targets': [{'queue': sales_taskqueue_sid}]
#             }
#         ],
#         'default_filter': {
#             'queue': support_taskqueue_sid
#         }
#     }
# }

# workflow = client.taskrouter.workspaces(workspace_sid).workflows.create(
# friendly_name='sales support workflow',
# configuration = json.dumps(config)
# 	)

# print(workflow.sid)

# # sales_taskqueue = client.taskrouter.workspaces(workspace_sid).task_queues.create(
# 	friendly_name='Sales',
# 	reservation_activity_sid=reserved_activity_sid,
# 	assignment_activity_sid = busy_activity_sid,
# 	target_workers = 'skills HAS "sales"'
# 	)

# print(sales_taskqueue.sid)
# support_taskqueue = client.taskrouter.workspaces(workspace_sid).task_queues.create(
# 	friendly_name='Support Taskqueue',
# 	assignment_activity_sid = busy_activity_sid,
# 	reservation_activity_sid = reserved_activity_sid,
# 	target_workers = 'skills HAS "support"'
# 	)
# print(support_taskqueue.sid, support_taskqueue.friendly_name)

# wrapup = client.taskrouter.workspaces(workspace_sid).activities.create(
# 	friendly_name='WrapUp', available=False)

# activities = client.taskrouter.workspaces(workspace_sid).activities.list()

# for activity in activities:
#  	print(activity.sid, activity.friendly_name)


# workspace = client.taskrouter.workspaces.create(
# 	friendly_name='Quality Clean')

# print(workspace.sid)