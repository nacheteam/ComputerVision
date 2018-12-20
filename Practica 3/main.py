# -*- coding: utf-8 -*-
import numpy as np
import cv2
import pickle
import random
random.seed(123456789)

NUM_IMAGENES = 440
NUM_CENTROIDES = 2000
NUM_SIMILARES = 5

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

# Se usan para las imagenes de los circulos
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

'''
@brief Función que obtiene una máscara con unos dentro del polígono
@param img Imagen de la que va a obtenerse la máscara
@param puntos_poly Lista de tuplas que respresentan puntos en la imagen img y que delimitan un polígono
@return Devuelve una matriz que representa una máscara
'''
def creaMascara(img,puntos_poly):
    # Tomamos las dimensiones
    (n,m,k) = img.shape
    # Rellenamos la imagen a ceros y con blancos la región
    img_region = np.zeros((n,m,3))
    img_region = cv2.fillConvexPoly(img_region,np.array(puntos_poly),(255,255,255))
    # Hacemos una matriz a ceros y si encontramos en la imagen de la región un blanco
    # ponemos a 1 la posición correspondiente
    mascara = np.zeros((n,m),dtype='uint8')
    for i in range(n):
        for j in range(m):
            if img_region[i][j][0]==255:
                mascara[i][j]=1
    return mascara

'''
@brief La función obtiene la imagen con las ocurrencias de los descriptores entre img1 y img2
las correspondencias Lowe-Average-2NN
@param img1 Imagen con la que se quiere establecer una correspondencia entre descriptores
@param img2 Imagen con la que se quiere establecer una correspondencia entre descriptores
@param kp_sift1 Puntos de interés de la imagen 1 usando SIFT
@param kp_sift2 Puntos de interés de la imagen 2 usando SIFT
@param des1 Descriptores de la imagen 1 de los puntos de interés kp_sift1
@param des2 Descriptores de la imagen 2 de los puntos de interés kp_sift2
@return Imagen con los matches
'''
def obtenerImagenLoweAverage2NNMatching(img1,img2,kp_sift1,kp_sift2,des1,des2):
    # Se crea el objeto BFMatcher con la norma L2 y con el crossCheck a False puesto que no es necesario
    brute_force = cv2.BFMatcher(cv2.NORM_L2,crossCheck=False)
    # Se encuentran las correspondencias con k=2
    matches = brute_force.knnMatch(des1,des2,k=2)

    # Se aplica el test de Lowe para quedarnos con puntos cercanos
    buenos = []
    for mat1,mat2 in matches:
        if mat1.distance < 0.8*mat2.distance:
            buenos.append([mat1])

    # Creamos una imagen a ceros necesaria para el drawMatchesKnn
    outImg = np.zeros((100,100))

    # Obtenemos la imagen con las correspondencias con el flags=2 para que no nos pinte
    # los key points sin correspondencias.
    res = cv2.drawMatchesKnn(img1,kp_sift1,img2,kp_sift2,buenos,outImg,flags=2)
    return res

'''
@brief Función que pinta la imagen con las correspondencias en una región
@param img1 Imagen
@param img2 Imagen
'''
def pintaCorrespondencias(img1,img2):
    # Se obtine la región mediante la interacción del usuario
    puntos1 = extractRegion(img1)
    # Creamos la máscara
    mascara1 = creaMascara(img1,puntos1)
    sift = cv2.xfeatures2d.SIFT_create()
    # Obtenemos los keypoints y descriptores con la máscara en el caso necesario
    kp1, des1 = sift.detectAndCompute(img1,mascara1)
    kp2, des2 = sift.detectAndCompute(img2,None)
    # Obtenemos las correspondencias
    img_correspondencias = obtenerImagenLoweAverage2NNMatching(img1,img2,kp1,kp2,des1,des2)
    # Pintamos el resultado
    pintaI(img_correspondencias)

################################################################################
##                              EJERCICIO 2                                   ##
################################################################################

def distanciaEuclidea(v1,v2s):
    return np.sqrt(np.sum(np.power(np.array(v1)-np.array(v2s),2),axis=1))

def normaEuclidea(v):
    return np.sqrt(np.sum(np.array(v)*np.array(v)))

def convierteAVectorNormalizado(histograma):
    vec = []
    for i in range(NUM_CENTROIDES):
        if str(i) in histograma:
            vec.append(histograma[str(i)])
        else:
            vec.append(0)
    return vec/normaEuclidea(vec)

def obtenerHistograma(sift,img,centroides):
    _, des = sift.detectAndCompute(img,None)
    histograma = {}
    #des_sample = random.sample(list(des),200) if 200<len(des) else des
    print("Tamaño del descriptor: " + str(len(des)))
    for d in des:
        distancias = distanciaEuclidea(d,centroides)
        min = np.argmin(distancias)
        if not str(min) in histograma:
            histograma[str(min)] = 1
        else:
            histograma[str(min)]+=1
    return histograma

def crearModeloHistogramas():
    sift = cv2.xfeatures2d.SIFT_create(contrastThreshold=0.07)
    dic = loadDictionary("./kmeanscenters2000.pkl")
    imagenes = []
    for i in range(NUM_IMAGENES+1):
        img = cv2.imread("./imagenes/" + str(i) + ".png",-1)
        imagenes.append(img)
    histogramas = []

    contador = 0
    for img in imagenes:
        print("Creando modelo de histogramas " + str(contador) + "/" + str(len(imagenes)))
        contador+=1
        histogramas.append(obtenerHistograma(sift,img,dic[2]))
    histogramas_vec=convierteHistogramasVectores(histogramas)
    return histogramas_vec

def convierteHistogramasVectores(histogramas):
    histogramas_vec = []
    for i in range(len(histogramas)):
        histogramas_vec.append(convierteAVectorNormalizado(histogramas[i]))
    return histogramas_vec

def devuelveSimilares(pos,histogramas_vec):
    similitudes = []
    for i in range(len(histogramas_vec)):
        if pos!=i:
            # Estoy usando la distancia euclidea, puede que sea el producto escalar
            similitudes.append(np.sum(np.power(histogramas_vec[i]-histogramas_vec[pos],2)))
        else:
            similitudes.append(float('inf'))
    return np.array(similitudes).argsort()[-NUM_SIMILARES:]

def pintaRespuestas(imagen,histo_vec,pos):
    indices_similares = devuelveSimilares(pos,histo_vec)
    imagenes_similares=[]
    for ind in indices_similares:
        img = cv2.imread("./imagenes/" + str(ind) + ".png",-1)
        imagenes_similares.append(img)
    pintaMI([imagen]+imagenes_similares)

################################################################################
##                                    MAIN                                    ##
################################################################################

def main():
    '''
    # Ejercicio 1

    # Aplicado con las imagenes 91 y 92
    frame91 = cv2.imread("./imagenes/91.png",-1)
    frame92 = cv2.imread("./imagenes/92.png",-1)
    pintaCorrespondencias(frame91,frame92)

    # Aplicaco con las imagenes 1 y 4
    frame1 = cv2.imread("./imagenes/1.png",-1)
    frame4 = cv2.imread("./imagenes/4.png",-1)
    pintaCorrespondencias(frame1,frame4)
    '''


    histogramas_vec = crearModeloHistogramas()
    frame1 = cv2.imread("./imagenes/1.png",-1)
    frame91 = cv2.imread("./imagenes/91.png",-1)
    frame200 = cv2.imread("./imagenes/200.png",-1)
    print("Frame1")
    pintaRespuestas(frame1,histogramas_vec,1)
    print("Frame91")
    pintaRespuestas(frame91,histogramas_vec,91)
    print("Frame200")
    pintaRespuestas(frame200,histogramas_vec,200)
    

main()
