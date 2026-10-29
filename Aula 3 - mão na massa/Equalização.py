import io
import cv2
import numpy as np
import urllib.request
from PIL import Image
import matplotlib.pyplot as plt

path = r"C:\Users\cauep\OneDrive\Documentos\Visão Computacional 20262\ImagensCodigoSlide\puppy.jpg"
image = np.array(Image.open(path))
image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

#apply histogram equalization
equalized = cv2.equalizeHist(image)

# Create CLAHE object and apply
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
clahe_equalized = clahe.apply(image)

# Displaying the results
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Grayscale Image')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(equalized, cmap='gray')
plt.title('Histogram Equalized Image')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(clahe_equalized, cmap='gray')
plt.title('CLAHE Equalized Image')
plt.axis('off')

plt.show()
