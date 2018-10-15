################################################################################
#                        EJERCICIOS DE LA PRÁCTICA 0                           #
################################################################################

import cv2

# Ejercicio 1

'''
@brief La función toma la dirección de una imagen y la muestra en color o en
       blanco y negro.
@param filename Dirección de la imagen
@param flagcolor Si es 0 será en grises, si es menor que 0 se carga tal como es
       y si es mayor que 0 se carga en formato BGR.
'''
def leeimagen(filename,flagColor):
    img = cv2.imread(filename,flagColor)

    cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
    cv2.imshow('Imagen',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Ejercicio 2

'''
@brief La función toma una matriz de formato (x,y,3) con tipo np.uint8 y pinta
       la imagen asociada.
@param im Matriz que representa la imagen.
'''

def pintaI(im):
    cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
    cv2.imshow('Imagen',im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Ejercicio 3

'''
@brief La función toma una secuencia de imágenes y las
       concatena para poder imprimirlas en una sola ventana.
@param vim Secuencia de direcciones absolutas a las imágenes a dibujar. Deben
       tener la misma altura.
'''

# Si las imágenes tienen formatos de color distintos no se podrían unir con hacontat puesto que en cada
# posición de la matriz una tendria una tripleta y la otra un sólo valor. Este problema se solventa con la función
# cvtColor que nos convierte una imagen en escala de grises a RGB.

def pintaMI(vim):
    imagenes = []
    max_h = 0
    max_w = 0
    for im in vim:
        if im.shape[0]>max_h:
            max_h = im.shape[0]
        if im.shape[1]>max_w:
            max_w = im.shape[1]
    for im in vim:
        if len(im.shape)==2:
            imagenes.append(cv2.copyMakeBorder(cv2.cvtColor(im,cv2.COLOR_GRAY2RGB),top=0,bottom=max_h-im.shape[0],left=0,right=0,borderType= cv2.BORDER_CONSTANT, value=[0,0,0]))
        else:
            imagenes.append(cv2.copyMakeBorder(im,top=0,bottom=max_h-im.shape[0],left=0,right=0,borderType= cv2.BORDER_CONSTANT, value=[0,0,0]))
    concatenada = cv2.hconcat(imagenes)
    cv2.namedWindow('Imagenes', cv2.WINDOW_NORMAL)
    cv2.imshow("Imagenes",concatenada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Ejercicio 4

'''
@brief La función toma una imagen como entrada y una secuencia de píxeles y colores
       de forma que modifica la imagen y la pinta con los nuevos colores pasados
       como argumento.
@param imagen Dirección absoluta de la imagen a modificar.
@param pixeles Píxeles que se quieren modificar en la imagen.
@param colores Tripletas de color para modificar la imagen.
'''

def cambiaColor(imagen,pixeles,colores):
    matriz_imagen = cv2.imread(imagen,-1)
    for pix,col in zip(pixeles,colores):
        matriz_imagen[pix[1]][pix[0]] = col
    cv2.namedWindow('Imagen modificada colores', cv2.WINDOW_NORMAL)
    cv2.imshow("Imagen modificada colores",matriz_imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Ejercicio 5

'''
@brief La función toma una secuencia de imagenes y de títulos de forma que las pinta
       en la misma ventana con los títulos concatenados.
@param vim Secuencia de direcciones absolutas de imágenes.
@param titulos Secuencia de títulos asociados a las imágenes.
'''

def pintaMITitulos(vim,titulos):
    imagenes = []
    max_h = 0
    max_w = 0
    for im in vim:
        if im.shape[0]>max_h:
            max_h = im.shape[0]
        if im.shape[1]>max_w:
            max_w = im.shape[1]
    for im in vim:
        if len(im.shape)==2:
            imagenes.append(cv2.copyMakeBorder(cv2.cvtColor(im,cv2.COLOR_GRAY2RGB),top=0,bottom=max_h-im.shape[0],left=0,right=max_w-im.shape[1],borderType= cv2.BORDER_CONSTANT, value=[0,0,0]))
        else:
            imagenes.append(cv2.copyMakeBorder(im,top=0,bottom=max_h-im.shape[0],left=0,right=max_w-im.shape[1],borderType= cv2.BORDER_CONSTANT, value=[0,0,0]))
    concatenada = cv2.hconcat(imagenes)
    titulo = ""
    for tit in titulos:
        if tit != titulos[-1]:
            titulo+=tit+"/"
        else:
            titulo+=tit
    cv2.namedWindow(titulo, cv2.WINDOW_NORMAL)
    cv2.imshow(titulo,concatenada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
