import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

path = r"C:\Users\cauep\OneDrive\Documentos\Visão Computacional 20262\ImagensCodigoSlide\sheep.jpg"
image = np.array(Image.open(path))
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

dft = np.fft.fft2(image)
dft_shift = np.fft.fftshift(dft)

rows, cols = image.shape
ccrow, ccol = rows // 2, cols // 2

low_mask = np.zeros((rows, cols), np.uint8)
low_mask[ccrow-10:ccrow+10, ccol-10:ccol+10] = 1

high_mask = np.ones((rows, cols), np.uint8)
high_mask[ccrow-10:ccrow+10, ccol-10:ccol+10] = 0

lowpass_dft_filtered = dft_shift * low_mask
highpass_dft_filtered = dft_shift * high_mask

lowpass_dft_shift = np.fft.ifftshift(lowpass_dft_filtered)
image_filtered_lowpass = np.fft.ifft2(lowpass_dft_shift)
image_filtered_lowpass = np.abs(image_filtered_lowpass)
highpass_dft_shift = np.fft.ifftshift(highpass_dft_filtered)
image_filtered_highpass = np.fft.ifft2(highpass_dft_shift)
image_filtered_highpass = np.abs(image_filtered_highpass)

# Displaying the results

plt.figure(figsize=(10, 10))

plt.subplot(3, 1, 1)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Original Image')

plt.subplot(3, 1, 2)
plt.imshow(image_filtered_lowpass, cmap='gray')
plt.title('Low-pass Filtered Image')

plt.subplot(3, 1, 3)
plt.imshow(image_filtered_highpass, cmap='gray')
plt.title('High-pass Filtered Image')

plt.show()