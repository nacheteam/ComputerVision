# -*- coding: utf-8 -*-
import numpy as np
import cv2
import pickle
import random
import cProfile
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
            if img_region[i][j][0]==255 and img_region[i][j][1]==255 and img_region[i][j][2]==255:
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

'''
@brief Función que obtiene la distancia euclídea entre un vector y una lista de vectores
@param v1 Vector
@param v2s Lista de vectores
@return Vector con la distancia euclídea del vector v1 a cada uno de la lista v2s
'''
def distanciaEuclidea(v1,v2s):
    return np.sqrt(np.sum(np.power(np.array(v1)-np.array(v2s),2),axis=1))

'''
@brief Función que obtiene la norma euclídea de un vector
@param v Vector del que se quiere obtener la norma euclídea
@return Devuelve la norma euclídea del vector v
'''
def normaEuclidea(v):
    return np.sqrt(np.sum(np.array(v)*np.array(v)))

'''
@brief Función que convierte un histograma a un vector normalizado
@param histograma Histograma con las ocurrencias de cada centroide
@return Devuelve un vector que tiene en cada posición un 0 si no hay ocurrencias
del centroide o el número de ocurrencias del mismo. Este vector está normalizado.
'''
def convierteAVectorNormalizado(histograma):
    vec = []
    for i in range(NUM_CENTROIDES):
        if str(i) in histograma:
            vec.append(histograma[str(i)])
        else:
            vec.append(0)
    return vec/normaEuclidea(vec)

'''
@brief Función que obtiene el histograma de una imagen dada
@param sift Objeto de tipo SIFT que se usa para obtener los descriptores
@param img Imagen de la que se quiere obtener el histograma
@param centroides Lista de centroides para sacar los mas cercanos y el número de ocurrencias de los mismos.
@return Devuelve un objeto de tipo diccionario con el histograma
'''
def obtenerHistograma(sift,img,centroides):
    # Obtenemos los descriptores
    _, des = sift.detectAndCompute(img,None)
    histograma = {}
    #des_sample = random.sample(list(des),200) if 200<len(des) else des
    print("Tamaño del descriptor: " + str(len(des)))


    # Se crea el objeto BFMatcher con norma L2
    brute_force = cv2.BFMatcher(cv2.NORM_L2,crossCheck=False)
    # Se obtiene el elemento mas cercan para cada descriptor
    matches = brute_force.match(des,centroides)

    for m in matches:
        indice_centroide = m.trainIdx
        if not str(indice_centroide) in histograma:
            histograma[str(indice_centroide)] = 1
        else:
            histograma[str(indice_centroide)]+=1

    return histograma

'''
@brief Función que obtiene todos los histogramas como vectores de todas las imágenes
@return Devuelve una lista de vectores que representan los histogramas
'''
def crearModeloHistogramas():
    # Creo el objeto SIFT
    sift = cv2.xfeatures2d.SIFT_create(contrastThreshold=0.01,edgeThreshold=6,sigma=1.6)
    # Cargamos los centroides
    dic = loadDictionary("./kmeanscenters2000.pkl")
    # Hacemos un vector con todas las imagenes en orden
    imagenes = []
    for i in range(NUM_IMAGENES+1):
        img = cv2.imread("./imagenes/" + str(i) + ".png",-1)
        imagenes.append(img)
    histogramas = []

    contador = 0
    # Para cada imagen
    for img in imagenes:
        print("Creando modelo de histogramas " + str(contador) + "/" + str(len(imagenes)))
        contador+=1
        # Añadimos el histograma de la imagen correspondiente
        histogramas.append(obtenerHistograma(sift,img,dic[2]))
    # Convertimos todos los histogramas en vectores
    histogramas_vec=convierteHistogramasVectores(histogramas)
    return histogramas_vec

'''
@brief Función que convierte una lista de histogramas en una lista de vectores
@param histogramas Lista de histogramas
@return Devuelve una lista de vectores asociados a los histogramas
'''
def convierteHistogramasVectores(histogramas):
    histogramas_vec = []
    # Para cada histograma
    for i in range(len(histogramas)):
        # Lo convertimos en vector normalizado y lo añadimos a la lista
        histogramas_vec.append(convierteAVectorNormalizado(histogramas[i]))
    return histogramas_vec

'''
@brief Función que devuelve los indices de las imágenes más similares a una dada
@param pos Posición de la imagen pregunta
@param histogramas_vec Histogramas de las imágenes como vectores
@return Lista con los índices de las imágenes más similares a la dada
'''
def devuelveSimilares(pos,histogramas_vec):
    similitudes = []
    #Para cada histograma
    for i in range(len(histogramas_vec)):
        # Si la posición no es la de la pregunta, hacemos la distancia euclídea
        if pos!=i:
            # Uso la distancia euclidea TODO: Cambiarlo a producto escalar
            similitudes.append(np.dot(histogramas_vec[i],histogramas_vec[pos]))
            #similitudes.append(np.sum(np.power(histogramas_vec[i]-histogramas_vec[pos],2)))
        # Si la posición es la de la pregunta le asignamos distancia infinita
        else:
            similitudes.append(-1)
    # Devolvemos los 5 primeros indices
    return np.array(similitudes).argsort()[::-1][:NUM_SIMILARES]

'''
@brief Función que dada una imagen pinta las más similares
@param imagen Imagen de la que queremos obtener las más similares
@param histo_vec Histograma como vectores
@param pos Posición de la imagen preguntas
'''
def pintaRespuestas(imagen,histo_vec,pos):
    # Obtenemos los índices de las imagenes más similares
    indices_similares = devuelveSimilares(pos,histo_vec)
    imagenes_similares=[]
    # Para cada indice
    for ind in indices_similares:
        # Cargamos la imagen
        img = cv2.imread("./imagenes/" + str(ind) + ".png",-1)
        # La añadimos a la lista
        imagenes_similares.append(img)
    # Imprimimos primero la imagen pregunta y luego las 5 mas similares
    pintaMI([imagen]+imagenes_similares)

'''
@brief Devuelve un modelo de indice invertido en el que para cada centroide, se
obtiene en qué imagenes aparece.
@param histogramas_vec Histogramas de todas las imágenes como vectores.
@return Devuelve una lista de listas de apariciones de imágenes para cada centroide.
'''
def obtenerIndiceInvertido(histogramas_vec):
    indice_invertido=[]
    # Para cada centroide
    for i in range(NUM_CENTROIDES):
        #Inicializamos las apariciones de dicho centroide en cada imagen
        apariciones = []
        # Para cada histograma
        for j in range(len(histogramas_vec)):
            # Si el histograma tiene la posición correspondiente al centroide mayor que 0
            if histogramas_vec[j][i]>0:
                # Añadimos el índice
                apariciones.append(j)
        # Añadimos la lista de indices para cada centroide
        indice_invertido.append(apariciones)
    return indice_invertido

'''
@brief Función que dado el histograma y una posición pinta las imágenes que se asocian al
centroide pos.
@param histogramas_vec Histogramas de las imágenes como vectores
@param pos Posición del descriptor del que queremos obtener las imágenes
'''
def pintaInvertido(histogramas_vec,pos):
    # Obtenemos el modelo de indice invertido
    indice = obtenerIndiceInvertido(histogramas_vec)
    # Obtenemos una muestra de 5 imágenes aleatorias asociadas al descriptor pos
    imagenes = random.sample(indice[pos],5) if len(indice[pos])>5 else indice[pos]

    # Leemos las imagenes y las almacenamos en una lista
    imgs = []
    for imagen in imagenes:
        im = cv2.imread("./imagenes/" + str(imagen) + ".png",-1)
        imgs.append(im)
    # Pinta las imagenes
    pintaMI(imgs)

################################################################################
##                              EJERCICIO 3                                   ##
################################################################################

'''
@brief Función que obtiene una lista de listas de minimos. En general obtiene
5 elementos aleatorios de kmeanscenters2000 y obtiene los 10 mas cercanos de descriptorsAndpatches2000.
@param n_aleatorios Cuantos elementos aleatorios queremos obtener de kmeanscenters2000
@param n_min El número de elementos que queremos obtener con distancia mínima
@return Devuelve una lista que tiene en cada posición una lista con los índices de mínima distancia
'''
def obtenMinimos(n_aleatorios,n_min):
    # Lee el fichero
    dic = loadDictionary("./kmeanscenters2000.pkl")[2]
    # Tomo n_aleatorios elementos de forma aleatoria de los descriptores
    aleatorios = random.sample(list(dic),n_aleatorios)

    # Lee el fichero
    desc = loadAux("./descriptorsAndpatches2000.pkl", True)[0]
    minimos = []

    # Para cada aleatorio
    for aleatorio in aleatorios:
        distancias = []
        # Para cada descriptor
        for i in range(len(desc)):
            # Obtenemos las distancias
            distancias.append(np.dot(aleatorio,desc[i]))
        # Calculamos los n_min primeros elementos con distancia mínima a aleatorio
        minimos.append(np.array(distancias).argsort()[:n_min][::-1])
    return minimos

'''
@brief Función que pinta los parches con mínima distancia calculados por obtenMinimos.
Los pinta en escala de grises
'''
def pintaMinimos():
    # Lee el fichero
    dic = loadAux("./descriptorsAndpatches2000.pkl",True)
    # Obtenemos 5 elementos aleatorios y le calculamos los 10 parches más cercanos
    minimos = obtenMinimos(5,10)

    # Para cada minimo
    for min in minimos:
        imagenes = []
        # Para cada parche de mínima distancia
        for m in min:
            # Convierte a escala de grises y adjunta a imagenes
            imagenes.append(cv2.cvtColor(dic[1][m],cv2.COLOR_RGB2GRAY))
        # Pinta las imagenes
        pintaMI(imagenes)


################################################################################
##                                    MAIN                                    ##
################################################################################

def main():

    # Ejercicio 1

    # Aplicado con las imagenes 91 y 92
    frame91 = cv2.imread("./imagenes/91.png",-1)
    frame92 = cv2.imread("./imagenes/92.png",-1)
    pintaCorrespondencias(frame91,frame92)

    #Aplicado con las imagenes 23 y 24
    frame23 = cv2.imread("./imagenes/23.png",-1)
    frame24 = cv2.imread("./imagenes/24.png",-1)
    pintaCorrespondencias(frame23,frame24)

    # Aplicado con las imagenes 1 y 4
    frame1 = cv2.imread("./imagenes/1.png",-1)
    frame4 = cv2.imread("./imagenes/4.png",-1)
    pintaCorrespondencias(frame1,frame4)

    # Aplicado con las imagenes 132 y 133
    frame142 = cv2.imread("./imagenes/142.png",-1)
    frame143 = cv2.imread("./imagenes/143.png",-1)
    pintaCorrespondencias(frame142,frame143)

    # Ejercicio 2

    # Obtenemos los histogramas como vectores
    histogramas_vec = crearModeloHistogramas()

    #Tomamos las imagenes
    frame1 = cv2.imread("./imagenes/1.png",-1)
    frame15 = cv2.imread("./imagenes/15.png",-1)
    frame91 = cv2.imread("./imagenes/91.png",-1)
    frame209 = cv2.imread("./imagenes/209.png",-1)
    frame200 = cv2.imread("./imagenes/200.png",-1)

    #Vemos las imagenes mas similares para estas
    print("Las 5 imágenes más similares para la imagen 15")
    pintaRespuestas(frame15,histogramas_vec,15)
    print("Las 5 imágenes más similares para la imagen 209")
    pintaRespuestas(frame209,histogramas_vec,209)
    print("Las 5 imágenes más similares para la imagen 1")
    pintaRespuestas(frame1,histogramas_vec,1)
    print("Las 5 imágenes más similares para la imagen 91")
    pintaRespuestas(frame91,histogramas_vec,91)
    print("Las 5 imágenes más similares para la imagen 200")
    pintaRespuestas(frame200,histogramas_vec,200)

    # Obtenemos la estructura de indice invertido para las imagenes con los centroides.
    print("Recupera 5 imágenes aleatorias del descriptor 5")
    pintaInvertido(histogramas_vec,5)
    print("Recupera 5 imágenes aleatorias del descriptor 222")
    pintaInvertido(histogramas_vec,222)
    print("Recupera 5 imágenes aleatorias del descriptor 100")
    pintaInvertido(histogramas_vec,100)
    print("Recupera 5 imágenes aleatorias del descriptor 76")
    pintaInvertido(histogramas_vec,76)
    print("Recupera 5 imágenes aleatorias del descriptor 1300")
    pintaInvertido(histogramas_vec,1300)

    # Ejercicio 3
    pintaMinimos()

main()
