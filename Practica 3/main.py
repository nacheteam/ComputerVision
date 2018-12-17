import numpy as np
import cv2
import pickle

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
##                             FUNCIONES DE AYUDA                             ##
################################################################################

def click_and_draw(event,x,y,flags,param):
    global refPt, imagen,FlagEND


   # if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
    if  event == cv2.EVENT_LBUTTONDBLCLK:
        FlagEND= False
        cv2.destroyWindow("image")

    elif event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))
        #cropping = True
        print("rfePt[0]",refPt[0])


    elif (event == cv2.EVENT_MOUSEMOVE) & (len(refPt) > 0) & FlagEND:
    # check to see if the mouse move
        clone=imagen.copy()
        nPt=(x,y)
        print("npt",nPt)
        sz=len(refPt)
        cv2.line(clone,refPt[sz-1],nPt,(0, 255, 0), 2)
        cv2.imshow("image", clone)
        cv2.waitKey(0)

    elif event == cv2.EVENT_RBUTTONDOWN:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
        refPt.append((x, y))
        #cropping = False
        sz=len(refPt)
        print("refPt[sz]",sz,refPt[sz-1])
        cv2.line(imagen,refPt[sz-2],refPt[sz-1],(0, 255, 0), 2)
        cv2.imshow("image", imagen)
        cv2.waitKey(0)


def extractRegion(image):
    global refPt, imagen,FlagEND
    imagen=image.copy()
    # load the image and setup the mouse callback function
    refPt=[]
    FlagEND=True
    #image = cv2.imread(filename)
    cv2.namedWindow("image")
    # keep looping until the 'q' key is pressed
    cv2.setMouseCallback("image", click_and_draw)
    #
    while FlagEND:
    	# display the image and wait for a keypress
        cv2.imshow("image", image)
        cv2.waitKey(0)
    #
    print('FlagEND', FlagEND)
    refPt.pop()
    refPt.append(refPt[0])
    #cv2.destroyWindow("image")
    return refPt


def loadDictionary(filename):
    with open(filename,"rb") as fd:
        feat=pickle.load(fd)
    return feat["accuracy"],feat["labels"], feat["dictionary"]

def loadAux(filename, flagPatches):
    if flagPatches:
        with open(filename,"rb") as fd:
            feat=pickle.load(fd)
        return feat["descriptors"],feat["patches"]
    else:
        with open(filename,"rb") as fd:
            feat=pickle.load(fd)
        return feat["descriptors"]

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

def creaMascara(img,puntos_poly):
    (n,m,k) = img.shape
    img_region = np.zeros((n,m,3))
    img_region = cv2.fillConvexPoly(img_region,np.array(puntos_poly),(255,255,255))
    mascara = []
    for i in range(n):
        for j in range(m):
            if img_region[i][j][0]==255:
                mascara.append(True)
            else:
                mascara.append(False)
    return mascara

################################################################################
##                                    MAIN                                    ##
################################################################################

def main():

    frame91 = cv2.imread("./imagenes/91.png",-1)
    frame92 = cv2.imread("./imagenes/92.png",-1)

    puntos91 = extractRegion(frame91)
    creaMascara(frame91,puntos91)

main()
