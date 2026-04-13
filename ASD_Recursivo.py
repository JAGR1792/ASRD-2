import sys
import argparse
from collections import defaultdict

EPSILON = 'ε'
FIN = '$'

# =======================
# CLASE GRAMATICA
# =======================

class Gramatica:
    def __init__(self):
        self.producciones = defaultdict(list)
        self.no_terminales = set()
        self.terminales = set()
        self.inicial = None

    def cargar(self, archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                if not linea or linea.startswith('#'):
                    continue

                izquierda, derecha = linea.split("->")
                izquierda = izquierda.strip()

                if self.inicial is None:
                    self.inicial = izquierda

                self.no_terminales.add(izquierda)

                alternativas = derecha.split("|")
                for alt in alternativas:
                    simbolos = alt.strip().split()
                    self.producciones[izquierda].append(simbolos)

        # detectar terminales
        for A in self.producciones:
            for prod in self.producciones[A]:
                for s in prod:
                    if s not in self.producciones and s != EPSILON:
                        self.terminales.add(s)


def cargar_desde_texto(contenido):
    G = Gramatica()

    for linea in contenido.strip().splitlines():
        linea = linea.strip()
        if not linea or linea.startswith('#'):
            continue

        izquierda, derecha = linea.split("->")
        izquierda = izquierda.strip()

        if G.inicial is None:
            G.inicial = izquierda

        G.no_terminales.add(izquierda)

        alternativas = derecha.split("|")
        for alt in alternativas:
            simbolos = alt.strip().split()
            G.producciones[izquierda].append(simbolos)

    for A in G.producciones:
        for prod in G.producciones[A]:
            for s in prod:
                if s not in G.producciones and s != EPSILON:
                    G.terminales.add(s)

    return G


# =======================
# PRIMEROS
# =======================

def calcular_primeros(G):
    PRIMEROS = defaultdict(set) # si encontramos que por ejemplo A no existe lo crea
    

    # Paso 1: FIRST(a) = {a} si a es terminal
    for t in G.terminales:
        PRIMEROS[t].add(t)

    # Paso 2: FIRST(ε) = {ε}
    PRIMEROS[EPSILON].add(EPSILON)

    # Paso 3: inicializar FIRST de no terminales vacío
    for nt in G.no_terminales:
        PRIMEROS[nt] = set()

    # Paso 4: aplicar reglas hasta que no haya cambios
    cambio = True
    while cambio:
        cambio = False

        for A in G.producciones:
            for prod in G.producciones[A]:

                antes = len(PRIMEROS[A])

                # Paso 5: si A -> ε
                if prod == [EPSILON]:
                    PRIMEROS[A].add(EPSILON)

                else:
                    # Paso 6: recorrer símbolos de la producción
                    for X in prod:
                        # agregar FIRST(X) sin ε
                        PRIMEROS[A] |= (PRIMEROS[X] - {EPSILON})

                        # Paso 7: si X no produce ε, detener
                        if EPSILON not in PRIMEROS[X]:
                            break
                    else:
                        # Paso 8: si todos producen ε
                        PRIMEROS[A].add(EPSILON)

                if len(PRIMEROS[A]) > antes:
                    cambio = True

    return PRIMEROS


# =======================
# FUNCION AUXILIAR
# =======================

def primeros_secuencia(seq, PRIMEROS):
    resultado = set()

    for X in seq:
        resultado |= (PRIMEROS[X] - {EPSILON})
        if EPSILON not in PRIMEROS[X]:
            return resultado

    resultado.add(EPSILON)
    return resultado


# =======================
# SIGUIENTES
# =======================

def calcular_siguientes(G, PRIMEROS):
    SIGUIENTES = defaultdict(set)

    # Paso 1: FOLLOW(S) incluye $
    SIGUIENTES[G.inicial].add(FIN)

    # Paso 2: inicializar demás
    for nt in G.no_terminales:
        if nt != G.inicial:
            SIGUIENTES[nt] = set()

    # Paso 3: iterar hasta estabilizar
    cambio = True
    while cambio:
        cambio = False

        for A in G.producciones:
            for prod in G.producciones[A]:

                for i, B in enumerate(prod):

                    if B in G.no_terminales:

                        antes = len(SIGUIENTES[B])

                        beta = prod[i+1:]

                        # Paso 4: FIRST(beta) sin ε
                        if beta:
                            first_beta = primeros_secuencia(beta, PRIMEROS)
                            SIGUIENTES[B] |= (first_beta - {EPSILON})

                            # Paso 5: si beta produce ε
                            if EPSILON in first_beta:
                                SIGUIENTES[B] |= SIGUIENTES[A]
                        else:
                            # Paso 6: si B está al final
                            SIGUIENTES[B] |= SIGUIENTES[A]

                        if len(SIGUIENTES[B]) > antes:
                            cambio = True

    return SIGUIENTES


# =======================
# PREDICCION
# =======================

def calcular_prediccion(G, PRIMEROS, SIGUIENTES):
    PREDICCION = dict()

    for A in G.producciones:
        for prod in G.producciones[A]:

            # Paso 1: calcular FIRST(α)
            first_alpha = primeros_secuencia(prod, PRIMEROS)

            # Paso 2: agregar FIRST sin ε
            conjunto = set(first_alpha - {EPSILON})

            # Paso 3: si ε ∈ FIRST(α)
            if EPSILON in first_alpha:
                conjunto |= SIGUIENTES[A]

            PREDICCION[(A, tuple(prod))] = conjunto

    return PREDICCION


# =======================
# IMPRESION
# =======================

def imprimir_tabla_ascii(headers, filas):
    def linea(relleno='-'):
        return "+" + "+".join(relleno * (ancho + 2) for ancho in anchos) + "+"

    anchos = []
    for i, header in enumerate(headers):
        max_col = len(str(header))
        for fila in filas:
            max_col = max(max_col, len(str(fila[i])))
        anchos.append(max_col)

    separador = linea('-')
    separador_encabezado = linea('=')

    print(separador)
    print("| " + " | ".join(str(headers[i]).ljust(anchos[i]) for i in range(len(headers))) + " |")
    print(separador_encabezado)

    for fila in filas:
        print("| " + " | ".join(str(fila[i]).ljust(anchos[i]) for i in range(len(headers))) + " |")

    print(separador)

# =======================
# FUNCION AUXILIAR
# =======================

def mostrar_resultados_tabla(G, primeros, siguientes, predicciones):
    """
    Muestra los resultados de PRIMEROS, SIGUIENTES y PREDICCIONES en formato de tabla.
    :param primeros: Diccionario con los conjuntos PRIMEROS.
    :param siguientes: Diccionario con los conjuntos SIGUIENTES.
    :param predicciones: Lista de reglas con sus predicciones.
    """
    # Mostrar PRIMEROS (solo no terminales)
    print("\nPRIMEROS:")
    tabla_primeros = [
        [nt, ", ".join(sorted(primeros[nt]))]
        for nt in sorted(G.no_terminales)
    ]
    imprimir_tabla_ascii(["No Terminal", "PRIMEROS"], tabla_primeros)

    # Mostrar SIGUIENTES (solo no terminales)
    print("\nSIGUIENTES:")
    tabla_siguientes = [
        [nt, ", ".join(sorted(siguientes[nt]))]
        for nt in sorted(G.no_terminales)
    ]
    imprimir_tabla_ascii(["No Terminal", "SIGUIENTES"], tabla_siguientes)

    # Mostrar PREDICCIONES
    print("\nPREDICCION:")
    tabla_predicciones = [
        [f"{A} -> {' '.join(prod)}", ", ".join(sorted(conjunto))]
        for (A, prod), conjunto in predicciones.items()
    ]
    imprimir_tabla_ascii(["Regla", "PREDICCION"], tabla_predicciones)


def resolver_conjuntos(G):
    primeros = calcular_primeros(G)
    siguientes = calcular_siguientes(G, primeros)
    prediccion = calcular_prediccion(G, primeros, siguientes)
    return primeros, siguientes, prediccion

# =======================
# MAIN
# =======================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calcula PRIMEROS, SIGUIENTES y PREDICCION de una o varias gramaticas."
    )
    parser.add_argument(
        "archivos",
        nargs="+",
        help="Uno o mas archivos de entrada con producciones de la gramatica.",
    )

    # Mantiene el comportamiento de mensaje historico cuando no se envia ningun archivo.
    if len(sys.argv) == 1:
        print("Uso: python nombre.py archivo.txt")
        print("FALTA <<archivo.txt>>")
        sys.exit(1)

    args = parser.parse_args()

    for i, archivo in enumerate(args.archivos, start=1):
        if len(args.archivos) > 1:
            print(f"\n=== Archivo {i}: {archivo} ===")

        G = Gramatica()
        G.cargar(archivo)

        PRIMEROS, SIGUIENTES, PREDICCION = resolver_conjuntos(G)

        mostrar_resultados_tabla(G, PRIMEROS, SIGUIENTES, PREDICCION)
