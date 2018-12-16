import numpy as np
import cv2

################################################################################
##                                COLORES RGB                                 ##
################################################################################

AMARILLO = (255,255,51)
ROJO = (255,0,0)
NARANJA = (255,128,0)
VERDE = (128,255,0)
VERDE_AZULADO = (0,255,128)
AZUL_CLARO = (0,255,255)
AZUL = (0,0,255)
MORADO = (127,0,255)
ROSA = (255,0,255)
GRIS = (128,128,128)

# Se usan para las imágenes de los círculos
COLORES = [AMARILLO,ROJO,NARANJA,VERDE,VERDE_AZULADO,AZUL_CLARO,AZUL,MORADO,ROSA,GRIS]

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
##                              EJERCICIO 1                                   ##
################################################################################




################################################################################
##                                    MAIN                                    ##
################################################################################

def main():



main()
