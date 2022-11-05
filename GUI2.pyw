import PySimpleGUI as sg
import Main_Intercarlador as inter

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

#? Menu superior de opciones
menu_opciones = [
  ['Programa', ['Salir']],
  ['Ayuda', ['Tutoriales','Licencia','Acerca de...']],
]

#? Layout Principal para el Programa
layout = [
  #* Titulo de la Aplicación
  [
    sg.Text(text='Intercalador', font=('Open Sans', 26, 'bold', 'italic'), background_color='#FFFFFF', pad=((120,20),15)),
    sg.Image(filename='Assets/LogoTecResize.png', background_color='#FFFFFF', pad=((60,20),15))
  ],
  #* Abrir Archivo y Ruta
  [
    sg.FileBrowse('Abrir Archivo', file_types=(('Excel File','*.xlsx'),('Todos los archivos','*.*')), font=('Open Sans', 14), pad=((25,7),5)),
    sg.In(size=(50,1), key='EXCEL_FILE', font=('Open Sans', 14), justification='c', pad=((5,15),5))
  ],
  #* Abrir Carpeta y Ruta
  [
    sg.FolderBrowse('Abrir Carpeta', font=('Open Sans', 14), pad=((25,3),5)), 
    sg.In(size=(50,1), key='FOLDER', font=('Open Sans', 14), justification='c', pad=((5,15),5))
  ],
  #* Nombre el archivo y nombre
  [
    sg.Text(text='Nombre Archivo', font=('Open Sans', 14), pad=((5,7),5),background_color='#FFFFFF'),
    sg.In(size=(25,1), key='NAME', font=('Open Sans', 14), justification='c', pad=((0,15),5))
  ],
  #* Casillas de opciones
  [
    sg.Checkbox('Reporte', 'G1', key='REPORT', font=('Open Sans', 16), background_color='#FFFFFF', pad=((40,20),10)),
    sg.Checkbox('Excel Error Ord.', 'G1', key='EXCEL_ERR_ORD', font=('Open Sans', 16), background_color='#FFFFFF', pad=((20,20),10)),
  ],
  #* Boton Principal de Ejecutar
  [
    sg.Checkbox('Excel Ord.', 'G1', key='EXCEL_ORD', font=('Open Sans', 16), background_color='#FFFFFF', pad=((120,0),10)),
    sg.Button('Ejecutar', size=(15,1), font=('Open Sans', 14), pad=((280,10),10))
  ]
]

main_layout = [
  [sg.Menu(menu_opciones, tearoff=False)],
  [sg.Frame('', layout, background_color='#FFFFFF', element_justification='l')]
]

window = sg.Window('Intercalador', main_layout, element_justification='l', icon='Assets/book_icon.ico')

while True:
  event,values = window.read()
  # print(event)
  # print("-"*20) 
  # print(values)
  if event in (sg.WINDOW_CLOSED, 'Exit', 'Salir'): break
  elif event == 'Ejecutar':
    # ? Checar si se ha puesto un archivo
    if values['EXCEL_FILE'] == '':
      sg.popup('Porfavor!!','Seleccione un Archivo de Excel.', title='Archivo Excel', background_color='#FFFFFF', font=('Open Sans', 12, 'bold'), icon='Assets/book_icon.ico')
    elif values['FOLDER'] == '':
      sg.popup('Porfavor!!','Seleccione una Capeta de Salida.', title='Carpeta de Salida', background_color='#FFFFFF', font=('Open Sans', 12, 'bold'), icon='Assets/book_icon.ico')
    elif values['NAME'] == '':
      sg.popup('Porfavor!!','Dele nombre al archivo de Salida.', title='Nombre del Archivo', background_color='#FFFFFF', font=('Open Sans', 12, 'bold'), icon='Assets/book_icon.ico')
    elif values['REPORT'] + values['EXCEL_ERR_ORD'] + values['EXCEL_ORD'] == 0:
      sg.popup('Porfavor!!','Seleccione alguna opción.', title='Opciones', background_color='#FFFFFF', font=('Open Sans', 12, 'bold'), icon='Assets/book_icon.ico')
    else:
      status = inter.main_program(archivo=values['EXCEL_FILE'], carpeta=values['FOLDER'], nombre=values['NAME'], reporte=[values['REPORT'], values['EXCEL_ORD'], values['EXCEL_ERR_ORD']], codify=0)
      if not status:
        sg.popup_error('Error en el reporte Excel','Falla en exnontrar columna Clasificación','revisas tutoriales.', title='Error Datos Excel', background_color='#FFFFFF', font=('Open Sans', 12, 'bold'), icon='Assets/book_icon.ico', )
      else:
        sg.popup('El Programa Finalizó Exitosamente !!!', title='Exito en Ejecución', background_color='#FFFFFF', font=('Open Sans', 12, 'bold'), icon='Assets/book_icon.ico')
  elif event == 'Licencia':
    sg.popup('Producto bajo licencia del', 'Tecnologíco de Monterrey', title='Licencia', background_color='#FFFFFF', font=('Open Sans', 12, 'bold'), icon='Assets/book_icon.ico')
  elif event == 'Acerca de...':
    sg.popup('Procesador de Excels.', ('Versión ' + version + ' 2022'), 'Desarrollado: Jesus David Talamantes Morales', title='Intercalador Tec', background_color='#FFFFFF', font=('Open Sans', 12, 'bold'), icon='Assets/book_icon.ico')

window.close()
