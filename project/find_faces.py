import sys
import dlib
from skimage import io
import cv2
import numpy as np

# Nom du fichier image
file_name = "/home/rihab/workspace/project/ImagesBasic/Elon Musk.jpg"

# Créer un détecteur de visage HOG à l'aide de la classe intégrée dlib
face_detector = dlib.get_frontal_face_detector()

# Créer une fenêtre d'affichage d'image dlib
win = dlib.image_window()

# Charger l'image dans un tableau
image = io.imread(file_name)

# try:
#     # Charger l'image dans un tableau
#     image = io.imread(file_name)
#
#     # Vérifier le nombre de canaux et convertir si nécessaire
#     if image.ndim == 2:  # L'image est déjà en niveaux de gris
#         pass
#     elif image.shape[2] == 4:  # L'image est en RGBA
#         image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
#     elif image.shape[2] == 3:  # L'image est en RGB
#         pass
#     else:
#         raise ValueError("Unsupported image format")
#
# except FileNotFoundError:
#     print(f"Erreur : le fichier {file_name} n'a pas été trouvé.")
#     sys.exit(1)
# except Exception as e:
#     print(f"Erreur lors de la lecture de l'image : {e}")
#     sys.exit(1)

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Exécuter le détecteur de visage HOG sur les données de l'image
# Le résultat sera les boîtes englobantes des visages dans notre image
detected_faces = face_detector(image, 1)

print(f"J'ai trouvé {len(detected_faces)} visages dans le fichier {file_name}")

# Ouvrir une fenêtre sur le bureau affichant l'image
win.set_image(image)

# Parcourir chaque visage trouvé dans l'image
for i, face_rect in enumerate(detected_faces):
    # Les visages détectés sont renvoyés sous forme d'objet avec les coordonnées
    # des bords supérieur, gauche, droit et inférieur
    print(
        f"- Visage #{i + 1} trouvé à Gauche: {face_rect.left()} Haut: {face_rect.top()} Droit: {face_rect.right()} Bas: {face_rect.bottom()}")

    # Dessiner une boîte autour de chaque visage trouvé
    win.add_overlay(face_rect)

# Attendre que l'utilisateur appuie sur <entrer> pour fermer la fenêtre
dlib.hit_enter_to_continue()
