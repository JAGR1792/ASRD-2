import argparse
from pathlib import Path
from collections import defaultdict
from modulos_asdr import transformaciones as transf
from modulos_asdr import analisis as analisis_asdr

from ASD_Recursivo import (
    EPSILON,
    Gramatica,
    cargar_desde_texto,
    resolver_conjuntos,
    mostrar_resultados_tabla,
)


def nombre_auxiliar(nt, existentes):
    base = f"{nt}_p"
    candidato = base
    i = 1
    while candidato in existentes:
        i += 1
        candidato = f"{base}{i}"
    return candidato


def construir_gramatica(producciones, orden_nt=None, inicial=None):
    G = Gramatica()
    G.producciones = defaultdict(list)

    if orden_nt is None:
        orden_nt = list(producciones.keys())

    for nt in orden_nt:
        if nt in producciones:
            G.no_terminales.add(nt)
            for prod in producciones[nt]:
                G.producciones[nt].append(list(prod))

    if inicial is None:
        inicial = orden_nt[0]
    G.inicial = inicial

    for A in G.producciones:
        for prod in G.producciones[A]:
            for s in prod:
                if s not in G.producciones and s != EPSILON:
                    G.terminales.add(s)

    return G


def eliminar_recursion_izquierda_inmediata(G):
    return transf.eliminar_recursion_izquierda_inmediata(G, EPSILON, Gramatica)


def serializar_gramatica(G):
    return transf.serializar_gramatica(G)


def verificar_ll1(G, predicciones):
    return analisis_asdr.verificar_ll1(G.producciones, predicciones)


def generar_asdr(G, predicciones):
    return analisis_asdr.generar_asdr(
        G.no_terminales,
        G.producciones,
        predicciones,
        EPSILON,
    )


def serializar_asdr_py(nombre, G, predicciones):
    cuerpo = generar_asdr(G, predicciones)
    return analisis_asdr.serializar_asdr_py(nombre, cuerpo)


def mostrar_solucion(nombre, G, mostrar_asdr=False):
    print(f"\n=== {nombre} ===")
    primeros, siguientes, predicciones = resolver_conjuntos(G)
    mostrar_resultados_tabla(G, primeros, siguientes, predicciones)

    es_ll1, conflictos = verificar_ll1(G, predicciones)
    print("\nLL(1):", "SI" if es_ll1 else "NO")
    if not es_ll1:
        print("Conflictos detectados:")
        for A, p1, p2, inter in conflictos:
            print(
                f" - {A} -> {' '.join(p1)}  VS  {A} -> {' '.join(p2)}  | interseccion: {sorted(inter)}"
            )

    if mostrar_asdr:
        print("\nASDR (esqueleto):")
        print(generar_asdr(G, predicciones))

    return primeros, siguientes, predicciones


def cargar_gramatica_archivo(path):
    G = Gramatica()
    G.cargar(str(path))
    return G


def crear_entradas_originales(carpeta):
    carpeta.mkdir(parents=True, exist_ok=True)
    print(
        f"La carpeta {carpeta} se ha creado. Coloca aqui los archivos de entrada que quieras procesar."
    )


def procesar_directorio(input_dir, output_dir, generar_transformadas, mostrar_asdr):
    archivos = sorted(input_dir.glob("*.txt"))
    if not archivos:
        print(f"No hay archivos .txt en: {input_dir}")
        return

    if generar_transformadas:
        output_dir.mkdir(parents=True, exist_ok=True)

    for archivo in archivos:
        original = cargar_gramatica_archivo(archivo)
        nombre_base = archivo.stem

        if generar_transformadas:
            transformada = eliminar_recursion_izquierda_inmediata(original)
            destino = output_dir / archivo.name
            destino.write_text(serializar_gramatica(transformada), encoding="utf-8")
            primeros, siguientes, predicciones = mostrar_solucion(
                f"{archivo.name} (transformada)", transformada, mostrar_asdr
            )

            asdr_dir = input_dir.parent / "asdr"
            asdr_dir.mkdir(parents=True, exist_ok=True)
            asdr_file = asdr_dir / f"{nombre_base}.py"
            asdr_file.write_text(
                serializar_asdr_py(archivo.name, transformada, predicciones),
                encoding="utf-8",
            )
        else:
            mostrar_solucion(f"{archivo.name} (original)", original, mostrar_asdr)


def resolver_entrada_posicional(entrada, input_dir):
    candidata = Path(entrada)
    if candidata.exists():
        return candidata

    dentro_de_input = input_dir / entrada
    if dentro_de_input.exists():
        return dentro_de_input

    raise FileNotFoundError(
        f"No se encontro la entrada '{entrada}'. Busca en '{entrada}' o '{dentro_de_input}'."
    )


def procesar_archivo_entrada(entrada, input_dir, output_dir, generar_transformadas, mostrar_asdr):
    archivo = resolver_entrada_posicional(entrada, input_dir)
    original = cargar_gramatica_archivo(archivo)

    nombre_visible = archivo.name
    if generar_transformadas:
        output_dir.mkdir(parents=True, exist_ok=True)
        transformada = eliminar_recursion_izquierda_inmediata(original)
        destino = output_dir / archivo.name
        destino.write_text(serializar_gramatica(transformada), encoding="utf-8")
        primeros, siguientes, predicciones = mostrar_solucion(
            f"{nombre_visible} -> transformada", transformada, mostrar_asdr
        )

        asdr_dir = input_dir.parent / "asdr"
        asdr_dir.mkdir(parents=True, exist_ok=True)
        asdr_file = asdr_dir / f"{archivo.stem}.py"
        asdr_file.write_text(
            serializar_asdr_py(nombre_visible, transformada, predicciones),
            encoding="utf-8",
        )
    else:
        mostrar_solucion(f"{nombre_visible} -> original", original, mostrar_asdr)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Resuelve ejercicios ASDR importando calculos desde ASD_Recursivo y trabajando por carpetas."
        )
    )
    parser.add_argument(
        "entrada",
        nargs="?",
        help="Archivo de entrada, por ejemplo ejercicio1.txt. Si no tiene ruta, se busca en --input-dir.",
    )
    parser.add_argument(
        "--input-dir",
        default="entradas_originales",
        help="Carpeta con gramaticas originales (texto de diapositivas).",
    )
    parser.add_argument(
        "--output-dir",
        default="gramaticas_generadas",
        help="Carpeta donde guardar gramaticas transformadas.",
    )
    parser.add_argument(
        "--sin-transformar",
        action="store_true",
        help="No elimina recursion izquierda; procesa originales tal cual.",
    )
    parser.add_argument(
        "--asdr",
        action="store_true",
        help="Muestra esqueleto ASDR para cada gramatica procesada.",
    )
    parser.add_argument(
        "--crear-entradas",
        action="store_true",
        help="Crea en --input-dir las entradas base de los ejercicios de diapositivas.",
    )
    parser.add_argument(
        "--texto",
        help="Procesa una gramatica directa en texto (multilinea con A -> ...).",
    )

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if args.crear_entradas:
        crear_entradas_originales(input_dir)
        if not args.texto and not args.entrada:
            return

    if args.texto:
        G = cargar_desde_texto(args.texto)
        if args.sin_transformar:
            mostrar_solucion("Texto de entrada", G, mostrar_asdr=args.asdr)
        else:
            Gt = eliminar_recursion_izquierda_inmediata(G)
            mostrar_solucion("Texto de entrada -> transformada", Gt, mostrar_asdr=args.asdr)
        return

    if args.entrada:
        procesar_archivo_entrada(
            entrada=args.entrada,
            input_dir=input_dir,
            output_dir=output_dir,
            generar_transformadas=not args.sin_transformar,
            mostrar_asdr=args.asdr,
        )
        return

    procesar_directorio(
        input_dir=input_dir,
        output_dir=output_dir,
        generar_transformadas=not args.sin_transformar,
        mostrar_asdr=args.asdr,
    )


if __name__ == "__main__":
    main()
