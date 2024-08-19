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
        # Fetch a valid product ID
        product_id = models.execute_kw(db, uid, password, 'product.product', 'search', [[['purchase_ok', '=', True]]], {'limit': 1})
        if not product_id:
            raise Exception("No product found")

        # Fetch a valid vendor (partner) ID
        partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['supplier_rank', '>', 0]]], {'limit': 1})
        if not partner_id:
            raise Exception("No vendor found")

        # Define the purchase order data using fetched product and partner IDs
        purchase_order_data = {
            'partner_id': partner_id[0],  # Vendor's ID
            'date_order': '2024-08-19',  # Purchase order date
            'order_line': [(0, 0, {
                'product_id': product_id[0],  # Product's ID
                'product_uom_qty': 1,  # Quantity
                'price_unit': 100,  # Price per unit
            })]
        }

        # Create the purchase order
        purchase_order_id = models.execute_kw(db, uid, password, 'purchase.order', 'create', [purchase_order_data])
        print(f"Purchase Order created successfully with ID: {purchase_order_id}")

    except Exception as e:
        print(f"Failed to create purchase order: {str(e)}")

    # Wait for 500 milliseconds (0.5 seconds) before creating the next purchase order
    time.sleep(0.5)
