Especificar que funciones se corresponden a que apartados en la memoria.

- En los bonus se pueden usar funciones OpenCV.

# Bonus 1
- Para obtener los autovectores usar cv2.cornerEigenValsAndVecs() autovectores $\lambda_1$, $\lambda_2$
- $f_{HH}=\frac{\lambda_1 \lambda_2}{\lambda_1+\lambda_2}$
- Con esto construyes una matriz, te vas a un vecindario de 3x3 y coges el maximo local, lo mantienes si es mayor que 10 si no lo quitas si es mayor que 10 te quedas con el maximo y no con el vecindario.
- Para una cuadratica cv2.cornerSubPix() primer refinamiento.
- Esto se hace para cada nivel de la pirámide gaussiana (para 3 niveles va guay).
- Después buscamos el máximo global, tomamos  la máxima distancia euclídea entre ese punto y otro de la matriz. (Te vale con coger la máxima distancia euclídea posible).
- Vas bajando la distancia hasta que te encuentres un punto (d1=d0-1). Cuando te encuentres un punto coges una bola y miras si el punto que has visto es maximo local en esa bola centrada en el punto, si lo es lo metes en una lista. Tienes que coger los que se quedan fuera de la bola.

# Bonus 2
- Hay que sacar para cada punto el theta (orientación) y el nivel de la pirámide Gaussiana para toda la lista de puntos de interés.
- Para calcular los descriptores hay que bajar niveles en la pirámide gaussiana hasta que el vecindario de 40x40 de ese píxel sea 8x8 el pixel no está en el centro entonces ponlo como veas. Hay que hacerlo con imagenes grandes porque 40 es grande xdxdxdxd
- Tomamos la región de 8x8, normalizas para que tenga media 0 y varianza 1.
- Aplicamos una transformacion tochisima pyWavelet y aplicas la transformada de Haar. Nos quedamos con los tres primeros coeficientes no nulos, esto es el descriptor.

# Bonus 3
- Empieza con los matches ya calculados por SIFT o SURF.
- Tomas 4 matches aleatorios (lo minimo para tener una homografía) y la haces.
- Hay que usar coordenadas homogéneas (x,y)->(x,y,1).
- Haces H(x,y,1) = (x\*,y\*,w) y lo pasas a (x\*/w,y\*/w). Si a la correspondencia de (x,y) el punto calculado dista menos (o igual) de 3 pixeles entonces es un inliner (aumentas el contador) en caso contrario es outliner (aumentas el contador) (excluyendo los 4 probar en todos los matches)
- Vuelves a tomar 4 matches aleatorios y repites. Haces esto hasta que te quedes con el conjunto de inliners mas grande y con ellos calculas la homografía final.
- Hay que repetir esto el numero de veces que dice la tabla de las diapos.
