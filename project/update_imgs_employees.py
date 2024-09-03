import xmlrpc.client
import base64
import os

# Define connection parameters
url = 'http://localhost:8069'  # URL of the Odoo server
db = 'v16_ce_amani_demo3'      # Database name
username = 'admin'             # Username
password = 'admin'             # Password

# Create a Server Proxy
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

# Fetching and printing version information
print("Version info:", common.version())

# Authentication
uid = common.authenticate(db, username, password, {})

# Define the path to the folder containing images
image_folder_path = '/home/rihab/workspace/project/ImagesBasic'

if uid:
    print("Authentication success")

    # Create a model Proxy
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # Fetch employees data including images
    # vérifier que image field n'est pas vide
    employee_ids = models.execute_kw(db, uid, password, 'hr.employee', 'search_read', [[('image_1920', '!=', False)]], {'fields': ['name', 'image_1920']})
    # print(employee_ids[0])

    # Ensure the image folder exists or create it
    if not os.path.exists(image_folder_path):
        os.makedirs(image_folder_path)

    # loop chaque ligne et get name of each employee et son image
    for employee in employee_ids:
        employee_name = employee['name']
        image_base64 = employee['image_1920']

        # Decode the image from base64
        image_data = base64.b64decode(image_base64)

        # Construct the file path to save the image under employee name
        image_file_path = os.path.join(image_folder_path, f"{employee_name}.png")

        # Save the image to the file path
        with open(image_file_path, 'wb') as image_file:
            image_file.write(image_data)

        print(f"Saved image for employee {employee_name}.")

else:
    print("Authentication failed")




########################################################################################################################
# TO-DO : Créer une fonction de vérification & update de données (images des employés sous leurs names)
# pour mettre à jour à la fois le dossier des images et le tableau des employés Odoo
# chaque fois qu'un nouveau employé est ajouté dans l'une des deux sources.
########################################################################################################################