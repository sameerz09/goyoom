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
        product_id = models.execute_kw(db, uid, password, 'product.product', 'search', [[['sale_ok', '=', True]]], {'limit': 1})
        if not product_id:
            raise Exception("No product found")

        # Fetch a valid customer (partner) ID
        partner_id = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['customer_rank', '>', 0]]], {'limit': 1})
        if not partner_id:
            raise Exception("No customer found")

        # Define the sales order data using fetched product and partner IDs
        sales_order_data = {
            'partner_id': partner_id[0],  # Customer's ID
            'date_order': '2024-08-19',  # Sales order date
            'order_line': [(0, 0, {
                'product_id': product_id[0],  # Product's ID
                'product_uom_qty': 1,  # Quantity
                'price_unit': 100,  # Price per unit
            })]
        }

        # Create the sales order
        sale_order_id = models.execute_kw(db, uid, password, 'sale.order', 'create', [sales_order_data])
        print(f"Sales Order created successfully with ID: {sale_order_id}")

    except Exception as e:
        print(f"Failed to create sales order: {str(e)}")

    # Wait for 1 second before creating the next sales order
    time.sleep(0.2)
