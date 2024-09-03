# import libraries
import cv2
import face_recognition
import os
from datetime import datetime, timedelta
import re
import time

# Function to load and encode faces from our folder of images
def load_faces(folder_path):
    # initialisation
    known_face_encodings = []
    known_face_names = []

    # List all files in the given folder
    for file_name in os.listdir(folder_path):
        # Construct the full image path
        file_path = os.path.join(folder_path, file_name)
        print(file_name)

        # Check if the file is an image
        if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Load the image using OpenCV
            img = cv2.imread(file_path)
            # Convert the image from BGR to RGB
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Get the face encodings for the image
            img_encodings = face_recognition.face_encodings(rgb_img)
            print(img_encodings[0])
            # If a face is found / detected in file / image
            if img_encodings:
                # Store the face encoding and the name (without extension) in the lists
                known_face_encodings.append(img_encodings[0])
                known_face_names.append(os.path.splitext(file_name)[0])
            else:
                print(f"No faces found in {file_name}")

    return known_face_encodings, known_face_names

# Function to update les listes of encoded images and names chaque fois on détecte un nouveau face et l'enregistre dans notre dossier
def update_known_faces(unknown_count, folder_path, known_face_encodings, known_face_names):
    # get full path
    new_image_path = os.path.join(folder_path, f"visitor_{unknown_count}.png")
    # Load the new image file
    new_image = face_recognition.load_image_file(new_image_path)
    # encode image
    new_face_encoding = face_recognition.face_encodings(new_image)[0]
    # Append the new face encoding and the name of visitor to the lists
    known_face_encodings.append(new_face_encoding)
    known_face_names.append(f"visitor_{unknown_count}")

# Function to detect faces in a given frame and matche them with known faces
def detect_faces(frame, known_face_encodings, known_face_names):
    # Convert the frame from BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all face locations
    face_locations = face_recognition.face_locations(rgb_frame)
    # print("location : ",face_locations)
    # encode face detected
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # initialisation
        name = "Unknown"

        # Compare the face encoding with known faces encodings
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        # print("Matches : ",matches)
        # If a match is found, use the name of the first match
        # calculer toutes les diviations
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        print("Distances : ",face_distances)
        # get index of min distance
        best_match_index = min(range(len(face_distances)), key=lambda i: face_distances[i])
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    return face_locations, face_names

# Fonction pour récupérer le temps de détection de face
def markAttendance(name):
    # Determine the appropriate file based on the name
    if name.startswith("visitor"):
        file_name = 'Attendance_visitors.csv'
    else:
        file_name = 'Attendance.csv'

    # Check if the file exists, create it if it does not
    if not os.path.isfile(file_name):
        open(file_name, 'w').close()  # Create an empty file
        # f.write('Name,Time\n')  # Add headers to the file

    with open(file_name, 'r+') as f:
        myDataList = f.readlines()
        # Check if the file is empty or not
        if myDataList:
            nameList = [entry.strip().split(',')[0] for entry in myDataList]
            print(nameList)
            timeList = [entry.strip().split(',')[1] for entry in myDataList]
            print(timeList)
        else:
            nameList = []
            timeList = []

        now = datetime.now()
        dtString = now.strftime('%Y-%m-%d %H:%M:%S')
        # print(dtString)

        # assurer que la durée entre les détections est assez longue
        if name in nameList:
            # Get the latest recorded time for the name by finding the last occurrence
            index = len(nameList) - 1 - nameList[::-1].index(name)
            print(index)
            lastTimeString = timeList[index]
            lastcheck = datetime.strptime(lastTimeString, '%Y-%m-%d %H:%M:%S')
            # Calculate the time difference
            timeDifference = now - lastcheck
            print("Difference : ",timeDifference)

            # Check if the time difference is greater than 5 minutes
            if timeDifference < timedelta(minutes=5):
                print(f"Attendance for {name} already recorded within the last minute.")
            else:
                # print('Same Person')
                nameList.append(name)
                timeList.append(dtString)
                print(name, dtString)

                # Check if we are appending to an existing file
                if myDataList:
                    f.write(f'\n{name},{dtString}')
                else:
                    f.write(f'{name},{dtString}')

        else:
            # print('New Person')
            nameList.append(name)
            timeList.append(dtString)
            print(name, dtString)

            # Check if we are appending to an existing file
            if myDataList:
                f.write(f'\n{name},{dtString}')
            else:
                f.write(f'{name},{dtString}')

# Function to save the image
def save_image(image, path):
    cv2.imwrite(path, image)

# Function to get the maximum image number in the directory
def get_max_image_number(directory, prefix="visitor_", extension=".png"):
    max_num = 0
    pattern = re.compile(f"{prefix}(\\d+){extension}")

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num

    return max_num+1  # Increment by 1 to get the next number

#########################
# Create a directory to save unknown face images if it doesn't exist
output_dir = "ImagesBasic"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialiser le compteur unknown_count en fonction des fichiers existants dans le répertoire
unknown_count = get_max_image_number(output_dir)
print(f"Next unknown face number: {unknown_count}")

# Create a directory to save unknown face images if it doesn't exist
output_dir_vis = "visitors"
if not os.path.exists(output_dir_vis):
    os.makedirs(output_dir_vis)
# Get today's date and format it as a string
today_str = datetime.today().strftime('%Y-%m-%d')
# Create a subfolder with today's date
today_dir = os.path.join(output_dir_vis, today_str)
if not os.path.exists(today_dir):
    os.makedirs(today_dir)
print(f"Images will be saved in: {today_dir}")

# load data
folder_path = "/home/rihab/workspace/project/ImagesBasic"
known_face_encodings, known_face_names = load_faces(folder_path)
# print(known_face_encodings)
# print("*******************************")
# print(known_face_names)

#######################
# Initialisation
# Initialize variables to track status
unknown_saved = False

# temps avant détection et marque présence
face_recognition_counter = {}
recognition_threshold = 7  # Number of frames a face must be recognized to mark attendance

# Initialiser une variable pour stocker le temps de la dernière détection
last_detection_time = 0
face_detected = False
# Définir le délai entre les captures
capture_delay = 5

# Facteur pour agrandir le cadre de capture
enlargement_factor = 0.5

############################

# load the device's camera (webcam)
# create one camera and video capture object in order to capture the frame
cap = cv2.VideoCapture(0)
# Validation de la capture vidéo
if not cap.isOpened():
    print("Erreur : Impossible d'ouvrir la webcam")
    exit()

while True:
    # read our video and capturer des frames de la vidéo
    ret, frame = cap.read()
    # Validation de la lecture des frames
    if not ret:  # indicateur de succès de la capture de la frame
        print("Erreur : Impossible de lire la frame")
        break

    # Detect Faces
    face_locations, face_names = detect_faces(frame, known_face_encodings, known_face_names)
    # drawing a bounding box named
    for face_loc, name in zip(face_locations, face_names):
        # coordinates
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        ### Reconnaisance de unknown faces et ajout des photos de visiteurs au dossier
        if name == "Unknown":
            if unknown_saved:
                cv2.putText(frame, "Unknown Face Saved", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "Unknown Face Detected", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

            if not face_detected:
                # Enregistrer le temps de la première détection
                last_detection_time = time.time()
                face_detected = True
            else:
                # Vérifier si le délai est écoulé
                if (time.time() - last_detection_time) >= capture_delay:
                    # Capturer l'image de la première face détectée
                    x, y, w, h = x1, y1, x2 - x1, y2 - y1
                    # Agrandir le cadre de capture
                    x = max(0, x - int(w * enlargement_factor))
                    y = max(0, y - int(h * enlargement_factor))
                    w = min(frame.shape[1] - x, w + int(w * 2 * enlargement_factor))
                    h = min(frame.shape[0] - y, h + int(h * 2 * enlargement_factor))
                    # get frame of unknow face
                    face_img = frame[y:y + h, x:x + w]

                    # Sauvegarder l'image
                    save_image(face_img, os.path.join(output_dir, f"visitor_{unknown_count}.png"))
                    save_image(face_img, os.path.join(today_dir, f"visitor_{unknown_count}.png"))
                    print(f"Image capturée et sauvegardée dans : {output_dir}")

                    # Update known faces with the new image
                    update_known_faces(unknown_count,"/home/rihab/workspace/project/ImagesBasic",known_face_encodings,known_face_names)
                    unknown_count += 1
                    last_detection_time = time.time()  # Mettre à jour le temps de la dernière capture

                    face_detected = False  # Réinitialiser le flag de détection
                    unknown_saved=True

        ### Reconnaisance facial
        else:
            # Draw a box around the face
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
            # Draw a label with a name below the face
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)

            # Update face recognition counter
            if name in face_recognition_counter:
                face_recognition_counter[name] += 1
            else:
                face_recognition_counter[name] = 1

            # Check if the face has been recognized for enough frames to mark attendance
            if face_recognition_counter[name] == recognition_threshold:
                print(f"Attendance marked for: {name}")
                markAttendance(name)
                # Reset the counter for this name after marking attendance
                face_recognition_counter[name] = 0

    # Display the frame with annotations
    cv2.imshow("Frame", frame)

    # Key press to exit the window
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()




########################################################################################################################
# TO-DO : Ecrire un script de check in et un script de check out séparés.
########################################################################################################################