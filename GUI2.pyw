
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


def ventana_modificar_clasificacion(clasificacion_completa:str, clasif:str, volumen:str, copia:str, encabezado:str):
  '''Modifica el contenido y parametros de una etiqueta'''
  bandera_agregar = False
  
  # * Actualizar el Volumen a standard
  volumen = volumen[volumen.index('V.') + 2] if 'V.' in volumen else ''

  # * Seccion de Layout de la Ventana
  pipe_a = [
    [
      sg.Text(
        text="PIPE A", 
        font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF", 
        justification="center", 
        pad=5,
      )
    ],
    [
      sg.In(default_text="ESPERA", size=(14, 1), font=("Open Sans", 10),
      justification="center", key="PIPE_A", disabled=True,)
    ],
  ]
  pipe_b = [
    [
      sg.Text(
        text="PIPE B", 
        font=("Open Sans", 12, "bold"),
        background_color="#FFFFFF", 
        justification="center", 
        pad=5,
      )
    ],
    [
      sg.In(default_text="MODIFICAR", size=(12, 1),
      font=("Open Sans", 10), justification="center",
      key="PIPE_B", disabled=True,)
    ],
  ]
  indi_layout = [
    [
      sg.Text(
        text="Modif. Clasificación", 
        font=("Open Sans", 14, "bold"), 
        background_color="#FFFFFF", 
        justification="center",
      )
    ],
    [
      sg.In(
        default_text=clasif, 
        size=(28, 1), 
        enable_events=True,
        key="CLAS",
        font=("Open Sans", 12), 
        justification="center", 
        pad=(15, 5),
      )
    ],
    [
      sg.Text(
        text="Agregar Encabezado",
        font=("Open Sans", 12),
        background_color="#FFFFFF",
        justification="center",
      )
    ],
    [
      sg.In(
        default_text=encabezado, 
        size=(18, 1),
        enable_events=True,
        key="HEAD",
        font=("Open Sans", 10),
        justification="center",
      )
    ],
    [
      sg.Text(
        text="Volumen",
        font=("Open Sans", 12),
        background_color="#FFFFFF",
        justification="center",
      ),
      sg.In(
        default_text=volumen, 
        size=(2, 1),
        enable_events=True,
        key="VOL",
        font=("Open Sans", 10),
        justification="center",
      ),
      sg.Text(
        text="Copia",
        font=("Open Sans", 12),
        background_color="#FFFFFF",
        justification="center",
      ),
      sg.In(
        default_text=copia, 
        size=(2, 1),
        enable_events=True,
        key="COP",
        font=("Open Sans", 10),
        justification="center",
      ),
    ],
    [
      sg.Column(
        layout=pipe_a, 
        background_color="#FFFFFF", 
        element_justification="c"
      ),
      sg.VSeperator(),
      sg.Column(
        layout=pipe_b, 
        background_color="#FFFFFF", 
        element_justification="c"
      ),
    ],
  ]
  layout = [
    [
      sg.Text(
        text="Modificar una Etiqueta",
        font=("Open Sans", 18, "bold", "italic"),
        background_color="#FFFFFF",
        justification="center",
        pad=(0, (0, 15)),
      )
    ],
    [
      sg.Text(
        text=clasificacion_completa,
        font=("Open Sans", 16, "bold"),
        background_color="#FFFFFF",
        justification="center",
        key="TEXT",
      )
    ],
    [sg.HorizontalSeparator(color="#000000", pad=(0, (10, 6)))],
    [
      sg.Frame(
        "",
        layout=indi_layout,
        background_color="#FFFFFF",
        element_justification="c",
      )
    ],
    [sg.HorizontalSeparator(color="#000000", pad=(0, (6, 10)))],
    [
      sg.Button("Cancelar", font=("Open Sans", 14, "bold")),
      sg.Button("Modificar", font=("Open Sans", 14, "bold")),
    ],
  ]
  main_layout = [
    [
      sg.Frame("", layout, background_color="#FFFFFF", element_justification="c", pad=0)
    ]
  ]

  # * Creacion de la ventana
  window = sg.Window("Modificar una Etiqueta", main_layout, element_justification="c", icon="Assets/ticket_icon.ico")

  while True:
    event, values = window.read()
    # print('-'*50)
    # print(f'Eventos que suceden {event}')
    # print(f'Valores guardaros {values}')
    # print('-'*50 + '\n')

    # * Actualizar clasificacion
    clasif = str(values["CLAS"])
    volumen = str(values['VOL'])
    copia = str(values['COP'])
    encabezado = str(values['HEAD'])

    encabezado = encabezado + ' ' if encabezado != '' else ''
    volumen = 'V.' + volumen if volumen not in ('', '0') else ''
    clasificacion_completa = encabezado + sh.creador_clasificacion(clasif, volumen, copia)
    window['TEXT'].update(clasificacion_completa)

    if event in (sg.WINDOW_CLOSED, "Exit", "Cancelar"):
      break

    # * Modificar clase
    elif event == "CLAS":
      if len(str(values["CLAS"])) > 5:
        clasif = str(values["CLAS"])
        if sh.revisar_corte_pipe(clasif) and sh.revisar_pipeB(clasif):
          posicion_corte, diferencia = sh.buscar_pipe(clasif)
          if posicion_corte != 0:
            pipe_a_str = clasif[:posicion_corte]
            pipe_b_str = clasif[posicion_corte + diferencia :]
            window["PIPE_A"].update(pipe_a_str)
            window["PIPE_B"].update(pipe_b_str)
            bandera_agregar = True  # ? Bandera Verdadera
        else:
          window["PIPE_A"].update("NO")
          window["PIPE_B"].update("APLICA")
          bandera_agregar = False  # ? Bandera Falsa

    
    # * Modifica la etiqueta y cierra la ventana
    elif event == "Modificar" and bandera_agregar:
      # clasif = str(values["CLAS"])
      # volumen = str(values['VOL'])
      # copia = str(values['COP'])
      # encabezado = str(values['HEAD'])

      # volumen = 'V.' + volumen if volumen not in ('', '0') else ''
      # clasificacion_completa = encabezado + ' ' + sh.creador_clasificacion(clasif, volumen, copia)

      window.close()
      return [clasificacion_completa, values["PIPE_A"], values["PIPE_B"], "True"], [clasif, volumen, copia, encabezado]

  window.close()
  return [False],[False]


def ventana_principal():
  # ! Variables del programa no Modificar
  # Variables para guardar rutas de archivos
  ruta_archivo = ""
  ruta_folder = ""
  nombre_archivo = ""

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

  # ? bandera para manejo de datos
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
      # TODO Agregar ventana modificacion
      modif_principal, modif_datos = ventana_modificar_clasificacion(
        clasificacion_completa= tabla_principal[modify_index][0],
        clasif= tabla_datos[modify_index]['clasif'],
        copia= tabla_datos[modify_index]['copia'],
        volumen= tabla_datos[modify_index]['volumen'],
        encabezado= tabla_datos[modify_index]['encabeza']
      )
      
      #* Se checa si se realizaron cambios
      if not modif_principal[0] :continue
      
      # Agregamos elemento a una tabla de modificaciones
      title = tabla_datos[modify_index]['titulo']
      cbarras = tabla_datos[modify_index]['cbarras']
      aux_modify = [title, cbarras, tabla_principal[modify_index][0], modif_principal[0]]
      tabla_modify.append(aux_modify)

      # * Actualizamos la apariencia del elemento en la tabla
      main_dicc[modify_index] = "True"
      tabla_principal[modify_index] = modif_principal
      row_color_array[modify_index] = (int(modify_index), "#32A852")
      modify_flag = False

      # * Actualizar valores de tabla de datos
      tabla_datos[modify_index]['clasif'] = modif_datos[0]
      tabla_datos[modify_index]['volumen'] = modif_datos[1]
      tabla_datos[modify_index]['copia'] = modif_datos[2]
      tabla_datos[modify_index]['encabeza'] = modif_datos[3]
      
      window["TABLE"].update(values=tabla_principal, row_colors=row_color_array)

    #* Ejecutar el programa
    elif event == 'Ejecutar':
      # ? Checar si se ha puesto un archivo
      ruta_folder = values['FOLDER']
      ruta_archivo = values['EXCEL_FILE']
      nombre_archivo = values['NAME']

      if ruta_archivo == '':
        pop.warning_excel_file()
        continue
      
      if ruta_folder == '':
        pop.warning_folder()
        continue
      
      if nombre_archivo == '':
        pop.warning_name()
        continue
      
      if values['REPORT'] + values['EXCEL_ORD'] + values['EXCEL_ERR_ORD'] == 0:
        pop.warning_option()
        continue
      
     # * Checar si existe algun elemento erroneo
      for ind in range(len(tabla_principal)):
        if main_dicc[ind] == 'False':
          status_clas_flag = True
          break
      
      # if status_clas_flag:
      #   status_clas_flag = False
      #   pop.warning_clas()
      #   continue
      
      prog_config = [values['REPORT'],values['EXCEL_ORD'],values['EXCEL_ERR_ORD']]
      # TODO Mandar llamar funcion para partir y organizar
      if values['EXCEL_ORD']:
        salida = mainif.separar_atributos_libros(tabla_datos)
        salida, largos = mainif.limpiar_atributos_libros(salida)
        salida = mainif.estandarizar_atributos_libros(salida, largos)
        print(*salida, sep='\n\n')
        print(largos)
        salida_ordenada = mainif.ordenar_libros_atributo(salida)
        print(*salida_ordenada, sep='\n')
        
        # Sección para ordenar
        dataframe_salida = mainif.crear_excel_ordenado(salida_ordenada, tabla_datos, ruta_archivo)
        print(*dataframe_salida, sep='\n')
        mainif.escribir_excel(dataframe_salida, 'Prueba', ruta_folder, nombre_archivo)
      # prog_status = inter.main_posible(
      #   data=tabla_datos_principal, excel_file=values['EXCEL_FILE'],
      #   folder_path=values['FOLDER'], name_file=values['NAME'],
      #   report_config=prog_config, modif_list=tabla_modify
      # )
      pop.success_program()
      # if prog_status: pop_success_program
      # else: pop_error_excel_file()
    
    elif event == 'Licencia': pop.info_license()
    
    elif event == 'Acerca de...': pop.info_about()

  window.close()


if __name__ == '__main__':
  ventana_principal()