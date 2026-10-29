from PIL import Image
import numpy as np

# 1. Carrgar a imagem e transformar em array Numpy
caminho_entrada = r"C:\Users\cauep\OneDrive\Documentos\Visão Computacional 20262\ImagensCodigoSlide\tensor.jpg"
imagem = Image.open(caminho_entrada).convert("RGB")  # Converte para RGB, descartando o canal alfa se houver
arr = np.array(imagem)
# shape: (altura,largura, 3)

print(f"Original: shape Numpy: {arr.shape} (altura, largura, " f"canais)")

# 2. Rotacionar a imagem em 90 graus no sentido horário usando Numpy
#    np.rot90(arr, k=) gira k*90 graus no sentido anti-horário → k = -1 é horário
#    Rotação de 90 é so permutação de eixos + espelhamento (não precisa de interpolação)
arr_rotacionado = np.rot90(arr, k=-3)

print(f"Rotacionado: shape Numpy: {arr_rotacionado.shape}  " f"(altura e largura trocam de lugar)")

# 3. Voltar para imagem PIL só para salvar em disco
caminho_saida = r"C:\Users\cauep\OneDrive\Documentos\Visão Computacional 20262\ImagensCodigoSlide\tensor_rotacionado.jpg"
Image.fromarray(arr_rotacionado).save(caminho_saida)

print(f"Imagem rotacionada salva com sucesso!")