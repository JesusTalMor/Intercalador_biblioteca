# Implementacion de librerias necesarias
import pandas as pd

from ApoyoSTRLIST import *
from AtributeManager import *
from AuxIntercalado import *


def main_posible(excel_file:str, folder_path:str, name_file:str, report_config:list, data:list, modif_list:list):
  '''
    Funcion para correr el programa principal
    @archivo: Una ruta de acceso a un archivo Excel
    @carpeta: Donde se guaradará el archivo final
    @nombre: Del Archivo final
    @reporte: variable para manejar reporte se maneja con una lista
  '''
  #* Lectura de todas la hojas
  #* Insertar Nombres, es necesario poner el Path Absoluto para el archivo
  
  # Checar si se tiene que hacer un reporte
  if report_config[0]:
    reporte_txt_path = f'{folder_path}/{name_file}_reporte.txt'
    reporte_txt_writer = open(reporte_txt_path, 'w', encoding="utf-8")
    # Checar si crear el archivo de revision
    if len(modif_list) != 0:
      revision_txt_path = f'{folder_path}/{name_file}_listado_revision.txt'
      revision_txt_writer = open(revision_txt_path, 'w', encoding="utf-8")

  # Checar si se tiene que ordenar un excel
  if report_config[1]:
    excel_writer_path = f'{folder_path}/{name_file}.xlsx'
    excel_writer = ExcelWriter(excel_writer_path)

  # Checar si se tiene que realizar un ordenador
  if report_config[2]:
    orden_txt_path = f'{folder_path}/{name_file}_ordenador.txt'
    orden_txt_writer = open(orden_txt_path, 'w', encoding="utf-8")
  


  # * Cargar datos del Excel  
  dataExcel = cargarExcel(excel_file)
  # * Llaves de las hojas del Excel
  llaves_Excel = list(dataExcel)
  
  data_index = 0
  for key in llaves_Excel:
    # * Cargar datos de Hoja
    # print(F'Usando datos de Hoja {key}')
    data_keys = list(dataExcel[key])
    data_len = len(dataExcel[key][data_keys[0]])
    
    # * Escribir un reporte del sistema
    if report_config[0]:
      # print('Preparando reporte del Archivo')
      prepararReporte(
        excel_page=key, excel_file=excel_file, data_len=data_len, 
        modif_list=modif_list, cbarras_name=f'{name_file}_listado_revision.txt',
        writer_object=reporte_txt_writer, writer_object_aux=revision_txt_writer
      )

    # * Recibe una lista de string de datos y los separa
    # print('Separar lista completa')
    aux_list = data[data_index:(data_len-1)]
    
    # * Crear diccionarios de Clasificación
    # print('Creando diccionarios')
    dicc_list = crear_diccionario_clas(aux_list)
    
    # * Ordenar diccionario completo
    # print('Ordenando diccionario')
    lista_ord = ordenar_dicc(dicc_list)
    
    # * Escribir excel ordenado
    if report_config[1]:
      # print('Preparando Excel Ordenado')
      data_frame = prepararExcel(dataExcel[key], lista_ord)
      escribirExcel(data_frame,key,excel_writer)

    # * Escribir instrucciones para ordenar libros
    if report_config[2]:
      # print('Preparando Instrucciones Ordenar')
      prepararErrorExcel(lista_ord, dicc_list, aux_list, orden_txt_writer)

    data_index = data_len
    # print('Hoja Completada con Exito')
  
  if report_config[0]:
    reporte_txt_writer.close()
    if len(modif_list) != 0:
      revision_txt_writer.close()
  if report_config[1]:
    excel_writer.save()
  if report_config[2]:
    orden_txt_writer.close()
  
  
  # print('Excel Completado con Exito')
  return True


def prepararReporte(excel_page:str, excel_file:str, data_len:int, modif_list:list, cbarras_name:str, writer_object, writer_object_aux):
  len_char = 55
  writer_object.write('='*len_char + '\n')
  writer_object.write(f'\t Reporte de {excel_page}\n\n')
  writer_object.write(f'Archivo Utilizado:\n{excel_file}\n')
  writer_object.write('='*len_char + '\n')
  writer_object.write('='*len_char + '\n\n')
  writer_object.write("\t Detalle del Reporte \n")
  writer_object.write('='*len_char + '\n')
  writer_object.write(f'Total de Casos Cargados: {data_len}\n')
  writer_object.write(f'Casos Correctamente Analizados: {data_len - len(modif_list)}\n')
  writer_object.write(f'Casos Modificados: {len(modif_list)}\n')
  writer_object.write('='*len_char + '\n')

  if len(modif_list) == 0:
    writer_object.write('='*len_char + '\n')
    writer_object.write('\t Sin Casos Sin Estandar LC' + '\n')
    writer_object.write('='*len_char + '\n')
  else:
    writer_object.write('NOTA:\n')
    writer_object.write(f'En el archivo: {cbarras_name} encontraras los codigos de barra\n')
    writer_object.write('para cargarlos en una lista de Sierra.' + '\n')
    writer_object.write('\n\n')
    for elem in modif_list:
      writer_object_aux.write(f'{elem[3]}\n')
  
  reporte_modify(modif_list, writer_object)
  writer_object.write('\n\n')


def ordenar_dicc(main_list:list):
  llaves = ['clase','subdecimal','temaesp','autor','anio','vol','cop'] #* Llaves del diccionario
  # * Limpieza de caracteres no deseados y toma de tamaño de los string
  main_list, maxlen_All = limpiarLista(main_list,llaves)
  main_list = estandarizarLista(main_list, maxlen_All[0], maxlen_All[1], maxlen_All[2], maxlen_All[3], llaves)
  # * Ordenando Lista de Salida
  lista_ORD = []
  lista_ORD = sorted(main_list, key=lambda llave : llave[llaves[0]])
  lista_ORD = ordenarLista(lista_ORD,llaves,0)
  return lista_ORD


def crear_diccionario_clas(main_list:list):
  """ 
  Separa las caracteristicas de una clasificacion en un diccionario
  Retorna una lista de diccionarios
  """
  lista_salida = []
  for idx, dicc in enumerate(main_list):
    STR_clas_f = clas_maker(dicc['clasi'], dicc['volum'], dicc['copia'])
    lista_salida.append(
      caso_ideal(
        STR1=dicc['clasi'], STR_C=dicc['copia'], 
        STR_V=dicc['volum'], index=idx, STR_clas=STR_clas_f
      )
    )
  return lista_salida


def cargar_etiquetas(path: str):
  #? Acceder al archivo excel y extraer la columna Clasificación, Volumen y Copia
  #* Tomamos los datos del excel
  excel_data = cargarExcel(path)
  llaves_excel_data = list(excel_data)

  # Listas de salida de la función
  salida_etiquetas = []
  salida_dicc = []
  name_flag = True
  cbarras_flag = True

  for key in llaves_excel_data:
    # * Cargamos listas de clasificacion, Volumen y Copia
    clas_data,vol_data,cop_data,name_data,codb_data = cargarDatos(excel_data[key])
    
    # TODO revisar esta implementación
    # Checar si no tenemos errores
    if clas_data[0] == False: 
      print('Error en obtener info')
      continue
    
    # No contamos con columna de nombres
    if name_data[0] == False:
      name_flag = False
    
    if codb_data[0] == False:
      cbarras_flag = False


    for i in range(len(clas_data)):
      STR_clas = clas_data[i]       
      STR_cop = str(cop_data[i])    
      STR_vol = '' if pd.isna(vol_data[i]) else vol_data[i]      
      STR_name = 'NAN' if not name_flag else name_data[i] 
      STR_cbarras = 'NAN' if not cbarras_flag  else codb_data[i]
      
      # Revision de Caso con Nan
      if pd.isna(STR_clas):
        salida_etiquetas.append(['NAN', 'NO', 'APLICA', 'False'])
        salida_dicc.append(
          {'clasi': 'NAN', 'copia': STR_cop, 'volum': STR_vol,
          'titulo': STR_name, 'cb': STR_cbarras}
        )
        continue
      
      # Eliminar datos innecesarios
      if 'LX' in STR_clas: 
        char = 'LX'  # Para casos con XL
        STR_clas = STR_cutter(STR_clas, char)
      if 'MAT' in STR_clas: 
        char = 'MAT' # Para casos con MAT COM
        STR_clas = STR_cutter(STR_clas, char)
      
      
      # Crear Clasificacion completa
      STR_clas_f = clas_maker(STR_clas, STR_vol, STR_cop)

      if 'V.' in STR_clas or 'C.' in STR_clas:
        salida_etiquetas.append([STR_clas_f, 'NO', 'APLICA', 'False'])
        salida_dicc.append(
          {'clasi': STR_clas, 'copia': STR_cop, 'volum': STR_vol,
          'titulo': STR_name, 'cb': STR_cbarras}
        )
        continue

      # * Revisar si tiene error de estandar
      if revisarSep(STR_clas) and revisarPipeB(STR_clas):
        pos_div, sum = buscarPIPE(STR_clas)
        pipe_a_str = STR_clas[:pos_div]
        pipe_b_str = STR_clas[pos_div+sum:]
        salida_etiquetas.append([STR_clas, pipe_a_str, pipe_b_str, 'True'])
        salida_dicc.append(
          {'clasi': STR_clas, 'copia': STR_cop, 'volum': STR_vol,
          'titulo': STR_name, 'cb': STR_cbarras}
        )
      else:
        salida_etiquetas.append([STR_clas_f, 'NO', 'APLICA', 'False'])
        salida_dicc.append(
          {'clasi': STR_clas, 'copia': STR_cop, 'volum': STR_vol,
          'titulo': STR_name, 'cb': STR_cbarras}
        )
  return salida_etiquetas, salida_dicc  


def reporte_modify(lista:list, writer_object):
  """ Genera un reporte de una lista en un txt """
  # Escribir lo que necesitamos en el archivo
  writer_object.write(f'\tDATOS MODIFICADOS DENTRO DE LA APLICACION \n')
  writer_object.write('='*60)
  writer_object.write('\n\n')
  # Abrir lista y escribir
  for elem in lista:
    for item in elem:
      # Checar el  largo del item
      text = STR_limit(item) if len(item) > 40 else item + ' '*(40 - len(item))
      writer_object.write(f'{text}\t | \t')
    writer_object.write(f'\n')


def imprimir_lista(lista:list):
  for elem in lista:
    print(elem)
    print('-'*150)

if __name__ == '__main__':
  pass