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

    palheta = np.array(np.meshgrid(a, b, c)).T.reshape(-1,3)
   

    # para cada pixel da imagem, faz a distância entre esse pixel e cada um dos elementos da palheta de cores
    # armazena a distância como um elemento do vetor distance
    distancia = np.linalg.norm(img[:,:,None] - palheta[None,None,:], axis=3)
    # pega o índice de qual a cor de menor distância
    indices_palheta = np.argmin(distancia, axis=2)
    # cria a imagem nova com base na palheta
    img = palheta[indices_palheta]


    return img

def argmedian(array, column):
    return np.argsort(array[:, column])[len(array) // 2]

def mediancut(ncolors, img):
    bucket = []
    palheta = []
    dispersao = []
    # pega rgb de todos pixels e coloca em um array ordenado
    # esse array é jogado em um bucket

    colors = np.concatenate(img[:,:], axis = 0)
    colors = np.unique(colors, axis = 0)

    # descobre qual cor tem a maior dispersão e ordena
    dispersao.append(np.amax(colors[:, 0]) - np.amin(colors[:, 0]))
    dispersao.append(np.amax(colors[:, 1]) - np.amin(colors[:, 1]))
    dispersao.append(np.amax(colors[:, 2]) - np.amin(colors[:, 2]))
    dispersao_key = dispersao.index(max(dispersao))
    colors = sorted(colors, key=lambda x: x[dispersao_key])
    
    # print(colors)
    # colors = np.array[colors, 'uint8']
    bucket.append(colors)
 
    # divide o bucket original em n buckets em que n = numero de cores
    while len(bucket) < ncolors:
        tamanho = len(bucket)
        for i in range(tamanho):
            meio = int(len(bucket[i])/2)
            a = bucket[i][:meio]
            b = bucket[i][meio:]
            bucket.append(a)
            bucket.append(b)
        for i in range(tamanho):
            del bucket[0]

    # identifica a cor mediana para cada um dos buckets de cor
    for i in range (len(bucket)):
        bk = np.array(bucket[i], int)
        meio = argmedian(bk, dispersao_key)
        palheta.append(bk[meio])

    palheta = np.array(palheta).reshape(-1, 3)
    # para cada pixel da imagem, faz a distância entre esse pixel e cada um dos elementos da palheta de cores
    # armazena a distância como um elemento do vetor distance
    distancia = np.linalg.norm(img[:,:,None] - palheta[None,None,:], axis=3)
    # pega o índice de qual a cor de menor distância
    indices_palheta = np.argmin(distancia, axis=2)
    # cria a imagem nova com base na palheta
    img = palheta[indices_palheta]

    return img

def main():
    # metodo = int(input("Método de quantização:\n (1) Uniforme \n (2) Corte Mediano \n"))
    ncolors = 64
    metodo = 2
    img = cv2.imread("index.jpg")
    # ncolors = int(input("Insira o número de cores: "))
    
    if metodo == 1:
        imgUniforme = uniforme(ncolors, img)
        cv2.imwrite("uniforme.jpg", imgUniforme)
    
    elif metodo == 2:
        if ncolors % 2 == 0:
            imgMedian = mediancut(ncolors, img)
            cv2.imwrite("mediana.jpg", imgMedian)
        else: 
            raise Exception("Número de cores para o corte mediano precisa ser potência de 2")
    
    else:
        raise Exception("Método não identificado")

if __name__ == '__main__':
    main()