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

![GaussianBlur](./Imagenes/1A.png)

Podemos observar que el efecto se hace más visible de izquierda a derecha. Si nos fijamos en la imagen podemos ver que al hacer más grande el tamaño del núcleo podemos percibir de forma más nítida los rectángulos o cuadrados en la imagen. Además se observa que al aumentar los valores de la sigma el suavizado se hace más visible.
