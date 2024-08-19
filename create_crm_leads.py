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

# Fetch all CRM leads
lead_ids = models.execute_kw(db, uid, password, 'crm.lead', 'search', [[]])
if not lead_ids:
    raise Exception("No CRM leads found")

print(f"Found {len(lead_ids)} CRM leads")

for lead_id in lead_ids:
    for _ in range(100):
        try:
            # Define random lead data
            lead_data = {
                'name': f'Lead {generate_random_string()}',  # Random lead name
                'contact_name': f'Contact {generate_random_string()}',  # Random contact name
                'email_from': f'{generate_random_string()}@example.com',  # Random email
                'phone': f'+1-{random.randint(1000000000, 9999999999)}',  # Random phone number
                'partner_id': False,  # Optional: specify a partner ID if needed
                'user_id': uid,  # Assign the lead to the current user
                'stage_id': False,  # Optional: specify a stage ID if needed
                'priority': '3',  # Optional: specify priority (1: High, 2: Normal, 3: Low)
            }

            # Create the lead
            lead_id = models.execute_kw(db, uid, password, 'crm.lead', 'create', [lead_data])
            print(f"Lead created successfully with ID: {lead_id}")

            # Wait for 500 milliseconds before creating the next lead
            time.sleep(0.5)

        except Exception as e:
            print(f"Failed to create lead: {str(e)}")

    print(f"Completed leads for CRM Lead ID: {lead_id}")
