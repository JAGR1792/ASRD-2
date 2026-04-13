# ASDR de este ejercicio
# Archivo: ejercicio1.txt

token = None

def match(esperado):
    # TO DO probablemente en una futura tarea
    raise NotImplementedError('Implementa match() segun tu lexer/token stream')

def error(mensaje):
    raise SyntaxError(mensaje)

def A():
    global token
    if token == 'dos':
        match('dos')
        B()
        match('tres')
    elif token == '$' or token == 'cinco' or token == 'cuatro' or token == 'seis' or token == 'tres':
        pass
    else:
        error('Token inesperado en A')

def B():
    global token
    if token == '$' or token == 'cinco' or token == 'cuatro' or token == 'seis' or token == 'tres':
        B_p()
    else:
        error('Token inesperado en B')

def B_p():
    global token
    if token == 'cuatro':
        match('cuatro')
        C()
        match('cinco')
        B_p()
    elif token == '$' or token == 'cinco' or token == 'seis' or token == 'tres':
        pass
    else:
        error('Token inesperado en B_p')

def C():
    global token
    if token == 'seis':
        match('seis')
        A()
        B()
    elif token == '$' or token == 'cinco':
        pass
    else:
        error('Token inesperado en C')

def D():
    global token
    if token == 'uno':
        match('uno')
        A()
        E()
    elif token == 'cuatro' or token == 'tres':
        B()
    else:
        error('Token inesperado en D')

def E():
    global token
    if token == 'tres':
        match('tres')
    else:
        error('Token inesperado en E')

def S():
    global token
    if token == '$' or token == 'cuatro' or token == 'dos' or token == 'seis':
        A()
        B()
        C()
    elif token == 'cuatro' or token == 'tres' or token == 'uno':
        D()
        E()
    else:
        error('Token inesperado en S')

