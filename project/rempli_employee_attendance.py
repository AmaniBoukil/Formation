# Import libraries
import xmlrpc.client
import csv
from datetime import datetime

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

if uid:
    print("Authentication success")

    # Create a model Proxy
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # Read the CSV file
    csv_file_path = 'Attendance.csv'  # Path to the CSV file
    # read file csv of employee's attandance
    with open(csv_file_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        nameList = []
        timeList = []

        # Lists of names and times of file
        for entry in csv_reader:
            nameList.append(entry[0])
            timeList.append(entry[1])
        print("Names:", nameList)
        print("Times:", timeList)

        # Create a dictionary to track check-in/check-out state for each employee
        employee_states = {}
        # loop les deux listes
        for name, time in zip(nameList, timeList):
            ind=0
            employee_name = name
            print(employee_name)
            timestamp = time
            print(timestamp)

            # Search for the employee by name
            # condition
            employee_domain = [['name', 'like', employee_name]]
            # search method
            employee_ids = models.execute_kw(db, uid, password, 'hr.employee', 'search', [employee_domain], {'limit': 1})

            # check if entered person is an employee enregistred in table 'hr.employee'
            if employee_ids:
                employee_id = employee_ids[0]
                print(f"Found employee ID for {employee_name}: {employee_id}")

                # Determine if this is a check-in or check-out
                ### CHECK OUT
                if employee_name in employee_states and employee_states[employee_name] == 'check_in':
                    # Convert the timestamp to a datetime object
                    timestamp_dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                    # Recuperate last time of checking in for this employee
                    last_check_in_time = datetime.strptime(timeList[ind], '%Y-%m-%d %H:%M:%S')
                    print("last_check_in_time : ",last_check_in_time)
                    print("Ckech now : ",timestamp_dt)

                    # Ensure the check-out time is after the check-in time
                    if timestamp_dt > last_check_in_time:
                        # hours of working
                        diff = timestamp_dt - last_check_in_time
                        print("Hours of working : ",diff)

                        # Rechercher les enregistrements de présence existants sans check-out pour cet employé
                        attendance_ids = models.execute_kw(db, uid, password, 'hr.attendance', 'search', [
                            [['employee_id', '=', employee_id], ['check_out', '=', False]]
                        ])
                        print("Attendance records to update:", attendance_ids)

                        if attendance_ids:
                            # Mettre à jour l'enregistrement de présence trouvé
                            models.execute_kw(db, uid, password, 'hr.attendance', 'write',
                                              [attendance_ids, {'check_out': timestamp}])
                            print(f"Updated attendance record for {employee_name} -> {attendance_ids[0]}")
                        else:
                            print(f"No matching attendance record found for {employee_name}.")

                        # update state of this employee
                        employee_states[employee_name] = 'check_out'
                        # see updated states
                        print(employee_states)

                    else:
                        print(f"Invalid check-out time for {employee_name}. Check-out time is before check-in time.")
                        continue

                ### CHECK IN : new record / line
                else:
                    # create method
                    vals = {
                        'employee_id': employee_id,
                        'check_in': timestamp
                    }
                    created_id = models.execute_kw(db, uid, password, 'hr.attendance', 'create', [vals])
                    print("ID : ",created_id)
                    print(f"Created attendance record for {employee_name} -> {created_id}")

                    # update state of this employee
                    employee_states[employee_name] = 'check_in'
                    # see updated states
                    print(employee_states)

            else:
                print(f"No employee found matching the criteria for {employee_name}")

            ind+=1

else:
    print("Authentication failed")