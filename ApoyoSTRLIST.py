import re

'''
     # * Paquete de Funciones de apoyo para el trabajo de Strings y Manejo de Grupos para programa Descarte
'''
letras_array = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
num_array = ['1','2','3','4','5','6','7','8','9','0']


def checarLetras(STR):
    '''
        Funcion para contrar letras de un string
    '''
    C_letras = len(re.findall('[ABCDEFGHIJKLMNOPQRSTUVWXYZ]',STR))
    return C_letras != 0


def buscarEspacioPunto(STR):
    '''
        Funcion para buscar el separador de pipe " ."
        Recibe un string y regresa la posicion de " ."
    '''
    pos = 0
    if ' .' in STR: pos = STR.index(' .')
    return pos


def buscarEspacio(STR):
    '''
        Funcion para buscar el separador de pipe " "
        Recibe un string y regresa la posicion de " "
        Funcion especial para casos sin " ." separador
    '''
    pos = 0
    if ' ' in STR: pos = STR.index(' ')
    return pos


def buscarPuntoEspacio(STR):
    '''
        Funcion para buscar el separador de pipe ". "
        Recibe un string y regresa la posicion de ". "
    '''
    pos = 0
    if '. ' in STR: pos = STR.index('. ')
    return pos


def buscarPIPE(STR):
    '''
        Funcion para revisar separadores de PIPES
    '''
    pos = 0
    pos = buscarEspacioPunto(STR)
    if pos != 0: return pos, 2
    pos = buscarPuntoEspacio(STR)
    if pos != 0: return pos, 2
    pos = buscarEspacio(STR)
    if pos != 0: return pos, 1
    return pos, 0


def contarSeparadores(STR):
    """  
        Funcion principal para detecar los separadores en una cadena
        Toma en cuenta los doble espacios, espacio+punto y punto+espacio
        @STR:  Cadena que se utiliza en este metodo
        @return: Cantidad de separadores
    """
    sep_cont = len(re.findall('[. ,]', STR))
    length = len(STR)
    if sep_cont != 0:
        for pos in range(length):
            # Caso para detectar ". " punto + espacio
            if STR[pos] == '.' and pos + 1 <= (length-1):
                if STR[pos + 1] == ' ': sep_cont = sep_cont - 1
            # Caso para detectar "  " doble espacios
            if STR[pos] == ' ' and pos + 1 <= (length-1):
                if STR[pos + 1] == ' ': sep_cont = sep_cont - 1
        if 'MAT' in STR: sep_cont = sep_cont - 2
        elif 'V.' in STR: sep_cont = sep_cont - 2
    return sep_cont


def pos_Separadores(STR):
    '''
        Funcion para buscar posiciones en cadenas de caracteres
        @STR: Cadena a analizar
        @Return: vector con las posiciones de los separadores
    '''
    pos = [0,0,0]
    #Checa si existe algun punto en el string
    if '.' in STR: pos[0]=STR.index('.')
    #Checa si existe algun espacio en el string, sin marcar error
    if ' ' in STR: pos[1]=STR.index(' ')
    #Checa si existe alguna coma en el string sin marcar error
    if ',' in STR: pos[2]=STR.index(',')
    return pos


def pos_corte(sep_pos):
    '''
        Funcion para definir un punto de corte en base a separadores
        @pos: vector con las posiciones de puntos, comas o espacios
        @return: poscion para corte
    '''
    punto_p = sep_pos[0] #Posicion de Punto
    espa_p = sep_pos[1]  #Posicion de Espacio
    coma_p = sep_pos[2]  #Posicion de Coma  //Caso especial
    #Podemos tener estos casos
    # Espacio+punto = ' .' # punto+espacio = '. '
    # punto solito = '.' # espacio solito = ' '
    # Para Espacio+Punto y  Punto+Espacio
    if espa_p == 0 or punto_p == 0: main_pos = max(punto_p,espa_p)
    elif abs(punto_p - espa_p) == 1: main_pos = max(punto_p,espa_p)
    elif punto_p - espa_p < 0: main_pos = punto_p
    elif punto_p - espa_p > 0: main_pos = espa_p
    return main_pos


def revisarSep(STR):
    '''
        Funcion de Revision para Casos sin Estandar o Extraños
    '''
    pos_div, sum = buscarPIPE(STR)
    if pos_div == 0: return False
    PIPE_A = STR[:pos_div]
    PIPE_B = STR[pos_div+sum:]
    A = contarSeparadores(PIPE_A)
    B = contarSeparadores(PIPE_B)
    if A > 3: return False
    if B > 1: return False
    return True


def revisarPipeB(STR, tipo=0):
    if tipo != 0:
        if tipo == 1: char = 'LX' # Para casos con XL
        elif tipo == 2: char = 'MAT' # Para casos con MAT COM
        elif tipo == 3  or tipo == 5: char = 'V.'
        elif tipo == 4: char = 'C.'
        text_pos = STR.index(char) 
        STR = STR[:text_pos]
    posPIPE, flag = buscarPIPE(STR)
    newSTR = STR[::-1]
    length = len(newSTR)
    for pos in range(length):
        if newSTR[pos] in letras_array: 
            newpos = pos
            break
    #if newpos > 4: print("Tiene año")
    #print("Cadena: ", STR, "posPIPE ", posPIPE)
    #print("Cadena invertida: ", newSTR, "posPIPE ", newpos+1)
    newposPIPE = length-1-(newpos+flag)
    if posPIPE == newposPIPE: return True
    return False


def Porcent(X,MAX):
    '''
        Esta funcion recibe un numero máximo y un número común para obtener el porcentaje
        @X: Valor comun
        @MAX: Valor Maximo
    '''
    return round(((X/MAX)*100),2)


def MaxCheck(MAX,X):
    '''
        Funcion de Chequeo para confirmar si un numero es le maximo
        @MAX: Numero actual maximo
        @X: Numero a comparar con MAX
        @Return: El Valor maximo de ambos numeros
    '''
    if X >= MAX: MAX = X
    return MAX


def Limpieza(STR):
    '''
        Funcion para Limpiar Caracteres ". ," no deseados de una cadena
    '''
    STRPrueba = STR
    CharNoDeseado = ". ,-"
    for x in CharNoDeseado:
        STRPrueba = STRPrueba.replace(x,'')
    return STRPrueba


def Estandarizar(STR, maxLen):
    '''
        Funcion para estandarizar la salida del programa
        @STR: Cadena a estandarizar
        @maxLen: Tamanio maximo que ha obtenido una cadena
    '''
    #Toma el elemento de la lista de diccionarios, funciona de elemento en elemento
    length = len(STR)
    dif = maxLen - length
    #creamos una cadena llena de ceros para estandarizar
    cadena_ceros = '0' * (dif)
    if STR[0] in letras_array and STR[1] in letras_array: STR = STR[:2] + cadena_ceros + STR[2:]
    else: STR = STR[:1] + cadena_ceros + STR[1:]
    #Reemplaza el valor estadarizado en la lista
    return STR


def clas_maker(clas, vol, cop):
    ''' Funcion para crear una clasificacion completa'''
    STR_clas = clas
    if vol != '': STR_clas += ' ' + vol
    if cop != '1' and cop != '': STR_clas += ' C.' + cop
    return STR_clas


def STR_limit(STR, size=40):
    '''Funcion para limitar el tamanio de un string'''
    if len(STR) > size: return STR[:size] + '...'
    else: return STR


def STR_cutter(STR, char, flag=0):
    '''
    Funcion para cortar una seccion de una cadena con base a un caracter
    @flag: 
        False = quita desde el elemento en adelante
        True = quita todo lo anterior al elemento
    '''
    text_pos = STR.index(char)
    if not flag: return STR[:text_pos]
    else: return STR[text_pos:]
    


def sacarGrupos(lisMain,llave,main_index):
    '''
        Funcion para sacar grupos con el mismo valor
        Recibe una lista y cuenta los grupos que se repitan
        @lisMain: Una Lista de Diccionarios
        @Llave: La llave a analizar
        @main_index: el indice donde se empieza el grupo
        @Return: el indice donde se termina el grupo
    '''
    length = len(lisMain)
    while main_index < length:
        base_STR = lisMain[main_index][llave]
        if main_index + 1 < length:
            next_STR = lisMain[main_index+1][llave]
        else:
            next_STR = 'NAN'
        if base_STR == next_STR: main_index += 1
        else: return main_index
    return length-1


def revisarVersion(string):
    '''
        Funcion para revisar posicion del caracter de V para versiones
        @string: Cadena a analizar
        @return: True si se encuentra al final o False si esta dentro de la cadena
    '''
    
    length = len(string)
    # print(length)
    char = 'V.'
    text_pos = string.index(char)
    # print(text_pos)
    if length - (text_pos + 2)> 2:
        return False
    return True


if __name__ == '__main__':
    cadena = 'pte.2'
    salida = STR_cutter(cadena, 'pte.', 1)

    cadena1 = 'B463'
    cadena2 = 'B1463'
    nueva_cadena = Estandarizar(STR=cadena1, maxLen=len(cadena2))
    print(nueva_cadena)
    if nueva_cadena < cadena2:
        print('Funciona correctamente')
