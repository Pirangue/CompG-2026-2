import io
import cv2
import numpy as np
import urllib.request
from PIL import Image
import matplotlib.pyplot as plt

path = r"C:\Users\cauep\OneDrive\Documentos\Visão Computacional 20262\ImagensCodigoSlide\black_puppy.jpg"
image = np.array(Image.open(path))

# Write your code below
gaussian_blur = cv2.GaussianBlur(image, (15, 15), 0)

median_blur = cv2.medianBlur(image, 5)

# Displaying the results
plt.figure(figsize=(10, 10))

plt.subplot(1, 2, 1)
plt.imshow(gaussian_blur)
plt.title('Gaussian Blur')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(median_blur)
plt.title('Median Blur')
plt.axis('off')

plt.show()