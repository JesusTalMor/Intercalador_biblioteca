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
      [sg.In(default_text='', key="PIPE_A", ** in_format)],
    ]
    pipe_b_layout = [
      [sg.Text(text="PIPE B", pad=5, **text_format)],
      [sg.In(default_text='', key="PIPE_B", ** in_format)],
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
      sg.In(default_text=self._Libro.etiqueta.volumen, key="VOL", **in_format),
      sg.Text(text="Copia", **text_format),
      sg.In(default_text=self._Libro.etiqueta.copia, key="COP", **in_format),
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
      [sg.In(default_text=self._Libro.etiqueta.clasif, size=(28, 1), key="CLAS", pad=(15, 5), **in_format)],
      #* Funcion para agregar un encabezado
      [sg.Text(text="Agregar Encabezado", font=("Open Sans", 12), **text_format)],
      [sg.In(default_text=self._Libro.etiqueta.encabezado, size=(18, 1), key="HEAD", **in_format)],
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
          text=self._Libro.etiqueta.clasif_completa, key="TEXT",
          font=("Open Sans", 16, "bold"), **text_format
        )
      ],
      [sg.HorizontalSeparator(pad=(0, (10, 6)))],
      [sg.Frame("", layout=INDIV_LAYOUT, **frame_format)],
      [sg.HorizontalSeparator(pad=(0, (6, 10)))],
      [
        sg.Button("Cancelar", font=("Open Sans", 12, "bold")),
        sg.Button("Modificar", font=("Open Sans", 12, "bold"), disabled=True),
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
      self.show_window_events(event, values)
      #* Cerrar programa sin resultados
      if event in (sg.WINDOW_CLOSED, "Exit", "Cancelar"):
        window.close() 
        return False, self._Libro
      
      #* Actualizar elemento de Clasificacion Completa
      self.actualizar_clasif(window, values)
      window['TEXT'].update(self._Libro.etiqueta.clasif_completa)

      if event == 'Modificar':
        window.close()
        return True, self._Libro
      elif event == 'INFO': pop.show_info_libro(self._Libro.titulo)

  #? FUNCIONALIDAD GENERAL *********************************
  def show_window_events(self, event, values):
    print(f"""
      Imprimiendo Eventos de Suceden
      {'-'*50}
      Eventos que suceden {event}
      Valores guardados {values}
      {'-'*50}
    """)

  def actualizar_clasif(self, window, values):
    """ Construye una clasificacion en tiempo real 
    """
    #* Tomar datos
    try:
      self._Libro.etiqueta.clasif = str(values["CLAS"])
      self._Libro.etiqueta.volumen = str(values['VOL'])
      self._Libro.etiqueta.copia = str(values['COP'])
      self._Libro.etiqueta.encabezado = str(values['HEAD'])
    except TypeError:
      pass

    if self._Libro.etiqueta.clasif_valida:
      window["PIPE_A"].update(value=self._Libro.etiqueta.PIPE_A, text_color='#1AB01F')  
      window["PIPE_B"].update(value=self._Libro.etiqueta.PIPE_B, text_color='#1AB01F')
      window["Modificar"].update(disabled=False)
    else:
      window["PIPE_A"].update(value="XXXXXX", text_color='#F04150')  
      window["PIPE_B"].update(value="XXXXXX", text_color='#F04150')
      window["Modificar"].update(disabled=True)

if __name__ == "__main__":
  # VS = VentanaSeleccionarPosicion(10,10)
  # print(VS.run_window())
  pass