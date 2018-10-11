import practica0
import cv2

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


def main():
    #Leo la imagen
    img = cv2.imread("../Images/lena.jpg",-1)
    #Ejercicio 1 Apartado A
    print("Ejecutando el apartado A con varios parámetros.")
    for sigmaX,sigmaY,hsize,wsize in zip([0,1,3,5],[0,3,1,5],[1,3,5,7,11],[1,3,7,5,11]):
        gaussianConvolution(sigmaX,sigmaY,hsize,wsize,img)

main()
