# Editor: Jesus Talamantes Morales
# Fecha Ultima Mod: 16 de Julio 2024
# Versión implementando objetos
################################################

#?#********** VARIABLES CONTROL DE VERSIONES **********#
ALPHA = 0
FUNCIONALIDAD = 7
BUGS = 0
VERSION = f'{ALPHA}.{FUNCIONALIDAD}.{BUGS}'

import os
import re
import sys

import PySimpleGUI as sg

import main_inter_functions as mainif
import pop_ups as pop
import ticket_maker as ticket
from managers import ManejoTabla
from support_windows import VentanaModificar

#? Tema principal tipo Tec para las ventanas
sg.LOOK_AND_FEEL_TABLE['MyCreatedTheme'] = {
  'BACKGROUND': '#3016F3',
  'TEXT': '#000000',
  'INPUT': '#DEE6F7',
  'TEXT_INPUT': '#000000',
  'SCROLL': '#DEE6F7',
  'BUTTON': ('#000000', '#FFFFFF'),
  'PROGRESS': ('#DEE6F7', '#DEE6F7'),
  'BORDER': 2, 'SLIDER_DEPTH': 0,
  'PROGRESS_DEPTH': 0,
}
sg.theme('MyCreatedTheme')

#? Menu superior de opciones
menu_opciones = [
  ['Programa', ['Guardar','Salir']],
  ['Ayuda', ['Tutoriales','Licencia','Acerca de...']],
]

#?#********** Función apoyo para relative path *********#
def resource_path(relative_path):
  """ Get absolute path to resource, works for dev and for PyInstaller """
  try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

class VentanaGeneral:
  """ Ventana General del Programa """
  titulo_ventana = 'INTERCALADOR'
  def __init__(self) -> None:
    self.ruta_archivo = ''
    self.table_manager = ManejoTabla()

  #? CREACION de la Ventana. ***********************
  def left_layout(self):
    """ Layout de columna izquierda del programa

    Llaves que Maneja
    -----------------
    UPLOAD : Boton para escoger un archivo excel
    EXCEL_TEXT : Texto del nombre del archivo de excel
    Cargar : Boton para cargar el archivo de excel
    NAME : Nombre del archivo de salida
    REPORT : Selecciona el reporte del archivo
    EXCEL_INSTRUCT : Selecciona el generar instrucciones de libros
    EXCEL_ORD : Selecciona un generar un excel ordenado
    FOLDER : Ruta del folder de salida
    EXCEL_FILE : Ruta del archivo de excel
    Abrir : Boton de activacion para busqueda del archivo excel

    Llaves que Hereda
    -----------------
    Niguna llave es heredada de otra funcion o clase
    """

    #?#********* LAYOUT PARA SELECCIONAR EL ARCHIVO DE EXCEL #?#*********
    text_format = {
      'font':("Open Sans", 14, "italic"), 
      'background_color':"#FFFFFF",
      'justification':"c",
    }
    ruta_excel = "Sin Archivo" if self.ruta_archivo == "" else self.ruta_archivo.split("/")[-1]    
    SELECCIONAR_ARCHIVO = [
      [sg.Button(
        image_source=resource_path('Assets/subir_icon.png'), 
        image_subsample=5, border_width=0, key='UPLOAD'
      )],
      [sg.Text(size=(25,1), text=ruta_excel, key="EXCEL_TEXT", **text_format)],
      [sg.HSep()], # Separador horizontal
      [sg.Button("Cargar", font=("Open Sans", 14, 'bold'))],
    ]

    #?#********* LAYOUT OPCIONES DEL PROGRAMA #?#*********
    text_format = {
      'font':('Open Sans', 14, 'bold'),
      'background_color':'#FFFFFF',
    }
    option_format = {
      'font':('Open Sans', 14),
      'background_color':'#FFFFFF',
    }

    SELECCIONAR_OPCIONES = [
      #* Opciones del Programa
      [sg.Checkbox('Reporte', 'G1', key='REPORT', **option_format)],
      [sg.Checkbox('Excel Orden', 'G1', key='EXCEL_ORD', **option_format)],
      # Opcion en desarrollo invisible
      # [sg.Checkbox('Orden Instrucciones', 'G1', key='EXCEL_INSTRUCT', visible=False, **option_format)],
    ]

    #?#********* LAYOUT GENERAL DE COLUMNA IZQUIERDA #?#*********
    title_format = {
      'font':("Open Sans", 20, "italic", 'bold'), 
      'background_color':"#FFFFFF",
      'justification':"c",
    }
    text_format = {
      'font':("Open Sans", 14, "bold"), 
      'background_color':"#FFFFFF",
      'justification':"c",
    }    
    frame_format = {
      'background_color':"#FFFFFF",
    }
    GENERAL_LAYOUT = [
      #* Logo del Tec de Monterrey
      [sg.Image(filename=resource_path("Assets/LogoTecResize.png"), background_color='#FFFFFF')],
      #* Titulo de la aplicacion y texto de pantalla
      [sg.Text(text=self.titulo_ventana, **title_format)],
      [sg.Text(text='Rellene los siguiente parametros:', **text_format)],
      
      #* Seleccion de archivo de Excel
      [sg.HSep(pad=(0,(0,10)))], # Separador 
      [
        sg.Frame("",layout=SELECCIONAR_ARCHIVO, border_width=0, element_justification="c", **frame_format),
        sg.Frame("",layout=SELECCIONAR_OPCIONES, border_width=0, element_justification="l",**frame_format)
      ],
      #* Seleccion de opciones del programa
      [sg.HSep(pad=(0,(10,20)))], # Separador 
      #* Nombre del Archivo de Salida
      [
        sg.Text(text='Nombre', **text_format),
        sg.In(size=(25,1), key='NAME', **text_format)
      ],

      
      #* Layout Invisible para guardar el archivo
      [
        sg.Input(key="FOLDER", visible=False),
        sg.FolderBrowse("Guardar", target='FOLDER', visible=False),
      ],
      
      #* Layout Invisible para escoger archivo de excel
      [
        sg.In(key="EXCEL_FILE", visible=False),
        sg.FileBrowse("Abrir", target='EXCEL_FILE',visible=False, file_types=(("Excel Files", "*.xlsx"),)),
      ],
    ]
    return GENERAL_LAYOUT
  def table_layout(self):
    """ Layout columna izquierda del programa
    
    LLaves que Maneja
    -----------------
    TABLE : (Tabla) Manejo general de la tabla
    Modificar : (Tabla/ Click Derecho) Modificar una etiqueta de la tabla
    SELECT-ALL : (Boton) Seleccionar todas las etiquetas
    LIMPIAR : (Boton) Reiniciar todo el programa
    DESELECT-ALL : (Boton) Para deseleccionar todas las etiquetas
    EXPORTAR : (Boton) Lanzar la siguiente parte del programa
    
    """
    #?#********** DEFINIR VARIABLES UTILIZADAS #?#**********
    # * Configuración de la tabla
    colum = ["Clasificación", "PIPE_A", "PIPE_B", "STATUS"]
    col_width = [25, 15, 15, 10]
    tabla_principal = self.table_manager.tabla_principal
    row_color_array = self.table_manager.formato_tabla
    boton_font = {'font':("Open Sans", 14),}
    LAYOUT = [
      [sg.Text(text="Lista de Etiquetas", background_color="#FFFFFF",font=("Open", 18, "bold", "italic"),)],
      [
        sg.Table(
          values=tabla_principal,
          headings=colum,
          font=("Open Sans", 9),
          col_widths=col_width,
          row_height=25,
          num_rows=15,
          auto_size_columns=False,
          display_row_numbers=True,
          justification="l",
          expand_y=False,
          enable_events=True,
          right_click_menu=["Etiqueta", ["Modificar"]],
          alternating_row_color="#FFFFFF",
          background_color="#FFFFFF",
          header_border_width=2,
          row_colors=row_color_array,
          key="TABLE",
        )
      ],
      [
      sg.Button("Ejecutar", font=("Open Sans", 14, "bold", "italic")),
      # sg.Text(text="0/0", background_color="#FFFFFF", font=("Open", 16, "bold", "italic"), key='PAGE'),
      sg.Button("Limpiar", font=("Open Sans", 14)),
      sg.Button("Actualizar", visible=False)
      ],
    ]
    return LAYOUT
  def create_layout(self):
    """ Crea el layout principal para esta ventana """
    colum_format = {
      'background_color':"#FFFFFF", 
      'element_justification':"c", 
      'pad':0
    }
    COL_IZQ_LAYOUT = self.left_layout()
    COL_DER_LAYOUT = self.table_layout()
    LAYOUT = [
      [
        sg.Column(COL_IZQ_LAYOUT, **colum_format),
        sg.VSep(pad=(5, 0)),
        sg.Column(COL_DER_LAYOUT, **colum_format),
      ],
    ]
    return LAYOUT
  
  def create_window(self):
    """ Genera un Objeto tipo Ventana de PySimpleGUI """
    LAYOUT = self.create_layout()
    MAIN_LAYOUT = [
      #* Menu superior de la APP
      [sg.Menu(menu_opciones, tearoff=False)],
      [sg.Frame("",layout=LAYOUT, background_color='#FFFFFF', element_justification='c')],
    ]
    
    window = sg.Window(self.titulo_ventana, MAIN_LAYOUT, element_justification="c", icon=resource_path("Assets/book_icon.ico"))  
    return window
  
  #? FUNCIONAMIENTO PRINCIPAL DE LA VENTANA ***********************
  def run_window(self, window):
    #? MANEJO DE VARIABLES
    modify_object = {
      'INDEX': 0,
      'STATUS': 'XXXX',
      'FLAG': False,
    }
    
    #? LOOP PRINCIPAL
    while True:
      event, values = window.read()
      self.show_window_events(event, values)
      #? ******** FUNCIONALIDAD BASICA VENTANA  ***************
      #* Cerrar la aplicación
      if event in (sg.WINDOW_CLOSED, "Exit", "__TIMEOUT__", 'Salir'):
        #* Ver si quiere guardar el archivo
        self.guardar_programa()
        window.close()
        return
      #* Mostrar licencia del Programa
      elif event == "Licencia":
        pop.info_license()
      #* Mostrar version del Programa
      elif event == "Acerca de...":
        pop.info_about(VERSION)
      #* Guardar archivo
      elif event == 'Guardar':
        self.guardar_programa(True)
      
      #? ********** FUNCIONALIDAD CARGAR ARCHIVO *******************
      #* Seleccionar archivo de Excel
      elif event == 'UPLOAD':
        self.seleccionar_excel(window)
      # * Cargar excel completo de un archivo
      elif event == "Cargar":
        self.cargar_excel(window)
      
      #?#********** FUNCIONALIDAD DE TABLA **********#?#
      # * Reiniciar programa por completo
      elif event == "Limpiar":
        self.reset_window(window)
        bandera_modificar = False
      # * Eventos relacionados con clicks en la tabla
      elif event == "TABLE":
        modify_object = self.table_control(window, values, modify_object)
      # * Modificar un elemento seleccionado
      elif event == "Modificar" and bandera_modificar is True:
        bandera_modificar = self.modificar_elemento(window, index_modificar)

      # TODO Revisar la parte de implementar las funcionalidades extras
      elif event == 'Ejecutar':
        self.ejecutar_programa(window, values)
      elif event == 'Imprimir' and bandera_modificar == True and estatus_modificar != 'False':
        continue
        ruta_folder = values['FOLDER']
        if not ruta_folder:
          pop.warning_folder()
          continue

        # Crear la lista de datos
        encabezado = tabla_datos[modify_index]['encabeza']
        clasif = tabla_datos[modify_index]['clasif']
        volumen = tabla_datos[modify_index]['volumen']
        copia = tabla_datos[modify_index]['copia']

        dict_format = {'HEAD':encabezado, 'CLASS':clasif, 'VOL':volumen, 'COP':copia}

        # print(dict_format)
        # Individual Configuration Parameters
        ICP = {'PW':0, 'PH':0, 'TW':4.8, 'TH':3.7, 'PR':0, 'PC':0} 
        ticket.ticket_maker_main([dict_format], str(modify_index), ruta_folder, ICP, (None,None))

        # * Actualizamos la apariencia del elemento en la tabla
        main_dicc[modify_index] = "True"
        tabla_principal[index_value][3] = 'Printed'
        row_color_array[modify_index] = (int(modify_index), "#7699D4")
        modify_flag = False

        window["TABLE"].update(values=tabla_principal, row_colors=row_color_array)
      elif event == 'Actualizar':
        continue
        # * Realizar proceso de actualización a nueva hoja
        index_hoja += 1
        if index_hoja > len(hojas_excel)-1: 
          pop.success_program()
          continue
        
        main_dicc = {}
        row_color_array = []
        tabla_modify = []
        main_dataframe = {}
        tabla_datos = []
        tabla_principal = []
        
        # print('Vamos a actualizar datos')
        # print(index_hoja, hojas_excel[index_hoja])

        hoja_actual = hojas_excel[index_hoja]
        main_dataframe = excel_completo[hoja_actual]
        # print(main_dataframe)
        # Sacar datos de clasificacion de etiquetas
        temp_etiquetas = mainif.generar_etiquetas_libros(main_dataframe)
        # Sacamos la tabla de titulo de libro y de QRO
        temp_informacion = mainif.generar_informacion_libros(main_dataframe)  

        # ? Se cargaron etiquetas
        if not temp_etiquetas[0]:
          pop.error_excel_file()
          continue

        # * Generamos la tabla de datos para el Excel
        for ind in range(len(temp_etiquetas)):
          status = temp_etiquetas[ind][3]
          main_dicc[len(tabla_principal) + ind] = status
          if status == "False": row = ((len(tabla_principal) + ind), "#B00020")
          else: row = ((len(tabla_principal) + ind), "#FFFFFF")
          row_color_array.append(row)

        #  * Concatenamos los nuevos datos a los antiguos
        tabla_principal = temp_etiquetas
        tabla_datos = temp_informacion
        
        window["TABLE"].update(values=tabla_principal, row_colors=row_color_array)
        window["PAGE"].update(f'{index_hoja+1}/{len(hojas_excel)}')
  #? MOSTRAR ELEMENTOS DEL VENTANA **********
  def show_window_events(self, event, values):
    print(f"""
      Imprimiendo Eventos de Suceden
      {'-'*50}
      Eventos que suceden {event}
      Valores guardados {values}
      {'-'*50}
    """)

  #? CARGAR ELEMENTOS DESDE EXCEL *************
  def seleccionar_excel(self, window):
    window["Abrir"].click() # Activar funcionalidad para abrir archivo
    self.ruta_archivo = window['EXCEL_FILE'].get() # Actualizar ruta del archivo
    # Actualizar nombre del archivo de la ventana
    nombre_archivo = self.ruta_archivo.split('/')[-1] if len(self.ruta_archivo) != 0 else 'Sin Archivo'
    window["EXCEL_TEXT"].update(nombre_archivo)
  
  def cargar_excel(self, window):
    # Revisar que tengamos un archivo excel
    if len(self.ruta_archivo) == 0:
      pop.warning_excel_file()
      return False

    # Crear tabla de datos    
    self.table_manager.crear_tabla(self.ruta_archivo)
    #* Actualizar apariencia de la tabla
    window["TABLE"].update(
      values=self.table_manager.tabla_principal, 
      row_colors=self.table_manager.formato_tabla
    )

  #? FUNCIONALIDAD MANEJO DE TABLA *************
  def reset_window(self, window):
    """ Reiniciar todos los valores de la tabla que se trabaja """
    self.ruta_archivo = ''
    window["EXCEL_TEXT"].update('Sin Archivo')
    window["NAME"].update('')
    self.table_manager.reset_tabla()
    
    #* Actualizar tabla
    window["TABLE"].update(
      values=self.table_manager.tabla_principal, 
      row_colors=self.table_manager.formato_tabla
    )

  def table_control(self, window, values, modify_object):
    # Forma de la estructura modify_object.
    # modify_object = { 'INDEX': 0, 'STATUS': 'XXXX', 'FLAG': False,}
    #* Manejar excepcion con respecto a datos inexistentes
    if len(values["TABLE"]) == 0: return modify_object
    
    index = int(values["TABLE"][0])  # * elemento a seleccionar
    estatus = self.table_manager.lista_libros[index].estatus
    print(f'[DEBUG] Libro seleccionado. Numero {index}.')
    print(f'[DEBUG] Libro seleccionado. Estatus {estatus}.')

    # * Seleccionar casilla para modificar
    if estatus in ("Valid", "Error") and modify_object['FLAG'] is False:
      #* Actualizar datos de modificacion
      modify_object['STATUS'] = estatus
      modify_object['FLAG'] = True
      modify_object['INDEX'] = index
      #* Modificar elemento visualmente
      self.table_manager.actualizar_estatus_elemento(index, "Modify")

    # * Quitar casilla de modificar
    elif estatus == "Modify":
      #? Cambiar elemento modificado/seleccionado a Normal
      if modify_object['STATUS'] == "Valid":
        self.table_manager.actualizar_estatus_elemento(index, "Valid")
      #? Cambiar elemento modificado/error a Error
      elif modify_object['STATUS'] == "Error":
        self.table_manager.actualizar_estatus_elemento(index, "Error")
      modify_object['FLAG'] = False

    #* Actualizar tabla
    window["TABLE"].update(
      values=self.table_manager.tabla_principal, 
      row_colors=self.table_manager.formato_tabla)
    
    print(f"""
      [DEBUG] Objeto Modificar:
      Indice Modificado:  {modify_object['INDEX']}
      Estatus Modificado: {modify_object['STATUS']}
      Bandera Modificar:  {modify_object['FLAG']}
    """)
    return modify_object

  def modificar_elemento(self, window, modify_index):
    #* Sacar los datos de esa etiqueta
    libro_a_modificar = self.table_manager.lista_libros[modify_index]
    clasif_libro_a_modificar = libro_a_modificar.etiqueta.clasif_completa
    #* Mandar llamar ventana modificar
    VM = VentanaModificar(libro_a_modificar)
    estatus, libro_modificado = VM.run_window()
    del VM

    print('Se modifico? ', estatus)
    #* Checar si hubieron cambios
    if estatus is False: return True
    
    # * Agregamos elemento a una tabla de modificaciones
    self.table_manager.agregar_elemento_modificado(modify_index, libro_modificado, clasif_libro_a_modificar)

    # * Actualizar valores de tabla de datos
    self.table_manager.actualizar_elemento(modify_index, libro_modificado)

    # * Cambiamos la apariencia del elemento en la tabla
    self.table_manager.actualizar_estatus_elemento(modify_index, 'Valid')
    
    #* Actualizar apariencia de la tabla
    window["TABLE"].update(
      values=self.table_manager.tabla_principal, 
      row_colors=self.table_manager.formato_tabla
    )
    return False

  #? EJECUTAR PROGRAMA ***************************
  def ejecutar_programa(self, window, values):
    #* Revisar archivo de Excel
    if len(self.ruta_archivo) == 0: 
      pop.warning_excel_file()
      return False 
    nombre_archivo = self.ruta_archivo.split('/')[-1]

    # * Checar si existe algun elemento erroneo
    if self.table_manager.revisar_tabla() is False:
      pop.warning_clas()
      return False
    
    #* Revisar nombre archivo salida
    nombre_salida = window['NAME'].get()
    if len(nombre_salida) == 0:
      pop.warning_name()
      return False
    
    #* Proceso para seleccionar un folder de guardado
    window['Guardar'].click()
    ruta = window['FOLDER'].get()
    if len(ruta) == 0: return False
    
    #* Revisar que se haya seleccionado una opcion
    if values['REPORT'] + values['EXCEL_ORD'] + values['EXCEL_INSTRUCT'] == 0:
      pop.warning_option()
      return False
    
    #? Crear reporte sobre el archivo
    if values['REPORT']: 
      self.table_manager.crear_reporte_general(ruta, nombre_salida, nombre_archivo)
      # self.table_manager.crear_reporte_modificados(ruta, nombre_salida)
      self.table_manager.crear_reporte_QRO(ruta, nombre_salida)

    #? Ordenar tabla del programa
    if values['EXCEL_ORD'] or values['EXCEL_INSTRUCT']:
      orden_de_libros = self.table_manager.ordenar_libros()
      self.table_manager.organizar_libros_tabla(orden_de_libros)
      #* Actualizar apariencia de la tabla
      window["TABLE"].update(
        values=self.table_manager.tabla_principal, 
        row_colors=self.table_manager.formato_tabla
      )

    #? Crear un archivo de excel ordenado
    if values['EXCEL_ORD']:
      excel_ordenado = self.table_manager.organizar_libros_excel(self.ruta_archivo, orden_de_libros)
      self.table_manager.escribir_excel(ruta, nombre_salida, excel_ordenado)
    
    # * Sección para crear instrucciones ordenar
    if values['EXCEL_INSTRUCT']: 
      pass
    #   lista_retirar, lista_colocar = mainif.instrucciones_ordenar(lista_ordenada, lista_no_ordenada, tabla_datos)
    #   if not lista_retirar[0]: 
    #     window['Actualizar'].click()
    #     continue
    #   ventana_instruc_ordenar(lista_retirar, lista_colocar, hoja_actual, nombre_archivo)

    # window['Actualizar'].click()

  def guardar_programa(self, bypass=False):
    # Revisar si tenemos datos en el programa.
    if self.table_manager.tabla_len == 0:
      print('[INFO] Sin datos que guardar')
      return False
    # Revisar archivo de Excel
    if len(self.ruta_archivo) == 0: 
      print('[INFO] Sin ruta para guardar')
      return False 
    
    if bypass is False:
      if pop.save_file() is False:
        print('[INFO] Anular guardado')
        return False

    # Obtener el nombre del archivo
    nombre_archivo = self.ruta_archivo.split('/')[-1]
    nombre_archivo = re.sub(r'\.xlsx', '', nombre_archivo)
    # Obtener la ruta a la carpeta de guardado
    regex = '/' + nombre_archivo + '.*'
    ruta_folder = re.sub(regex, '', self.ruta_archivo)
    # Crear y actualizar el dataframe del excel
    nombre_archivo = nombre_archivo + '_saved'
    print(f'[DEBUG] Nombre generado {nombre_archivo}')
    print(f'[DEBUG] Ruta Generada {ruta_folder}')
    guardar_df = self.table_manager.guardar_libros_tabla(self.ruta_archivo)
    self.table_manager.escribir_excel(ruta_folder, nombre_archivo, guardar_df)
    print(f'[DEBUG] Archivo Salvado Correctamente')
    return True

def main():
  """ Funcion principal para el manejo de la aplicacion """
  VG = VentanaGeneral()
  VG_window = VG.create_window()
  VG.run_window(VG_window)

if __name__ == '__main__':
  # ventana_principal()
  main()