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
    linhas, colunas, canais = img.shape
    dist = []
    
    # Transforma a imagem original na imagem de saída, com a técnica de quantização
    for i in range (linhas):
        for j in range (colunas):
            for color in colorsarray:
                dist.append(np.linalg.norm(img[i,j] - color))
            img[i,j] = colorsarray[dist.index(min(dist))]
            dist.clear()
    

    return img
    
def mediancut(ncolors, img):
    pixels = []
    final = []
    palheta = []
    colorsarray = []
    linhas, colunas, canais = img.shape
    pixels = img[:]
    # pixels = sorted([pixels], key=lambda x: x[0])
    for i in range (colunas):
        test = pixels[:,i]
        test = sorted(test, key=lambda x: x[0])
        final.extend(np.unique(test, axis = 0))
    final = sorted(final, key=lambda x: x[0])
    final = np.unique(final, axis = 0)
    palheta.append(final)



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

    for i in range (len(palheta)):
        meio = int(len(palheta[i])/2)
        colorsarray.append(palheta[i][meio])

    dist = []
    for i in range (linhas):
        for j in range (colunas):
            for color in colorsarray:
                dist.append(np.linalg.norm(img[i,j] - color))
            img[i,j] = colorsarray[dist.index(min(dist))]
            dist.clear()

    return img


if __name__ == '__main__':
    # ncolors = int(input("Insira o número de cores: "))
    ncolors = 64
    img = cv2.imread("index.jpg")

    imgUniforme = uniforme(ncolors, img)
    cv2.imwrite("uniforme.jpg", imgUniforme)
    
    # imgMedian = mediancut(ncolors, img)
    # cv2.imwrite("mediana.jpg", imgMedian)