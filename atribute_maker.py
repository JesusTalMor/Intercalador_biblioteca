import string_helper as sh

'''
  Funciones para Seccionar Clasificacion por Atributos
'''

def sacar_atributos(clasif_basica, copia='1', volumen='A0', clasif_completa='A0', numero=1):
  ''' Saca los atributos de una clasificacion'''
  letras_array = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
  Dic = {"indice":numero, "clase":"A0", "subdecimal":"A0", "temaesp":"A0", "autor":"A0", "anio":"1000", "vol":volumen, "cop":copia, "clas":clasif_completa}
  cortar_pipe, diferencia = sh.buscar_pipe(clasif_basica)
  
  # Se puede cortar en PIPE A y B
  if cortar_pipe == 0:
    print("Caso Extraño: \n" + clasif_completa)
    return Dic
  
  PIPE_A = clasif_basica[:cortar_pipe]
  PIPE_B = clasif_basica[cortar_pipe + diferencia:]

  # print(PIPE_A,' + ', PIPE_B)

  # Separar usando atributo de split
  atributos_pipe_a = PIPE_A.split('.')
  atributos_pipe_b = PIPE_B.split(' ')

  # print(atributos_pipe_a)
  # print(atributos_pipe_b)

  # Rellenar en diccionario
  for index, elem in enumerate(atributos_pipe_a):
    if index == 0: Dic['clase'] = elem
    elif index == 1: Dic['subdecimal'] = elem
    elif index == 2: Dic['temaesp'] = elem
  
  for index, elem in enumerate(atributos_pipe_b):
    if index == 0: Dic['autor'] = elem
    elif index == 1: Dic['anio'] = elem

  # Revisar los casos especiales
  # ? Autor no tiene letra 
  if Dic["autor"][0] not in letras_array: 
    Dic['anio'] = Dic['autor']
    Dic['autor'] = 'A0'


  return Dic 
  
  # numA = contarSeparadores(PIPE_A)
  # numB = contarSeparadores(PIPE_B)
  # # print(numA)
  # # print(numB)
  # for i in range(numA+1):
  #   sep_pos = pos_Separadores(PIPE_A)
  #   main_pos = pos_corte(sep_pos)
  #   if main_pos == 0: main_pos = len(PIPE_A) 
  #   else: main_pos += 1
  #   Sal = PIPE_A[:main_pos]
  #   if not checarLetras(Sal):
  #     Sal = 'A' + Sal
  #   if i == 0: Dic["clase"] = Sal
  #   elif i == 1: Dic["subdecimal"] = Sal
  #   elif i == 2: Dic["temaesp"] = Sal
  #   PIPE_A = PIPE_A[main_pos:]
  # # Caso sin Año
  # if numB == 0 and PIPE_B[0] in letras_array: Dic["autor"] = PIPE_B
  # # Caso sin Autor
  # elif numB == 0: Dic["anio"] = PIPE_B
  # else:
  #   sep_pos = pos_Separadores(PIPE_B)
  #   main_pos = pos_corte(sep_pos)
  #   Dic["autor"] = PIPE_B[:main_pos+1]
  #   Dic["anio"] = PIPE_B[main_pos+1:]
    
  # #Si el anio tiene algun caracter del alfabeto
  # #Es un caso con Tema especial y sin Anio
  # if Dic["anio"][0] in letras_array:
  #   Dic["temaesp"] = Dic["autor"]
  #   if not checarLetras(Dic["anio"]):
  #     Dic["autor"] = 'A' + Dic["anio"]
  #   else: Dic["autor"] = Dic["anio"]
  #   Dic["anio"] = "3000"

  # # Zona de Ajuste para Biblioteca
  # # Revisamos si tenemos un autor
  # if flag:
  #   if Dic["autor"] != "A0":
  #     if Dic["subdecimal"] == "A0": 
  #       Dic["subdecimal"] = Dic["autor"]
  #       Dic["autor"] = "A0"
  #     elif Dic["temaesp"] == "A0": 
  #       Dic["temaesp"] = Dic["autor"]
  #       Dic["autor"] = "A0"    
  # return Dic


def correr_CasosIdeales():
  # print(sacar_atributos('BX4705.Q8 Z3 1965'))
  # print(sacar_atributos('BX4705.Q8 .Z3 1965'))
  # print(sacar_atributos('B823.3.A3 .S3'))
  # print(sacar_atributos('BX1378 .H3 1954'))
  # print(sacar_atributos('BX1428 .R5'))
  # print(sacar_atributos('BX1586.M36 .M36'))
  # print(sacar_atributos('BX2320.5.M6 .R87 1994'))
  # print(sacar_atributos('BX1538.R37.B47 R3 1942'))
  # print(sacar_atributos('B1162 2000'))
  print('----------------------------------------------------------------')
  print('----------------------------------------------------------------')

if __name__ == '__main__':
  # Insertamos funciones para depurar
  correr_CasosIdeales()
  