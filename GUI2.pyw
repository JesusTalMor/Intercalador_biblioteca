import numpy as np
import PySimpleGUI as sg

import Main_Intercarlador as inter
from ApoyoSTRLIST import *
from pop_ups import *

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



# ? Ventanas de apoyo y configuraciones
def ventana_modify(STR_clas_f: str, STR_clas:str, volumen:str, copia:str, name:str, cb:str):
  # Eliminar Volumen y Copia de la clasificación
  volumen = volumen.replace('V.', '') if 'V.' in volumen else volumen
  STR_clas = STR_cutter(STR_clas, 'V.') if 'V.' in STR_clas else STR_clas
  STR_clas = STR_cutter(STR_clas, 'C.') if 'C.' in STR_clas else STR_clas
  add_flag = False

  # * Seccion de Layout de la Ventana
  pipe_a = [
    [sg.Text( text="PIPE A", font=("Open Sans", 14, "bold"), background_color="#FFFFFF", justification="center", pad=5,)],
    [sg.In(default_text="ESPERA", size=(14, 1), font=("Open Sans", 12), justification="center", key="PIPE_A", disabled=True,)],
  ]
  pipe_b = [
    [sg.Text(text="PIPE B", font=("Open Sans", 14, "bold"), background_color="#FFFFFF", justification="center", pad=5, )],
    [sg.In(default_text="MODIFICAR", size=(12, 1), font=("Open Sans", 12), justification="center", key="PIPE_B", disabled=True, )],
  ]
  indi_layout = [
    [sg.Text(text="Modif. Clasificación", font=("Open Sans", 14, "bold"), background_color="#FFFFFF", justification="center",)],
    [sg.In(default_text= STR_clas, size=(28, 1), enable_events=True, key="CLAS", font=("Open Sans", 12), justification="center", pad=(15, 5), )],
    [
      sg.Text(text="VOL", font=("Open Sans", 14, "bold"),background_color="#FFFFFF", justification="center",),
      sg.In(default_text= volumen,size=(2, 1), enable_events=True, key="VOL", font=("Open Sans", 12), justification="center",),
      sg.Text(text="COP", font=("Open Sans", 14, 'bold'), background_color="#FFFFFF", justification="center",),
      sg.In(default_text= copia, size=(2, 1), enable_events=True, key="COP", font=("Open Sans", 12), justification="center",),
    ],
    [
      sg.Column(layout=pipe_a, background_color="#FFFFFF", element_justification="c"),
      sg.VSeperator(),
      sg.Column(layout=pipe_b, background_color="#FFFFFF", element_justification="c"),
    ],
  ]
  layout = [
    [sg.Text(text="Modificar Clasificación", font=("Open Sans", 16, "bold", "italic"), background_color="#FFFFFF", justification="center", pad=(0, (0, 15)),)],
    [sg.Text(text=STR_clas_f, font=("Open Sans", 16, "bold"), background_color="#FFFFFF", justification="center", key="TEXT",)],
    [sg.HorizontalSeparator(color="#000000", pad=(0, (10, 6)))],
    [sg.Frame("",layout=indi_layout, background_color="#FFFFFF", element_justification="c",)],
    [sg.HorizontalSeparator(color="#000000", pad=(0, (6, 10)))],
    [
      sg.Button("Cancelar", font=("Open Sans", 14, "bold")),
      sg.Button("Modificar", font=("Open Sans", 14, "bold")),
    ],
  ]
  main_layout = [
    [sg.Frame("", layout, background_color="#FFFFFF", element_justification="c", pad=0)]
  ]

  # * Creacion de la ventana
  window = sg.Window("Modificar una Etiqueta", main_layout, element_justification="c", icon="Assets/ticket_icon.ico")

  while True:
    event, values = window.read()

    # print('-'*50)
    # print(f'Eventos que suceden {event}')
    # print(f'Valores guardaros {values}')
    # print('-'*50 + '\n')

    if event in (sg.WINDOW_CLOSED, "Exit", "Cancelar"):
      break

    # * Modificar clase
    elif event in ("CLAS",'VOL','COP') :
      if len(str(values["CLAS"])) > 5:
        clas = str(values["CLAS"])
        if revisarSep(clas) and revisarPipeB(clas):
          pos_div, sum = buscarPIPE(clas)
          if pos_div != 0:
            pipe_a_str = clas[:pos_div]
            pipe_b_str = clas[pos_div + sum :]
            window["PIPE_A"].update(pipe_a_str)
            window["PIPE_B"].update(pipe_b_str)
            temp_vol = f'V.{values["VOL"]}' if values["VOL"] != '' else ''
            STR_clas = clas_maker(values["CLAS"], temp_vol, values["COP"])  # Genera la clasificacion completa
            window["TEXT"].update(STR_clas)  # Actualiza la etiqueta en la GUI
            add_flag = True  # ? Bandera Verdadera
        else:
          window["PIPE_A"].update("NO")
          window["PIPE_B"].update("APLICA")
          add_flag = False  # ? Bandera Falsa

    # * Modifica la etiqueta y cierra la ventana
    elif event == "Modificar" and add_flag:
      temp_vol = f'V.{values["VOL"]}' if values["VOL"] != '' else ''
      STR_clas = clas_maker(values["CLAS"], temp_vol, values["COP"])  # Genera la clasificacion completa
      window.close()
      tabla_apariencia = [STR_clas, values["PIPE_A"], values["PIPE_B"], "True"]
      tabla_datos = {'clasi': values['CLAS'], 'copia': values['COP'], 'volum': temp_vol, 'titulo': name, 'cb': cb}

      return tabla_apariencia, tabla_datos
  window.close()
  return []


def main():
  #? Manejo Principal del elemento tabla
  tabla_principal = []
  tabla_datos_principal = []
  main_dicc = {}
  row_color_array = []

  #? Variables para manejo de modificacion
  modify_flag = False
  modify_index = 0

  #? Tabla para manejo de modificaciones
  tabla_modify = []



  #? Menu superior de opciones
  menu_opciones = [
    ['Programa', ['Salir']],
    ['Ayuda', ['Tutoriales','Licencia','Acerca de...']],
  ]

  #? Layout para cargar archivo de Excel
  excel_layout = [
    [
      sg.FileBrowse(
        'Abrir', size=(7,1),
        file_types=(('Excel File','*.xlsx'),('Todos los archivos','*.*')), 
        font=('Open Sans', 12)
        ),
      sg.In(size=(50,1), key='EXCEL_FILE', font=('Open Sans', 9), justification='c')
    ],
    #* Abrir Carpeta y Ruta
    [
      sg.FolderBrowse('Guardar', font=('Open Sans', 12)), 
      sg.In(size=(50,1), key='FOLDER', font=('Open Sans', 9), justification='c')
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
        'Excel Error Ord.', 'G1', 
        key='EXCEL_ERR_ORD', 
        font=('Open Sans', 14), 
        background_color='#FFFFFF'
        ),
      sg.Checkbox(
        'Excel Ord.', 'G1', 
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
    #* Cargar Datos a la tabla
    elif event == 'Cargar':
      # Checar si se tiene un archivo excel
      if values['EXCEL_FILE']  == '':
        pop_warning_excel_file()
        continue
      # Checar si se tiene una carpeta para guardar
      if values['FOLDER'] == '':
        pop_warning_folder()
        continue

      # * Cargar Columna Clasificacion a la tabla
      tabla_aux, tabla_datos = inter.cargar_etiquetas(values['EXCEL_FILE'])

      # * Generamos la tabla de datos para el Excel
      for ind in range(len(tabla_aux)):
        status = tabla_aux[ind][3]
        main_dicc[len(tabla_principal) + ind] = status
        if status == "False": row = ((len(tabla_principal) + ind), "#F04150")
        else: row = ((len(tabla_principal) + ind), "#32A852")
        row_color_array.append(row)

      # ? Se cargaron algunas etiquetas pero otras no contienen información
      # if excel_flag: pop_warning_excel_file_data_error()

      # ? No se cargo ni una etiqueta
      if len(tabla_aux) == 0: 
        pop_error_excel_file()
        continue
      
      # ? Concatenamos los nuevos datos a los antiguos
      if len(tabla_principal) != 0:
        tabla_principal = np.concatenate((np.array(tabla_principal), np.array(tabla_aux)), axis=0)
        tabla_principal = tabla_principal.tolist()

        tabla_datos = np.concatenate((np.array(tabla_datos_principal), np.array(tabla_datos)), axis=0)
        tabla_datos = tabla_datos.tolist()
      # ? No tenemos aun datos en la tabla 
      else: 
        tabla_principal = tabla_aux
        tabla_datos_principal = tabla_datos
      
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
      
      if values['REPORT'] + values['EXCEL_ERR_ORD'] + values['EXCEL_ORD'] == 0:
        pop_warning_option()
        continue
      
      # * Crear reporte de modificaciones
      inter.reporte_modify(tabla_modify, values['FOLDER'])

      inter.crear_diccionario_clas(tabla_datos_principal)
      # status = inter.main_program(
      #   archivo=values['EXCEL_FILE'], carpeta=values['FOLDER'], nombre=values['NAME'], 
      #   reporte=[values['REPORT'], values['EXCEL_ORD'], values['EXCEL_ERR_ORD']], codify=0
      # )
      # if not status: pop_error_excel_file()
      # else: pop_success_program()
    
    elif event == 'Licencia': pop_info_license()
    
    elif event == 'Acerca de...': pop_info_about()

  window.close()


if __name__ == '__main__':
  main()
  # val = ventana_modify(STR_clas_f='Q126.4 E88 1999 V.3', STR_clas='Q126.4 E88 1999', copia='1', volumen='3')
  # print(val)
