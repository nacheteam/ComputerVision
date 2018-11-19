import numpy as np
import cv2

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

'''
@brief Función que obtiene los puntos clave de la imagen img con los parámetros dados.
@param img Imagen de opencv de la que se quieren obtener los puntos clave
@param contrastThreshold parámetro de umbral de SIFT (es un double)
@param edgeThreshold parámetro de umbral de SIFT para la detección de puntos en los bordes de las figuras de la imagen (es un double)
@param sigma parámetro de la Gaussiana (es un double).
'''
def keyPointsSIFT(img,contrastThreshold,edgeThreshold,sigma):
    sift = cv2.xfeatures2d.SIFT_create(nfeatures=0,nOctaveLayers=3,contrastThreshold=contrastThreshold,edgeThreshold=edgeThreshold,sigma=sigma)
    kp = sift.detect(img,None)
    return kp


'''
@brief Función que obtiene los puntos clave de la imagen img con los parámetros dados.
@param img Imagen de opencv de la que se quieren obtener los puntos clave
@param hessianThreshold parámetro de umbral para el valor de la hessiana de los posibles puntos clave (es un double)
@param nOctaves número de octavas (es un entero)
@param nOctaveLayers número de capas (es un entero)
@param extended booleano de información extendida
@param upright booleano de detección de características en vertical y rotadas.
'''
def keyPointsSURF(img,hessianThreshold,nOctaves,nOctaveLayers,extended,upright):
    sift = cv2.xfeatures2d.SURF_create(hessianThreshold=hessianThreshold,nOctaves=nOctaves,nOctaveLayers=nOctaveLayers,extended=extended,upright=upright)
    kp = sift.detect(img,None)
    return kp


'''
@brief Obtiene la octava y la capa de los puntos dados.
@param kp puntos clave de los que se quieren obtener información.
'''
def unpackOctave(kp):
    unpacked = []
    for kpt in kp:
        oc = kpt.octave
        octava = oc&0xFF
        capa  = (oc>>8)&0xFF
        if octava>=128:
            octava |= -128
            octava+=1
        unpacked.append([octava,capa])
    return unpacked

def obtenNumeroPuntosOctava(kp):
    unpacked = unpackOctave(kp)
    numero_puntos = {}
    for ol in unpacked:
        if not str(ol[0]) in numero_puntos:
            numero_puntos[str(ol[0])]=1
        else:
            numero_puntos[str(ol[0])]+=1
    return numero_puntos

################################################################################
##                                    MAIN                                    ##
################################################################################

def main():
    # Ejercicio 1 apartado a
    yosemite1 = cv2.imread("imagenes/yosemite/Yosemite1.jpg",-1)
    kp_sift = keyPointsSIFT(yosemite1,contrastThreshold=0.06,edgeThreshold=6,sigma=1.6)
    yosemite1=cv2.drawKeypoints(yosemite1,kp_sift,yosemite1)
    print("El número de puntos obtenidos por SIFT: " + str(len(kp_sift)))
    pintaI(yosemite1)

    yosemite1 = cv2.imread("imagenes/yosemite/Yosemite1.jpg",-1)
    kp_surf = keyPointsSURF(yosemite1,hessianThreshold=400,nOctaves=4,nOctaveLayers=3,extended=False,upright=False)
    yosemite1=cv2.drawKeypoints(yosemite1,kp_surf,yosemite1)
    print("El número de puntos obtenidos por SURF: " + str(len(kp_surf)))
    pintaI(yosemite1)

    # Ejercicio 1 apartado b
    print("El número de puntos por octava en SIFT ha sido: " + str(obtenNumeroPuntosOctava(kp_sift)))
    print("El número de puntos por octava en SURF ha sido: " + str(obtenNumeroPuntosOctava(kp_surf)))

main()
