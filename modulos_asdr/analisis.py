def verificar_ll1(producciones, predicciones):
    conflictos = []
    for A in sorted(producciones):
        prods = [tuple(p) for p in producciones[A]]
        for i in range(len(prods)):
            for j in range(i + 1, len(prods)):
                p1 = prods[i]
                p2 = prods[j]
                inter = predicciones[(A, p1)] & predicciones[(A, p2)]
                if inter:
                    conflictos.append((A, p1, p2, inter))
    return len(conflictos) == 0, conflictos


def generar_asdr(no_terminales, producciones, predicciones, epsilon):
    lineas = []

    for nt in sorted(no_terminales):
        lineas.append(f"def {nt}():")
        lineas.append("    global token")

        ramas = []
        for prod in producciones[nt]:
            pred = sorted(predicciones[(nt, tuple(prod))])
            if not pred:
                continue

            condicion = " or ".join([f"token == '{t}'" for t in pred])
            cuerpo = []

            if prod == [epsilon]:
                cuerpo.append("pass")
            else:
                for s in prod:
                    if s in no_terminales:
                        cuerpo.append(f"{s}()")
                    elif s != epsilon:
                        cuerpo.append(f"match('{s}')")

            ramas.append((condicion, cuerpo))

        if not ramas:
            lineas.append("    error('No hay producciones para este no terminal')")
            lineas.append("")
            continue

        for i, (condicion, cuerpo) in enumerate(ramas):
            prefijo = "if" if i == 0 else "elif"
            lineas.append(f"    {prefijo} {condicion}:")
            for stmt in cuerpo:
                lineas.append(f"        {stmt}")

        lineas.append("    else:")
        lineas.append(f"        error('Token inesperado en {nt}')")
        lineas.append("")

    return "\n".join(lineas)


def serializar_asdr_py(nombre, cuerpo_asdr):
    return (
        "# ASDR de este ejercicio\n"
        f"# Archivo: {nombre}\n\n"
        "token = None\n\n"
        "def match(esperado):\n"
        "    raise NotImplementedError('Implementa match() segun tu lexer/token stream')\n\n"
        "def error(mensaje):\n"
        "    raise SyntaxError(mensaje)\n\n"
        f"{cuerpo_asdr}\n"
    )
