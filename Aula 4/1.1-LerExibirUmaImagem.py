import cv2
import matplotlib.pyplot as plt

#exibição utilizando matplotlib
imagemColor = cv2.imread("img/bernie-almanzar.png")

cv2.imshow("Mostrando a imagem", imagemColor)
#abre a janela com o titulo dado "Mostrando a imagem"

cv2.waitKey # Aguarda tecla (0 = espera infinita)
cv2.destroyAllWindows() # Fecha todas as janelas abertas

# Exibição utilizando matplotlib
img_rgb = cv2.cvtColor(imagemColor, cv2.COLOR_BGR2RGB)

plt.imshow(img_rgb)                 # Exibição da imagem no plot
plt.title("Mostrando a imagem")     # Define o título
plt.axis("off")                     # Remove os eixos (mais limpo para a imagem)
plt.show()                          # Renderiza a janela do matplotlib