import xmlrpc.client
import time
import random
from datetime import datetime, timedelta

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

# Fetch all Time Off Types (leave types)
leave_type_ids = models.execute_kw(db, uid, password, 'hr.leave.type', 'search', [[]])
if not leave_type_ids:
    raise Exception("No Time Off types found")

print(f"Found {len(leave_type_ids)} Time Off types")

# Function to create random leave requests
def create_random_leave(employee_id, leave_type_id):
    """Generates random leave data"""
    today = datetime.today()
    start_date = today + timedelta(days=random.randint(1, 10))
    end_date = start_date + timedelta(days=random.randint(1, 3))

    leave_data = {
        'employee_id': employee_id,   # Employee ID
        'holiday_status_id': leave_type_id,   # Time Off type ID
        'request_date_from': start_date.strftime('%Y-%m-%d'),
        'request_date_to': end_date.strftime('%Y-%m-%d'),
        'number_of_days': (end_date - start_date).days,
        'name': 'Random Time Off',   # Reason or name of Time Off
        'user_id': uid,  # Assign the Time Off request to the current user
    }

    # Create the Time Off request
    return models.execute_kw(db, uid, password, 'hr.leave', 'create', [leave_data])

# Fetch all Employees
employee_ids = models.execute_kw(db, uid, password, 'hr.employee', 'search', [[]])
if not employee_ids:
    raise Exception("No employees found")

print(f"Found {len(employee_ids)} employees")

# Create 100 random Time Off requests iteratively, cycling through employees and leave types
leave_count = 100
for i in range(leave_count):
    try:
        # Choose an employee and a leave type for each iteration
        employee_id = random.choice(employee_ids)
        leave_type_id = random.choice(leave_type_ids)

        # Create the leave request
        leave_id = create_random_leave(employee_id, leave_type_id)
        print(f"Time Off created successfully with ID: {leave_id}")

        # Wait for 500 milliseconds before creating the next request
        time.sleep(0.5)

    except Exception as e:
        print(f"Failed to create Time Off: {str(e)}")
