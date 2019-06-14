import numpy as np
import cv2
import copy
from operator import itemgetter

def uniforme(ncolors, img):
    
    aux = copy.deepcopy(ncolors)
    rgbarray = []
    colorsarray = []
    d = 2

    # decompõe o número de cores em três
    while aux > 1:
        if aux % d == 0:
            aux = aux/d
            rgbarray.append(d)
        else:
            d += 1
    # se no vetor tiver mais que 3 cores, combina elas até ficar 3. se tiver menos, preenche com 1 até ter 3
    if (len(rgbarray) > 3):
        while (len(rgbarray) > 3):
            min1 = min(rgbarray)
            rgbarray.remove(min1)
            newmin = min1*min(rgbarray)
            rgbarray.remove(min(rgbarray))
            rgbarray.append(newmin)
    else:
        while (len(rgbarray) < 3):
            rgbarray.append(1)

    rgbarray.sort(reverse=True)

    # gera o código das cores. quantidade de códigos = ncolors
    a = np.linspace(0, 255, num = rgbarray[0], dtype = int)
    b = np.linspace(0, 255, num = rgbarray[1], dtype = int)
    c = np.linspace(0, 255, num = rgbarray[2], dtype = int)

    colorsarray = np.array(np.meshgrid(a, b, c)).T.reshape(-1,3)
    row, columns, canais = img.shape
    dist = []
    
    # Transforma a imagem original na imagem de saída, com a técnica de quantização

    
    # for i in range (row):
    #     for j in range (columns):
    #         pixel = img[i, j]
    #         for color in colorsarray:
    #             dist.append(np.linalg.norm(pixel - color))
    #         img[i,j] = colorsarray[dist.index(min(dist))]
    #         dist.clear()
    # print(img[:,:,None])
    # print(colorsarray)
    # para cada pixel da imagem, faz a distância entre esse pixel e cada um dos elementos da palheta de cores
    # armazena a distância como um elemento do vetor distance
    distance = np.linalg.norm(img[:,:,None] - colorsarray[None,None,:], axis=3)
    print(distance[0,0])
    # pega o índice de qual a cor de menor distância
    pal_img = np.argmin(distance, axis=2)
    print(colorsarray[pal_img])
    print(img)
    rgb_img = colorsarray[pal_img]


    return rgb_img
    
def mediancut(ncolors, img):
    pixels = []
    final = []
    palheta = []
    colorsarray = []
    linhas, colunas, canais = img.shape
    pixels = img[:]

    ################
    ################# FALTOU VERIFICAR QUAL O TOM (R, G OU B) PREVALECE NA IMAGEM, PRA ORDENAR O ARRAY DE ACORDO COM ISSO
    ###############
    # pixels = sorted([pixels], key=lambda x: x[0])
    
    # pega rgb de todos pixels e coloca em um array ordenado
    for i in range (colunas):
        test = pixels[:,i]
        test = sorted(test, key=lambda x: x[0])
        final.extend(np.unique(test, axis = 0))
    final = sorted(final, key=lambda x: x[0])
    final = np.unique(final, axis = 0)
    palheta.append(final)

    
    # divide os pixels em n arrays em que n = numero de cores
    while len(palheta) < ncolors:
        tamanho = len(palheta)
        for i in range(len(palheta)):
            meio = int(len(palheta[i])/2)
            a = palheta[i][:meio]
            b = palheta[i][meio:]
            palheta.append(a)
            palheta.append(b)
        for i in range(tamanho):
            del palheta[0]

    # pega a cor que fica no meio de cada vetor
    for i in range (len(palheta)):
        meio = int(len(palheta[i])/2)
        colorsarray.append(palheta[i][meio])

    dist = []
    # calcula a distancia entre a cor do pixel na imagem original e as cores encontradas
    for i in range (linhas):
        for j in range (colunas):
            for color in colorsarray:
                dist.append(np.linalg.norm(img[i,j] - color))
            img[i,j] = colorsarray[dist.index(min(dist))]
            dist.clear()

    return img


if __name__ == '__main__':
    # ncolors = int(input("Insira o número de cores: "))
    ncolors = 8
    img = cv2.imread("index.jpg")

    imgUniforme = uniforme(ncolors, img)
    cv2.imwrite("uniforme.jpg", imgUniforme)
    
    # imgMedian = mediancut(ncolors, img)
    # cv2.imwrite("mediana.jpg", imgMedian)