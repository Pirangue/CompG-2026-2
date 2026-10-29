import io
import cv2
import numpy as np
import urllib.request
from PIL import Image
import matplotlib.pyplot as plt

path = r"C:\Users\cauep\OneDrive\Documentos\Visão Computacional 20262\ImagensCodigoSlide\sheep.jpg"
image = np.array(Image.open(path))

# Write your code below
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

dft = cv2.dft(np.float32(gray_image), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)

magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:,:,0], dft_shift[:,:,1]) + 1e-10)

# Displaying the results

plt.figure(figsize=(10, 10))

plt.subplot(2, 1, 1)
plt.imshow(gray_image, cmap='gray')

plt.subplot(2, 1, 2)
plt.imshow(magnitude_spectrum, cmap='gray')
plt.show()