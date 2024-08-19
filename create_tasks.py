import xmlrpc.client
import time
import random
import string

# Odoo connection details
url = "http://localhost:1717"
db = "Goyoom"
username = "sameerz09@hotmail.com"
password = "Test@111"

# Establishing connection to the Odoo instance
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if uid:
    print("Authenticated as", username)
else:
    raise Exception("Failed to authenticate")

# Creating the XML-RPC object to interact with Odoo models
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

def generate_random_string(length=10):
    """Generate a random string of fixed length"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Fetch all projects
project_ids = models.execute_kw(db, uid, password, 'project.project', 'search', [[]])
if not project_ids:
    raise Exception("No projects found")

print(f"Found {len(project_ids)} projects")

for project_id in project_ids:
    for _ in range(100):
        try:
            # Define random task data
            task_data = {
                'name': f'Task {generate_random_string()}',  # Random task name
                'project_id': project_id,  # Assign the task to the current project
                'date_deadline': '2024-08-19',  # Optional: specify a deadline date
                'priority': '1',  # Optional: specify priority (1: Urgent, 2: High, 3: Normal, 4: Low)
                'stage_id': False,  # Optional: specify a stage ID if needed
            }

            # Create the task
            task_id = models.execute_kw(db, uid, password, 'project.task', 'create', [task_data])
            print(f"Task created successfully with ID: {task_id} in Project ID: {project_id}")

            # Wait for 500 milliseconds before creating the next task
            time.sleep(0.5)

        except Exception as e:
            print(f"Failed to create task: {str(e)}")

    print(f"Completed tasks for Project ID: {project_id}")
