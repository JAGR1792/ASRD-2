# ASDR de este ejercicio
# Archivo: ejercicio2.txt

token = None

def match(esperado):
    # TO DO probablemente en una futura tarea
    raise NotImplementedError('Implementa match() segun tu lexer/token stream')

def error(mensaje):
    raise SyntaxError(mensaje)

def A():
    global token
    if token == 'cinco' or token == 'cuatro' or token == 'dos' or token == 'tres' or token == 'uno':
        S()
        match('tres')
        B()
        C()
    elif token == 'cuatro':
        match('cuatro')
    elif token == 'cinco':
        pass
    else:
        error('Token inesperado en A')

def B():
    global token
    if token == 'cinco' or token == 'cuatro' or token == 'dos' or token == 'tres' or token == 'uno':
        A()
        match('cinco')
        C()
        match('seis')
    elif token == '$' or token == 'cinco' or token == 'seis' or token == 'siete' or token == 'tres' or token == 'uno':
        pass
    else:
        error('Token inesperado en B')

def C():
    global token
    if token == 'siete':
        match('siete')
        B()
    elif token == '$' or token == 'cinco' or token == 'seis' or token == 'tres':
        pass
    else:
        error('Token inesperado en C')

def S():
    global token
    if token == 'cinco' or token == 'cuatro' or token == 'dos' or token == 'tres' or token == 'uno':
        B()
        match('uno')
    elif token == 'dos':
        match('dos')
        C()
    elif token == '$' or token == 'tres':
        pass
    else:
        error('Token inesperado en S')

