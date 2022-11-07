import PySimpleGUI as sg

import Main_Intercarlador as inter
from pop_ups import *

version = '6.0'

# Tema principal de las ventanas
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
col_just = ["c", "l", "l", "c"]

#? Manejo Principal del elemento tabla
tabla_principal = []
main_dicc = {}
row_color_array = []


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

#? Layout Principal para el Programa
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

# * Layout tabla general de etiquetas,
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
  # print(event)
  # print("-"*20) 
  # print(values)
  if event in (sg.WINDOW_CLOSED, 'Exit', 'Salir'): break
  #* Cargar Datos a la tabla
  elif event == 'Cargar':
    pass
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
    
    status = inter.main_program(archivo=values['EXCEL_FILE'], carpeta=values['FOLDER'], nombre=values['NAME'], reporte=[values['REPORT'], values['EXCEL_ORD'], values['EXCEL_ERR_ORD']], codify=0)
    if not status: pop_error_excel_file()
    else: pop_success_program()
      
  
  elif event == 'Licencia': pop_info_license()
  
  elif event == 'Acerca de...': pop_info_about()

window.close()
