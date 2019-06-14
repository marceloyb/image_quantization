import numpy as np
import cv2
import copy

def uniforme():
    ncolors = int(input("Insira o número de cores: "))
    aux = copy.deepcopy(ncolors)
    lista = [1, 2, 3]
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

    while (len(rgbarray) > 3):
        min1 = min(rgbarray)
        rgbarray.remove(min1)
        min2 = min(rgbarray)
        rgbarray.remove(min2)
        newmin = min1*min2
        rgbarray.append(newmin)
    rgbarray.sort(reverse = True)
    # print (rgbarray)

    # gera o código das cores. quantidade de códigos = ncolors
    a = np.linspace(0, 255, num = rgbarray[0], dtype = int)
    b = np.linspace(0, 255, num = rgbarray[1], dtype = int)
    c = np.linspace(0, 255, num = rgbarray[2], dtype = int)
    
    # print(a)
    # print(b)
    # print(c)
    # gambiarra starts here
    # for i in range(len(a)):
    #     lista[0] = a[i]
    #     for j in range(len(b)):
    #         lista[1] = b[j]
    #         for k in range(len(c)):
    #             lista[2] = c[k]
    #             colorsarray.extend(lista)
    # colorslist = []
    # while(len(colorslist) < ncolors):
    #     colorslist.append(colorsarray[0:3])
    #     colorsarray[0:3] = []
    # print(colorslist)
    # gambiarra ends here

    colorsarray = np.array(np.meshgrid(a, b, c)).T.reshape(-1,3)
    print(colorsarray)
    

if __name__ == '__main__':
    uniforme()
    # mediano()