---
title: Práctica 3
author: "Ignacio Aguilera Martos"
date: VC
lang: es
toc: true
toc-depth: 1
fontsize: 12pt
header-includes:
   - \usepackage{subcaption}
   - \usepackage{graphicx}
geometry: margin=1in
---

# \huge{Práctica 3}
# Ignacio Aguilera Martos
# Visión por Computador

## Ejercicio 1
Emparejamiento de descriptores.
- Mirar las imágenes en imagenesIR.rar y elegir parejas de imágenes que tengan partes de escena comunes. Haciendo uso de una máscara binaria o de las funciones extractRegion() y clickAndDraw(), seleccionar una región en la primera imagen que esté presente en la segunda imagen. Para ello sólo hay que fijar los vértices de un polígono que contenga a la región.
- Extraiga los puntos SIFT contenidos en la región seleccionada de la primera imagen y calcule las correspondencias con todos los puntos SIFT de la segunda imagen (ayuda: use el concepto de máscara con el parámetro mask)
- Pinte las correspondencias encontradas sobre las imágenes.
- Jugar con distintas parejas de imágenes, valorar las correspondencias correctas obtenidas y extraer conclusiones respecto a la utilidad de esta aproximación de recuperación de regiones/objetos de interés a partir de descriptores de una región.

**\underline{Solución:}**
Las parejas que he escogido han sido dos para ejemplificar el buen comportamiento cuando las imágenes son similares entre sí y otra en la que el reconocimiento no es tan bueno.

Las parejas escogidas son:

\begin{figure}[!h]
    \begin{subfigure}{0.45\textwidth}
      \includegraphics[scale=0.33]{./Imagenes/1.png}
    \end{subfigure}
    \begin{subfigure}{0.45\textwidth}
      \includegraphics[scale=0.33]{./Imagenes/4.png}
    \end{subfigure}
    \caption{Imágenes 1 y 4}
\end{figure}

\begin{figure}[!h]
    \begin{subfigure}{0.45\textwidth}
      \includegraphics[scale=0.33]{./Imagenes/23.png}
    \end{subfigure}
    \begin{subfigure}{0.45\textwidth}
      \includegraphics[scale=0.33]{./Imagenes/24.png}
    \end{subfigure}
    \caption{Imágenes 23 y 24}
\end{figure}

\begin{figure}[!h]
    \begin{subfigure}{0.45\textwidth}
      \includegraphics[scale=0.33]{./Imagenes/91.png}
    \end{subfigure}
    \begin{subfigure}{0.45\textwidth}
      \includegraphics[scale=0.33]{./Imagenes/92.png}
    \end{subfigure}
    \caption{Imágenes 91 y 92}
\end{figure}

La forma de proceder es, mostrar la imagen para que se pueda seleccionar la región de la misma que se desee. Esta región es diferenciada del resto mediante una máscara. La construcción de dicha máscara se hace tomando los puntos que determinan el polígono de la región y, mediante la función fillConvexPoly se rellena esta área a blanco, esto es $(255,255,255)$. Tras esto sólo tenemos que crear una matriz de ceros del mismo tamaño que la imagen y, en dichos puntos poner el valor 1. Con esto tendríamos una máscara que podemos aplicar a la función detectAndCompute para hallar los keypoints y descriptores.
