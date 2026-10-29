from PIL import Image
import numpy as np

# 1. Carrgar a imagem e transformar em array Numpy
caminho_entrada = r"C:\Users\cauep\OneDrive\Documentos\Visão Computacional 20262\ImagensCodigoSlide\tensor.jpg"
imagem = Image.open(caminho_entrada).convert("RGB")  # Converte para RGB, descartando o canal alfa se houver
arr = np.array(imagem)
# shape: (altura,largura, 3)


altura, largura = arr.shape[:2]  # altura e largura originais da imagem
print(f"Original: shape Numpy: {arr.shape} (altura, largura, " f"canais)")


# 2. Definir o fator de cisalhamento horzontal.
#    shx = 0.3 significa: cada linha é deslocada 0.3 * y pixels para a direita.
#    A linha do topo (y=0) fica parada; a de baixo (y=altura-1) é a mais deslocada.
shx = 0.3 


# 3. Calcular a nova largura para que a imagem cisalhada caiba inteira no canvas.
deslocamento_max = int(np.ceil(shx * (altura - 1))) 
nova_largura = largura + deslocamento_max


# 4. Cisalhamento em Numpy usando MAPEAMENTO INVERSO:
#    Para cada pixel (x_out, y_out), calculamos de qual pixel da ENTRADA
#    ele veio, aplicando a inversa da transformação: x_in = x_out - shx * y_out.
#    Isso evita "buracos" que apareceriam se fizéssemos o mapeamento direto.
y_out, x_out = np.indices((altura, nova_largura))  # malhas de coordenadas
x_in = (x_out - shx * y_out).astype(int)  # vizinho mais próximo

y_in = y_out  


# 5. Máscara: pixals cuja coordenada de origem cai dentro da imagem original
#    Os que ficam fora viram fundo (preto por padrão, pois o canvas começa zerado)
valido = (x_in >= 0) & (x_in < largura) 


# 6. Montar a imagem de saída usando indexação avançada do Numpy (s loops)
arr_cisalhado = np.zeros( shape= (altura, nova_largura, arr.shape[2]), 
                         dtype=arr.dtype ) 
arr_cisalhado[valido] = arr[y_in[valido], x_in[valido]]

print(f"Cisalhado: shape Numpy = {arr_cisalhado.shape} (largura " f"aumenta em {deslocamento_max} px")


#7. Voltar para imagem PIL só para salvar em disco
caminho_saida = r"C:\Users\cauep\OneDrive\Documentos\Visão Computacional 20262\ImagensCodigoSlide\tensor_cisalhado.jpg"
Image.fromarray(arr_cisalhado).save(caminho_saida)


print(f"Imagem cisalhada salva com sucesso!")