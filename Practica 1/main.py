import cv2
import numpy as np

################################################################################
##                         FUNCIONES AUXILIARES                               ##
################################################################################

'''
@brief La función toma una matriz de formato (x,y,3) y pinta la imagen asociada.
@param im Matriz que representa la imagen.
'''

def pintaI(im):
    cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
    cv2.imshow('Imagen',im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

'''
@brief La función toma una secuencia de imágenes y las
       concatena para poder imprimirlas en una sola ventana.
@param vim Secuencia de direcciones absolutas a las imágenes a dibujar. Deben
       tener la misma altura.
'''

# Si las imágenes tienen formatos de color distintos no se podrían unir con hconcat puesto que en cada
# posición de la matriz una tendria una tripleta y la otra un sólo valor. Este problema se solventa con la función
# cvtColor que nos convierte una imagen en escala de grises a RGB.

def pintaMI(vim):
    imagenes = []
    max_h = 0
    for im in vim:
        # Tomamos la mayor altura de todas las imágenes.
        if im.shape[0]>max_h:
            max_h = im.shape[0]
    # Iteramos sobre las imágenes para añadirles bordes.
    for im in vim:
        # Distinguimos si la imagen es o no en color para poder convertirla.
        if len(im.shape)==2:
            imagenes.append(cv2.copyMakeBorder(cv2.cvtColor(im,cv2.COLOR_GRAY2RGB),top=0,bottom=max_h-im.shape[0],left=0,right=0,borderType= cv2.BORDER_CONSTANT, value=[0,0,0]))
        else:
            imagenes.append(cv2.copyMakeBorder(im,top=0,bottom=max_h-im.shape[0],left=0,right=0,borderType= cv2.BORDER_CONSTANT, value=[0,0,0]))
    concatenada = cv2.hconcat(imagenes)
    cv2.namedWindow('Imagenes', cv2.WINDOW_NORMAL)
    cv2.imshow("Imagenes",concatenada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

################################################################################
####   PUNTO 1: escribir funciones que implementen los siguientes puntos.   ####
################################################################################

################################################################################
## Apartado A: El cálculo de la convolución de una imagen con una máscara     ##
## Gaussiana 2D (Usar GaussianBlur). Mostrar ejemplos con distintos tamaños   ##
## de máscara y valores de sigma. Valorar los resultados.                     ##
################################################################################

def gaussianConvolution(sigmaX,sigmaY,hsize,wsize,im):
    # Nótese que wsize y hsize tienen que ser impares y pueden ser distintos
    # sigmaY puede ser 0, con lo que se toma sigmaY como sigmaX.
    # En caso de ser los dos 0 se calcula con wsize y hsize.
    smoothed = cv2.GaussianBlur(im,(wsize,hsize),sigmaX,sigmaY)
    return smoothed

################################################################################
## Apartado B: Usar getDerivKernels para obtener las máscaras 1D que permiten ##
## calcular la convolución 2D con máscaras de derivadas. Representar e        ##
## interpretar dichas máscaras 1D para distintos valores de sigma.            ##
################################################################################

def DerivKernel(ksize,dx,dy):
    kx,ky = cv2.getDerivKernels(dx,dy,ksize)
    return kx,ky


################################################################################
## Apartado C: Usar la función Laplacian para el cálculo de la convolución    ##
## 2D con una máscara de Laplaciana-de-Gaussiana de tamaño variable. Mostrar  ##
## ejemplos de funcionamiento usando dos tipos de bordes y dos valores de     ##
## sigma: 1 y 3.                                                              ##
################################################################################

# NO FUNCIONA MUESTRA TODO NEGRO

def convolutionLaplacian(img,ksize,borderType,sigma,depth=-1):
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(img_gray,depth,ksize,borderType=borderType)
    return laplacian


################################################################################
#### PUNTO 2: implementar, apoyándose en las funciones getDerivKernels,     ####
#### getGaussianKernel, pyrUp,pyrDown, los siguientes puntos.               ####
################################################################################

################################################################################
## Apartado A: El cálculo de la convolución 2D con una máscara separable de   ##
## tamaño variable. Usar bordes reflejados. Mostrar resultados.               ##
################################################################################

def convolution2dSeparableMaskReflected(img,kernelRow,kernelCol):
    # El kernel debe estar normalizado.
    return cv2.sepFilter2D(img,-1,kernelRow,kernelCol,borderType=cv2.BORDER_REFLECT)

'''
def convolution2dSeparableMaskReflected(img,kernelRow,kernelCol):
    # Primero hacemos una imagen que nos permita encuadrar el kernel en la matriz de la imagen.
    offsetCol = int(np.floor(len(kernelCol)/2))
    offsetRow = int(np.floor(len(kernelRow)/2))

    img_conv = cv2.copyMakeBorder(img,offsetRow,offsetRow,offsetCol,offsetCol,borderType=cv2.BORDER_REFLECT)
    img_conv_copy = np.copy(img_conv)

    # Convolución por filas
    for i in range(offsetRow,len(img)-offsetRow):
        for j in range(offsetCol,len(img[0])-offsetCol):
            coord = 0
            for k in range(-offsetCol,offsetCol+1):
                coord += kernelRow[k+offsetCol]*img_conv_copy[i-k][j]
            img_conv[i][j] = coord

    img_conv_copy = np.copy(img_conv)

    # Convolución por columnas
    for i in range(offsetRow,len(img)-offsetRow):
        for j in range(offsetCol,len(img[0])-offsetCol):
            coord = 0
            for k in range(-offsetRow,offsetRow+1):
                coord += kernelRow[k+offsetCol]*img_conv_copy[i][j-k]
            img_conv[i][j] = coord

    return img_conv
'''

################################################################################
## Apartado B: El cálculo de la convolución 2D con una máscara 2D de 1ª       ##
## derivada de tamaño variable. Mostrar ejemplos de funcionamiento usando     ##
## bordes a cero.                                                             ##
################################################################################

def convolution2dDerivMask(img,ksize):
    kernel = DerivKernel(ksize,1,1)
    return cv2.sepFilter2D(img,-1,kernel[0],kernel[1])

################################################################################
## Apartado C: El cálculo de la convolución 2D con una máscara 2D de 2ª       ##
## derivada de tamaño variable.                                               ##
################################################################################

def convolution2dDerivMaskSecOr(img,ksize):
    kernel = DerivKernel(ksize,2,2)
    return cv2.sepFilter2D(img,-1,kernel[0],kernel[1])

################################################################################
## Apartado D: Una función que genere una representación en pirámide          ##
## Gaussiana de 4 niveles de una imagen. Mostrar ejemplos de funcionamiento   ##
## usando bordes ¿reflejados?                                                 ##
################################################################################

def gaussianPyramid(img,levels=4):
    pyr = []
    img_pyr = cv2.pyrDown(img,borderType=cv2.BORDER_REFLECT)
    pyr.append(img)
    pyr.append(img_pyr)
    for i in range(levels-2):
        img_pyr = cv2.pyrDown(img_pyr)
        pyr.append(img_pyr)
    return pyr

################################################################################
## Apartado E: Una función que genere una representación en pirámide          ##
## Laplaciana de 4 niveles de una imagen. Mostrar ejemplos de funcionamiento  ##
## usando bordes ¿reflejados?                                                 ##
################################################################################

def laplacianPyramid(img,levels=4):
    pyr = gaussianPyramid(img,levels)
    res = []
    for i in range(levels-1,0,-1):
        gauss_up = cv2.pyrUp(pyr[i],dstsize=(len(pyr[i-1][0]),len(pyr[i-1])))
        sub = cv2.subtract(gauss_up,pyr[i-1]) + 45
        res.append(sub)
    res = res[::-1]
    res.append(pyr[-1])
    return res

################################################################################
#### PUNTO 3: imágenes híbridas                                             ####
################################################################################

################################################################################
## Apartado 1: Escribir una función que muestre las tres imágenes (alta,baja  ##
## e híbrida) en una misma ventana. (Recordar que las imágenes después de     ##
## una convolución contienen números flotantes que pueden ser positivos y     ##
## negativos).                                                                ##
################################################################################

def showHibrid(img1,img2,hsize,wsize,sigmaX,sigmaY):
    low_freq1 = np.absolute(cv2.GaussianBlur(img1,(hsize,wsize),sigmaX,sigmaY))
    low_freq2 = np.absolute(cv2.GaussianBlur(img2,(hsize,wsize),sigmaX,sigmaY))
    high_freq2 = cv2.subtract(img2,low_freq2)
    hibrid = cv2.add(low_freq1,high_freq2)
    pintaMI([low_freq1,high_freq2,hibrid])

################################################################################
##                                 MAIN                                       ##
################################################################################

def main():

    #Leo la imagen
    img = cv2.imread("imagenes/lena.jpg",-1)
    #Ejercicio 1 Apartado A
    print("Convolución gaussiana.")
    gaussian_conv = []
    for sigmaX,sigmaY,hsize,wsize in zip([0,1,3,5],[0,3,1,5],[3,5,7,11],[3,7,5,11]):
        gaussian_conv.append(gaussianConvolution(sigmaX,sigmaY,hsize,wsize,img))
    pintaMI(gaussian_conv)

    #Ejercicio 1 Apartado B
    print("Kernel de primera derivada con varios tamaños.")
    for ksize in [3,5,7,11]:
        kx,ky = DerivKernel(ksize,1,1)
        print("Tamaño " + str(ksize))
        print("dx: " + str(kx.transpose()[0]))
        print("dy: " + str(ky.transpose()[0]))

    #Ejercicio 1 Apartado C
    print("Convolución laplaciana.")
    ksizes = [3,5,9,3,5,9,3,5,9,3,5,9]
    borders = [cv2.BORDER_REFLECT,cv2.BORDER_REFLECT,cv2.BORDER_REFLECT,cv2.BORDER_REFLECT,cv2.BORDER_REFLECT,cv2.BORDER_REFLECT,cv2.BORDER_REPLICATE,cv2.BORDER_REPLICATE,cv2.BORDER_REPLICATE,cv2.BORDER_REPLICATE,cv2.BORDER_REPLICATE,cv2.BORDER_REPLICATE]
    sigma = [1,1,1,1,1,1,3,3,3,3,3,3]
    laplacian_conv = []
    for ksize,borderType,sigma in zip(ksizes,borders,sigma):
        laplacian_conv.append(convolutionLaplacian(img,ksize,borderType,sigma))
    laplacian_conv1 = laplacian_conv[:len(laplacian_conv)//2]
    laplacian_conv2 = laplacian_conv[len(laplacian_conv)//2:]
    pintaMI(laplacian_conv1)
    pintaMI(laplacian_conv2)


    # Cargo la imagen en blanco y negro
    img2 = cv2.imread("imagenes/bicycle.bmp",0)


    # Ejercicio 2 Apartado A
    print("Convolución con máscaras separables. (Gaussiana,identidad y detección de bordes)")
    conv_sep = []
    conv_sep.append(convolution2dSeparableMaskReflected(img2,np.array([1,2,1])/np.sum([1,2,1]),np.array([1,2,1])/np.sum([1,2,1])))
    conv_sep.append(convolution2dSeparableMaskReflected(img2,np.array([0,1,0])/np.sum([0,1,0]),np.array([0,1,0])/np.sum([0,1,0])))
    conv_sep.append(convolution2dSeparableMaskReflected(img2,np.array([1,2,1])/np.sum([1,2,1]),np.array([1,0,-1])/np.sum(np.absolute([1,0,-1]))))
    pintaMI(conv_sep)

    # Ejercicio 2 Apartado B
    derivMask_conv = []
    for ksize in [3,5,7,11]:
        derivMask_conv.append(convolution2dDerivMask(img2,ksize))
    print("Convolución 2D primera derivada")
    pintaMI(derivMask_conv)

    # Ejercicio 2 Apartado C
    derivMask2_conv = []
    for ksize in [3,5,7,11]:
        derivMask2_conv.append(convolution2dDerivMaskSecOr(img2,ksize))
    print("Convolución 2D segunda derivada")
    pintaMI(derivMask2_conv)

    # Ejercicio 2 Apartado D
    print("Pirámide gaussiana")
    pyr = gaussianPyramid(img2)
    pintaMI(pyr)


    # Ejercicio 2 Apartado E
    print("Pirámide laplaciana")
    pyr2 = laplacianPyramid(img2)
    pintaMI(pyr2)

    # Ejercicio 3
    bird = cv2.imread("imagenes/bird.bmp",0)
    plane = cv2.imread("imagenes/plane.bmp",0)
    print("Imagen híbrida avión y pájaro.")
    showHibrid(plane,bird,13,13,7,7)

    submarine = cv2.imread("imagenes/submarine.bmp",0)
    fish = cv2.imread("imagenes/fish.bmp",0)
    print("Imagen híbrida submarino y pez.")
    showHibrid(submarine,fish,17,17,2,2)

    bicycle = cv2.imread("imagenes/bicycle.bmp",0)
    motorcycle = cv2.imread("imagenes/motorcycle.bmp",0)
    print("Imagen híbrida bicicleta y moto.")
    showHibrid(bicycle,motorcycle,23,23,8,8)

main()
