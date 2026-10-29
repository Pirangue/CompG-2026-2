import cv2
import matplotlib.pyplot as plt

# - Função: Separar canais RGB

def separar_canais_rgb(img_brg):
    """
    Separar os 3 canais de uma imagem RGB.
    Retorna (vermelho, verde, azul) com array 3D (escala de cinza).
    Nota: no OpenCV a ordem é BGR, então [:,:,0] = azul, [:,:,1] = verde, [:,:,2] = vermelho.
    """
    #img[:,:,0] = primeiro canal = azul (blue)
    #img[:,:,1] = segundo canal = verde (green)
    #img[:,:,2] = terceiro canal = vermelho (red)

    azul = img_brg[:,:,0]
    verde = img_brg[:,:,1]
    vermelho = img_brg[:,:,2]

    return vermelho, verde, azul

# - Função: visualização dos canais -
def visualizar_canais(img_brg):
    """
    Plota a imagem original e os 3 canais R, G, B lado a lado.
    """
    img_brg = cv2.cvtColor(img_brg, cv2.COLOR_BGR2RGB)  # Converte BGR para RGB para exibição correta
    r, g, b = separar_canais_rgb(img_brg)

    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    axes[0].imshow(img_brg); axes[0].set_title('Original RGB')
    axes[1].imshow(r, cmap='gray'); axes[1].set_title('Canal R (Vermelho)')
    axes[2].imshow(g, cmap='gray'); axes[2].set_title('Canal G (Verde)')
    axes[3].imshow(b, cmap='gray'); axes[3].set_title('Canal B (Azul)')
    for ax in axes: ax.axis('off')
    plt.tight_layout(); plt.show()

# entendendo os vetores
imageColor = cv2.imread("img/bernie-almanzar.png", cv2.IMREAD_COLOR)
imageBlack = cv2.imread("img/bernie-almanzar.png", cv2.IMREAD_GRAYSCALE)

print("-> Conteúdo númerico da imagem ImageBlack.png (escala de cinza):")
print("Forma do vetor : ", imageBlack.shape) # tamanho e formato da matriz
print("Primeiros 3x3 pixels (RGB):\n", imageColor[:3, :3, :]) # pega 3 pixels
# 3 dimensões

#Exibição de canais
ImageColor = cv2.imread("img/bernie-almanzar.png")
visualizar_canais(ImageColor)
ImageColor = cv2.imread("img/cereja.png")
visualizar_canais(ImageColor)
ImageColor = cv2.imread("img/connor-ward.png")
visualizar_canais(ImageColor)
ImageColor = cv2.imread("img/laranja.png")
visualizar_canais(ImageColor)
ImageColor = cv2.imread("img/GuardaSol.png")
visualizar_canais(ImageColor)