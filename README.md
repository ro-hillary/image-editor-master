## Aplicación para edición de fotos usando OpenCv
Esta aplicación esta fue desarrollada en Python (3.10.0 y 3.11.0) utilizando las librerías CustomTkinter y OpenCv.
La aplicación permite cargar imágenes desde una ruta seleccionada, guardar la imágen modificada,
modificar el brillo y contraste, llevarla a escala de grises y negativo, cambiar el tamaño, rotarla,
trasladarla y voltearla en todas las direcciónes, a su vez tambíen es posible realizar operaciones 
aritméticas y lógicas como son la suma, resta, and y or.

## Requerimientos
Para utilizar esta aplicación, es necesario tener instaladas las siguientes librerias de Python:
-Tkinter
-CustomTkinter
-OpenCv(cv2)
-Numpy
-PIL

## Funcionamiento
La aplicación se ejecuta desde el archivo "main.py". Al abrir la aplicación se muestra una 
ventana con un menú de opciones de las cuales solo estarán habilidatos los botones "Open" y "Quit".
Una vez abierta una imágen se activarán el resto de botones y se podrá comenzar a editar la imágen.

-Open: Permite seleccionar la ruta desde donde se cargará la imágen
-Undo: Revierte la última acción realizada
-Revert: Revierte todos los cambios realizados en la imágen
-Save: Guarda la imágen en la ruta que se especifique

-Flip: Voltea la imágen en dirección vertical y horizontal
-Brightness: Aumenta o disminuye el brillo de la imagen
-Contrast: Aumenta o disminuye el contraste de la imagen

-Grayscale: Lleva la imagen a escala de grises
-Negative: Invierte los colores de la imagen

-Rotate: Rota la imágen hacia derecha o izquierda
-Move: Traslada la imágen hacia arriba, abajo, derecha e izquierda
-Resize: Aumenta o disminuye el ancho y largo de la imágen

-Arithmetics operations: Suma o resta una imágen seleccionada a la imágen abierta en ese momento
-Logic operations: Realiza un AND o un OR a la imágen abierta en ese momento con una imágen seleccionada

## Limitaciones
-PIL: esta librería no es compatible con imágenes de alta calidad y puede tener problemas de rendimiento
con imágenes muy grandes
-OpenCv: esta librería no es compatible con imágenes de formatos antiguos o poco comunes,no es compatible 
con imágenes png de tipo "indexed color" o "grayscale with aplha channel", no es compatible con imágenes
de formato GIF.
