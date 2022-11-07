# Implementacion de librerias necesarias
import pandas as pd

from ApoyoSTRLIST import *
from AtributeManager import *
from AuxIntercalado import *


def main_program(archivo,carpeta,nombre,reporte, codify):
  '''
    Funcion para correr el programa principal
    @archivo: Una ruta de acceso a un archivo Excel
    @carpeta: Donde se guaradará el archivo final
    @nombre: Del Archivo final
    @reporte: variable para manejar reporte se maneja con una lista
  '''
  #* Lectura de todas la hojas
  #* Insertar Nombres, es necesario poner el Path Absoluto para el archivo
  Nombre = archivo
  path = carpeta
  name = nombre
  txt_path = path + '/' + name + '_reporte.txt'
  txt_path2 = path + '/' + name + '_listadoRevision.txt'
  main_path = path + '/' + name +'.xlsx'
  main_path2 = path + '/' + name + '_Ordenador.txt'
  
  # Objetos de escritura para archivos
  if reporte[0] == 1: 
    report_file = open(txt_path, 'w', encoding="utf-8")
    CB_file = open(txt_path2, 'w', encoding="utf-8")
  if reporte[1] == 1: writer = ExcelWriter(main_path)
  if reporte[2] == 1: order_file = open(main_path2, 'w', encoding="utf-8")
  
  dataExcel = cargarExcel(Nombre)
  #Cargamos Datos
  llaves_Excel = list(dataExcel)
  for key in llaves_Excel:
    Data,Data_vol,Data_cop,Data_name,Data_codB = cargarDatos(dataExcel[key])
    if Data[0] == False: return False
    len_Data = len(Data)
    CN = 0 # Variables para casos Normales
    CLX = 0 # Variable para Casos con Texto LX
    CMAT = 0 # Variable para Casos con Texto MAT COM
    CV = 0 # Variables para Casos con Versiones
    CP = 0 # Variable para Casos con Copia
    CE = 0 # Variables para Casos Extraños sin análisis
    #* Definir listas principales para guardar los datos
    lista_Dic = []      #Lista para Guardar Diccionarios ya separados
    lista_Raros = []    #Lista para casos sin analisis
    llaves = ['clase','subdecimal','temaesp','autor','anio','vol','cop'] #* Llaves del diccionario
    #* Bucle Principal para revision de cadenas (string)
    for i in range(len_Data):
      STR = Data[i]   # Tiene la clasificación incompleta del libro
      STR_C = str(Data_cop[i]) # Contiene la copia del libro
      STR_V = Data_vol[i] # Contiene el volumen del libro
      
      # Se checa si se tiene codigo de Barra o No
      if Data_codB[0] == False: CB_STR = 'NAN' 
      else: CB_STR = Data_codB[i] 
      
      # Se checa si se tiene titulo o no
      if Data_name[0] == False: STR_NAME = 'Sin Título' 
      else: STR_NAME = Data_name[i] 
      
      # Revisión para el volumen
      if pd.isna(STR_V): STR_V = ''
      
      
      # Crear Clasificacion
      print(STR, STR_V, STR_C)
      STR_clas = clas_maker(STR, STR_V, STR_C)

      # Revision de Caso con Nan
      if pd.isna(STR):
        lista_Raros.append({"indice": i, "cadena": 'NAN',
                  "titulo": STR_limit(STR_NAME), "c_barras": CB_STR})
        CE += 1
      else:
        if 'LX' in STR: 
          char = 'LX'  # Para casos con XL
          STR = STR_cutter(STR, char)
        elif 'MAT' in STR: 
          char = 'MAT' # Para casos con MAT COM
          STR = STR_cutter(STR, char)
        
        
        if 'V.' in STR or 'C.' in STR:
          lista_Raros.append({"indice": i, "cadena": STR_clas,
                    "titulo": STR_limit(STR_NAME, 25), "c_barras": CB_STR})
          CE += 1
        else:
          if analisisCasosIdeales(STR, STR_C, STR_V, i, lista_Dic, STR_clas, codify):
            CN += 1
          else:
            lista_Raros.append({"indice": i, "cadena": STR_clas,
                      "titulo": STR_limit(STR_NAME, 25), "c_barras": CB_STR})
            CE += 1
    
    
    if reporte[1] == 1 or reporte[2] == 1:
      
      lista_Dic, maxlen_All = limpiarLista(lista_Dic,llaves)
      lista_Dic = estandarizarLista(lista_Dic, maxlen_All[0], maxlen_All[1], maxlen_All[2], maxlen_All[3], llaves)
      # Detectar casos raros
      # Ordenando Lista
      lista_ORD = []
      #for elem in lista_Dic:
      #    print(elem)
      #print('\n\n\n')
      lista_ORD = sorted(lista_Dic, key=lambda llave : llave[llaves[0]])
      lista_ORD = ordenarLista(lista_ORD,llaves,0)
    
    
    if reporte[1] == 1:
      data_frame = prepararExcel(dataExcel[key], lista_ORD)
      escribirExcel(data_frame,key,writer)
    
    
    if reporte[2] == 1:
      prepararErrorExcel(lista_ORD, lista_Dic, Data_name, order_file)
    
    
    if reporte[0] == 1:
      report_file.write('='*55 + '\n')
      report_file.write('\t Reporte de ' + key + '\n')
      report_file.write('\n')
      report_file.write('Archivo Utilizado:\n')
      report_file.write(Nombre + '\n')
      report_file.write('='*55 + '\n')
      report_file.write('\n')
      imprimirResultados(CN, CLX, CMAT, CV, CE, CP, len_Data, report_file)
      if lista_Raros == []:
        report_file.write('='*55 + '\n')
        report_file.write('\t Sin Casos Sin Estandar LC' + '\n')
        report_file.write('='*55 + '\n')
      else:
        report_file.write('NOTA:\n')
        report_file.write('En el archivo: ' + str(txt_path2) + ' encontraras los codigos de barra\n')
        report_file.write('para cargarlos en una lista de Sierra.' + '\n')
        report_file.write('\n\n')
        imprimirLista(lista_Raros, 'Items con Estandar LC Incorrecto',report_file)
        for elem in lista_Raros: CB_file.write(elem["c_barras"] + '\n')
      report_file.write('\n\n')
  if reporte[2] == 1: order_file.close()
  if reporte[1] == 1: writer.save()
  if reporte[0] == 1: 
    report_file.close()
    CB_file.close()
  return True



def cargar_etiquetas(path: str):
  #? Acceder al archivo excel y extraer la columna Clasificación, Volumen y Copia
  #* Tomamos los datos del excel
  excel_data = cargarExcel(path)
  llaves_excel_data = list(excel_data)
  salida_etiquetas = []
  salida_dicc = []
  for key in llaves_excel_data:
    # * Cargamos listas de clasificacion, Volumen y Copia
    clas_data,vol_data,cop_data,name_data,codb_data = cargarDatos(excel_data[key])
    
    # TODO revisar esta implementación
    # Checar si no tenemos errores
    if clas_data[0] == False: 
      print('Error en obtener info')
      continue

    for i in range(len(clas_data)):
      STR_clas = clas_data[i]       # Tiene la clasificación incompleta del libro
      STR_cop = str(cop_data[i])    # Contiene la copia del libro
      STR_vol = vol_data[i]         # Contiene el volumen del libro      
      
      # Revisión para el volumen
      if pd.isna(STR_vol): STR_vol = ''
      
      # Revision de Caso con Nan
      if pd.isna(STR_clas):
        salida_etiquetas.append(['NAN', 'NO', 'APLICA', 'False'])
        salida_dicc.append({'clasi': 'NAN', 'copia': STR_cop, 'volum': STR_vol})
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
        salida_dicc.append({'clasi': STR_clas, 'copia': STR_cop, 'volum': STR_vol})
        continue

      # * Revisar si tiene error de estandar
      if revisarSep(STR_clas) and revisarPipeB(STR_clas):
        pos_div, sum = buscarPIPE(STR_clas)
        pipe_a_str = STR_clas[:pos_div]
        pipe_b_str = STR_clas[pos_div+sum:]
        salida_etiquetas.append([STR_clas, pipe_a_str, pipe_b_str, 'True'])
        salida_dicc.append({'clasi': STR_clas, 'copia': STR_cop, 'volum': STR_vol})
      else:
        salida_etiquetas.append([STR_clas_f, 'NO', 'APLICA', 'False'])
        salida_dicc.append({'clasi': STR_clas, 'copia': STR_cop, 'volum': STR_vol})
  return salida_etiquetas, salida_dicc  


if __name__ == '__main__':
  #archivo = "C:/00_UniversidadTec/10_SextSemestre/01_SB/Excel/B.xlsx"
  excel = 'Para ordenar-Caso HB 3717_ 1-06-2022'
  archivo = "C:/Users/EQUIPO/Desktop/" + excel + ".xlsx"
  carpeta = "C:/Users/EQUIPO/Desktop"
  nombre = 'Reto'
  reporte = [1,1,1]
  print(main_program(archivo,carpeta,nombre,reporte,0))