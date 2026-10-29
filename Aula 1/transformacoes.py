import io
import cv2 
import numpy as np
import urllib.request
from PIL import Image
import matplotlib.pyplot as plt


path = r"C:\Users\cauep\OneDrive\Documentos\Visão Computacional 20262\ImagensCodigoSlide\puppy.jpg"

image = np.array(Image.open(path))

#  Write your code below 
resized = cv2.resize(image, (100, 100))  

height, width = image.shape[:2]
center = (width // 2, height // 2)

rotation_matrix = cv2.getRotationMatrix2D(center, 90, 1)
rotated = cv2.warpAffine(image, rotation_matrix, (width, height))

cropped = image[100:450, 250:600]  

# Displaying the results

plt.figure(figsize=(10, 10))

plt.subplot(2, 2, 1)
plt.imshow(image)
plt.title('Original Image')

plt.subplot(2, 2, 2)
plt.imshow(resized)
plt.title('Resized Image')

plt.subplot(2, 2, 3)
plt.imshow(rotated)
plt.title('Rotated Image')

plt.subplot(2, 2, 4)
plt.imshow(cropped)
plt.title('Cropped Image')

plt.tight_layout()
plt.show()