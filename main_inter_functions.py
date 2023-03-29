
# Implementacion de librerias necesarias
# import os

import pandas as pd

import pop_ups as pop
import string_helper as sh


# ? Pasos para el programa 
# ? Cargar los datos de las clasificaciones desde el excel
def cargar_excel(path:str):
  '''Obtiene todo el dataframe de datos de un excel'''
  Datos = pd.read_excel(path, sheet_name=None)
  return Datos


def cargar_clasif_libros(dataframe):
  '''
    Carga los datos para generar clasificaciones
    NOTA: Unicamente carga los datos de las columnas de Excel, no realiza modificaciones
  '''
  clasif = [False]
  volumen = [False]
  copia = [False]

  llaves = list(dataframe)

  # Revisar si podemos extraer los datos necesarios
  if 'Clasificación' in llaves and 'Volumen' in llaves and 'Copia' in llaves:
    clasif = dataframe['Clasificación']
    volumen = dataframe['Volumen']
    copia = dataframe['Copia']
  
  return clasif, volumen, copia


def cargar_informacion_libros(dataframe):
  ''' 
    Carga los datos de información de los libros
    NOTA: Unicamente carga los datos de las columnas de Excel, no realiza modificaciones
  '''
  titulo = [False]
  codigo_barras = [False]
  clasif = [False]
  volumen = [False]
  copia = [False]
  encabezado = [False]

  llaves = list(dataframe)

  if 'Título' in llaves: titulo = dataframe['Título']
  if 'C. Barras' in llaves: codigo_barras = dataframe['C. Barras']
  if 'Clasificación' in llaves: clasif = dataframe['Clasificación']
  if 'Volumen' in llaves: volumen = dataframe['Volumen']
  if 'Copia' in llaves: copia = dataframe['Copia']
  if 'Encabezado' in llaves: encabezado = dataframe['Encabezado']
  
  return titulo, codigo_barras, clasif, volumen, copia, encabezado


def generar_etiquetas_libros(dataframe):
  """ Genera las etiquetas de un archivo Excel """
  salida = []
  
  # * Solo vamos a usar una pagina en este programa
  CLAS, VOL, COP = cargar_clasif_libros(dataframe)
  len_data = len(CLAS)
  
  # * Checa si se cargaron todos los datos
  if not CLAS[0]: return [False]
  
  # * Inicia proceso de sacar todas las clasificaciones
  for i in range(len_data):
    STR = CLAS[i] # ya vienen como String por defecto
    STR_C = str(COP[i])
    STR_V = VOL[i] # ya vienen como String por defecto

    # * Checar si el atributo CLAS esta vacio
    if pd.isna(STR):
      salida.append(['None', 'No', 'Aplica', 'False'])
      continue

    STR = sh.limpiar_clasif(STR)

    # * Checar si el atributo VOL esta vacio
    if pd.isna(STR_V): STR_V = ''

    # * Checar si el atributo COP esta vacio
    if pd.isna(STR_C): STR_C = ''

    STR_Clas = sh.creador_clasificacion(STR, STR_V, STR_C)
    
    # * Revisamos si se puede dividir Pipe A y Pipe B
    if sh.revisar_corte_pipe(STR) and sh.revisar_pipeB(STR):
      pos_div, sum = sh.buscar_pipe(STR)
      pipe_a_str = STR[:pos_div]
      pipe_b_str = STR[pos_div+sum:]
      salida.append([STR_Clas, pipe_a_str, pipe_b_str, 'True'])
    else:
      salida.append([STR_Clas, 'No', 'Aplica', 'False'])
  
  if len(salida) != 0: return salida
  else: return [False]


def generar_informacion_libros(dataframe):
  '''
  Genera una lista completa con la información de 
  Titulo y codigo de Barras de los libros
  '''
  Salida = []
  
  titu, cb, clas, vol, cop, enc = cargar_informacion_libros(dataframe)
  # * Checar si clase tiene error
  if not clas[0]: return [False]

  for index in range(len(clas)):
    # * Creamos el diccionario
    temp_dicc = {}
    # * Rellenamos el diccionario
    temp_dicc['titulo'] = str(titu[index]) if titu[0] else ''
    temp_dicc['cbarras'] = str(cb[index]) if cb[0] else ''
    temp_dicc['clasif'] = str(sh.limpiar_clasif(clas[index])) if clas[0] and not pd.isna(clas[index]) else ''
    temp_dicc['volumen'] = str(vol[index]) if vol[0] and not pd.isna(vol[index]) else ''
    temp_dicc['copia'] = str(cop[index]) if cop[0] and not pd.isna(cop[index]) else ''
    temp_dicc['encabeza'] = str(enc[index]) if enc[0] else ''
    # * Añadimos el diccionario
    Salida.append(temp_dicc)
  return Salida



# TODO Realizar el cambio a valores de Atributos de las Clasificaciones

def sacar_atributos(clasif_basica, copia='1', volumen='A0', clasif_completa='A0', numero=1):
  ''' Saca los atributos de una clasificacion'''
  letras_array = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
  Dic = {"indice":numero, "clase":"A0", "subdecimal":"A0", "temaesp":"A0", "autor":"A0", "anio":"1000", "vol":volumen, "cop":copia, "clas":clasif_completa}
  cortar_pipe, diferencia = sh.buscar_pipe(clasif_basica)
  
  # Se puede cortar en PIPE A y B
  if cortar_pipe == 0:
    print("Caso Extraño: ", clasif_completa)
    return Dic
  
  PIPE_A = clasif_basica[:cortar_pipe]
  PIPE_B = clasif_basica[cortar_pipe + diferencia:]

  # print(PIPE_A,' + ', PIPE_B)

  # Separar usando atributo de split

  atributos_pipe_a = PIPE_A.split('.') if '.' in PIPE_A else PIPE_A.split(' ')
  atributos_pipe_b = PIPE_B.split(' ') if ' ' in PIPE_B else PIPE_B.split('.')

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

def separar_atributos_libros(lista):
  ''' Toma una lista de diccionarios y le saca los atributos para clasificación'''
  lista_salida = []
  for index, elem in enumerate(lista):
    clasif_basica = elem['clasif']
    volumen = elem['volumen']
    copia = elem['copia']
    
    encabezado = elem['encabeza'] + ' ' if elem['encabeza'] != '' else ''
    clasif_completa = encabezado + sh.creador_clasificacion(clasif_basica, volumen, copia)
    
    temp_dicc = sacar_atributos(clasif_basica, copia, volumen, clasif_completa, index)
    lista_salida.append(temp_dicc)
  
  return lista_salida

def limpiar_atributos_libros(lista):
  '''
  Toma una lista de dicccionarios y limpia de caracteres no deseados
  Limpia los siguientes atributos:
  'Clase': clase, 'Subdecimal':subdecimal, 'Tema_especial':temaesp, 'Autor':autor
  '''
  llaves_dicc = list(lista[0])
  dicc_largos = {'clase': 0, 'subdecimal': 0, 'temaesp': 0, 'autor': 0}
  for index, dicc in enumerate(lista):
    for ind, llave in enumerate(llaves_dicc):
      if ind == 5: break
      elif ind == 0: continue
      temp_string = sh.limpiar_cadena(dicc[llave])
      dicc_largos[llave] = sh.checar_maximo(dicc_largos[llave], len(temp_string))
      lista[index][llave] = temp_string
  return lista, dicc_largos

def estandarizar_atributos_libros(lista, largos):
  '''Toma una lista y un diccionario de largos para estandarizar dicha lista a los largos'''
  llaves_dicc = list(lista[0])
  for index, dicc in enumerate(lista):
    for ind, llave in enumerate(llaves_dicc):
      if ind == 5: break
      elif ind == 0: continue
      temp_string = sh.estandarizar_cadena(dicc[llave], largos[llave])
      lista[index][llave] = temp_string
  return lista


# TODO Ordenar las clasificaciones usando los atributos

def ordenar_lista_semi(lisMain,llaves,i):
    '''
        Funcion que recibe una lista de diccionarios semiordenados y 
        los ordena por llaves
    '''
    lenght = len(lisMain)
    lista_ORD = []
    # Crea Grupos de Temas
    start_index = 0
    while start_index < lenght:
        final_index = sh.sacar_grupos(lisMain,llaves[i],start_index)
        lista_aux = lisMain[start_index : final_index+1]
        if len(lista_aux) == 1:
            # Si se recibe una lista de un solo elemento ya esta ordenada
            lista_ORD.append(lista_aux[0])
        else:
            if i + 1 < len(llaves):
                # Se ordena la sublista y se agrega al resultado
                lista_aux = sorted(lista_aux, key=lambda llave : llave[llaves[i+1]])
                #Parte Recursiva
                lista_aux = ordenar_lista_semi(lista_aux,llaves,i+1)
            for elem in lista_aux:
                lista_ORD.append(elem)
        start_index = final_index + 1
    return lista_ORD


def ordenar_libros_atributo(lista):
  '''
  Ordena las clasficaciones de los libros con base a sus atributos siguiendo
  el siguiente orden
  "Clase" -> "Subdecimal" -> "Tema Esp." -> "Autor" -> Año -> Volumen -> Copia
  '''
  llaves_dicc = list(lista[0])
  
  lista_salida = sorted(lista, key=lambda llave : llave[llaves_dicc[1]])
  lista_salida = ordenar_lista_semi(lista_salida,llaves_dicc,1)
  return lista_salida


# TODO Crear nuevo excel corregido

def crear_excel_ordenado(lista_orden, lista_datos, dataframe):
  atributos = list(dataframe)
  
  lista_salida = []
  # * Corregir Valores cambiados en el programa
  lista_clasif = []
  lista_volumen = []
  lista_copia = []
  lista_clasif_completa = []
  # lista_encabeza = []
  for elem in lista_orden:
    index = elem['indice']
    lista_clasif.append(lista_datos[index]['clasif'])
    lista_volumen.append(lista_datos[index]['volumen'])
    lista_copia.append(lista_datos[index]['copia'])
    lista_clasif_completa.append(elem['clas'])
    # lista_encabeza.append(lista_datos[index]['encabeza'])

  # * Crear listas de datos dentro del excel
  for atributo in atributos:
    lista_aux = []
    # Corregir Clasificación
    if atributo == 'Clasificación': 
      lista_salida.append(lista_clasif)
      continue
    # Corregir Volumen
    if atributo == 'Volumen': 
      lista_salida.append(lista_volumen)
      continue
    # Corregir Copia
    if atributo == 'Copia':
      lista_salida.append(lista_copia)
      continue

    # Crear lista de Atributo X
    for elem in lista_orden:
      index = elem['indice']
      lista_aux.append(dataframe[atributo][index])
    
    lista_salida.append(lista_aux)
  
  # Agregar clasificacion completa
  lista_salida.append(lista_clasif_completa)

  
  # * Creamos el diccionario de Salida para Excel
  dataframe_salida = {}
  for index, atributo in enumerate(atributos):
      dataframe_salida[atributo] = lista_salida[index]
  dataframe_salida['Clasificación Completa'] = lista_salida[-1]
  return dataframe_salida

def escribir_excel(dataframe_escritura, archivo_info, hoja, num_hoja):
    '''Usando un dataframe escribe un Excel de solo una hoja'''
    ruta_folder, nombre = archivo_info['folder'], archivo_info['nombre']
    excel_writer_path = f'{ruta_folder}/{nombre}.xlsx'
    excel_writer = pd.ExcelWriter(excel_writer_path, mode='a') if num_hoja != 0 else pd.ExcelWriter(excel_writer_path, mode='w')

    df = pd.DataFrame(dataframe_escritura)
    atributos = list(df)
    df = df[atributos]
    df.to_excel(excel_writer, sheet_name=hoja, index=False)
    excel_writer.save()

# TODO Crear archivo para el correcto ordenamiento de los libros

def marcar_condiciones_libros(lista_ordenada, lista_no_ordenada):
  '''Checar y asigna una condicion a cada libro dependido de su situacion'''
  lisSAL = []
  for ind in range(len(lista_ordenada)):
    # * Comparar indices de entrada y salida
    entry_INDX = lista_no_ordenada[ind]["indice"]
    out_INDX = lista_ordenada[ind]["indice"]
    entry_clas = lista_no_ordenada[ind]["clas"]
    
    # * Revisar coinciden los indices
    if entry_INDX == out_INDX:
      lisSAL.append([entry_INDX, 'correcto', entry_clas])
      continue
    
    # * Indices no coinciden
    if (ind - 1) >= 0 or (ind + 1) < len(lista_ordenada):
      # Erroneo por completo
      cond = 'erroneo'
      # Condicionado Anterior
      if (ind - 1) >= 0: 
        cond_INDX = lista_ordenada[ind - 1]["indice"]
        if entry_INDX == cond_INDX: cond = 'con_ant'
      # Condicionado Posterior
      if (ind + 1) < len(lista_ordenada):
        cond_INDX = lista_ordenada[ind + 1]["indice"]
        if entry_INDX == cond_INDX: cond = 'con_pos'
      
      lisSAL.append([entry_INDX, cond, entry_clas])
  # print(*lisSAL, sep='\n')
  
  # * Solucionar casos con condicionales
  while True:
    cond_flag = False
    for index in range(len(lisSAL)):
      # Si el elemento es condicionado Anterior
      if lisSAL[index][1] == 'con_ant' and index - 1 >= 0 and lisSAL[index - 1][1] == 'erroneo':
        lisCOPY = lisSAL[index - 1].copy()
        lisSAL[index - 1] = lisSAL[index]
        lisSAL[index - 1][1] = 'correcto'

        lisSAL[index] = lisCOPY
        lisSAL[index][1] = 'erroneo'
      
      # Si el elemento es condicionado Siguiente
      if lisSAL[index][1] == 'con_pos' and index + 1 < len(lisSAL) and lisSAL[index + 1][1] == 'erroneo':
        lisCOPY = lisSAL[index + 1].copy()
        lisSAL[index + 1] = lisSAL[index]
        lisSAL[index + 1][1] = 'correcto'

        lisSAL[index] = lisCOPY
        lisSAL[index][1] = 'erroneo'
          
      for elem in lisSAL:
        if elem[1] == 'con_pos' or elem[1] == 'con_ant': 
          cond_flag = True
          break
      
    # * Revisar si ya se solucionaron casos condicionados
    if not cond_flag: break
  
  # print(*lisSAL, sep='\n')
  return lisSAL

def instrucciones_ordenar(lista_ordenada, lista_no_ordenada, lista_datos):
  '''
    Genera un TXT con instrucciones para organizar libros
    
    PARAMETROS:
      :param lisORD: Es una lista de diccionarios ya ordenada con los parametros
      :param lisDIC: Es una lista de diccionarios que no esta ordenada
      :param lisNAME: Es una lista que contiene todos los nombres de los libros
      :param txt_file: Es un objeto para escribir en un archivo tipo txt
  '''

  # * Checar si los datos son muy pequeños
  if len(lista_ordenada) <= 5:
    pop.not_enough_books()
    return [False], [False]

  # * Si ambos diccionarios no son iguales no se procede
  if len(lista_ordenada) != len(lista_no_ordenada):
    pop.error_manual_order()
    return [False], [False]

  # * Llenar lista de las condiciones de libros y solucionar condicionados
  lista_condiciones = marcar_condiciones_libros(lista_ordenada, lista_no_ordenada)
  len_lista = len(lista_condiciones)
  # print(*lista_condiciones, sep='\n')

  # * LLenar lista de libros erroneos y correctos
  lisERROR, lisCORR = [], []
  for elem in lista_condiciones: 
      if elem[1] == 'erroneo': lisERROR.append(elem[0])
      else: lisCORR.append(elem[0])

  # * Casos sin errores no se puede acomodar
  if len(lisERROR) == 0:
    pop.success_manual_order()
    return [False], [False]
  
  
  # * Texto inicial del programa
  error_porcent = sh.obtener_porcentaje(len(lisERROR), len_lista)
  # print(f'Procentaje de libros erroneos: {error_porcent}%')
  # txt_file.write('='*85 + '\n')
  # txt_file.write(f'\t Con {len_lista} libros, {len(lisERROR)} estan mal colocados, que equivale al {error_porcent}%\n')
  # txt_file.write('='*85 + '\n')
  
  # txt_file.write("\n\n\tPROCESO PARA ORGANIZAR LIBROS\n")
  # txt_file.write("\tPASO 1. RETIRE LOS SIGUIENTES LIBROS\n")
  # txt_file.write('#'*85 + '\n')
  
  # * Sacar pocos libros erroneos
  # Se sacan los libros como aparecen
  lista_retirar = []
  if error_porcent < 60 and len(lisERROR) < 20:
    for error_index in lisERROR:
      # * Sacar datos de libro erroneo
      diccio_temporal = {'libro': ('',''), 'anterior':('',''), 'siguiente':('','')}
      clasif_error = lista_no_ordenada[error_index]['clas']
      nombre_error = sh.limitador_string(lista_datos[error_index]['titulo'])
      diccio_temporal['libro'] = (clasif_error, nombre_error)

      # *Sacar datos de libros correctos
      # * Buscar libro anterior correcto
      for corr_index in range(error_index-1, -1, -1):
        if corr_index not in lisCORR: continue
        clasif_ant = lista_no_ordenada[corr_index]['clas']
        nombre_ant = sh.limitador_string(lista_datos[corr_index]['titulo'])
        diccio_temporal['anterior'] = (clasif_ant, nombre_ant)
        break
      
      lista_retirar.append(diccio_temporal)
  # * Caso común
  # Sacar los libros en el orden en el que se van a meter
  else:
    # * Ordenar lista de errores
    ordenar_retirar = []
    for index in range(len_lista):
      if lista_ordenada[index]['indice'] in lisERROR:
        ordenar_retirar.append(lista_ordenada[index]['indice'])
    
    # * Sacar los libros
    for error_index in ordenar_retirar:
      # * Sacar datos de libro erroneo
      diccio_temporal = {'libro': ('',''), 'anterior':('',''), 'siguiente':('','')}
      clasif_error = lista_no_ordenada[error_index]['clas']
      nombre_error = sh.limitador_string(lista_datos[error_index]['titulo'])
      diccio_temporal['libro'] = (clasif_error, nombre_error)

      # * Sacar datos de libros correctos
      # * Buscar libro anterior correcto
      for corr_index in range(error_index-1, -1, -1):
        if corr_index not in lisCORR: continue
        clasif_ant = lista_no_ordenada[corr_index]['clas']
        nombre_ant = sh.limitador_string(lista_datos[corr_index]['titulo'])
        diccio_temporal['anterior'] = (clasif_ant, nombre_ant)
        break
      # * Buscar libro siguiente correcto
      for corr_index in range(error_index+1, len_lista, +1):
        if corr_index not in lisCORR: continue
        clasif_ant = lista_no_ordenada[corr_index]['clas']
        nombre_ant = sh.limitador_string(lista_datos[corr_index]['titulo'])
        diccio_temporal['siguiente'] = (clasif_ant, nombre_ant)
        break
      lista_retirar.append(diccio_temporal)

  # * Colocar libros
  lista_colocar = []
  for index in range(len_lista):
    # Buscar libro erroneo en lista ordenada
    indice_error = lista_ordenada[index]['indice']
    if indice_error not in lisERROR: continue

    # Sacar datos libro erroneo
    diccio_temporal = {'libro': ('',''), 'anterior':('',''), 'siguiente':('','')}
    clasif_error = lista_ordenada[index]['clas']
    nombre_error = sh.limitador_string(lista_datos[indice_error]['titulo'])
    diccio_temporal['libro'] = (clasif_error, nombre_error)

    # * Sacar datos de libros correctos
    # * Buscar libro anterior correcto
    for corr_index in range(index-1, -1, -1):
      indice_correcto = lista_ordenada[corr_index]['indice']
      if indice_correcto not in lisCORR: continue
      clasif_ant = lista_ordenada[corr_index]['clas']
      nombre_ant = sh.limitador_string(lista_datos[indice_correcto]['titulo'])
      diccio_temporal['anterior'] = (clasif_ant, nombre_ant)
      break
    for corr_index in range(index+1, len_lista, +1):
      indice_correcto = lista_ordenada[corr_index]['indice']
      if indice_correcto not in lisCORR: continue
      clasif_ant = lista_ordenada[corr_index]['clas']
      nombre_ant = sh.limitador_string(lista_datos[indice_correcto]['titulo'])
      diccio_temporal['siguiente'] = (clasif_ant, nombre_ant)
      break
    lista_colocar.append(diccio_temporal)

  return lista_retirar, lista_colocar


# TODO Crear reporte de modificaciones de clasificaciones

def crear_reporte(len_archivo:int, modificados:list, archivo_info:dict, hoja:str, num_hoja:int):
  '''Genera un reporte en un txt de libros modificados'''
  ruta_folder, ruta_archivo, nombre = archivo_info['folder'], archivo_info['archivo'], archivo_info['nombre']
  txt_path = f'{ruta_folder}/{nombre}_reporte.txt'
  
  if len_archivo == 0: return # Revisar si tenemos datos
  
  len_sep = 50 # largo de separadores de caracteres
  len_correctos = len_archivo - len(modificados)
  # Escribir en el archivo
  archivo_txt = open(txt_path, 'a', encoding="utf-8") if num_hoja != 0 else open(txt_path, 'w', encoding="utf-8")
  archivo_txt.write('='*len_sep + '\n')
  archivo_txt.write(f'\t Reporte de {hoja} \n')
  archivo_txt.write('='*len_sep + '\n\n')
  archivo_txt.write(f'Archivo Utilizado:\n{ruta_archivo}\n\n')
  archivo_txt.write('='*len_sep + '\n')
  archivo_txt.write(f'\t Registro de Analisis Estandar LC \n')
  archivo_txt.write('='*len_sep + '\n')
  archivo_txt.write(f'Clasificaciones cargadas: {len_archivo} | 100%\n')
  archivo_txt.write(f'Clasificaciones con Estandar LC: {len_correctos} | {sh.obtener_porcentaje(len_correctos, len_archivo)}%\n')
  archivo_txt.write(f'Clasificaciones modificadas: {len(modificados)} | {sh.obtener_porcentaje(len(modificados), len_archivo)}&\n')
  archivo_txt.write('='*len_sep + '\n\n')
  
  # * Tenemos casos con modificaciones
  if modificados:
    archivo_txt.write(f'''NOTA:
    En el archivo: {nombre}_modificados.txt encontraras
    los codigos de barras para cargarlos a Sierra \n\n'''
    )
    archivo_txt.write(f'\t\tLista de Clasificaciones Modificadas\n')
    archivo_txt.write('='*len_sep + '\n')
    for target in modificados:
      for index, elem in enumerate(target):
        if index == 0: diferencia = 40 - len(elem) if len(elem) < 40 else 0
        else: diferencia = 0
        archivo_txt.write(sh.limitador_string(elem) + ' '*diferencia + ' | ')
      archivo_txt.write('\n')
    archivo_txt.write('\n\n\n')
  else:
    archivo_txt.write('*'*len_sep + '\n')
    archivo_txt.write('Sin casos Modificados\n')
    archivo_txt.write('*'*len_sep + '\n\n\n')
  archivo_txt.close()

  if modificados:
    # Crear archivo txt con los codigo de barras modificados
    txt_modif = f'{ruta_folder}/{nombre}_modificados.txt'
    archivo_txt = open(txt_modif, 'a', encoding="utf-8") if num_hoja != 0 else open(txt_modif, 'w', encoding="utf-8")
    for target in modificados: archivo_txt.write(target[1] + '\n')
    archivo_txt.close()

if __name__ == '__main__':
  pass