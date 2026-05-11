# Parcial_3_Estructuras_Algortimos_Sp
Detección de objetos en imágenes binarias usando BFS en Python. Representación ASCII en consola, estadísticas de objetos y exportación de reportes.

# Detección de Objetos en Imágenes Binarias

## Descripción

Este programa lee una imagen binaria desde un archivo de texto, donde:
- `0` representa un píxel negro
- `1` representa un píxel blanco

A partir de esa matriz, el programa:

- Determina si la imagen tiene marco
- Cuenta cuántos objetos hay en la imagen
- Muestra una visualización de la imagen en consola
- Etiqueta los objetos encontrados
- Calcula estadísticas básicas de cada objeto
- Puede exportar un reporte en archivo `.txt`

La detección de objetos se realiza usando BFS (Breadth-First Search) con conectividad de 4 vecinos: arriba, abajo, izquierda y derecha.

## Representación en consola

El programa muestra la imagen en consola usando caracteres ASCII para una lectura visual rápida:

- `█` = Blanco (1)
- `░` = Negro (0)

Ejemplo de salida en consola:

```text
     0 1 2 3 4 5 6 7 8 9
   ─────────────────────
 0 | ░ ░ ░ ░ ░ ░ ░ ░ ░ ░
 1 | ░ █ █ ░ ░ ░ ░ █ ░ ░
 2 | ░ █ █ █ █ ░ ░ █ ░ ░
 3 | ░ █ █ █ ░ ░ ░ █ ░ ░
 4 | ░ ░ █ █ ░ ░ █ █ ░ ░
 5 | ░ ░ ░ ░ ░ ░ ░ █ ░ ░
 6 | ░ ░ ░ ░ ░ ░ ░ ░ ░ ░
 7 | ░ ░ ░ █ █ █ █ █ ░ ░
 8 | ░ ░ ░ ░ █ █ █ █ ░ ░
 9 | ░ ░ ░ ░ ░ █ ░ ░ ░ ░
```

## Estructura usada

La imagen se almacena en una matriz bidimensional de enteros, representada en Python como una lista de listas.

Ejemplo:

```python
[
    ,
   ,[1]
   ,[1]
    
]
```

## Funcionalidades

- Lectura de imagen desde archivo `.txt`
- Validación del formato del archivo
- Detección de marco en la imagen
- Conteo de objetos conectados
- Visualización de la matriz en consola (ASCII)
- Etiquetado de objetos encontrados
- Estadísticas por objeto
- Exportación de reporte

## Formato del archivo de entrada

El archivo debe ser un `.txt` con una matriz de ceros y unos separados por espacios.

Ejemplo:

```txt
0 0 0 0 0
0 1 1 0 0
0 1 0 0 0
0 0 0 1 0
0 0 0 0 0
```

## Cómo ejecutar el programa

### Desde Python

```bash
python deteccion_objetos.py
```

### Desde el ejecutable `.exe`

Ejecuta el archivo generado con PyInstaller y sigue las instrucciones que aparecen en consola.

## Opciones del menú

- `1` Procesar imagen desde archivo
- `2` Crear imagen de prueba
- `0` Salir

## Salida del programa

El programa muestra:

- Dimensiones de la imagen
- Visualización de la matriz (█ blanco, ░ negro)
- Si la imagen tiene o no marco
- Número de objetos detectados
- Mapa de objetos etiquetados
- Estadísticas de cada objeto
- Resumen final

Si el usuario lo desea, también puede exportar un reporte en formato `.txt`.

## Algoritmo utilizado

Se recorre toda la matriz.  
Cuando se encuentra un píxel con valor `1` que no ha sido visitado, se inicia un recorrido BFS para visitar todos los píxeles conectados a ese objeto.  
Cada recorrido BFS identifica exactamente un objeto.

## Complejidad

- Tiempo: `O(M × N)`
- Espacio: `O(M × N)`

Donde:
- `M` es el número de filas
- `N` es el número de columnas
