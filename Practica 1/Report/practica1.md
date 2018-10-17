---
title: Práctica 1: Filtrado y Muestreo
author: "Ignacio Aguilera Martos"
date: VC
lang: es
toc: true
toc-depth: 1
fontsize: 12pt
geometry: margin=1.4in
---

# Práctica 1: Filtrado y Muestreo
# Ignacio Aguilera Martos

## Ejercicio 1

### Apartado A
Para aplicar la convolución con una máscara Gaussiana 2D en OpenCV nos valemos de la función GaussianBlur que toma como parámetros (los que nos interesan) la imagen, el tamaño del kernel y la varianza en el eje X y en el eje Y.
Para esta prueba he movido la varianza entre 0 y 5 (en ambos ejes) y el tamaño del núcleo de 3 a 11 haciendo kernels cuadrados y rectangulares.

![GaussianBlur](./Imagenes/1A.PNG)

Podemos observar que el efecto se hace más visible de izquierda a derecha. Si nos fijamos en la imagen podemos ver que al hacer más grande el tamaño del núcleo podemos percibir de forma más nítida los rectángulos o cuadrados en la imagen. Además se observa que al aumentar los valores de sigma el suavizado se hace más visible.

### Apartado B
En este caso el ejercicio nos pide que tomemos mediante la función getDerivKernels las máscadas 1-dimensionales que permiten calcular la convolución 2D con máscaras derivadas. Para ello la función getDerivKernels toma como parámetros el orden de la derivada tanto en el eje X como en el Y y el valor de sigma. Observemos el ejemplo para obtener conclusiones:

\vspace{50px}

![getDerivKernels](./Imagenes/1B.png)

Debemos saber que la función getDerivKernels utiliza por debajo el operador de Sobel para hacer los cálculos. Interpretemos ahora los vectores obtenidos.

Podemos observar que el orden de la derivada en cada eje nos varía cada uno de los vectores correspondientes. Debemos recordar que este operador (Sobel) es empleado para reconocimiento de bordes en las imágenes, o lo que es lo mismo, un cambio muy notable de color en el entorno de un píxel. La función nos devuelve dos vectores que correspoden a la máscara, ya que es separable.

Miremos el primer caso. Tenemos los vectores (-1,0,1) y (-1,0,1) tanto para filas como columnas. Esto lo que va a hacer es dar como resultado la diferencia de valores de color que hay entre el pixel a la izquierda y derecha del que estamos teniendo en cuenta y la diferencia entre el pixel superior e inferior. En otras palabras, si hallamos una diferencia muy grande de color entre los mencionados es que tendremos un borde en la figura y por tanto al obtener la diferencia en valor absoluto tendremos un valor muy alto próximo al blanco en escala de grises, con lo que se resaltarán en blanco los bordes.

Veamos los ejemplos tres y cuatro en los que los órdenes de las derivadas no coinciden en el eje X e Y. En estos casos podemos observar que la posición central es cero cuando tenemos que el orden de derivación es impar y en estos casos cuanto mayor es el orden de derivación mayores son los números estrictamente anterior y posterior al central, con lo que mayor relevacia se les está dando en la resta a los mismos. Esto quiere decir que si los píxeles estrictamente al lado del que estamos estudiando tienen valores muy diferentes el valor asignado al pixel será muy elevado y por tanto se le tomará como borde. Si el orden de la derivada es par podemos observar que la posición central deja de ser 0 para ser un número directamente proporcional al orden de derivación con lo que cuanto más alto sea el mismo mayor importancia se le asginará al color del pixel que estamos teniendo en cuenta. Además podemos observar que no realizan una resta de los píxeles que quedan a los lados del que estamos considerando de forma simétrica si no que lo que tiene en cuenta es de alguna manera como van haciendo el gradiente los píxeles colindantes hacia el centro.

### Apartado C
Para aplicar la laplaciana a las imágenes lo primero que tenemos que hacer es aplicar una convolución gaussiana para eliminar el ruido en la imagen. Para ello nos valemos de la función GaussianBlur ya utilizada en el apartado A con un kernel cuadrado y la varianza dada. Debemos recordar que el operador laplaciano está pensado para detectar bordes con lo que está pensado para ser aplicado a imágenes en blanco y negro. Convertimos la imagen de RGB a escala de grises y tras esto le aplicamos el operador laplaciano que consiste en sumar las derivadas de segundo orden de la imagen. Analicemos que obtenemos con esto:

![Laplacian1](./Imagenes/1C1.png)
![Laplacian2](./Imagenes/1C2.png)

En estos ejemplos podemos ver en la primera imagen el laplaciano aplicado con sigma=1, el tamaño del núcleo tomando valores 3,5,9,3,5,9 y los bordes reflejados y replicados y en la segunda imagen lo mismo pero con sigma=3.

Podemos observar que con sigma=1 la variación entre las imágenes en mínima notando, si acaso, pequeñas variaciones en el cuello y en el hombro. En cambio cuando cambiamos sigma a 3 ya notamos cambios significativos. El hecho de cambiar los bordes no nos ha dado diferencia entre las imágenes pero sí el hecho de variar el tamaño de la máscara. Podemos ver que al aumentar dicho tamaño el blur que obtenemos es mayor juntado además con el incremento de sigma por lo que los bordes se suavizan también y obtenemos una peor detección de bordes. Esto viene del hecho de que hemos hecho demasiado suavizado y por tanto hemos perdido información en la imagen.

La detección de bordes del operador lapaciano tiene una idea intuitiva por detrás consistente en que cuando tenemos variaciones notables de color al hacer la segunda derivada vamos a obtener ceros, ya que la primera derivada tendrá un máximo.
