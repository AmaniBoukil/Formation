# import libraries
import cv2
import os
import numpy as np
from datetime import datetime
import re
import time
#from recognition_in_real_time import load_faces, detect_faces

# Function to get the maximum image number in the directory
def get_max_image_number(directory, prefix="visitor_", extension=".png"):
    max_num = -1
    pattern = re.compile(f"{prefix}(\\d+){extension}")

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num

    return max_num+1  # Increment by 1 to get the next number

# Fonction pour sauvegarder l'image
def save_image(image, path):
    cv2.imwrite(path, image)

# Fonction pour détecter les visages
def detect_faces(frame, face_cascade):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

# Fonction pour capturer une image de la caméra
def capture_frame_from_camera():
    cap = cv2.VideoCapture(0)  # Index 0 pour la caméra par défaut
    ret, frame = cap.read()
    cap.release()
    if ret:
        return frame
    else:
        print("Erreur : Impossible de capturer une image de la caméra.")
        return None

# Fonction pour rendre une image plus nette et réduire le bruit
# def enhance_image(image):
#     # Convertir l'image en niveaux de gris
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # Réduction du bruit avec le filtre Non-Local Means avec des paramètres ajustés
#     denoised_image = cv2.fastNlMeansDenoising(gray_image, None, h=3, templateWindowSize=7, searchWindowSize=21)
#
#     # Appliquer un filtre gaussien pour le lissage avec un noyau plus petit
#     blurred_image = cv2.GaussianBlur(denoised_image, (3, 3), 0)
#
#     # Appliquer une transformation de netteté (unsharp mask) avec des poids ajustés
#     sharpened_image = cv2.addWeighted(denoised_image, 1.3, blurred_image, -0.3, 0)
#
#     # Reconstruire une image en couleur en utilisant l'image d'origine et l'image en niveaux de gris améliorée
#     enhanced_image = cv2.merge((sharpened_image, sharpened_image, sharpened_image))
#
#     return enhanced_image

##################
# Create a directory to save unknown face images if it doesn't exist
output_dir = "visitors"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get today's date and format it as a string
today_str = datetime.today().strftime('%Y-%m-%d')

# Create a subfolder with today's date
today_dir = os.path.join(output_dir, today_str)
if not os.path.exists(today_dir):
    os.makedirs(today_dir)

# Initialiser le classificateur de visage
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

print(f"Images will be saved in: {today_dir}")

# Initialiser le compteur unknown_count en fonction des fichiers existants dans le répertoire
unknown_count = get_max_image_number(today_dir)
print(f"Next unknown face number: {unknown_count}")

# Initialiser la capture vidéo de la caméra
cap = cv2.VideoCapture(0)

# Définir le délai entre les captures (en secondes)
capture_delay = 5
last_capture_time = 0

# Initialiser une variable pour stocker le temps de la dernière détection
last_detection_time = 0
face_detected = False

# Facteur pour agrandir le cadre de capture
enlargement_factor = 0.5

while True:
    # Lire une frame de la vidéo
    ret, frame = cap.read()
    if not ret:
        print("Erreur : Impossible de lire la frame")
        break

    # Détecter les visages dans la frame
    faces = detect_faces(frame, face_cascade)

    # Dessiner des rectangles autour des visages détectés
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Si des visages sont détectés
    if len(faces) > 0:
        if not face_detected:
            # Enregistrer le temps de la première détection
            last_detection_time = time.time()
            face_detected = True
        else:
            # Vérifier si le délai est écoulé
            if (time.time() - last_detection_time) >= capture_delay:
                # Capturer l'image de la première face détectée
                (x, y, w, h) = faces[0]

                # Agrandir le cadre de capture
                x = max(0, x - int(w * enlargement_factor))
                y = max(0, y - int(h * enlargement_factor))
                w = min(frame.shape[1] - x, w + int(w * 2 * enlargement_factor))
                h = min(frame.shape[0] - y, h + int(h * 2 * enlargement_factor))

                face_img = frame[y:y+h, x:x+w]

                # Améliorer l'image capturée
                # enhanced_image = enhance_image(face_img)

                # Sauvegarder l'image améliorée
                save_image(face_img, os.path.join(today_dir, f"visitor_{unknown_count}.png"))
                print(f"Image capturée et sauvegardée dans : {today_dir}")

                unknown_count += 1
                last_detection_time = time.time()  # Mettre à jour le temps de la dernière capture
                face_detected = False  # Réinitialiser le flag de détection

    # Afficher la frame avec les annotations
    cv2.imshow("Frame", frame)

    # Appuyer sur 'q' pour quitter
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()