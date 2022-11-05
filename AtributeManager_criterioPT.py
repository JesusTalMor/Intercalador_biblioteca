from ApoyoSTRLIST import *
'''
    Funciones para Seccionar Clasificacion por Atributos
'''

def caso_ideal(STR1, STR_C='1', STR_V='A0', STR_clas='A0', index=1):
    '''
        Funcion para Depuracion de casos Ideales con todos los atributos \n
        Ejemplos BX4705.Q8 .Z3 1965, BX4705.737 .M418 1938, B823.3 .A3.S3
        @STR1: Cadena a depurar
        @Index: indice de salida donde se coloca el resultado
        @Return: un diccionario con todos los atributos depurados
    '''
    letras_array = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    Dic = {"indice":index, "clase":"A0", "subdecimal":"A0", "temaesp":"A0", "autor":"A0", "anio":"3000", "vol":STR_V, "cop":STR_C, "clas":STR_clas}
    pos_div1, sum = buscarPIPE(STR1)
    if pos_div1 != 0:
        PIPE_A = STR1[:pos_div1]
        PIPE_B = STR1[pos_div1+sum:]
    else:
        print("Caso Extraño: \n" + STR1)
        return
    # print(PIPE_A)
    # print(PIPE_B)
    numA = contarSeparadores(PIPE_A)
    numB = contarSeparadores(PIPE_B)
    # print(numA)
    # print(numB)
    for i in range(numA+1):
        sep_pos = pos_Separadores(PIPE_A)
        main_pos = pos_corte(sep_pos)
        if main_pos == 0: main_pos = len(PIPE_A) 
        else: main_pos += 1
        Sal = PIPE_A[:main_pos]
        if not checarLetras(Sal):
            Sal = 'A' + Sal
        if i == 0: Dic["clase"] = Sal
        elif i == 1: Dic["subdecimal"] = Sal
        elif i == 2: Dic["temaesp"] = Sal
        PIPE_A = PIPE_A[main_pos:]
    # Caso sin Año
    if numB == 0 and PIPE_B[0] in letras_array: Dic["autor"] = PIPE_B
    # Caso sin Autor
    elif numB == 0: Dic["anio"] = PIPE_B
    else:
        sep_pos = pos_Separadores(PIPE_B)
        main_pos = pos_corte(sep_pos)
        Dic["autor"] = PIPE_B[:main_pos+1]
        Dic["anio"] = PIPE_B[main_pos+1:]
        
    #Si el anio tiene algun caracter del alfabeto
    #Es un caso con Tema especial y sin Anio
    if Dic["anio"][0] in letras_array:
        Dic["temaesp"] = Dic["autor"]
        if not checarLetras(Dic["anio"]):
            Dic["autor"] = 'A' + Dic["anio"]
        else: Dic["autor"] = Dic["anio"]
        Dic["anio"] = "3000"

    # Zona de Ajuste para Biblioteca
    # Revisamos si tenemos un autor
    if Dic["autor"] != "A0":
        if Dic["subdecimal"] == "A0": 
            Dic["subdecimal"] = Dic["autor"]
            Dic["autor"] = "A0"
        elif Dic["temaesp"] == "A0": 
            Dic["temaesp"] = Dic["autor"]
            Dic["autor"] = "A0"    
    return Dic


def correr_CasosIdeales():
    print(caso_ideal('BX4705.Q8 Z3 1965'))
    print(caso_ideal('BX4705.Q8 .Z3 1965'))
    print(caso_ideal('B823.3 .A3.S3'))
    print(caso_ideal('BX1378 .H3 1954'))
    print(caso_ideal('BX1428 .R5'))
    print(caso_ideal('BX1586.M36 .M36'))
    print(caso_ideal('BX2320.5.M6 .R87 1994'))
    print(caso_ideal('BX1538.R37.B47 .R3 1942'))
    print(caso_ideal('B1162 2000'))
    print('----------------------------------------------------------------')
    print('----------------------------------------------------------------')

if __name__ == '__main__':
    # Insertamos funciones para depurar
    correr_CasosIdeales()
    print(caso_ideal('PZ10.3 S625 A6 2014'))