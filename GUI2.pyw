
import numpy as np
import PySimpleGUI as sg

import main_inter_functions as mainif
import pop_ups as pop
import string_helper as sh

#* Tema principal de las ventanas
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

# * Configuración de la tabla
colum = ["Clasificación", "PIPE_A", "PIPE_B", "STATUS"]
col_width = [25, 15, 15, 10]
col_just = ['c', 'l', 'l', 'c']

# TODO Agregar Ventana de Configuracion

#? Menu superior de opciones
menu_opciones = [
  ['Programa', ['Salir']],
  ['Ayuda', ['Tutoriales','Licencia','Acerca de...']],
]


def ventana_principal():
  # ! Variables del programa no Modificar
  # Variables para guardar rutas de archivos
  ruta_archivo = ""
  ruta_folder = ""

  # Manejo Principal de Tabla
  tabla_principal = []
  main_dicc = {}
  row_color_array = []

  # Manejo de datos de los libros para modificar
  tabla_datos = []
  tabla_modify = []
  
  # Variables para manejo de modificacion
  modify_flag = False
  modify_index = 0
  modify_status = ""

  # ? Bandera de status_clas
  status_clas_flag = False

  #? Layout para cargar archivo de Excel
  excel_layout = [
    [
      sg.FileBrowse(
        'Abrir', size=(7,1), font=('Open Sans', 12),
        file_types=(('Excel File','*.xlsx'),('Todos los archivos','*.*')), 
      ),
      sg.In(
        default_text= ruta_archivo, size=(50,1), 
        key='EXCEL_FILE', font=('Open Sans', 9), justification='c'
      )
    ],
    #* Abrir Carpeta y Ruta
    [
      sg.FolderBrowse('Guardar', font=('Open Sans', 12)), 
      sg.In(
        default_text= ruta_folder, size=(50,1), 
        key='FOLDER', font=('Open Sans', 9), justification='c'
      )
    ],
    [sg.Button('Cargar', font=('Open Sans', 12, 'bold'))],
  ]

  #? Layout de la columna izquierda
  layout_izq = [
    #* Titulo de la Aplicación
    [sg.Image(filename='Assets/LogoTecResize.png', background_color='#FFFFFF')],
    [sg.Text(text='Intercalador', font=('Open Sans', 20, 'bold', 'italic'), background_color='#FFFFFF')],
    [sg.Text(text="Rellene los siguientes parametros:", font=("Open Sans", 14, "bold"), background_color="#FFFFFF", justification="c",)],
    [sg.HorizontalSeparator(pad=(0,(30,20)))],
    [sg.Frame('', layout=excel_layout, background_color='#FFFFFF', element_justification='r')],
    [sg.HorizontalSeparator(pad=(0,(20,20)))],
    # Nombre del archivo de salida
    [
      sg.Text(text='Nombre', font=('Open Sans', 14, 'bold'),background_color='#FFFFFF'),
      sg.In(size=(25,1), key='NAME', font=('Open Sans', 12), justification='c')
    ],
    #* Casillas de opciones
    [
      sg.Checkbox(
        'Reporte', 'G1', 
        key='REPORT', 
        font=('Open Sans', 14), 
        background_color='#FFFFFF'
        ),
      sg.Checkbox(
        'Orden Instrucciones', 'G1', 
        key='EXCEL_ERR_ORD', 
        font=('Open Sans', 14), 
        background_color='#FFFFFF'
        ),
      sg.Checkbox(
        'Excel Orden', 'G1', 
        key='EXCEL_ORD', 
        font=('Open Sans', 14), 
        background_color='#FFFFFF'
        ),
    ],
  ]

  #? Layout Tabla de la columna derecha
  layout_der = [
    [sg.Text(text="Lista de Clasificaciones a Imprimir", background_color="#FFFFFF", font=("Open", 16, "bold", "italic"),)],
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
    [sg.Button("Ejecutar", font=("Open Sans", 12, "bold"))],
  ]


  main_layout = [
    [sg.Menu(menu_opciones, tearoff=False)],
    [
      sg.Column(layout_izq, background_color="#FFFFFF", element_justification="c", pad=0 ),
      sg.VerticalSeparator(color="#000000", pad=(5, 0)),
      sg.Column( layout_der, background_color="#FFFFFF", element_justification="c", pad=0 ),  
    ]
  ]

  window = sg.Window('Intercalador', main_layout, element_justification='l', icon='Assets/book_icon.ico')

  while True:
    event,values = window.read()
    # print('-'*50)
    # print(f'Eventos que suceden {event}')
    # print(f'Valores guardaros {values}')
    # print('-'*50 + '\n')
    if event in (sg.WINDOW_CLOSED, 'Exit', 'Salir'): break
    
    # * Cargar Datos a la tabla
    elif event == 'Cargar':
      ruta_archivo = values["EXCEL_FILE"]
      ruta_folder = values["FOLDER"]
      
      # Checar si se tiene un archivo excel
      if len(ruta_archivo) == 0:
        pop.warning_excel_file()
        continue
      
      # Checar si se tiene una carpeta para guardar
      if len(ruta_folder) == 0:
        pop.warning_folder()
        continue
      
      # Sacar datos de clasificacion de etiquetas
      temp_etiquetas, excel_flag = mainif.generar_etiquetas_libros(ruta_archivo)
      # Sacamos la tabla de titulo de libro y de QRO
      temp_informacion = mainif.generar_informacion_libros(ruta_archivo)  

      # ? Se cargaron etiquetas
      if not temp_etiquetas[0]:
        pop.error_excel_file()
        continue

      # ? Algunas etiquetas tienen errores
      if excel_flag: pop.warning_excel_file_data_error()

      # * Generamos la tabla de datos para el Excel
      for ind in range(len(temp_etiquetas)):
        status = temp_etiquetas[ind][3]
        main_dicc[len(tabla_principal) + ind] = status
        if status == "False": row = ((len(tabla_principal) + ind), "#F04150")
        else: row = ((len(tabla_principal) + ind), "#32A852")
        row_color_array.append(row)

      #  * Concatenamos los nuevos datos a los antiguos
      if len(tabla_principal) != 0:
        tabla_principal = np.concatenate((np.array(tabla_principal), np.array(temp_etiquetas)), axis=0)
        tabla_principal = tabla_principal.tolist()

        tabla_datos = np.concatenate((np.array(tabla_datos), np.array(temp_informacion)), axis=0)
        tabla_datos = tabla_datos.tolist()
      # ? No tenemos aun datos en la tabla 
      else: 
        tabla_principal = temp_etiquetas
        tabla_datos = temp_informacion
      
      window["TABLE"].update(values=tabla_principal, row_colors=row_color_array)

    # * Eventos dentro de la tabla
    if event == "TABLE":
      if values["TABLE"] != []:
        index_value = int(values["TABLE"][0])  # * elemento a seleccionar
        status = main_dicc[index_value]  # * Revisar el status del elemento

        # * Seleccionar casilla para modfiicar
        if status == "False" and not modify_flag:
          # Tomar datos de la casilla
          modify_flag = True
          modify_index = index_value
          # Modificar casilla visualmente
          main_dicc[index_value] = "Modify"
          tabla_principal[index_value][3] = "Modify"
          row_color_array[index_value] = (int(index_value), "#E8871E")

        # * Quitar casilla de modificar
        elif status == "Modify":
          main_dicc[index_value] = "False"
          tabla_principal[index_value][3] = "False"
          row_color_array[index_value] = (int(index_value), "#F04150")
          modify_flag = False

      window["TABLE"].update(values=tabla_principal, row_colors=row_color_array)
    
    if event == "Modificar" and modify_flag == True:
      # * Vamos a abrir una nueva pantalla para modificar el texto
      # Manda llamar la ventana para modificar
      mod_output, mod_data = ventana_modify(
        STR_clas_f=tabla_principal[modify_index][0], 
        STR_clas=tabla_datos_principal[modify_index]['clasi'],
        volumen=tabla_datos_principal[modify_index]['volum'], 
        copia=tabla_datos_principal[modify_index]['copia'],
        name= tabla_datos_principal[modify_index]['titulo'],
        cb=tabla_datos_principal[modify_index]['cb']
      )  
      
      #* Se checa si se realizaron cambios
      if mod_output == []: continue 
      
      # Agregamos elemento a una tabla de modificaciones
      mod_title = tabla_datos_principal[modify_index]['titulo']
      mod_QRO = tabla_datos_principal[modify_index]['cb']
      aux_modify = [STR_limit(mod_title), tabla_principal[modify_index][0], mod_output[0], mod_QRO] 
      tabla_modify.append(aux_modify)

      # * Actualizamos la apariencia del elemento en la tabla
      main_dicc[modify_index] = "True"
      # Actualizar valores en la tabla principal
      tabla_principal[modify_index] = mod_output
      # Actualizar valores en la tabla de datos
      tabla_datos_principal[modify_index] = mod_data

      row_color_array[modify_index] = (int(modify_index), "#32A852")
      modify_flag = False
      
      window["TABLE"].update(values=tabla_principal, row_colors=row_color_array)

    #* Ejecutar el programa
    elif event == 'Ejecutar':
      # ? Checar si se ha puesto un archivo
      if values['EXCEL_FILE'] == '':
        pop_warning_excel_file()
        continue
      
      if values['FOLDER'] == '':
        pop_warning_folder()
        continue
      
      if values['NAME'] == '':
        pop_warning_name()
        continue
      
      if values['REPORT'] + values['EXCEL_ORD'] + values['EXCEL_ERR_ORD'] == 0:
        pop_warning_option()
        continue
      
     # * Checar si existe algun elemento erroneo
      for ind in range(len(tabla_principal)):
        if main_dicc[ind] == 'False':
          status_clas_flag = True
          break
      
      if status_clas_flag:
        status_clas_flag = False
        pop_warning_clas()
        continue
      
      prog_config = [values['REPORT'],values['EXCEL_ORD'],values['EXCEL_ERR_ORD']]
      prog_status = inter.main_posible(
        data=tabla_datos_principal, excel_file=values['EXCEL_FILE'],
        folder_path=values['FOLDER'], name_file=values['NAME'],
        report_config=prog_config, modif_list=tabla_modify
      )
      if prog_status: pop_success_program()
      else: pop_error_excel_file()
    
    elif event == 'Licencia': pop_info_license()
    
    elif event == 'Acerca de...': pop_info_about()

  window.close()


if __name__ == '__main__':
  ventana_principal()