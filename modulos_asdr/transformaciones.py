from collections import defaultdict


def nombre_auxiliar(nt, existentes):
    base = f"{nt}_p"
    candidato = base
    i = 1
    while candidato in existentes:
        i += 1
        candidato = f"{base}{i}"
    return candidato


def construir_gramatica(producciones, gramatica_cls, epsilon, orden_nt=None, inicial=None):
    G = gramatica_cls()
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
                if s not in G.producciones and s != epsilon:
                    G.terminales.add(s)

    return G


def eliminar_recursion_izquierda_inmediata(G, epsilon, gramatica_cls):
    nuevas = defaultdict(list)
    orden = []
    existentes = set(G.no_terminales)

    for A in G.producciones:
        orden.append(A)
        alfas = []
        betas = []

        for prod in G.producciones[A]:
            if prod and prod[0] == A:
                alfas.append(prod[1:])
            else:
                betas.append(prod)

        if not alfas:
            nuevas[A].extend(betas)
            continue

        Ap = nombre_auxiliar(A, existentes)
        existentes.add(Ap)
        orden.append(Ap)

        for beta in betas:
            if beta == [epsilon]:
                nuevas[A].append([Ap])
            else:
                nuevas[A].append(beta + [Ap])

        for alfa in alfas:
            nuevas[Ap].append(alfa + [Ap])
        nuevas[Ap].append([epsilon])

    return construir_gramatica(nuevas, gramatica_cls, epsilon, orden_nt=orden, inicial=G.inicial)


def serializar_gramatica(G):
    lineas = []
    for A in G.producciones:
        for prod in G.producciones[A]:
            lineas.append(f"{A} -> {' '.join(prod)}")
    return "\n".join(lineas) + "\n"
