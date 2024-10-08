from skimage.feature import hog
from skimage import exposure
import cv2
import matplotlib as plt

import numpy as np

import matplotlib.pyplot as plt

from skimage.io import imread, imshow
from skimage.transform import resize
from skimage.feature import hog
from skimage import data, exposure

import cv2

# Charger l'image à partir du chemin spécifié
image = cv2.imread('/home/rihab/workspace/project/ImagesBasic/Elon Musk.jpg')
# cv2.imshow('Image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16),
                    cells_per_block=(1, 1), visualize=True, multichannel=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), sharex=True, sharey=True)

ax1.axis('off')
ax1.imshow(image, cmap=plt.cm.gray)
ax1.set_title('Input image')

# Rescale histogram for better display
hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))

ax2.axis('off')
ax2.imshow(hog_image_rescaled, cmap=plt.cm.gray)
ax2.set_title('Histogram of Oriented Gradients')
plt.show()




