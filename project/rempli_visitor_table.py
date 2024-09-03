# Import libraries
import xmlrpc.client
import csv
from datetime import datetime
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

    # Path to the CSV file
    csv_file_path = 'Attendance_visitors.csv'
    # read our csv attendance file
    with open(csv_file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        nameList = []
        timeList = []

        # Lists of names and times
        for entry in csv_reader:
            nameList.append(entry[0])
            timeList.append(entry[1])
        print("Names:", nameList)
        print("Times:", timeList)

        # Create a dictionary to track check-in/check-out state for each employee
        visitor_states = {}
        # loop les deux listes
        for name, time in zip(nameList, timeList):
            ind=0 # compteur
            visitor_name = name
            print(visitor_name)
            timestamp = time
            print(timestamp)

            # Determine if this is a check-in or check-out
            ### CHECK OUT
            if visitor_name in visitor_states and visitor_states[visitor_name] == 'check_in':
                # Convert the timestamp to a datetime object
                timestamp_dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                # Recuperate last time of checking in for this employee
                last_check_in_time = datetime.strptime(timeList[ind], '%Y-%m-%d %H:%M:%S')
                print("last_check_in_time : ", last_check_in_time)
                print("Ckech now : ", timestamp_dt)

                # Ensure the check-out time is after the check-in time
                if timestamp_dt > last_check_in_time:
                    # hours of working
                   diff = timestamp_dt - last_check_in_time
                   print("Hours of working : ", diff)

                   # Rechercher les enregistrements de présence existants sans check-out pour cet employé
                   attendance_ids = models.execute_kw(db, uid, password, 'visitor.table', 'search', [[['name', '=', visitor_name], ['check_out', '=', False]]])
                   print("Attendance records to update:", attendance_ids)

                   if attendance_ids:
                       # Mettre à jour l'enregistrement de présence trouvé
                       models.execute_kw(db, uid, password, 'visitor.table', 'write',[attendance_ids, {'check_out': timestamp}])
                       print(f"Updated attendance record for {visitor_name} -> {attendance_ids[0]}")
                   else:
                        print(f"No matching attendance record found for {visitor_name}.")

                   # update state of this employee
                   visitor_states[visitor_name] = 'check_out'
                   # see updated states
                   print(visitor_states)

                else:
                    print(f"Invalid check-out time for {visitor_name}. Check-out time is before check-in time.")

            ### CHECK IN : new record / line
            else:
                # The name of the camera used in our case
                cam_name = 'WebCam'
                # Camera name has to be in our table of cameras
                cam_id = models.execute_kw(db, uid, password, 'camera.table', 'search', [[['name', '=', cam_name]]])
                # get ID of the camera
                if cam_id:
                    cam_id = cam_id[0]
                else:
                    print(f"Camera with name '{cam_name}' not found.")

                # get image of the visitor à l'aide de name
                image_file_path = os.path.join(image_folder_path, f"{visitor_name}.png")

                # Check if the image file exists
                if os.path.isfile(image_file_path):
                    # Read the image file and encode it as base64
                    with open(image_file_path, 'rb') as imgfile:
                        base64_bytes = base64.b64encode(imgfile.read())
                        decoded_image = base64_bytes.decode()

                # create method
                vals = {
                    'name': visitor_name,
                    'check_in': timestamp,
                    'camera_id': cam_id,
                    'image': decoded_image,
                }
                created_id = models.execute_kw(db, uid, password, 'visitor.table', 'create', [vals])
                # messages
                print("ID : ", created_id)
                print(f"Created attendance record for {visitor_name} -> {created_id}")

                # update state of this employee
                visitor_states[visitor_name] = 'check_in'
                # see updated states
                print(visitor_states)

            ind+=1 # update compteur

else:
    print("Authentication failed")