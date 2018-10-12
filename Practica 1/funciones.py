import practica0
import cv2

################################################################################
##                             CONSTANTES                                     ##
################################################################################

KERNEL1D_SIZE = 100

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

def printDerivKernel(sigma,ksize):
    kernel = cv2.getGaussianKernel(ksize,sigma)
    practica0.pintaI(kernel)


################################################################################
## Apartado C: Usar la función Laplacian para el cálculo de la convolución    ##
## 2D con una máscara de Laplaciana-de-Gaussiana de tamaño variable. Mostrar  ##
## ejemplos de funcionamiento usando dos tipos de bordes y dos valores de     ##
## sigma: 1 y 3.                                                              ##
################################################################################

def convolutionLaplacian(img,ksize,borderType,sigma,depth=cv2.CV_16S,scale=1,delta=0):
    gaussian = cv2.GaussianBlur(img,(ksize,ksize),sigma,sigma,borderType)
    gaussian_gray = cv2.cvtColor(gaussian,cv2.COLOR_BGR2GRAY)
    laplacian = cv2.convertScaleAbs(cv2.Laplacian(gaussian_gray,depth,ksize,scale,delta,borderType))
    practica0.pintaI(laplacian)

################################################################################
##                                 MAIN                                       ##
################################################################################

def main():
    #Leo la imagen
    img = cv2.imread("../Images/lena.jpg",-1)
    #Ejercicio 1 Apartado A
    print("Ejecutando el apartado A con varios parámetros.")
    for sigmaX,sigmaY,hsize,wsize in zip([0,1,3,5],[0,3,1,5],[1,3,5,7,11],[1,3,7,5,11]):
        gaussianConvolution(sigmaX,sigmaY,hsize,wsize,img)

    #Ejercicio 1 Apartado B
    print("Ejecutando el apartado B con varios parámetros de sigma. Se pinta con tamaño 100 para poder ver bien el resultado.")
    for sigma in [0.1,1,2,3,4,5,6,7,8,9,10]:
        printDerivKernel(sigma,KERNEL1D_SIZE)

    #Ejercicio 1 Apartado C
    print("Ejecutando el apartado C con varios parámetros de ksize y borderType.")
    ksizes = [1,3,5,1,3,5,1,3,5,1,3,5]
    borders = [cv2.BORDER_REFLECT,cv2.BORDER_REFLECT,cv2.BORDER_REFLECT,cv2.BORDER_REPLICATE,cv2.BORDER_REPLICATE,cv2.BORDER_REPLICATE,cv2.BORDER_REFLECT,cv2.BORDER_REFLECT,cv2.BORDER_REFLECT,cv2.BORDER_REPLICATE,cv2.BORDER_REPLICATE,cv2.BORDER_REPLICATE]
    sigma = [1,1,1,3,3,3,3,3,3,1,1,1]
    for ksize,borderType,sigma in zip(ksizes,borders,sigma):
        convolutionLaplacian(img,3,cv2.BORDER_DEFAULT,0)

main()
