# ASDR de este ejercicio
# Archivo: ejercicio3.txt

token = None

def match(esperado):
    raise NotImplementedError('Implementa match() segun tu lexer/token stream')

def error(mensaje):
    raise SyntaxError(mensaje)

def A():
    global token
    if token == 'dos':
        match('dos')
        B()
        C()
    elif token == '$' or token == 'cuatro' or token == 'tres' or token == 'uno':
        pass
    else:
        error('Token inesperado en A')

def B():
    global token
    if token == 'cuatro' or token == 'tres':
        C()
        match('tres')
    elif token == '$' or token == 'cuatro' or token == 'tres' or token == 'uno':
        pass
    else:
        error('Token inesperado en B')

def C():
    global token
    if token == 'cuatro':
        match('cuatro')
        B()
    elif token == '$' or token == 'cuatro' or token == 'tres' or token == 'uno':
        pass
    else:
        error('Token inesperado en C')

def S():
    global token
    if token == '$' or token == 'cuatro' or token == 'dos' or token == 'tres' or token == 'uno':
        A()
        B()
        C()
        S_p()
    else:
        error('Token inesperado en S')

def S_p():
    global token
    if token == 'uno':
        match('uno')
        S_p()
    elif token == '$':
        pass
    else:
        error('Token inesperado en S_p')

