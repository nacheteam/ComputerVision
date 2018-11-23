import numpy as np
import cv2
import random
import math
import itertools
random.seed(123456789)

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
    surf = cv2.xfeatures2d.SURF_create(hessianThreshold=hessianThreshold,nOctaves=nOctaves,nOctaveLayers=nOctaveLayers,extended=extended,upright=upright)
    kp = surf.detect(img,None)
    return kp


'''
@brief Obtiene la octava y la capa de los puntos dados.
@param kp puntos clave de los que se quieren obtener información. (lista)
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

'''
@brief Obtiene un diccionario con el número de puntos por cada octava
@param kp Puntos clave (lista)
'''
def obtenNumeroPuntosOctava(kp):
    unpacked = unpackOctave(kp)
    numero_puntos = {}
    for ol in unpacked:
        if not str(ol[0]) in numero_puntos:
            numero_puntos[str(ol[0])]=1
        else:
            numero_puntos[str(ol[0])]+=1
    return numero_puntos

'''
@brief Obtiene un diccionario con el número de puntos por cada capa
@param kp Puntos clave (lista)
'''
def obtenNumeroPuntosCapa(kp):
    unpacked = unpackOctave(kp)
    numero_puntos = {}
    for ol in unpacked:
        if not str(ol[1]) in numero_puntos:
            numero_puntos[str(ol[1])]=1
        else:
            numero_puntos[str(ol[1])]+=1
    return numero_puntos

'''
@brief Obtiene una imagen con círculos en cada punto clave del color correspondiente a la octava
@param img Imagen sobre la que se quiere superponer la información de los puntos clave
@param kp Puntos clave de la imagen img
@param sigma Sigma empleado en la detección de los puntos clave
@param surf Si es true se le han pasado puntos SURF, si es false son SIFT
'''
def pintaCirculos(img,kp,surf=False):
    unpacked = unpackOctave(kp)
    imagen_circulos = img
    for i  in range(len(kp)):
        if not surf:
            imagen_circulos = cv2.circle(imagen_circulos,(int(kp[i].pt[0]),int(kp[i].pt[1])),int(kp[i].size),COLORES[unpacked[i][0]])
        else:
            imagen_circulos = cv2.circle(imagen_circulos,(int(kp[i].pt[0]),int(kp[i].pt[1])),int(kp[i].size/7),COLORES[unpacked[i][0]])
    return imagen_circulos

'''
@brief Función que obtiene el vector de descriptores.
@param img Imagen de la que queremos obtener los descriptores.
@param kp Puntos de interés de la imagen img.
@param sift Objeto SIFT empleado en la detección de los puntos de interes kp de img.
'''
def obtenerDescriptoresSIFT(img,kp,sift):
    des = sift.compute(img,kp)
    return des

'''
@brief Función que obtiene el vector de descriptores.
@param img Imagen de la que queremos obtener los descriptores.
@param kp Puntos de interés de la imagen img.
@param surf Objeto SURF empleado en la detección de los puntos de interes kp de img.
'''
def obtenerDescriptoresSURF(img,kp,surf):
    des = surf.compute(img,kp)
    return des

################################################################################
##                              EJERCICIO 2                                   ##
################################################################################

'''
@brief La función obtiene la imagen con las ocurrencias de los descriptores entre img1 y img2
usando las correspondencias BruteForce y CrossCheck
@param img1 Imagen con la que se quiere establecer una correspondencia entre descriptores
@param img2 Imagen con la que se quiere establecer una correspondencia entre descriptores
@param kp_sift1 Puntos de interés de la imagen 1 usando SIFT
@param kp_sift2 Puntos de interés de la imagen 2 usando SIFT
@param des1 Descriptores de la imagen 1 de los puntos de interés kp_sift1
@param des2 Descriptores de la imagen 2 de los puntos de interés kp_sift2
@param crossCheck Booleano que indica si se activa o no el Cross Check
@param nMatches Número de matches que se quiere obtener en la imagen devuelta.
@return Imagen con los matches
'''
def obtenerImagenBruteForceMatching(img1,img2,kp_sift1,kp_sift2,des1,des2,crossCheck,nMatches):
    # Se crea el objeto BFMatcher con norma L2 y con el crosscheck que le hayamos pasado
    brute_force = cv2.BFMatcher(cv2.NORM_L2,crossCheck=crossCheck)
    # Se obtiene el matching
    matches = brute_force.match(des1,des2)

    # Se obtiene una muestra sin reemplazamiento
    random_seq = random.sample(range(len(matches)),nMatches)
    rand_matches = [matches[i] for i in random_seq]

    #Se obtiene la imagen con las correspondencias. El flag está puesto a 2 para que no dibuje
    #los keypoints sin correspondencias.
    matched = cv2.drawMatches(img1,kp_sift1,img2,kp_sift2,rand_matches,None, flags=2)
    return matched

'''
@brief La función obtiene la imagen con las ocurrencias de los descriptores entre img1 y img2
las correspondencias Lowe-Average-2NN
@param img1 Imagen con la que se quiere establecer una correspondencia entre descriptores
@param img2 Imagen con la que se quiere establecer una correspondencia entre descriptores
@param kp_sift1 Puntos de interés de la imagen 1 usando SIFT
@param kp_sift2 Puntos de interés de la imagen 2 usando SIFT
@param des1 Descriptores de la imagen 1 de los puntos de interés kp_sift1
@param des2 Descriptores de la imagen 2 de los puntos de interés kp_sift2
@param nMatches Número de matches que se quiere obtener en la imagen devuelta.
@return Imagen con los matches
'''
def obtenerImagenLoweAverage2NNMatching(img1,img2,kp_sift1,kp_sift2,des1,des2,nMatches):
    # Se crea el objeto BFMatcher con la norma L2 y con el crossCheck a False puesto que no es necesario
    brute_force = cv2.BFMatcher(cv2.NORM_L2,crossCheck=False)
    # Se encuentran las correspondencias con k=2
    matches = brute_force.knnMatch(des1,des2,k=2)

    # Se aplica el test de Lowe para quedarnos con puntos cercanos
    buenos = []
    for mat1,mat2 in matches:
        if mat1.distance < 0.8*mat2.distance:
            buenos.append([mat1])

    # Tomamos una muestra sin reemplazamiento sobre los cribados por el test
    random_seq = random.sample(range(len(buenos)),nMatches)
    rand_matches = [buenos[i] for i in random_seq]

    # Creamos una imagen a ceros necesaria para el drawMatchesKnn
    outImg = np.zeros((100,100))

    # Obtenemos la imagen con las correspondencias con el flags=2 para que no nos pinte
    # los key points sin correspondencias.
    res = cv2.drawMatchesKnn(img1,kp_sift1,img2,kp_sift2,rand_matches,outImg,flags=2)
    return res

################################################################################
##                              EJERCICIO 3                                   ##
################################################################################

'''
@brief Función que devuelve una matriz con la homografía entre las imagenes usando Lowe-Average-2NN
@param image1 Imagen de opencv
@param image2 Imagen de opencv
@return Devuelve una matriz de numpy de 3x3 con floats que representa la homografía.
'''
def getHomograhy(image1,image2):
    sift = cv2.xfeatures2d.SIFT_create()
    brute_force = cv2.BFMatcher(cv2.NORM_L2,crossCheck=False)
    kp_image1, descriptores_image1 = sift.detectAndCompute(image1,None)
    kp_image2, descriptores_image2 = sift.detectAndCompute(image2,None)
    matches = brute_force.knnMatch(descriptores_image1,descriptores_image2,k=2)
    buenos_matches = []
    for mat1,mat2 in matches:
        if mat1.distance < 0.8*mat2.distance:
            buenos_matches.append(mat1)

    p1 = np.array([kp_image1[match.queryIdx].pt for match in buenos_matches])
    p2 = np.array([kp_image2[match.trainIdx].pt for match in buenos_matches])
    return cv2.findHomography(p1,p2,cv2.RANSAC,1)[0]

'''
@brief Obtiene una estimación de tamaño para la imagen al unir el vector de imagenes por una homografía
@param images Vector de imagenes de opencv
@return Devuelve dos enteros, el primero el número de columnas y el segundo el de filas.
'''
def getTamano(images):
    sizes = [image.shape for image in images]
    n = 0
    m = 0
    for (t,r,z) in sizes:
        n+=t
        if m<r:
            m=r
    return n,m

'''
@brief Función que obtiene el mosaico con el vector de imagenes images de tamaño n filas y m columnas.
@param images Vector de imágenes de OpenCV
@param n Número de filas de la imagen resultado
@param m Número de columnas de la imagen resultado
@return Devuelve una imagen de OpenCV después de juntar convenientemente las imágenes del vector images.
'''
def obtenerMosaico(images,n=-1,m=-1):
    if n==-1:
        n,m=getTamano(images)
    # El indice central del vector de imagenes
    indice_central=math.floor(len(images)/2)
    # Tamaño de la imagen central (se usa para la traslacion)
    (n_central,m_central,z) = images[indice_central].shape
    traslacion = np.float32(np.array([[1,0,n//2-m_central//2],[0,1,m//2-n_central//2],[0,0,1]]))
    # Vector que vamos a rellenar con las homografias
    homografias_izq = [traslacion]
    homografias_der = [traslacion]
    # Imagen que se va a devolver
    imagen_res = np.zeros(n*m*3,dtype='uint8').reshape(m,n,3)

    # Para cada pareja de imagenes se calcula la homografía
    # Si estamos en la parte izquierda se calcula de fuera hacia dentro
    # Si estamos en la parte derecha se calcula de dentro hacia fuera
    for i in range(indice_central-1,-1,-1):
        H = getHomograhy(images[i],images[i+1])
        homografias_izq.append(H)

    for i in range(indice_central,len(images)-1):
        H = getHomograhy(images[i+1],images[i])
        homografias_der.append(H)

    for i in range(1,len(homografias_izq)):
        homografias_izq[i] = homografias_izq[i-1]@homografias_izq[i]

    # Le damos la vuelta y quitamos la  traslación
    homografias_izq = list(reversed(homografias_izq[1:]))

    for i in range(1,len(homografias_der)):
        homografias_der[i] = homografias_der[i-1]@homografias_der[i]

    homografias_buenas = homografias_izq + homografias_der

    for i in range(len(images)):
        imagen_res = cv2.warpPerspective(src=images[i],dst=imagen_res,M=homografias_buenas[i],dsize=(n,m),borderMode=cv2.BORDER_TRANSPARENT)

    return imagen_res

'''
@brief Función que obtiene a mano la imagen que resulta de unir tres imagenes
@param images Vector con tres imagenes de opencv
@return Devuelve una imagen resultado tras unir las imagenes de images
'''
def obtenerMosaico3(images):
    homografias = []

    sift = cv2.xfeatures2d.SIFT_create()
    kp_image1, descriptores_image1 = sift.detectAndCompute(images[0],None)
    kp_image2, descriptores_image2 = sift.detectAndCompute(images[1],None)
    kp_image3, descriptores_image3 = sift.detectAndCompute(images[2],None)

    # Calculamos los matches
    brute_force = cv2.BFMatcher(cv2.NORM_L2,crossCheck=False)
    matches = brute_force.knnMatch(descriptores_image2,descriptores_image1,k=2)
    buenos_matches = []
    for mat1,mat2 in matches:
        if mat1.distance < 0.8*mat2.distance:
            buenos_matches.append(mat1)

    p1 = np.array([kp_image1[match.trainIdx].pt for match in buenos_matches])
    p2 = np.array([kp_image2[match.queryIdx].pt for match in buenos_matches])
    H = cv2.findHomography(p1,p2,cv2.RANSAC,1)
    homografias.append(H)

    homografias.append(np.float32(np.array([[1,0,750-300],[0,1,350-300],[0,0,1]])))

    # Calculamos los matches
    matches = brute_force.knnMatch(descriptores_500image2,descriptores_image3,k=2)
    buenos_matches = []
    for mat1,mat2 in matches:
        if mat1.distance < 0.8*mat2.distance:
            buenos_matches.append(mat1)

    p1 = np.array([kp_image2[match.queryIdx].pt for match in buenos_matches])
    p2 = np.array([kp_image3[match.trainIdx].pt for match in buenos_matches])
    H = cv2.findHomography(p2,p1,cv2.RANSAC,1)
    homografias.append(H)

    img_res = np.zeros(shape=(700,1500),dtype='uint8')

    img_res = cv2.warpPerspective(src=images[0],dst=img_res,M=np.dot(homografias[1],homografias[0][0]),dsize=(1500,700))
    img_res = cv2.warpPerspective(src=images[1],dst=img_res,M=homografias[1],dsize=(1500,700),borderMode=cv2.BORDER_TRANSPARENT)
    img_res = cv2.warpPerspective(src=images[2],dst=img_res,M=np.dot(homografias[1],homografias[2][0]),dsize=(1500,700),borderMode=cv2.BORDER_TRANSPARENT)

    pintaI(img_res)


################################################################################
##                                    MAIN                                    ##
################################################################################

def main():
    '''
    # Ejercicio 1 apartado a
    print("Imagen Yosemite1")

    yosemite1 = cv2.imread("imagenes/yosemite/Yosemite1.jpg",-1)
    kp_sift1 = keyPointsSIFT(yosemite1,contrastThreshold=0.06,edgeThreshold=6,sigma=1.6)
    yosemite1_kp_sift=cv2.drawKeypoints(yosemite1,kp_sift1,yosemite1)
    print("El número de puntos obtenidos por SIFT: " + str(len(kp_sift1)))
    pintaI(yosemite1_kp_sift)

    yosemite1 = cv2.imread("imagenes/yosemite/Yosemite1.jpg",-1)
    kp_surf1 = keyPointsSURF(yosemite1,hessianThreshold=400,nOctaves=4,nOctaveLayers=3,extended=False,upright=False)
    yosemite1_kp_surf=cv2.drawKeypoints(yosemite1,kp_surf1,yosemite1)
    print("El número de puntos obtenidos por SURF: " + str(len(kp_surf1)))
    pintaI(yosemite1_kp_surf)

    print("Imagen Yosemite2")

    yosemite2 = cv2.imread("imagenes/yosemite/Yosemite2.jpg",-1)
    kp_sift2 = keyPointsSIFT(yosemite2,contrastThreshold=0.06,edgeThreshold=4,sigma=1.6)
    yosemite1_kp_sift=cv2.drawKeypoints(yosemite2,kp_sift2,yosemite1)
    print("El número de puntos obtenidos por SIFT: " + str(len(kp_sift2)))
    pintaI(yosemite1_kp_sift)

    yosemite2 = cv2.imread("imagenes/yosemite/Yosemite2.jpg",-1)
    kp_surf2 = keyPointsSURF(yosemite2,hessianThreshold=500,nOctaves=4,nOctaveLayers=3,extended=False,upright=False)
    yosemite2_kp_surf=cv2.drawKeypoints(yosemite2,kp_surf2,yosemite1)
    print("El número de puntos obtenidos por SURF: " + str(len(kp_surf2)))
    pintaI(yosemite2_kp_surf)

    # Ejercicio 1 apartado b
    print("Imagen Yosemite1")

    yosemite1 = cv2.imread("imagenes/yosemite/Yosemite1.jpg",-1)
    print("El número de puntos por octava en SIFT ha sido: " + str(obtenNumeroPuntosOctava(kp_sift1)))
    print("El número de puntos por octava en SURF ha sido: " + str(obtenNumeroPuntosOctava(kp_surf1)))
    print("El número de puntos por capa en SIFT ha sido: " + str(obtenNumeroPuntosCapa(kp_sift1)))
    pintaI(pintaCirculos(yosemite1,kp_sift1))
    pintaI(pintaCirculos(yosemite1,kp_surf1,surf=True))

    print("Imagen Yosemite2")

    yosemite2 = cv2.imread("imagenes/yosemite/Yosemite2.jpg",-1)
    print("El número de puntos por octava en SIFT ha sido: " + str(obtenNumeroPuntosOctava(kp_sift2)))
    print("El número de puntos por octava en SURF ha sido: " + str(obtenNumeroPuntosOctava(kp_surf2)))
    print("El número de puntos por capa en SIFT ha sido: " + str(obtenNumeroPuntosCapa(kp_sift2)))
    pintaI(pintaCirculos(yosemite2,kp_sift2))
    pintaI(pintaCirculos(yosemite2,kp_surf2,surf=True))

    # Ejercicio 1 apartado c
    print("Imagen Yosemite1")

    yosemite1 = cv2.imread("imagenes/yosemite/Yosemite1.jpg",-1)
    sift1 = cv2.xfeatures2d.SIFT_create(nfeatures=0,nOctaveLayers=3,contrastThreshold=0.06,edgeThreshold=6,sigma=1.6)
    surf1 = cv2.xfeatures2d.SURF_create(hessianThreshold=400,nOctaves=4,nOctaveLayers=3,extended=False,upright=False)
    kp_sift1 = sift1.detect(yosemite1,None)
    kp_surf1 = surf1.detect(yosemite1,None)
    _, descriptores_sift1 = sift1.compute(yosemite1,kp_sift1)
    _, descriptores_surf1 = surf1.compute(yosemite1,kp_surf1)
    print("Descriptores SIFT: " + str(descriptores_sift1))
    print("Descriptores SURF: " + str(descriptores_surf1))

    print("Imagen Yosemite2")

    yosemite2 = cv2.imread("imagenes/yosemite/Yosemite2.jpg",-1)
    sift2 = cv2.xfeatures2d.SIFT_create(nfeatures=0,nOctaveLayers=3,contrastThreshold=0.06,edgeThreshold=6,sigma=1.6)
    surf2 = cv2.xfeatures2d.SURF_create(hessianThreshold=400,nOctaves=4,nOctaveLayers=3,extended=False,upright=False)
    kp_sift2 = sift2.detect(yosemite2,None)
    kp_surf2 = surf2.detect(yosemite2,None)
    _, descriptores_sift2 = sift2.compute(yosemite2,kp_sift2)
    _, descriptores_surf2 = surf2.compute(yosemite2,kp_surf2)
    print("Descriptores SIFT: " + str(descriptores_sift2))
    print("Descriptores SURF: " + str(descriptores_surf2))

    # Ejercicio 2a
    print("Fuerza bruta+crosscheck")
    res_bf_ck = obtenerImagenBruteForceMatching(yosemite1,yosemite2,kp_sift1,kp_sift2,descriptores_sift1,descriptores_sift2,True,100)
    pintaI(res_bf_ck)

    print("Fuerza Lowe-Average 2NN")
    res_la_2nn = obtenerImagenLoweAverage2NNMatching(yosemite1,yosemite2,kp_sift1,kp_sift2,descriptores_sift1,descriptores_sift2,100)
    pintaI(res_la_2nn)

    '''
    # Ejercicio 3 y 4
    yosemite1 = cv2.imread("imagenes/yosemite_full/yosemite1.jpg",-1)
    yosemite2 = cv2.imread("imagenes/yosemite_full/yosemite2.jpg",-1)
    yosemite3 = cv2.imread("imagenes/yosemite_full/yosemite3.jpg",-1)
    yosemite4 = cv2.imread("imagenes/yosemite_full/yosemite4.jpg",-1)
    pintaI(obtenerMosaico([yosemite1,yosemite2,yosemite3]))
    pintaI(obtenerMosaico([yosemite1,yosemite2,yosemite3,yosemite4]))
    #pintaI(obtenerMosaico3([yosemite1,yosemite2,yosemite3]))

    mosaico1 = cv2.imread("imagenes/mosaico-1/mosaico002.jpg",-1)
    mosaico2 = cv2.imread("imagenes/mosaico-1/mosaico003.jpg",-1)
    mosaico3 = cv2.imread("imagenes/mosaico-1/mosaico004.jpg",-1)
    mosaico4 = cv2.imread("imagenes/mosaico-1/mosaico005.jpg",-1)
    mosaico5 = cv2.imread("imagenes/mosaico-1/mosaico006.jpg",-1)
    mosaico6 = cv2.imread("imagenes/mosaico-1/mosaico007.jpg",-1)
    mosaico7 = cv2.imread("imagenes/mosaico-1/mosaico008.jpg",-1)
    mosaico8 = cv2.imread("imagenes/mosaico-1/mosaico009.jpg",-1)
    mosaico9 = cv2.imread("imagenes/mosaico-1/mosaico010.jpg",-1)
    mosaico10 = cv2.imread("imagenes/mosaico-1/mosaico011.jpg",-1)

    pintaI(obtenerMosaico([mosaico1,mosaico2,mosaico3,mosaico4]))
    pintaI(obtenerMosaico([mosaico1,mosaico2,mosaico3,mosaico4,mosaico5,mosaico6,mosaico7,mosaico8,mosaico9,mosaico10],n=1400,m=600))

main()
