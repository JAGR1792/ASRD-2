# Publico

Repositorio de apoyo para resolver ejercicios de Análisis Sintáctico Descendente (ASD) y construcción de un parser LL(1).

Este repositorio se apoya en el trabajo previo del repositorio original de ASD:

- https://github.com/JAGR1792/Tareas_LP/tree/master

La idea es separar responsabilidades:

- `ASD_Recursivo.py` conserva el núcleo de cálculo de conjuntos y la impresión de resultados.
- `ASDR_Ejercicios.py` orquesta el flujo nuevo: carga entradas, elimina recursión por izquierda inmediata, genera gramáticas transformadas y reutiliza el cálculo del script anterior mediante `import`.

## Algoritmo

Para construir un parser LL(1) normalmente se siguen estos pasos:

1. Eliminar la recursión por izquierda.
2. Factorizar por la izquierda.
3. Construir el conjunto de PRIMEROS.
4. Construir el conjunto de SIGUIENTES.
5. Construir la tabla de parsing.

En este trabajo hay dos partes distintas:

- Lo que ya venía resuelto en la tarea anterior o en el repo previo: PRIMEROS, SIGUIENTES y la lógica asociada a predicción/tabla.
- Lo nuevo de este repositorio: el flujo de entrada por carpetas, la eliminación de recursión por izquierda inmediata, la reutilización por `import` entre scripts y la documentación del proceso.

Importante:

- La factorización por la izquierda no está automatizada aquí.
- Si la gramática aún tiene ambigüedades, el script las reporta al calcular conflictos LL(1).

## Cómo se comunican los scripts

La comunicación entre ambos archivos es directa, por importación:

- `ASDR_Ejercicios.py` importa desde `ASD_Recursivo.py`:
	- `EPSILON`
	- `Gramatica`
	- `cargar_desde_texto`
	- `resolver_conjuntos`
	- `mostrar_resultados_tabla`

Eso permite no repetir lógica ya construida en la entrega anterior.

El flujo es este:

1. `ASDR_Ejercicios.py` recibe una entrada como `ejercicio1.txt`.
2. Si no se entrega ruta completa, busca ese archivo dentro de `entradas_originales/`.
3. Si corresponde, elimina recursión por izquierda inmediata.
4. Guarda la gramática transformada en `gramaticas_generadas/`.
5. Llama a `ASD_Recursivo.py` como módulo para calcular PRIMEROS, SIGUIENTES y PREDICCIÓN.
6. Muestra si la gramática es LL(1) y genera un esqueleto ASDR.

## Estructura del proyecto

- `ASD_Recursivo.py`: script base del repo anterior. Calcula PRIMEROS, SIGUIENTES y PREDICCIÓN.
- `ASDR_Ejercicios.py`: script nuevo que organiza el flujo de ejercicios y reutiliza el script anterior.
- `ejercicioN.txt`: forma usual de invocar cada entrada.
- `entradas_originales/`: gramáticas originales tomadas de las diapositivas.
- `gramaticas_generadas/`: gramáticas después de eliminar recursión por izquierda inmediata.
- `asdr/`: archivos Python con el ASDR de cada ejercicio.
- `RESULTADOS_EJERCICIOS.md`: resumen del flujo y de los resultados.

## Cómo ejecutar

### 1. Procesar un ejercicio directamente

```bash
python3 ASDR_Ejercicios.py ejercicio1.txt
```

Si no das una ruta completa, el script busca el archivo dentro de `entradas_originales/`.

### 2. Crear las entradas originales

```bash
python3 ASDR_Ejercicios.py --crear-entradas
```

Esto solo crea la carpeta `entradas_originales/` como punto de organización. Los archivos de entrada los pone el usuario.

### 3. Procesar una entrada y generar su versión transformada

```bash
python3 ASDR_Ejercicios.py ejercicio1.txt --asdr
```

Con ese comando:

- se toma el archivo indicado como entrada;
- si hace falta, se busca dentro de `entradas_originales/`;
- se eliminan las recursiones por izquierda inmediatas;
- se genera la versión transformada en `gramaticas_generadas/`;
- se deja un archivo Python con el ASDR en `asdr/`;
- se calculan PRIMEROS, SIGUIENTES y PREDICCIÓN usando `ASD_Recursivo.py`;
- se muestra la validación LL(1);
- se imprime el esqueleto ASDR.

### 4. Procesar solo la gramática original

```bash
python3 ASDR_Ejercicios.py ejercicio1.txt --sin-transformar --asdr
```

Esto toma la gramática original y calcula los conjuntos sin generar una versión transformada.

### 5. Procesar una gramática escrita como texto

```bash
python3 ASDR_Ejercicios.py --texto """
S -> A B C
A -> a
B -> b
C -> c
""" --asdr
```

Útil si quieres probar una gramática pequeña sin crear un archivo.

## Qué hace cada paso

### 1. Eliminar recursión por izquierda

Se usa para evitar bucles infinitos en un parser descendente.

En este proyecto se elimina la recursión por izquierda inmediata. Si la gramática requiere factorización por la izquierda, esa parte debe revisarse aparte.

### 2. Factorizar por la izquierda

Es el paso que normalmente sigue, pero no se automatiza en este repositorio.

Se deja indicado en la documentación porque forma parte del algoritmo LL(1) completo.

### 3. PRIMEROS

El script calcula qué terminales pueden aparecer al inicio de las cadenas derivadas por cada no terminal.

### 4. SIGUIENTES

El script calcula qué terminales pueden aparecer inmediatamente después de cada no terminal en una derivación válida.

### 5. Tabla de predicción

Con PRIMEROS y SIGUIENTES se construye el conjunto de predicción de cada producción y se revisa si hay conflictos.

## Resultados esperados

El script imprime:

- PRIMEROS por no terminal
- SIGUIENTES por no terminal
- PREDICCIÓN por regla
- Verificación LL(1)
- Esqueleto ASDR

## Guias de apoyo

- docs/01_objetivo.md
- docs/02_estructura.md
- docs/03_comandos.md
- docs/04_flujo.md
- docs/05_ll1.md
- docs/06_asdr.md
- docs/07_errores_comunes.md
- docs/08_versionado.md
- docs/09_entrega.md
- docs/10_verificacion.md

## Nota sobre la entrega

Este repositorio no reemplaza el trabajo anterior: lo complementa.

La lógica central de conjuntos ya existía en el repositorio base, y aquí se agrega la capa de orden, ejecución por carpetas, transformación de gramáticas y documentación del proceso.

En otras palabras, el archivo no trae embebidas las gramáticas como parte del analizador. El usuario decide la entrada al invocar el script, y el repositorio solo organiza, transforma y resuelve esa entrada.

Además, cuando se pide la versión transformada, el proyecto deja también un archivo `.py` por ejercicio en `asdr/`, para que el ASDR quede separado y listo para revisarse o adaptarse por ejercicio.
