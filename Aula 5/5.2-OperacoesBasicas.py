import cv2
import matplotlib.pyplot as plt

# - Função: Ajustar brilho e contraste

def ajustar_brilho_contraste(img, alpha=1.0, beta=0):
    """
    Ajusta o brilho e contraste de uma imagem.
    alpha: fator de contraste (1.0 = sem alteração, >1.0 = aumenta contraste, <1.0 = diminui contraste)
    beta: offset de brilho (0 = sem alteração, >0 = aumenta brilho, <0 = diminui brilho)
    Fórmula aplicada pixel a pixel: novo = alpha * pixel + beta
    convertScaleAbs é usado para garantir que os valores dos pixels permaneçam dentro do intervalo [0, 255].
    """

    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)


# - Função: Redimensionar imagem
def redimencionar(img, largura=None, altura=None, escala=None):
    """
    Redimensionar a imagem de forma fléxivel
    - Se escala fornecida: aplica porcentagem (0.5 = 50% do tamanho original, 2.0 = 200% do tamanho original)
    - Se largura e altura fornecidas: usa o tamanho absoluto
    - Se apenas largura ou altura fornecida: mantém a proporção automaticamente
    """

    h_orig, w_orig = img.shape[:2] #shape = (altura, largura, canais)

    if escala is not None:
        nova_larg = int(w_orig * escala)
        nova_altura = int(h_orig * escala)
    elif largura is not None:
        nova_larg, nova_altura = largura, altura
    elif largura:
        nova_altura = altura
        nova_larg = int((largura / h_orig) * w_orig)
    elif altura:
        nova_altura = altura
        nova_larg = int((altura / w_orig) * h_orig)
    else:
        return img  # Retorna a imagem original se nenhum parâmetro for fornecido

    # INTER_AREA é ideal para reduzir.  INTER_LINEAR é ideal para aumentar.
    # imagem de 4 pixels e ir para 2, posso ter de 2 e ir para 1 e meio
    interpol = cv2.INTER_AREA if nova_larg < w_orig else cv2.INTER_LINEAR
    return cv2.resize(img, (nova_larg, nova_altura), interpolation=interpol)

# - Função: Corter região de interesse -
def cortar(img, x, y, largura, altura):
    """
    Cortar uma região retangular da imagem.
    x, y: canto superior esquerdo do recorte (coluna, linha)
    Nota: o acesso ao arrays Numpy é [linha:linha, coluna:coluna], ou seja, [y:y+altura, x:x+largura]
    """
    return img[y:y+altura, x:x+largura]

# Função: rotacionar imagem
def rotacionar(img, angulo, escala=1.0):
    """
    Rotaciona a imagem em torno do seu centro.
    angulo: graus(positivo = sentido anti-horário, negativo = sentido horário)
    escala: fator de zoom durante a rotação (1.0 = sem zoom, >1.0 = aumenta tamanho, <1.0 = diminui tamanho)
    """
    h, w = img.shape[:2]
    centro = (w // 2, h // 2) #rotacionando w-larg, h altura no Centro da imgaem em pixels
    M = cv2.getRotationMatrix2D(centro, angulo, escala)
    return cv2.warpAffine(img, M, (w, h))

image = cv2.imread("img/laranja.png")

# usa cada função definida acima e vamos plotar os resultados em subplots
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
img_brilho = ajustar_brilho_contraste(image, alpha=1.3, beta=30)
# aumenta a imagem OBS: TESTEM como 0.5 e 0
img_redim = redimencionar(image, escala=0.5)
img_corte = cortar(image, 100, 100, 800, 600) # x=100, y=100, largura=800, altura=600
img_rot = rotacionar(image, angulo=3.0)

plt.figure(figsize=(16, 10))

ax1 = plt.subplot(2, 3, 1)
ax1.imshow(image_rgb)
ax1.set_title("Original {image_rgb.shape}")
ax1.axis('off')

ax2 = plt.subplot(2, 3, 2)
ax2.imshow(cv2.cvtColor(img_brilho, cv2.COLOR_BGR2RGB))
ax2.set_title("Brilho/Contraste")
ax2.axis('off')

ax3 = plt.subplot(2, 3, 3)
ax3.imshow(cv2.cvtColor(img_redim, cv2.COLOR_BGR2RGB))
ax3.set_title("Redimensionando")
ax3.axis('off')

ax4 = plt.subplot(2, 3, 4)
ax4.imshow(cv2.cvtColor(img_corte, cv2.COLOR_BGR2RGB))
ax4.set_title("Cortar")
ax4.axis('off')

ax5 = plt.subplot(2, 3, 5)
ax5.imshow(cv2.cvtColor(img_rot, cv2.COLOR_BGR2RGB))
ax5.set_title("Rotacionar")
ax5.axis('off')

plt.tight_layout()
plt.show()