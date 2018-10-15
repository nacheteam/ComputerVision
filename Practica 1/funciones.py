import practica0
import cv2
import numpy as np

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
    practica0.pintaI(smoothed)


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
    practica0.pintaI(laplacian)


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
##                                 MAIN                                       ##
################################################################################

def main():
    #Leo la imagen
    img = cv2.imread("../Images/lena.jpg",-1)
    #Ejercicio 1 Apartado Acv2.copyMakeBorder(img,offsetRow,offsetRow,offsetCol,offsetCol,borderType=cv2.BORDER_R
    print("Ejecutando el apartado A con varios parámetros.")
    for sigmaX,sigmaY,hsize,wsize in zip([0,1,3,5],[0,3,1,5],[1,3,5,7,11],[1,3,7,5,11]):
        gaussianConvolution(sigmaX,sigmaY,hsize,wsize,img)

    #Ejercicio 1 Apartado B
    print("Ejecutando el apartado B con varios parámetros de sigma. Se pinta con tamaño 100 para poder ver bien el resultado.")
    for ksize in [3,5,7,11]:
        kx,ky = DerivKernel(ksize,1,1)
        practica0.pintaMI([kx,ky])

    #Ejercicio 1 Apartado C
    print("Ejecutando el apartado C con varios parámetros de ksize y borderType.")
    ksizes = [3,5,9,3,5,9,3,5,9,3,5,9]
    borders = [cv2.BORDER_REFLECT,cv2.BORDER_REFLECT,cv2.BORDER_REFLECT,cv2.BORDER_REFLECT,cv2.BORDER_REFLECT,cv2.BORDER_REFLECT,cv2.BORDER_REPLICATE,cv2.BORDER_REPLICATE,cv2.BORDER_REPLICATE,cv2.BORDER_REPLICATE,cv2.BORDER_REPLICATE,cv2.BORDER_REPLICATE]
    sigma = [1,1,1,1,1,1,3,3,3,3,3,3]
    for ksize,borderType,sigma in zip(ksizes,borders,sigma):
        convolutionLaplacian(img,ksize,borderType,sigma)


    # Cargo la imagen en blanco y negro
    img2 = cv2.imread("../Images/lena.jpg",0)

    # Ejercicio 2 Apartado A
    print("Ejecutando el apartado A del segundo ejercicio")
    practica0.pintaI(convolution2dSeparableMaskReflected(img2,np.array([1,2,1])/np.sum([1,2,1]),np.array([1,2,1])/np.sum([1,2,1])))

    # Ejercicio 2 Apartado B
    for ksize in [3,5,7,11]:
        practica0.pintaI(convolution2dDerivMask(img2,ksize))


    # Ejercicio 2 Apartado C
    for ksize in [3,5,7,11]:
        practica0.pintaI(convolution2dDerivMaskSecOr(img2,ksize))

main()
