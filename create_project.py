import xmlrpc.client
import time

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

while True:
    try:
        # Define the project data
        project_data = {
            'name': 'Project ' + time.strftime('%Y%m%d%H%M%S'),  # Unique name using timestamp
            'user_id': uid,  # Set as the current user (or specify a different user ID if needed)
            'partner_id': False,  # Optional: specify a partner ID if needed
        }

        # Create the project
        project_id = models.execute_kw(db, uid, password, 'project.project', 'create', [project_data])
        print(f"Project created successfully with ID: {project_id}")

    except Exception as e:
        print(f"Failed to create project: {str(e)}")

    # Wait for 500 milliseconds (0.5 seconds) before creating the next project
    time.sleep(0.5)
