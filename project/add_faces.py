# install OpenCV package : pip install opencv-python
# Unable wayland in Ubunto SE
import cv2
import pickle
import numpy as np
import os

# load the device's camera (webcam)
# create one camera and video capture object in order to capture the frame
video = cv2.VideoCapture(0)
print("video.........", video)
# Validation de la capture vidéo
if not video.isOpened():
    print("Erreur : Impossible d'ouvrir la webcam")
    exit()

# load the classifier et assurer que le chemin est correct
# ce fichier contient les données pré-entrainées pour reconnaître les visages.
facedetect=cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# initialisation
faces_data = []  # liste pour stocker les images de visages détectés
i = 0  # compteur pour le nombre de frames
name=input("Enter Your Name: ")

while True:
    # read our video and capturer des frames de la vidéo
    ret,frame=video.read()
    print("frame...............", frame)
    # Validation de la lecture des frames
    if not ret: # indicateur de succès de la capture de la frame
        print("Erreur : Impossible de lire la frame")
        break

    # convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Gray Img .................", gray)
    # perform the face detection
    faces = facedetect.detectMultiScale(gray, 1.3, 5) # détecter visage
    # drawing a bounding box
    for (x, y, w, h) in faces:
        crop_img = frame[y:y + h, x:x + w, :] # extraire rectangle de visage
        resized_img = cv2.resize(crop_img, (50, 50)) # redimensionner img de visage
        nb=0
        if len(faces_data) <= 100 and i % 10 == 0:
            print(nb)
            faces_data.append(resized_img) # ajouter img tous les 10 frames jusqu'à ce que 100 images soient capturées
            nb+=1
            cv2.imshow("Resized Img .................", gray)
        i = i + 1

        # annotations
        cv2.putText(frame, str(len(faces_data)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 1)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (50, 50, 255), 1)

    # affichage
    cv2.imshow("frame", frame)

    # key to exit windows
    k=cv2.waitKey(1) # for infinite time
    if k==ord('q') or len(faces_data)==100:
        break

video.release()
cv2.destroyAllWindows()

# pré-processing
faces_data=np.asarray(faces_data)
print(faces_data)
faces_data=faces_data.reshape(100, -1)
print(faces_data)

# sauvegarder les données
# s'il n'existe pas, création
if 'names.pkl' not in os.listdir('data/'):
    names=[name]*100
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)
# s'il n'existe pas, extendre et mettre à jour
else:
    with open('data/names.pkl', 'rb') as f:
        names=pickle.load(f)
    names=names+[name]*100
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(names, f)

# s'il n'existe pas, création
if 'faces_data.pkl' not in os.listdir('data/'):
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)
# s'il n'existe pas, extendre et mettre à jour
else:
    with open('data/faces_data.pkl', 'rb') as f:
        faces=pickle.load(f)
    faces=np.append(faces, faces_data, axis=0)
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)