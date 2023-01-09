import re

'''Paquete de Funciones de apoyo para el trabajo de Strings y Manejo de Grupos para programa Descarte'''

letras_array = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
num_array = ['1','2','3','4','5','6','7','8','9','0']


def revisar_letras(STR: str) -> int:
  C_letras = len(re.findall('[ABCDEFGHIJKLMNOPQRSTUVWXYZ]',STR))
  return C_letras != 0


def buscar_caracter(STR: str, char: str) -> int:
  try: pos = STR.index(char)
  except: pos = 0
  
  return pos


def buscar_pipe(STR:str) -> int:
  ''' Retorna la posición para partir PIPE A y PIPE B '''
  lista_char = [(' .', 2), ('. ', 2), (' ', 1)]
  pos = 0
  for char, lenght in lista_char:
    pos = buscar_caracter(STR, char)
    if pos != 0: return pos, lenght
  return pos, 0


def contar_separadores(STR: str) -> int:
  '''
    Detecta y cuenta los separadores basicos ('.',',',' ') \n
    Tambien se toman en cuenta (' .', '. ') \n
    Retorna la cantidad de separadores encontrados
  '''
  cuenta_separador = len(re.findall('[. ,]' , STR))
  lista_char = [' .', '. ']
  length = len(STR)
  
  # * No se encontraron separadores
  if cuenta_separador == 0: return 0
  
  # * No tienen porque existir estos parametros
  if 'MAT' in STR or 'V.' in STR: return None
  
  cuenta_separadores_especiales = 0
  for char in lista_char: cuenta_separadores_especiales += STR.count(char)
  
  return cuenta_separador - cuenta_separadores_especiales


def posicion_separadores(STR:str) -> list:
  ''' Retorna una lista con la posicion de los separadores (',', '.', ' ')'''
  pos = (0,0,0)
  # Busca un punto (.) en string
  if '.' in STR: pos[0]=STR.index('.') 
  # Busca un espacio ( ) en string
  if ' ' in STR: pos[1]=STR.index(' ') 
  # Busca una coma (,) en string
  if ',' in STR: pos[2]=STR.index(',') 
  return pos


def posicion_corte(posicion_separadores:list) -> int:
  ''' Retorna la posición del separador más cercana (',', '.', ' ') '''
  # Desempaquetar variables
  punto_pos, espacio_pos, coma_pos = posicion_separadores

  if espacio_pos == 0 or punto_pos == 0: 
    posicion_salida = max(punto_pos,espacio_pos)
  elif abs(punto_pos - espacio_pos) == 1: 
    posicion_salida = max(punto_pos,espacio_pos)
  elif punto_pos - espacio_pos < 0: 
    posicion_salida = punto_pos
  elif punto_pos - espacio_pos > 0: 
    posicion_salida = espacio_pos
  return posicion_salida


def revisar_corte_pipe(STR:str) -> bool:
  ''' Revisar si se puede cortar de manera correcta '''
  
  posicion_corte, diferencia = buscar_pipe(STR)
  
  #!  Si no se ubica la posición de corte
  if posicion_corte == 0: return False
  
  PIPE_A = STR[:posicion_corte]
  PIPE_B = STR[posicion_corte + diferencia:]
  
  separadores_PIPE_A = contar_separadores(PIPE_A)
  separadores_PIPE_B = contar_separadores(PIPE_B)
  
  # Estandar de separadores
  if separadores_PIPE_A > 3: return False
  if separadores_PIPE_B > 1: return False
  
  return True


def revisar_pipeB(STR:str) -> bool:
  ''' Revisa si tiene sentido el corte de pipe B'''
  posicion_pipe, diferencia = buscar_pipe(STR)
  nuevo_str = STR[::-1]
  length = len(nuevo_str)

  nuevo_posicion_corte = 0
  for pos in range(length):
    if nuevo_str[pos] in letras_array:
      nuevo_posicion_corte = pos
      break

  nueva_posicion_pipe = length - 1 - (nuevo_posicion_corte + diferencia)
  if posicion_pipe == nueva_posicion_pipe: return True
  else: return False


def obtener_porcentaje(X,MAX):
  ''' Retorna el valor en porcentaje de una variable '''
  return round(((X/MAX)*100),2)



def checar_maximo(MAX,X):
  ''' Checa si el numero (x) es mayor al maximo '''
  MAX = X if X >= MAX else MAX
  return MAX



def limpiar_cadena(STR:str) -> str:
  ''' Remueve los caracteres no deseados de una cadena '''
  str_salida = STR
  CharNoDeseado = ". ,-"
  for x in CharNoDeseado:
    str_salida = str_salida.replace(x,'')
  return str_salida


def estandarizar_cadena(STR:str, maxLen:int) -> str:
  '''Estandariza las cadenas a un tamaño fijo '''
  length = len(STR)
  diferencia = maxLen - length
  #creamos una cadena llena de ceros para estandarizar
  cadena_ceros = '0' * diferencia
  str_salida = STR + cadena_ceros 
  #Reemplaza el valor estadarizado en la lista
  return str_salida


def creador_clasificacion(clas:str, vol:str, cop:str):
  ''' Retorna una clasificacion completa '''
  str_clasificacion_completa = clas
  # caso principal tenemos datos
  if vol != '':
    # Checar si es de tipo texto completo o solo numero
    if 'V.' in vol:  str_clasificacion_completa += ' ' + vol
    else: str_clasificacion_completa += ' V.' + vol
  
  if cop not in ('1', '', '0'): str_clasificacion_completa += ' C.' + cop
  return str_clasificacion_completa


def limitador_string(STR:str, size:int) -> str:
  ''' Limitar el tamaño de un string'''
  if len(STR) > size: return STR[:size] + '...'
  else: return STR


def cortar_string(STR:str, char:str) -> str:
  '''Corta la cadena a partir de un caracter especial'''
  posicion_corte = STR.index(char)
  return STR[:posicion_corte]


def sacar_grupos(lisMain,llave,main_index):
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
  pass