import os
import sys

import PySimpleGUI as sg

import pop_ups as pop
from managers import Libro

"""En este modulo se almacenan las ventanas auxiliares de trabajo."""

# * Tema principal de las ventanas
sg.LOOK_AND_FEEL_TABLE["MyCreatedTheme"] = {
  "BACKGROUND": "#3016F3",
  "TEXT": "#000000",
  "INPUT": "#DEE6F7",
  "TEXT_INPUT": "#000000",
  "SCROLL": "#DEE6F7",
  "BUTTON": ("#000000", "#FFFFFF"),
  "PROGRESS": ("#DEE6F7", "#DEE6F7"),
  "BORDER": 2,
  "SLIDER_DEPTH": 0,
  "PROGRESS_DEPTH": 0,
}
sg.theme("MyCreatedTheme")

#?#********** Función apoyo para relative path *********#
def resource_path(relative_path):
  """ Get absolute path to resource, works for dev and for PyInstaller """
  try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.abspath(".")
  return os.path.join(base_path, relative_path)

class VentanaModificar:
  '''Modifica el contenido y parametros de una etiqueta

    Parametros:
      clasificacion_completa: Clasificación completa del libro a modificar
      Dicc_info:
        titulo: Titulo del libro a modificar
        cbarras: Codigo de Barras del Libro a modificar
        clasif: Clasificación Basica
        volumen: Volumen expresado en V.(Num)
        copia: Copia expresado en Num.
        encabeza: Encabezado anterior a Clasificación
    
        Retorna:
          2 Listas con datos, en caso de finalizar correctamente.
          Caso contrario regresa 2 listas de la siguiente manera [False],[False]
  '''
  titulo_ventana = 'Modificar Etiqueta'
  def __init__(self, aLibro:Libro):
    self._Libro = aLibro

  def clasification_layout(self):
    """ Layout para insertar clasificaciones 
    
    Llaves que Maneja
    -----------------
      PIPE_A: (str) PIPE A de la clasificacion
      PIPE_B: (str) PIPE B de la clasificacion
      VOL: (int) Volumen del Libro
      COP: (int) Copia del Libro
      CLAS: (str) Clasificacion del Libro
      HEAD: (str) Encabezado del Libro

    """
    #?#********* LAYOUT PARA MANEJO DE PIPE'S #?#*********
    color = '#1AB01F' if self._Libro.etiqueta.clasif_valida is True else '#F04150'
    text_format = {
      'font':("Open Sans", 12, "bold"), 
      'background_color':"#FFFFFF", 
      'justification':"center",
    }
    in_format = {
      'size':(14, 1), 
      'font':("Open Sans", 10, "bold"), 
      'justification':"center", 
      'disabled':True,
    }
    pipe_a_layout = [
      [sg.Text(text="PIPE A", pad=5, **text_format)],
      [sg.In(
        default_text=self._Libro.etiqueta.PIPE_A, 
        key="PIPE_A", 
        text_color= color,
        ** in_format
      )],
    ]
    pipe_b_layout = [
      [sg.Text(text="PIPE B", pad=5, **text_format)],
      [sg.In(
        default_text=self._Libro.etiqueta.PIPE_B, 
        key="PIPE_B",
        text_color=color, 
        ** in_format,
      )],
    ]
    colum_format = {'background_color':"#FFFFFF", 'element_justification':"c"}
    PIPE_AB_LAYOUT = [[
      sg.Column(layout=pipe_a_layout, **colum_format),
      sg.VSeperator(),
      sg.Column(layout=pipe_b_layout, **colum_format),
    ]]
    
    #?#********* LAYOUT PARA MANEJO DE COPIA Y VOLUMEN #?#*********
    text_format = {
      'font':("Open Sans", 12,), 
      'background_color':"#FFFFFF", 
      'justification':"center",
    }
    in_format = {
      'size':(2, 1), 
      'enable_events':True,
      'font':("Open Sans", 10), 
      'justification':"center", 
    }
    VOL_COP_LAYOUT = [
      sg.Text(text="Volumen", **text_format),
      sg.In(
        default_text=self._Libro.etiqueta.volumen, 
        key="VOL", 
        **in_format
      ),
      sg.Text(text="Copia", **text_format),
      sg.In(
        default_text=self._Libro.etiqueta.copia, 
        key="COP", 
        **in_format
      ),
    ],
    
    #?#********* LAYOUT PARA MANEJO DE CLASIFICACION Y ENCABEZADO #?#*********
    text_format = {
      'background_color':"#FFFFFF", 
      'justification':"center",
    }
    in_format = {
      'enable_events':True,
      'font':("Open Sans", 12), 
      'justification':"center", 
    }
    frame_format = {
      'background_color':"#FFFFFF", 
      'element_justification':"c",
      'border_width':0
    }
    LAYOUT_GENERAL = [
      #* Titulo de esta seccion
      [sg.Text(text="Clasificación", font=("Open Sans", 14, "bold"), **text_format)],
      [sg.In(
        default_text=self._Libro.etiqueta.clasif, 
        size=(28, 1), 
        key="CLAS", 
        pad=(15, 5), 
        **in_format
      )],
      #* Funcion para agregar un encabezado
      [sg.Text(text="Agregar Encabezado", font=("Open Sans", 12), **text_format)],
      [sg.In(
        default_text=self._Libro.etiqueta.encabezado, 
        size=(18, 1), 
        key="HEAD", 
        **in_format
      )],
      [sg.Frame("",layout=VOL_COP_LAYOUT, **frame_format)],
      [sg.Frame("",layout=PIPE_AB_LAYOUT, **frame_format)],
    ]
    return LAYOUT_GENERAL

  def create_layout(self):
    """ Crea el layout General de Esta Ventana 
    Llaves que Maneja
    -----------------
      INFO: (boton) Muestra el titulo del Libro
      TEXT: (str) Texto de clasificacion completa
      Cancelar: (boton) Cierra la ventana
      Modificar: (boton) Cierra la ventana y mandar los datos modificados


    Llaves que Hereda
    -----------------
      PIPE_A: (str) PIPE A de la clasificacion
      PIPE_B: (str) PIPE B de la clasificacion
      VOL: (int) Volumen del Libro
      COP: (int) Copia del Libro
      CLAS: (str) Clasificacion del Libro
      HEAD: (str) Encabezado del Libro
    """
    INDIV_LAYOUT = self.clasification_layout()
    text_format = {'background_color':"#FFFFFF", 'justification':"c",}
    frame_format = {'background_color':"#FFFFFF", 'element_justification':"c",}
    GENERAL_LAYOUT = [
      #* Titulo de la aplicacion y Boton de Mas Info
      [
        sg.Text(
          text=self.titulo_ventana, font=("Open Sans", 18, "bold", "italic"), 
          pad=(0, (0, 10)), ** text_format,
        ),
        sg.Button(
          image_source=resource_path('Assets/info_icon.png'), image_subsample=10, 
          border_width=0, key='INFO', pad=(5,(0,10))
        )
      ],
      [
        sg.Text(
          text=self._Libro.etiqueta.clasif_completa, 
          key="CLASS_FULL",
          font=("Open Sans", 16, "bold"), 
          **text_format
        )
      ],
      [sg.HorizontalSeparator(pad=(0, (10, 6)))],
      [sg.Frame("", layout=INDIV_LAYOUT, **frame_format)],
      [sg.HorizontalSeparator(pad=(0, (6, 10)))],
      [
        sg.Button("Cancelar", font=("Open Sans", 12, "bold")),
        sg.Button(
          "Modificar", 
          font=("Open Sans", 12, "bold"), 
          disabled=not(self._Libro.etiqueta.clasif_valida)
        ),
      ],    
    ]
    return GENERAL_LAYOUT

  def create_window(self):
    LAYOUT = self.create_layout()
    MAIN_LAYOUT = [[sg.Frame('', LAYOUT, background_color='#FFFFFF', element_justification='c')]]
    window = sg.Window(self.titulo_ventana, MAIN_LAYOUT, element_justification='c', icon=resource_path('Assets/book_icon.ico'))
    return window

  #? FUNCIONAMIENTO PRINCIPAL DE LA VENTANA ***********************
  def run_window(self):
    window = self.create_window()
    while True:
      event, values = window.read()
      # self.show_window_events(event, values)
      #* Cerrar programa sin resultados
      if event in (sg.WINDOW_CLOSED, "Exit", "Cancelar"):
        window.close() 
        return None      
      #* Mostrar informacion del libro.
      elif event == 'INFO': pop.show_info_libro(self._Libro.titulo)
      #* Actualizar Ventana.
      self.actualizar_ventana(window)

      if event == 'Modificar':
        window.close()
        return self._Libro

  #? FUNCIONALIDAD GENERAL *********************************
  def show_window_events(self, event, values):
    print(f"""
      Imprimiendo Eventos de Suceden
      {'-'*50}
      Eventos que suceden {event}
      Valores guardados {values}
      {'-'*50}
    """)

  def actualizar_ventana(self, window):
    """ Construye una clasificacion en tiempo real 
    """
    self._Libro.etiqueta.volumen = window['VOL'].get()
    self._Libro.etiqueta.copia = window['COP'].get()
    self._Libro.etiqueta.encabezado = window['HEAD'].get()
    self._Libro.etiqueta.clasif = window['CLAS'].get()
    window['CLASS_FULL'].update(self._Libro.etiqueta.clasif_completa)

    # * Actualizar PIPES
    if self._Libro.etiqueta.clasif_valida:
      window["PIPE_A"].update(value=self._Libro.etiqueta.PIPE_A, text_color='#1AB01F')  
      window["PIPE_B"].update(value=self._Libro.etiqueta.PIPE_B, text_color='#1AB01F')
      window["Modificar"].update(disabled=False)
    else:
      window["PIPE_A"].update(value="XXXXXX", text_color='#F04150')  
      window["PIPE_B"].update(value="XXXXXX", text_color='#F04150')
      window["Modificar"].update(disabled=True)

def ventana_instruc_ordenar(lista_colocar:list, lista_retirar:list, hoja:str, nombre_archivo:str):
  # Sacar datos de libros
  lista_main = [lista_colocar, lista_retirar]
  main_index = 0
  libro_erroneo = lista_main[0][main_index]['libro'] 
  libro_ant_corr = lista_main[0][main_index]['anterior']
  libro_pos_corr = lista_main[0][main_index]['siguiente']
  instruc_index = 0
  action = ('RETIRAR', 'ORDENAR')
  len_listas = (len(lista_colocar), len(lista_retirar))

  title_frame = [
    [
      sg.Text(
        text=f'{nombre_archivo} - {hoja}', 
        font=('Open Sans', 18, 'bold', 'italic'), 
        background_color='#FFFFFF', justification='c', pad=0
      ),
    ],
    [
      sg.Text(
        text=f'pasos para ordenar:', 
        font=('Open Sans', 14, 'italic'), 
        background_color='#FFFFFF', justification='c', pad=0
      ),
    ],

  ]
  instruction_frame = [
    [
      sg.Text(
        text='Instrucción:',
        font=('Open Sans', 18, 'bold'),
        background_color='#FFFFFF', justification='c', pad=0
      )
    ],
    [
      sg.Text(
        text=f'{action[0]}',
        font=('Arial', 18, 'bold'),
        background_color='#FFFFFF',
        justification='c', key='INSTRUCT', pad=0
      )
    ]
  ]
  libro_erroneo_frame = [
    [
      sg.Text(
        text='Información Libro Erróneo',
        font=('Open Sans', 14, 'bold', 'italic'),
        background_color='#FFFFFF', justification='c', pad=0
      )
    ],
    [
      sg.Text(
        text=f'{libro_erroneo[0]} \n {libro_erroneo[1]}',
        font=('Open Sans', 12, 'italic'),
        background_color='#FFFFFF', justification='c', key='LIBRO', pad=0
      )
    ]
  ]
  libro_anterior_corr = [
    [
      sg.Text(
        text='Libro Anterior Correcto',
        font=('Open Sans', 14, 'bold', 'italic'),
        background_color='#FFFFFF', justification='c', pad=0
      )
    ],
    [
      sg.Text(
        text=f'{libro_ant_corr[0]} \n {libro_ant_corr[1]}',
        font=('Open Sans', 12, 'italic'),
        background_color='#FFFFFF', justification='c', key='ANT', pad=0
      )
    ]
  ]
  libro_posterior_corr = [
    [
      sg.Text(
        text='Libro Posterior Correcto',
        font=('Open Sans', 14, 'bold', 'italic'),
        background_color='#FFFFFF', justification='c', pad=0
      )
    ],
    [
      sg.Text(
        text=f'{libro_pos_corr[0]} \n {libro_pos_corr[1]}',
        font=('Open Sans', 12, 'italic'),
        background_color='#FFFFFF', justification='c', key='POS', pad=0
      )
    ]
  ]
  boton_count = [
    [
      sg.Text(
        text=f'{main_index+1}/{len_listas[0]}',
        font=('Open Sans', 18, 'bold', 'italic'),
        background_color='#FFFFFF', justification='c', key='COUNT', pad=0
      )
    ],
    [
      sg.Button(
        button_text='Siguiente',
        font=('Open Sans', 18, 'bold', 'italic'),
        pad=0
      )
    ],
  ]
  left_column = [
    [sg.Frame('', libro_erroneo_frame, background_color='#FFFFFF', element_justification='l', border_width=0, pad=(15,(20,10)))],
    [sg.Frame('', libro_anterior_corr, background_color='#FFFFFF', element_justification='l', border_width=4, pad=(15,(5,5)))],
    [sg.Frame('', libro_posterior_corr, background_color='#FFFFFF', element_justification='l', border_width=4, pad=(15,(5,5))),],
  ]
  right_column = [
    [sg.Frame('', boton_count, background_color='#FFFFFF', element_justification='c', border_width=0, pad=0)]
  ]
  
  main_layout = [
    [
      sg.Frame('', title_frame, background_color='#FFFFFF', element_justification='c', border_width=0, pad=((10,200), (10,20))),
      sg.Frame('', instruction_frame, background_color='#FFFFFF', element_justification='c', border_width=0, pad=((0,10), (10,10)))
    ],
    [sg.HorizontalSeparator(color='#000000', pad=0)],
    [
      sg.Column(layout=left_column, background_color='#FFFFFF', element_justification='l'),
      sg.Column(layout=right_column, background_color='#FFFFFF', element_justification='c', pad=((40,10), (140,10)))
    ]
  ]

  layout = [[sg.Frame('', main_layout, background_color='#FFFFFF', element_justification='l', pad=0)]]
  window = sg.Window('Salida', layout, element_justification='c', icon=resource_path('Assets/book_icon.ico'))

  while True:
    event, values = window.read()
    # print('-'*50)
    # print(f'Eventos que suceden {event}')
    # print(f'Valores guardaros {values}')
    # print('-'*50 + '\n')

    if event in (sg.WINDOW_CLOSED, "Exit"): 
      window.close()
      return
    
    if event == 'Siguiente':
      # print('Cambio de libro')
      # * Revisar si se terminaron los libros
      main_index += 1
      if main_index >= len_listas[instruc_index]: 
        if instruc_index != 0: 
          pop.success_manual_order()
          window.close()
          return
        instruc_index = 1
        main_index = 0
        window['INSTRUCT'].update(f'{action[instruc_index]}')
      
      # * Sacar datos
      libro_erroneo = lista_main[instruc_index][main_index]['libro'] 
      libro_ant_corr = lista_main[instruc_index][main_index]['anterior']
      libro_pos_corr = lista_main[instruc_index][main_index]['siguiente']

      # * Actualizar datos
      window['LIBRO'].update(f'{libro_erroneo[0]} \n {libro_erroneo[1]}')
      window['ANT'].update(f'{libro_ant_corr[0]} \n {libro_ant_corr[1]}')
      window['POS'].update(f'{libro_pos_corr[0]} \n {libro_pos_corr[1]}')
      window['COUNT'].update(f'{main_index+1}/{len_listas[0]}')




if __name__ == "__main__":
  # VS = VentanaSeleccionarPosicion(10,10)
  # print(VS.run_window())
  pass