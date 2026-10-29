import cv2
import matplotlib.pyplot as plt

# Exibindo a imagem com o OpenCV
imageColor = cv2.imread("img/lenna.png")
img_rgb = cv2.cvtColor(imageColor, cv2.COLOR_BGR2RGB)

linhas = 2
colunas = 3

# cria a figura com a grade de subplots
fig, axs = plt.subplots(linhas, colunas, figsize=(15, 5))

# [linha, coluna]
axes[0, 0].imshow(img_rgb)
axes[0, 0].set_title('fig 1 - L0C0')

axes[0, 1].imshow(img_rgb)
axes[0, 1].set_title('fig 2 - L0C1')
axes[0, 1].axis('off')  # Desativa os eixos para a segunda figura

axes[1, 0].imshow(img_rgb)
axes[1, 0].set_title('fig 3 - L1C2')
axes[1, 0].axis('off')  # Desativa os eixos para a terceira figura

