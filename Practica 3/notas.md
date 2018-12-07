Hay que usar la función clickAndDraw que empieza con click izquierdo, los
puntos se ponen con click derecho y el último con doble izquierdo.

Hay que hacer una máscara con 0s fuera de la región y 1s dentro, para eso
usar fillConvexPoly.

Comentar destroyAllWindows() y usar extractRegion.

Usar la función kmeans de opencv.

En el ejercicio 2 para cada imagen buscamos la bolsa de palabras: sacamos los
descriptores con SIFT, SURF lo que sea (si tarda mucho baja el numero de
imagenes a menos de las 400 que vienen), para cada descriptor nos vamos por
la distancia euclídea al centroide más cercano guardando el índice del
centroide, con esta información de los centroides hacemos un histograma y ya
tendríamos la bolsa de palabras para esa imagen.

El índice invertido guardamos para cada centroide la imagen en la que ha salido
como más cercano.
