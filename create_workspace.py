from twilio.rest import Client
import os
import json

account_sid = os.environ.get("TWILIO_ACME_ACCOUNT_SID")
auth_token = os.environ.get("TWILIO_ACME_AUTH_TOKEN")

workspace_sid = "WS31b70c72384e4071ff18177f21e86e85"

busy_activity = "WA0e99bae0f1e7e207b9e837f12a8224e5"
reserved_activity = "WAe4adaa773be981a6c06a34e8e4c070eb"
wrap_up_activity = "WA8c7da385a1cb597050c57ff0856eb822"
offline_activity_sid ="WA914f2d474fc5ebf01852b0edfd3ad270"

taskqueue_support_sid = "WQ2c817f60279b692a58ebfe287975a320"
taskqueue_sales_sales_sid = "WQdc167a891abd4641663b8969b128de4f"

workflow_sid = "WW7d6f97035966412a19bc888bc2584745"

client = Client(account_sid, auth_token)

task = client.taskrouter.workspaces(workspace_sid).tasks.create(
	workflow = workflow_sid,
	attributes='{"selected_product": "support"}'
	)

print(task.sid, task.attributes, task.assignment_status)

# worker_support = client.taskrouter.workspaces(workspace_sid).workers.create(
# 	friendly_name ='Bob',
# 	activity_sid = offline_activity_sid,
# 	attributes ='{"skills": "support"}'
# 	)

# sales_worker = client.taskrouter.workspaces(workspace_sid).workers.create(
# 	friendly_name = 'susan',
# 	activity_sid = offline_activity_sid,
# 	attributes = '{"skills": "sales"}'
# 	)
# multi_skill_worker = client.taskrouter.workspaces(workspace_sid).workers.create(
# 	friendly_name = 'Enrique',
# 	activity_sid = offline_activity_sid,
# 	attributes = '{"skills": "[sales, support]"}'
# 	)

# workers = client.taskrouter.workspaces(workspace_sid).workers.list()
# for worker in workers:
# 	print(worker.friendly_name, worker.attributes)

# config = {
#     'task_routing': {
#         'filters': [
           
#             {
#                 'friendly_name': 'support filter',
#                 'expression': "selected_product =='support'",
#                 'targets': [{'queue': taskqueue_support_sid}]
#             },
#             {
#                 'friendly_name': 'sales filter',
#                 'expression': "selected_product =='sales'",
#                 'targets': [{'queue': taskqueue_sales_sales_sid}]
#             }
#         ],
#         'default_filter': {
#             'queue': taskqueue_support_sid
#         }
#     }
# }

# workflow = client.taskrouter.workspaces(workspace_sid).workflows.create(
# 	friendly_name='sales and support', configuration=json.dumps(config)
# 	)

# print(workflow.sid, workflow.configuration)

# taskqueue_support = client.taskrouter.workspaces(workspace_sid).task_queues.create(
# 	friendly_name='sales', 
# 	reservation_activity_sid=reserved_activity, 
# 	assignment_activity_sid=busy_activity,
# 	target_workers='skills HAS "sales"'
# 	)

# print(taskqueue_support.sid, taskqueue_support.friendly_name, taskqueue_support.target_workers)

# wrapup = client.taskrouter.workspaces(workspace_sid).activities.create(
# 	friendly_name='WrapUp', available=False)
# print(wrapup.sid, wrapup.friendly_name)


# activities = client.taskrouter.workspaces(workspace_sid).activities.list()
# for activity in activities:
# 	print(activity.sid, activity.friendly_name)



# workspace = client.taskrouter.workspaces.create(
# 	friendly_name='QualityClean')

# print(workspace.sid, workspace.friendly_name) 